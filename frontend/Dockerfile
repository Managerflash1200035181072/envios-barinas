# Imagen base de Node.js para el frontend Vite
FROM node:22-alpine

WORKDIR /app

# Copiar los manifiestos e instalar dependencias de forma reproducible
COPY package*.json ./
RUN npm ci

# Copiar el código fuente del frontend
COPY . .

# Puerto interno del servidor de desarrollo de Vite
EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
