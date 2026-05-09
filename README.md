# URL Shortener

A serverless URL shortener built on AWS Lambda, API Gateway, and DynamoDB.  
Supports URL creation, redirection, and click analytics. Tested using AWS free tier account

---

## Architecture

```text
POST /shorten             → Lambda → DynamoDB (write)
GET /{shortCode}          → Lambda → DynamoDB (read) → HTTP 302 redirect
GET /{shortCode}/stats    → Lambda → DynamoDB (read) → JSON response
```

---

## Tech Stack

- **Runtime:** Python 3.12
- **Compute:** AWS Lambda
- **API:** AWS API Gateway (REST)
- **Database:** AWS DynamoDB (single-table design)
- **CI/CD:** GitHub Actions
- **Testing:** pytest, moto

---

## Project Structure

```text
url-shortener/
├── src/
│   ├── handler.py       # Lambda entry point
│   ├── create.py        # POST /shorten logic
│   ├── redirect.py      # GET /{shortCode} logic
│   ├── analytics.py     # GET /{shortCode}/stats logic
│   ├── db.py            # DynamoDB helpers
│   └── utils.py         # Short code generator
├── tests/
│   ├── test_create.py
│   ├── test_redirect.py
│   └── test_analytics.py
└── requirements.txt
```

---

## API Endpoints

### Create Short URL

```http
POST /shorten
Content-Type: application/json
```

Request body:

```json
{
  "url": "https://example.com"
}
```

Response:

```json
{
  "short_url": "https://<api-id>.execute-api.<region>.amazonaws.com/prod/NargTf"
}
```

---

### Redirect

```http
GET /{shortCode}
```

Response:

```text
HTTP 302 redirect to original URL
```

---

### Analytics

```http
GET /{shortCode}/stats
```

Response:

```json
{
  "shortCode": "NargTf",
  "originalUrl": "https://example.com",
  "createdAt": "2026-05-09T04:30:17+00:00",
  "clicks": 5
}
```

---

## Local Development

Clone the repository and install dependencies:

```bash
git clone https://github.com/yourusername/url-shortener.git
cd url-shortener
pip install -r requirements.txt
```

Run tests:

```bash
python -m pytest tests/ -v
```

---

## Deployment

Package and deploy to Lambda manually:

```bash
zip -j deployment.zip src/*.py

aws lambda update-function-code \
  --function-name url-shortener \
  --zip-file fileb://deployment.zip
```

---

## Environment Variables

| Variable     | Description          | Default         |
|--------------|----------------------|-----------------|
| TABLE_NAME   | DynamoDB table name  | url-shortener   |
