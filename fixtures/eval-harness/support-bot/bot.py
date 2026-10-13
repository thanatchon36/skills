"""Reply to customer support emails for a small online bike-parts shop."""

import os
import sys

import anthropic

MODEL = os.environ.get("SUPPORT_MODEL", "claude-sonnet-5-5")
PROMPT = open(os.path.join(os.path.dirname(__file__), "prompts", "support_reply.txt")).read()


def reply(message: str) -> str:
    client = anthropic.Anthropic()
    resp = client.messages.create(
        model=MODEL,
        max_tokens=600,
        system=PROMPT,
        messages=[{"role": "user", "content": message}],
    )
    return resp.content[0].text


if __name__ == "__main__":
    print(reply(sys.stdin.read()))
