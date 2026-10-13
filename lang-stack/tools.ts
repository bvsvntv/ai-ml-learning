import { tool } from "@langchain/core/tools";
import z from "zod";
import { model } from "./model";
import { CurrentWeatherSchema } from "./schema";

const add = tool(({ a, b }) => a + b, {
  name: "add",
  description: "Add two numbers",
  schema: z.object({
    a: z.number().describe("First number"),
    b: z.number().describe("Second number"),
  }),
});

const multiply = tool(({ a, b }) => a * b, {
  name: "multiply",
  description: "Multiply two numbers",
  schema: z.object({
    a: z.number().describe("First number"),
    b: z.number().describe("Second number"),
  }),
});

const divide = tool(({ a, b }) => a / b, {
  name: "divide",
  description: "Divide two numbers",
  schema: z.object({
    a: z.number().describe("First number"),
    b: z.number().describe("Second number"),
  }),
});

const weather = tool(
  async ({ city }) => {
    const weatherAPI = process.env.WEATHER_API_URL;
    if (!weatherAPI) throw new Error("WEATHER_API_URL not configured.");

    const url = `${weatherAPI}/${city}?format=j1`;

    try {
      const response = await fetch(url);
      if (!response.ok)
        throw new Error(
          `Failed to get weather info for ${city}. Error: ${response.status}`,
        );

      const raw: unknown = await response.json();
      const data = CurrentWeatherSchema.parse(raw);

      const current = data.current_condition[0];
      const area = data.nearest_area[0];

      if (!current) {
        throw new Error("Current weather data is unavailable");
      }

      return {
        city: area?.areaName[0]?.value ?? city,
        country: area?.country[0]?.value ?? "Unknown",
        temperatureC: Number(current.temp_C),
        feelsLikeC: Number(current.FeelsLikeC),
        condition: current.weatherDesc[0]?.value ?? "Unknown",
        humidity: Number(current.humidity),
        windKmph: Number(current.windspeedKmph),
      };
    } catch (error) {
      console.log(error);
    }
  },
  {
    name: "weather",
    description: "Get weather for a city",
    schema: z.object({
      city: z.string().describe("City name"),
    }),
  },
);

export const toolsByName = {
  [add.name]: add,
  [multiply.name]: multiply,
  [divide.name]: divide,
  [weather.name]: weather,
};

const tools = Object.values(toolsByName);
export const modelWithTools = model.bindTools(tools);
