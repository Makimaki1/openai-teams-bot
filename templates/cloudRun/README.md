# Google Cloud Run deployment

These files show one way to deploy the bot to [Cloud Run](https://cloud.google.com/run).

1. Build and push a container image:
   ```bash
   gcloud builds submit --tag gcr.io/PROJECT_ID/openai-chat-bot
   ```
2. Deploy to Cloud Run:
   ```bash
   gcloud run deploy openai-chat-bot \
     --image gcr.io/PROJECT_ID/openai-chat-bot \
     --platform managed --region us-central1 --allow-unauthenticated
   ```
3. Set the environment variables shown in `service.yaml` from the Cloud Run console or using `--update-env-vars`.

Your bot will be reachable at the URL shown after deployment.

