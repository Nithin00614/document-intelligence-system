"""
Answer Generation Service

Generates answers from retrieved document context using
a local Hugging Face language model.
"""

from transformers import (
    AutoTokenizer,
    AutoModelForSeq2SeqLM,
)

from app.core.config import settings
from app.core.logger import logger
import torch      


class AnswerGenerator:
    """
    Local LLM inference service.
    """

    def __init__(self):

        logger.info(
            f"Loading LLM: {settings.LLM_MODEL}"
        )

        self.tokenizer = AutoTokenizer.from_pretrained(
            settings.LLM_MODEL
        )

        self.model = AutoModelForSeq2SeqLM.from_pretrained(
            settings.LLM_MODEL
        )

        logger.info(
            "LLM loaded successfully."
        )

    def generate(
        self,
        prompt: str,
    ) -> str:
        """
        Generate answer from prompt.
        """
        try:
            logger.info("Generating answer...")
            inputs = self.tokenizer(
                prompt,
                return_tensors="pt",
                truncation=True,
                max_length=settings.MAX_INPUT_TOKENS,
            )

            with torch.no_grad():
                outputs = self.model.generate(

                **inputs,

                max_new_tokens=settings.MAX_NEW_TOKENS,

                do_sample=False,

                repetition_penalty=1.1,
            )

            answer = self.tokenizer.decode(
                outputs[0],
                skip_special_tokens=True,
            )
            logger.info("Answer generated successfully.")
            return answer.strip()
        
        except Exception as e:

            logger.exception("LLM generation failed.")

            raise RuntimeError(
                "Failed to generate answer."
            ) from e