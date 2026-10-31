from app.services.vector_store import get_vector_store
from app.services.llm import llm
from app.prompts.rag_prompt import prompt


def ask_question(question: str):
    documents = get_vector_store().similarity_search(
        query=question,
        k=3,
    )

    context = "\n\n".join(
        doc.page_content for doc in documents
    )

    final_prompt = prompt.format(
        context=context,
        question=question
    )

    answer = llm.invoke(final_prompt)

    return {
        "question": question,
        "answer": answer,
        "page_numbers": [
            doc.metadata.get("page")
            for doc in documents
        ]
    }