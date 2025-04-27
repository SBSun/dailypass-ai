import os
import weaviate

from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings

load_dotenv()

client = weaviate.Client(url=os.getenv("WEAVIATE_URL"),)

schema = {
    "classes": [
        {
            "class": "Question",
            "vectorizer": "none",
            "properties": [
                {
                    "name": "text",
                    "dataType": ["text"],
                },
            ],
        }
    ]
}

class QuestionVectorStore:
    _instance = None
    _client = client
    _embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

    @classmethod
    def get_instance(cls) -> "QuestionVectorStore":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        if not client.schema.exists(class_name="Question"):
            client.schema.create(schema)

    def generate_embedding(self, text: str) -> list:
        """질문 텍스트 임베딩"""
        return self._embeddings.embed_query(text)

    def find_similar_question(self, embedding: list, threshold: float = 0.8) -> bool:
        """임베딩을 기반으로 유사한 질문이 존재하는지 확인"""
        near_vector = {
            "vector": embedding,
            "certainty": threshold
        }
        result = self._client.query \
            .get("Question", ["text"]) \
            .with_near_vector(near_vector) \
            .with_limit(1) \
            .do()

        similar_questions = result["data"]["Get"]["Question"]
        print("찾은 유사한 질문:", similar_questions)
        return bool(similar_questions)

    def save_question(self, text: str, embedding: list) -> None:
        """질문 데이터를 백터화해서 저장"""
        data_object = {
            "text": text
        }
        self._client.data_object.create(
            data_object=data_object,
            class_name="Question",
            vector=embedding
        )

        print("질문이 성공적으로 Vector DB에 저장되었습니다.")