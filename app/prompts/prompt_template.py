"""
Prompt Template

Builds grounded prompts for Retrieval-Augmented Generation (RAG).
"""

from typing import List

from app.core.config import settings


class PromptTemplate:
    """
    Constructs prompts for the LLM using retrieved document context.
    """

    @staticmethod
    def build(
        question: str,
        retrieved_chunks: List[dict],
        mode: str = "answer",
    ) -> str:

        context_sections = []

        for index, chunk in enumerate(retrieved_chunks, start=1):

            context_sections.append(
                f"""
[Document {index}]
Filename: {chunk['filename']}
Page: {chunk['page_number']}

Content:
{chunk['chunk_text']}
"""
            )

        context = "\n----------------------------------------\n".join(
            context_sections
        )

        if len(context) > settings.MAX_CONTEXT_CHARS:
            context = context[: settings.MAX_CONTEXT_CHARS]

        if mode == "answer":

            prompt = f"""
        You are an AI Document Intelligence Assistant.

        Answer the user's question using ONLY the retrieved document context.

        STRICT RULES

        - Use ONLY the provided document context.
        - NEVER use outside knowledge.
        - NEVER invent facts.
        - NEVER guess.
        - Combine information from multiple retrieved sections whenever appropriate.
        - Every statement must be supported by the retrieved document context.
        - If the retrieved evidence is incomplete, clearly state that the answer is based only on the available document evidence.
        - If the retrieved context does not contain enough information to answer the question, reply EXACTLY:

        I could not find sufficient information in the uploaded documents.

        Return your response using EXACTLY the following structure.

        ## Answer

        Provide a clear and concise answer to the user's question.

        ## Supporting Evidence

        - Summarize 2–3 important supporting facts from the retrieved document context.
        - Do not copy large portions of the document.
        - Use complete sentences.

        ## Notes

        - Mention whether the answer is based on multiple retrieved sections or limited evidence.
        - If no additional note is required, write:
        "The available retrieved context sufficiently supports the answer."

        Do not include any additional headings or explanations.

        ==========================
        DOCUMENT CONTEXT
        ==========================

        {context}

        ==========================
        QUESTION
        ==========================

        {question}

        ==========================
        RESPONSE
        ==========================
        """

        elif mode == "answer_insights":

                    prompt = f"""
        You are an AI Document Intelligence Assistant.

        Answer the user's question using ONLY the retrieved document context.

        After answering, analyze the retrieved evidence and produce a structured document analysis.

        STRICT RULES

        - Use ONLY the provided document context.
        - NEVER use outside knowledge.
        - NEVER invent facts.
        - NEVER guess.
        - If multiple retrieved sections discuss the same topic, combine them into one complete answer.
        - Every statement must be supported by the retrieved context.
        - If information is incomplete, explicitly state that the conclusion is based only on the available document evidence.
        - If the retrieved context does not contain enough information to answer the question, reply EXACTLY:

        I could not find sufficient information in the uploaded documents.

        DO NOT copy the template.
        DO NOT repeat instruction text.
        DO NOT write placeholders such as "Insight 1", "Finding 1", or "Recommendation 1".

        Instead, generate complete sentences using the retrieved document evidence.

        Return your response in EXACTLY the following format.

        ## Answer
        Provide a clear answer to the user's question in one or more complete sentences.

        ## Key Insights
        - Write 2 or 3 meaningful insights derived from the retrieved document.
        - Each insight must be a complete sentence.

        ## Important Findings
        - Write 2 important findings supported by the retrieved context.
        - Each finding must summarize important evidence from the document.

        ## Suggested Next Steps
        - Write 1 or 2 practical recommendations based ONLY on the retrieved document.
        - If no recommendation can reasonably be inferred from the document, write:
        "No further recommendations can be derived from the available document."

        Do not include any additional headings or explanations.

        ==========================
        DOCUMENT CONTEXT
        ==========================

        {context}

        ==========================
        QUESTION
        ==========================

        {question}

        ==========================
        RESPONSE
        ==========================
        """

        else:

            raise ValueError(
                f"Unsupported prompt mode: {mode}"
            )

        return prompt.strip()