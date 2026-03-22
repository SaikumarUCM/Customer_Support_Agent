"""Collect thumbs-up / thumbs-down feedback per LangSmith run_id."""

from fastapi import APIRouter
from pydantic import BaseModel, Field

from agent.core.config import get_settings
from agent.core.logging import get_logger

log = get_logger(__name__)
router = APIRouter(tags=["feedback"])


class FeedbackRequest(BaseModel):
    run_id: str = Field(..., description="The run_id returned by /chat")
    score: float = Field(..., ge=0.0, le=1.0, description="1.0 = thumbs up, 0.0 = thumbs down")
    comment: str = Field(default="", max_length=1000)


class FeedbackResponse(BaseModel):
    accepted: bool
    message: str


@router.post("/feedback", response_model=FeedbackResponse, summary="Submit run feedback")
async def submit_feedback(body: FeedbackRequest) -> FeedbackResponse:
    """Record user feedback for a specific run in LangSmith.

    Falls back to a structured log entry if LangSmith is unavailable.
    """
    settings = get_settings()

    if settings.tracing_enabled:
        try:
            from langsmith import Client  # type: ignore[import]  # noqa: PLC0415

            client = Client()
            client.create_feedback(
                run_id=body.run_id,
                key="user_score",
                score=body.score,
                comment=body.comment or None,
            )
            log.info(
                "feedback: recorded in LangSmith",
                run_id=body.run_id,
                score=body.score,
            )
            return FeedbackResponse(accepted=True, message="Feedback recorded. Thank you!")
        except Exception as exc:
            log.warning("feedback: LangSmith error", error=str(exc))

    # Fallback: structured log
    log.info(
        "feedback: logged locally",
        run_id=body.run_id,
        score=body.score,
        comment=body.comment,
    )
    return FeedbackResponse(accepted=True, message="Feedback recorded. Thank you!")
