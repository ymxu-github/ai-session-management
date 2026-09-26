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
    """Call DeepSeek and print the model's response."""
    api_key = os.getenv(API_KEY_ENV)
    if not api_key:
        raise RuntimeError(
            f"Set the {API_KEY_ENV} environment variable before running this example."
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
            "You are a sweet AI assistant named Sweetie. "
            "Answer the user's questions in a gentle, affectionate tone."
        ),
    }
    user_message: ChatCompletionUserMessageParam = {
        "role": "user",
        "content": "Who are you? What can you help me with?",
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