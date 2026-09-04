
from typing import Literal

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

from app.crew.crew_setup import (
    build_coding_crew,
    build_research_coding_crew,
    build_testing_crew,
    build_debugging_crew,
    build_coding_fix_crew,
    build_code_review_crew,
    build_manager_crew,
)

from app.utils.file_parser import parse_files
from app.utils.test_runner import run_project_tests
from app.utils.project_writer import (
    PROJECTS_ROOT,
    create_project_zip,
    update_project,
    write_project,
)

from app.utils.validation import (
    validate_generated_files,
    compact_validation_summary,
)


router = APIRouter()


# Maximum number of debugging/fixing attempts
MAX_RETRIES = 2


@router.get("/projects/{project_id}/download")
def download_project(project_id: str):
    try:
        archive = create_project_zip(project_id, PROJECTS_ROOT)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Project not found") from exc

    return StreamingResponse(
        archive,
        media_type="application/zip",
        headers={
            "Content-Disposition":
            f'attachment; filename="{project_id}.zip"'
        },
    )


class ProjectRequest(BaseModel):
    project_request: str = Field(min_length=3)

    complexity: Literal[
        "auto",
        "simple",
        "complex",
    ] = "auto"

    review: bool = False


def detect_complexity(request: str) -> str:
    """
    Rule-based complexity detection.

    This does NOT use an LLM.
    """

    text = request.lower()

    complex_terms = (
        "production",
        "full stack",
        "full-stack",
        "saas",
        "microservice",
        "multi agent",
        "multi-agent",
        "authentication",
        "payment",
        "database",
        "deploy",
        "deployment",
        "ai platform",
        "ecommerce",
        "e-commerce",
    )

    for term in complex_terms:
        if term in text:
            return "complex"

    return "simple"


