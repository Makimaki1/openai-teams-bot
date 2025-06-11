import OpenAI from "openai";
import config from "./config";

export class GoogleChatBot {
  private openai: OpenAI;

  constructor() {
    this.openai = new OpenAI({
      apiKey: config.openaiApiKey,
    });
  }

  async handleMessage(text: string): Promise<string> {
    try {
      const response = await this.openai.chat.completions.create({
        model: "gpt-3.5-turbo",
        messages: [{ role: "user", content: text }],
        temperature: 0,
      });
      return response.choices[0].message?.content ?? "";
    } catch (error: any) {
      console.error("OpenAI request failed", error.message || error);
      return "Sorry, I couldn't process your request.";
    }
  }
}
