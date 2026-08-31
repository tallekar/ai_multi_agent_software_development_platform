
from typing import Literal

from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.crew.crew_setup import (
    build_coding_crew,
    build_research_coding_crew,
    build_testing_crew,
    build_debugging_crew,
    build_coding_fix_crew,
    build_manager_crew,
)

from app.utils.file_parser import parse_files

from app.utils.validation import (
    validate_generated_files,
    compact_validation_summary,
)


router = APIRouter()


# Maximum number of debugging/fixing attempts
MAX_RETRIES = 2


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
    manager_review = ""

    retry_count = 0


    # --------------------------------
    # 3. INITIAL CODE GENERATION
    # --------------------------------

    if complexity == "simple":

        # Simple:
        # Coding only

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

        # Complex:
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
    # 6. TEST + DEBUG LOOP
    # --------------------------------

    if complexity == "complex":

        while retry_count <= MAX_RETRIES:

            # ----------------------------
            # Run Testing Agent
            # ----------------------------

            if validation["status"] == "PASS":

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


            # ----------------------------
            # Determine whether problems
            # exist
            # ----------------------------

            validation_failed = (
                validation["status"] == "FAIL"
            )

            testing_failed = (
                testing_output
                and any(
                    word in testing_output.lower()
                    for word in [
                        "fail",
                        "error",
                        "bug",
                        "broken",
                        "invalid",
                    ]
                )
            )


            # ----------------------------
            # Everything looks good
            # ----------------------------

            if not validation_failed and not testing_failed:

                break


            # ----------------------------
            # Maximum retry reached
            # ----------------------------

            if retry_count >= MAX_RETRIES:

                break


            retry_count += 1


            # ----------------------------
            # Debugging Agent
            # ----------------------------

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

                        "validation_summary":
                        validation_summary,

                        "testing_output":
                        testing_output,
                    }
                )
            )

            if debugging_result.tasks_output:

                debugging_output = str(
                    debugging_result.tasks_output[-1]
                )


            # ----------------------------
            # Coding Fix Agent
            # ----------------------------

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
                    }
                )
            )

            if coding_fix_result.tasks_output:

                coding_output = str(
                    coding_fix_result.tasks_output[-1]
                )


            # ----------------------------
            # Parse corrected files
            # ----------------------------

            generated_files = parse_files(
                coding_output
            )


            # ----------------------------
            # Local validation again
            # ----------------------------

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


    # --------------------------------
    # 7. OPTIONAL MANAGER REVIEW
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
    # 8. RETURN RESPONSE
    # --------------------------------

    return {

        "status":
        "success",

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

        "debugging":
        debugging_output,

        "files":
        generated_files,

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