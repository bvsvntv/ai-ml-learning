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
      const result = await agent.invoke({
        messages: [new HumanMessage(query)],
      });

      console.log(result.messages.at(-1)?.content);
    } catch (error) {
      console.error("Error:", error);
    }

    askQuestion();
  });
}

askQuestion();
