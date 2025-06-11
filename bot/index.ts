import express from "express";
import { GoogleChatBot } from "./googleChatBot";

export const app = express();
const bot = new GoogleChatBot();

app.use(express.json());

app.post("/chat", async (req, res) => {
  try {
    const text = req.body.message?.text;
    if (!text || typeof text !== "string" || text.trim() === "") {
      res.status(400).json({ error: "Message text is required" });
      return;
    }
    const reply = await bot.handleMessage(text);
    res.json({ text: reply });
  } catch (error) {
    console.error("Error processing chat event", error);
    res.status(500).send("Internal server error");
  }
});

app.post("/mcp", async (req, res) => {
  try {
    const text = req.body.text || "";
    const reply = await bot.handleMessage(text);
    res.json({ text: reply });
  } catch (error) {
    console.error("Error processing MCP event", error);
    res.status(500).send("Internal server error");
  }
});

if (require.main === module) {
  const port = Number(process.env.PORT) || 3978;
  app.listen(port, () => {
    console.log(`Server started on port ${port}`);
  });
}
