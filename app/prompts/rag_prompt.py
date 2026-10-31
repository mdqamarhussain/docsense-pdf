from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_template(
    """
Answer the question using only the context below.
If the answer is not present in the context, say "I don't know".

Context:
{context}

Question:
{question}
"""
)