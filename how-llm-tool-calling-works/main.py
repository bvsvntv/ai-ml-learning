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

        if user_input.lower() == 'quit':
            print("bye!")
            break

        response = client.chat(
                model='llama3.2',
                messages=[
                    {
                        'role': 'user',
                        'content': user_input
                    }
                ]
            )

        print(color_text(response.message.content, color='green'))


if __name__ == "__main__":
    main()
