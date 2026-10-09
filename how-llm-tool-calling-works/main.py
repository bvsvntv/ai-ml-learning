import os
from dotenv import load_dotenv
from ollama import Client
from color_cli import color_text

load_dotenv()

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

        try:
            stream = client.chat(
                    model='llama3.2',
                    messages=[
                        {
                            'role': 'user',
                            'content': user_input
                            }
                        ],
                    stream=True
                    )

            for chunk in stream:
                print(chunk.message.content, end="", flush=True)

            print()

        except Exception as e:
            print(f"\nERROR: {e}")

if __name__ == "__main__":
    main()
