import os
from dotenv import load_dotenv
from ollama import Client
from color_cli import color_text
from pydantic import BaseModel, ValidationError

load_dotenv()

class ToolCall(BaseModel):
    tool: str
    parameters: dict

def main():

    ollama_host = os.environ.get(
            "OLLAMA_HOST",
            "http://localhost:11434"
            )
    client = Client(host=ollama_host)

    while True:
        user_input = input(">>> ")

        quitting_words = ["bye", "exit", "q", "quit"]
        if user_input.lower() in quitting_words:
            print("bye!")
            break

        with open("./system-prompt.md", "r") as f:
            system_prompt = f.read()

        try:
            response = client.chat(
                    model="llama3.2",
                    messages=[
                        {
                            "role": "system",
                            "content": system_prompt
                        },
                        {
                            "role": "user",
                            "content": user_input
                        }
                    ],
                )

            print(response.message.content)
            response_content = response.message.content
            try:
                tool_call = ToolCall.model_validate_json(response_content)
                if tool_call.tool == "weather":
                    print("do tool call")
            except ValidationError as e:
                print("Response is not a tool call.")

        except Exception as e:
            print(f"\nERROR: {e}")

if __name__ == "__main__":
    main()
