from typing import Literal

from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.crew.crew_setup import (
    build_coding_crew,
    build_research_coding_crew,
    build_manager_crew
)

from app.utils.file_parser import parse_files

from app.utils.validation import (
    validate_generated_files,
    compact_validation_summary
)


router = APIRouter()


class ProjectRequest(BaseModel):

    project_request: str = Field(
        min_length=3
    )

    complexity: Literal[
        "auto",
        "simple",
        "complex"
    ] = "auto"

    review: bool = False


def detect_complexity(
    request: str
) -> str:

    """
    Simple rule-based complexity detection.

    IMPORTANT:
    This does NOT call an LLM.
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
        "e-commerce"
    )

    for term in complex_terms:

        if term in text:
            return "complex"

    return "simple"


@router.post("/run-company")
async def run_company(
    data: ProjectRequest
):

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
    # 2. RUN APPROPRIATE CREW
    # --------------------------------

    research_output = ""

    coding_output = ""


    if complexity == "simple":

        # ONLY CODING AGENT
        # 1 LLM CALL

        crew = build_coding_crew()

        result = crew.kickoff(
            inputs={
                "project_request":
                data.project_request,

                "research_output":
                ""
            }
        )

        if result.tasks_output:

            coding_output = str(
                result.tasks_output[0]
            )


    else:

        # RESEARCH + CODING
        # 2 LLM CALLS

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

            coding_output = str(
                task_outputs[1]
            )


    # --------------------------------
    # 3. PARSE GENERATED FILES
    # --------------------------------

    generated_files = parse_files(
        coding_output
    )


    # --------------------------------
    # 4. LOCAL VALIDATION
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
    # 5. MANAGER ONLY WHEN NECESSARY
    # --------------------------------

    manager_review = ""


    should_review = (

        data.review

        or

        validation["status"] == "FAIL"
    )


    if should_review:

        manager_crew = build_manager_crew()

        manager_result = (
            manager_crew.kickoff(
                inputs={
                    "project_request":
                    data.project_request,

                    "validation_summary":
                    validation_summary
                }
            )
        )


        if manager_result.tasks_output:

            manager_review = str(
                manager_result.tasks_output[0]
            )


    # --------------------------------
    # 6. RETURN RESPONSE
    # --------------------------------

    return {

        "status": "success",

        "complexity": complexity,

        "research": research_output,

        "code": coding_output,

        "files": generated_files,

        "validation": validation,

        "manager_review":
        manager_review,

        # Frontend compatibility
        "review":
        manager_review
    }