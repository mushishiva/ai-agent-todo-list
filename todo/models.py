from langchain_openai import ChatOpenAI
from pydantic import SecretStr

from todo.config import ModelConfig


def create_llm(model: ModelConfig) -> ChatOpenAI:
    """LM Studio"""

    return ChatOpenAI(
        base_url="http://localhost:1234/v1",
        api_key=SecretStr("no-api-key"),
        model="qwen3-8b",
    )
