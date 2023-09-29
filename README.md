# Usage
```
docker build -t taipei-arena .
docker run -e DATE="${DATE_TO_QUERY}" -e WEBHOOK_URL="${DISCORD_WEBHOOK_URL}" taipei-arena
```