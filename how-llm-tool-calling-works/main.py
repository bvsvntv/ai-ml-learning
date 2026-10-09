import os
from dotenv import load_dotenv
from ollama import Client
from color_cli import color_text
from pydantic import BaseModel, Field, ValidationError
import requests

load_dotenv()

class ToolCall(BaseModel):
    tool: str
    parameters: dict

class WeatherDescription(BaseModel):
    value: str

class WeatherCondition(BaseModel):
    weather: list[WeatherDescription] = Field(alias="weatherDesc")
    temperature: float = Field(alias="temp_C")
    humidity: float
    wind_speed: float = Field(alias="windspeedKmph")


class WeatherResponse(BaseModel):
    current_condition: list[WeatherCondition]


def weather_tool(location: str) -> str:
    weather_api_url = os.environ.get(
            "WEATHER_API_URL",
            "https://wttr.in"
            )

    url = f"{weather_api_url}/{location}?format=j1"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        weather_data = WeatherResponse.model_validate(response.json())
        current = weather_data.current_condition[0]

        description = current.weather[0].value

        return (
            f"The weather in {location} is {description}, "
            f"with a temperature of {current.temperature}°C, "
            f"humidity of {current.humidity}%, "
            f"and wind speed of {current.wind_speed} km/h."
        )

    except (requests.RequestException, ValidationError, IndexError, KeyError) as e:
        return f"Error retrieving weather for {location}: {e}"


def kelvin_to_celsius(kelvin):
    temp = kelvin - 273.15
    return f"{temp:.1f}"


def main():

    ollama_host = os.environ.get(
            "OLLAMA_HOST",
            "http://localhost:11434"
            )
    client = Client(host=ollama_host)

    while True:
        user_input = input("> ")

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

            response_content = response.message.content

            try:
                tool_call = ToolCall.model_validate_json(response_content)
                if tool_call.tool == "weather":
                    location = tool_call.parameters.get("city", "unknown")
                    if not location:
                        print("Weather tool requires a location.")

                    weather = weather_tool(location)
                    response_content = weather

            except ValidationError as e:
                print(color_text("Response is not a tool call.", color='yellow'))

            print(color_text(">", color='green'), response_content)

        except Exception as e:
            print(f"\nERROR: {e}")


if __name__ == "__main__":
    main()
