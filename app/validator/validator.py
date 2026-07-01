"""
Retrieval Validator

Evaluates retrieval quality before answer generation.
"""

from app.core.config import settings
from app.core.logger import logger


class RetrievalValidator:
    """
    Validate retrieval confidence.
    """

    def validate(self, retrieved_chunks: list):
        """
        Evaluate retrieval confidence.

        Returns
        -------
        dict
        """

        if not retrieved_chunks:

            logger.warning(
                "No chunks retrieved."
            )

            return {
                "confidence": "Low",
                "average_score": 0.0,
                "should_generate": False,
            }

        scores = [
            chunk["score"]
            for chunk in retrieved_chunks
        ]

        # Highest similarity score
        top_score = scores[0]

        # Average similarity score
        average_score = sum(scores) / len(scores)

        # Weighted confidence score
        final_score = (0.7 * top_score) + (0.3 * average_score)

        if final_score >= settings.HIGH_CONFIDENCE_THRESHOLD:

            confidence = "High"
            should_generate = True

        elif final_score >= settings.MEDIUM_CONFIDENCE_THRESHOLD:

            confidence = "Medium"
            should_generate = True

        else:

            confidence = "Low"
            should_generate = False

        logger.info(
            f"Retrieval Confidence: {confidence} | "
            f"Top Score: {top_score:.3f} | "
            f"Average Score: {average_score:.3f} | "
            f"Final Score: {final_score:.3f}"
        )

        return {
        "confidence": confidence,
        "top_score": round(top_score, 3),
        "average_score": round(average_score, 3),
        "final_score": round(final_score, 3),
        "should_generate": should_generate,
    }