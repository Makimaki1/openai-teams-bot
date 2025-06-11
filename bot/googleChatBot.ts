import { Configuration, OpenAIApi } from "openai";

export class GoogleChatBot {
  private openai: OpenAIApi;

  constructor() {
    const apiKey = process.env.OPENAI_API_KEY;
    if (!apiKey) {
      throw new Error(
        'Missing OPENAI_API_KEY. Please set the OPENAI_API_KEY environment variable.'
      );
    }
    const configuration = new Configuration({ apiKey });
    this.openai = new OpenAIApi(configuration);
  }

  async handleMessage(text: string): Promise<string> {
    try {
      const response = await this.openai.createChatCompletion({
        model: "gpt-3.5-turbo",
        messages: [{ role: "user", content: text }],
        temperature: 0,
      });
      return response.data.choices[0].message?.content ?? "";
    } catch (error: any) {
      console.error("OpenAI request failed", error.message || error);
      return "Sorry, I couldn't process your request.";
    }
  }
}

