import psycopg2
from sentence_transformers import SentenceTransformer
from openai import OpenAI

class RAGService:
    def __init__(self, embedModel: SentenceTransformer, llmModel:OpenAI):
        self.embeddingModel = embedModel
        self.llmModel = llmModel
        self.llmID = self.llmModel.models.list().data[0].id
    
    def answer(self, dbConn:psycopg2.extensions.connection, question: str):        
        cursor = dbConn.cursor()

        queryEmbedding = self.embeddingModel.encode(question)

        cursor.execute("SELECT content FROM cat_facts ORDER BY embedding <=> %s::vector LIMIT 3;", (queryEmbedding.tolist(), )) #biar jadi tuple (queryEmbedding.tolist(), ), kalau queryembedding.tolist() doang bukan. ::vector maksa jadi vector
        result = cursor.fetchmany()
        cursor.close()

        context = "\n\n".join(
        f"{row[0]}"
        for row in result
        )

        instruction = f""""
        You are a helpful chatbor to answer question about cat facts.
        Answer the question using ONLY relevant information from the context.
        Ignore any information that is not related to the question.

        If the answer is not found in the context, say you dont know.
        
        Context:
        {context}

        Question:
        {question}

        Answer:
        """

        response = self.llmModel.responses.create(
            model=self.llmID,
            instructions=instruction,
            input=question,
        )
        return response.output_text
