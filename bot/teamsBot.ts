import { Configuration, OpenAIApi } from "openai";
import config from "./config";

export class TeamsBot {
  private openai: OpenAIApi;

  constructor() {
    const configuration = new Configuration({
      apiKey: config.openaiApiKey,
    });
    this.openai = new OpenAIApi(configuration);
  }

  async handleMessage(text: string): Promise<string> {
    try {
      const response = await this.openai.createCompletion({
        model: "text-davinci-003",
        prompt: text,
        temperature: 0,
        max_tokens: 2048,
      });

      return response.data.choices[0].text ?? "";
    } catch (error) {
      console.error("OpenAI request failed", error);
      return "";
    }
  }
}
