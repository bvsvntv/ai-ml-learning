import z from "zod";

export const CurrentWeatherSchema = z.object({
  current_condition: z.array(
    z.object({
      temp_C: z.string(),
      FeelsLikeC: z.string(),
      humidity: z.string(),
      windspeedKmph: z.string(),
      weatherDesc: z.array(
        z.object({
          value: z.string(),
        }),
      ),
    }),
  ),
  nearest_area: z.array(
    z.object({
      areaName: z.array(z.object({ value: z.string() })),
      country: z.array(z.object({ value: z.string() })),
    }),
  ),
});
