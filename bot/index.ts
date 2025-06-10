import express from "express";
import bodyParser from "body-parser";
import { google } from "googleapis";
import config from "./config";
import { TeamsBot } from "./teamsBot";

const bot = new TeamsBot();
const app = express();
app.use(bodyParser.json());

app.post("/chat", async (req, res) => {
  try {
    const text = req.body.message?.text || "";
    const reply = await bot.handleMessage(text);
    res.json({ text: reply });
  } catch (error) {
    console.error("Error processing chat event", error);
    res.status(500).send("Internal server error");
  }
});

const port = process.env.PORT || 3978;
app.listen(port, () => {
  console.log(`Server started on port ${port}`);
});
