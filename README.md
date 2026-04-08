## URL Shortener 3000
Simple FastAPI microservice for shortening URLs.

#### Endpoints:
- `POST /shorten { "url": "https://example.com" } -> { "short_id": "..." }`
- `GET /{short_id} -> redirect to original URL (increments visits)`
- `GET /stats/{short_id} -> { short_id, url, visits }`


#### 🔧 Build: 
```
docker compose build app
```
#### 🕵️‍♀️ Test: 
```
docker compose run app python -m pytest
```
#### 🟢 Run: 
```
docker compose up app -d
```

