import readline from "node:readline";
import { config } from "dotenv";
import { HumanMessage } from "@langchain/core/messages";
import { agent } from "./agent";

config();

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
});

async function askQuestion() {
  rl.question(">> ", async (query) => {
    if (["exit", "quit", "q"].includes(query.trim().toLowerCase())) {
      rl.close();
      return;
    }

    try {
      const stream = await agent.stream(
        {
          messages: [new HumanMessage(query)],
        },
        { streamMode: "messages" },
      );

      for await (const [chunk] of stream) {
        if (typeof chunk.content === "string") {
          process.stdout.write(chunk.content);
        } else if (Array.isArray(chunk.content)) {
          for (const part of chunk.content) {
            if (part.type === "text") {
              process.stdout.write(part.text as string);
            }
          }
        }
      }

      console.log();
    } catch (error) {
      console.error("Error:", error);
    }

    askQuestion();
  });
}

askQuestion();
