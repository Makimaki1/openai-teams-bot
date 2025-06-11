# OpenAI Chat Bot

See [bot/README.md](./bot/README.md) for instructions on running the Google Chat bot.
For details on how messages work in Chat, check the [Google Chat message overview](https://developers.google.com/workspace/chat/messages-overview). The page also covers the [anatomy of a card message](https://developers.google.com/workspace/chat/messages-overview#anatomy-of-a-card-message), which is useful when customizing replies.
You can design cards visually using the [Card Builder](https://addons.gsuite.google.com/uikit/builder).

The `templates/cloudRun` folder contains example files for deploying the bot to Google Cloud Run. Older Azure/Teams templates were removed as they no longer apply to this project.

You could also try the [ChatGPT Teams Bot app](https://github.com/formulahendry/chatgpt-teams-bot) which uses the latest `gpt-3.5-turbo` model. `Turbo` is the same model family that powers ChatGPT.

![OpenAI](./bot/images/openai-chat.png)

