from dataclasses import dataclass
from enum import Enum
from typing import Literal


class ModelProvider(str, Enum):
    OLLAMA = "ollama"
    LMSTUDIO = "lmstudio"


@dataclass
class ModelConfig:
    name: str
    temperature: float
    provider: ModelProvider


QWEN_2_5 = ModelConfig(
    name="qwen2.5-coder-7b-instruct",
    temperature=0.0,
    provider=ModelProvider.LMSTUDIO,
)


class Config:
    SEED = 42
    MODEL = QWEN_2_5

    class Server:
        HOST = "localhost"
        PORT = 3001
        SSE_PATH = "/sse"
        TRANSPORT: Literal["sse", "stdio"] = "sse"

    class Agent:
        MAX_ITERATIONS = 10
