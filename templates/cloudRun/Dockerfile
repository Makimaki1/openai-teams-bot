# Sample Dockerfile for deploying the bot to Google Cloud Run
FROM node:18
WORKDIR /app
COPY package*.json ./
RUN npm ci --omit=dev
COPY . .
RUN npm run build --if-present
CMD ["node", "lib/index.js"]
