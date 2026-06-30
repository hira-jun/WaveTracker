FROM node:20-slim

WORKDIR /app

COPY package.json /app/package.json
COPY tsconfig.json /app/tsconfig.json
COPY vite.config.ts /app/vite.config.ts
RUN npm install

COPY . /app

EXPOSE 3000

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "3000"]
