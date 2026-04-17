# Use Node.js as the base image
FROM node:22-slim

# Install Python and pip
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy package.json and install Node dependencies
COPY package*.json ./
RUN npm install --omit=dev

# Install Python dependencies
# Using --break-system-packages as it's a dedicated container environment
RUN python3 -m pip install --break-system-packages numpy nltk pandas

# Download NLTK data
RUN python3 -c "import nltk; nltk.download('punkt'); nltk.download('punkt_tab')"

# Copy the rest of the application
COPY . .

# Expose port
EXPOSE 3000

# Environment variables (defaults)
ENV NODE_ENV=production
ENV PORT=3000

# Start the application
CMD ["node", "server.js"]
