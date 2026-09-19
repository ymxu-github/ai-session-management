import os

from openai import OpenAI
from openai.types.chat import (
    ChatCompletionSystemMessageParam,
    ChatCompletionUserMessageParam,
)


API_KEY_ENV = "DEEPSEEK_API_KEY"
BASE_URL = "https://api.deepseek.com"
MODEL = "deepseek-chat"


def main() -> None:
    """调用 DeepSeek 并输出模型回复。"""
    api_key = os.getenv(API_KEY_ENV)
    if not api_key:
        raise RuntimeError(
            f"请先设置环境变量 {API_KEY_ENV}，再运行此示例。"
        )

    client = OpenAI(
        api_key=api_key,
        base_url=BASE_URL,
        timeout=30.0,
        max_retries=2,
    )

    system_message: ChatCompletionSystemMessageParam = {
        "role": "system",
        "content": (
            "你是一名非常可爱的AI助理，名字叫小甜甜，"
            "请使用温柔可爱的语气回答用户的问题。"
        ),
    }
    user_message: ChatCompletionUserMessageParam = {
        "role": "user",
        "content": "你是谁？你能帮我做什么？",
    }

    response = client.chat.completions.create(
        model=MODEL,
        messages=(system_message, user_message),
    )

    answer = response.choices[0].message.content
    if answer:
        print(answer)


if __name__ == "__main__":
    main()