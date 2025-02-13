FROM python:3.12-alpine

# Install dependencies, including su-exec
RUN apk update && apk add --no-cache ffmpeg su-exec

# Create appuser and appgroup
RUN addgroup -g 1000 appgroup && adduser -D -u 1000 -G appgroup appuser

# Set environment variables
ARG SPOTSPOT_VERSION
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/spotspot \
    SPOTSPOT_VERSION=${SPOTSPOT_VERSION}

# Set the working directory
WORKDIR /app

# Copy the application code
COPY . .

# Install Python dependencies
RUN pip install --upgrade pip --root-user-action=ignore && \
    pip install --no-cache-dir --root-user-action=ignore -r requirements.txt
    
# Ensure proper ownership of directories
RUN mkdir -p /config /home/appuser/.spotdl/.spotipy /data  && \
    chown -R appuser:appgroup /config /home /data 

# Make script executable
RUN chmod +x /app/start.sh

# Expose the application port
EXPOSE 6544

# Use the start script as the entrypoint
ENTRYPOINT ["/app/start.sh"]