@router.post("/run-company")
async def run_company(data: ProjectRequest):

    # --------------------------------
    # 1. DETERMINE COMPLEXITY
    # --------------------------------

    if data.complexity == "auto":
        complexity = detect_complexity(
            data.project_request
        )
    else:
        complexity = data.complexity


    # --------------------------------
    # 2. INITIALIZE OUTPUTS
    # --------------------------------

    research_output = ""
    architecture_output = ""
    coding_output = ""
    testing_output = ""
    debugging_output = ""
    code_review_output = ""
    manager_review = ""

    retry_count = 0


    # --------------------------------
    # 3. INITIAL CODE GENERATION
    # --------------------------------

    if complexity == "simple":

        crew = build_coding_crew()

        result = crew.kickoff(
            inputs={
                "project_request":
                    data.project_request,

                "research_output":
                    "",
            }
        )

        if result.tasks_output:

            coding_output = str(
                result.tasks_output[-1]
            )

    else:

        # Research → Architecture → Coding

        crew = build_research_coding_crew()

        result = crew.kickoff(
            inputs={
                "project_request":
                    data.project_request
            }
        )

        task_outputs = result.tasks_output

        if len(task_outputs) >= 1:

            research_output = str(
                task_outputs[0]
            )

        if len(task_outputs) >= 2:

            architecture_output = str(
                task_outputs[1]
            )

        if len(task_outputs) >= 3:

            coding_output = str(
                task_outputs[2]
            )


    # --------------------------------
    # 4. PARSE GENERATED FILES
    # --------------------------------

    generated_files = parse_files(
        coding_output
    )

    try:
        project = write_project(
            generated_files,
            project_request=data.project_request,
            architecture=architecture_output,
        )
        project["download_url"] = (
            f"/projects/{project['project_id']}/download"
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    test_result = run_project_tests(project["project_path"])
    test_attempts = [test_result]
    fixes_applied = []


    # --------------------------------
    # 5. LOCAL VALIDATION
    #
    # NO LLM CALL
    # --------------------------------

    validation = validate_generated_files(
        generated_files
    )

    validation_summary = (
        compact_validation_summary(
            validation
        )
    )


    # --------------------------------
    # 6. TEST + DEBUG + FIX LOOP
    #
    # Maximum 2 fix attempts
    # --------------------------------

    while retry_count < MAX_RETRIES:

            # --------------------------------
            # TESTING
            # --------------------------------

            if complexity == "complex" and validation["status"] == "PASS":

                testing_crew = (
                    build_testing_crew()
                )

                testing_result = (
                    testing_crew.kickoff(
                        inputs={
                            "project_request":
                                data.project_request,

                            "coding_output":
                                coding_output,
                        }
                    )
                )

                if testing_result.tasks_output:

                    testing_output = str(
                        testing_result.tasks_output[-1]
                    )

            else:

                testing_output = ""


            # --------------------------------
            # CHECK FOR PROBLEMS
            # --------------------------------

            validation_failed = validation["status"] == "FAIL"

            testing_failed = test_result["status"] == "FAIL"

            # --------------------------------
            # EVERYTHING PASSED
            # --------------------------------

            if not validation_failed and not testing_failed:
                break


            # --------------------------------
            # DEBUGGING
            # --------------------------------

            debugging_crew = (
                build_debugging_crew()
            )

            debugging_result = (
                debugging_crew.kickoff(
                    inputs={
                        "project_request":
                            data.project_request,

                        "coding_output":
                            coding_output,

                        "project_path":
                            project["project_path"],

                        "validation_summary":
                            validation_summary,

                        "testing_output":
                            test_result["output"],
                    }
                )
            )

            if debugging_result.tasks_output:

                debugging_output = str(
                    debugging_result.tasks_output[-1]
                )


            # --------------------------------
            # CODING FIX
            # --------------------------------

            coding_fix_crew = (
                build_coding_fix_crew()
            )

            coding_fix_result = (
                coding_fix_crew.kickoff(
                    inputs={
                        "project_request":
                            data.project_request,

                        "coding_output":
                            coding_output,

                        "debugging_output":
                            debugging_output,

                        "project_path":
                            project["project_path"],
                    }
                )
            )

            if coding_fix_result.tasks_output:

                coding_output = str(
                    coding_fix_result.tasks_output[-1]
                )


            # --------------------------------
            # INCREASE RETRY COUNT
            # --------------------------------

            retry_count += 1


            # --------------------------------
            # PARSE CORRECTED FILES
            # --------------------------------

            generated_files = parse_files(
                coding_output
            )

            fixes_applied.append({
                "attempt": retry_count,
                "files": list(generated_files.keys()),
            })

            try:
                project = update_project(
                    project["project_path"],
                    generated_files,
                    architecture=architecture_output,
                )
                project["download_url"] = (
                    f"/projects/{project['project_id']}/download"
                )
            except ValueError as exc:
                raise HTTPException(status_code=422, detail=str(exc)) from exc


            # --------------------------------
            # LOCAL VALIDATION AGAIN
            #
            # NO LLM CALL
            # --------------------------------

            validation = (
                validate_generated_files(
                    generated_files
                )
            )

            validation_summary = (
                compact_validation_summary(
                    validation
                )
            )

            test_result = run_project_tests(project["project_path"])
            test_attempts.append(test_result)


    # --------------------------------
    # 7. FINAL TEST
    # --------------------------------

    if (
        complexity == "complex"
        and validation["status"] == "PASS"
        and test_result["status"] == "PASS"
    ):

        testing_crew = (
            build_testing_crew()
        )

        testing_result = (
            testing_crew.kickoff(
                inputs={
                    "project_request":
                        data.project_request,

                    "coding_output":
                        coding_output,
                }
            )
        )

        if testing_result.tasks_output:

            testing_output = str(
                testing_result.tasks_output[-1]
            )


    # --------------------------------
    # 8. CODE REVIEW
    #
    # One LLM call only.
    # Reviews existing generated code.
    # --------------------------------

    if (
        complexity == "complex"
        and validation["status"] == "PASS"
        and test_result["status"] == "PASS"
    ):

        code_review_crew = (
            build_code_review_crew()
        )

        code_review_result = (
            code_review_crew.kickoff(
                inputs={
                    "project_request":
                        data.project_request,

                    "coding_output":
                        coding_output,

                    "validation_summary":
                        validation_summary,

                    "debugging_output":
                        debugging_output,
                }
            )
        )

        if code_review_result.tasks_output:

            code_review_output = str(
                code_review_result.tasks_output[-1]
            )


    # --------------------------------
    # 9. OPTIONAL MANAGER REVIEW
    # --------------------------------

    if data.review:

        manager_crew = (
            build_manager_crew()
        )

        manager_result = (
            manager_crew.kickoff(
                inputs={
                    "project_request":
                        data.project_request,

                    "validation_summary":
                        validation_summary,
                }
            )
        )

        if manager_result.tasks_output:

            manager_review = str(
                manager_result.tasks_output[-1]
            )


    # --------------------------------
    # 10. RETURN RESPONSE
    # --------------------------------

    return {
        "status": "success",

        "complexity":
            complexity,

        "research":
            research_output,

        "architecture":
            architecture_output,

        "code":
            coding_output,

        "testing":
            testing_output,

        "test_status":
            test_result["status"],

        "test_attempts":
            test_attempts,

        "fixes_applied":
            fixes_applied,

        "remaining_errors":
            test_result["output"] if test_result["status"] == "FAIL" else "",

        "debugging":
            debugging_output,

        "code_review":
            code_review_output,

        "files":
            generated_files,

        "project_name":
            project["project_name"],

        "project_path":
            project["project_path"],

        "generated_files":
            project["generated_files"],

        "file_count":
            project["file_count"],

        "manifest_path":
            project["manifest_path"],

        "generation_status":
            "success",

        "project":
            project,

        "validation":
            validation,

        "retry_count":
            retry_count,

        "manager_review":
            manager_review,

        # Frontend compatibility
        "review":
            manager_review,
    }