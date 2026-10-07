9. API EXAMPLES
Create API_EXAMPLES.md.
Health
GET /health

PowerShell:
Invoke-RestMethod `
  -Uri "http://127.0.0.1:8000/health"

10. Ask API
POST /ask
Content-Type: application/json

Body:
{
  "question": "What is the leave policy?"
}

PowerShell:
$body = @{
    question = "What is the leave policy?"
} | ConvertTo-Json

Invoke-RestMethod `
  -Method Post `
  -Uri "http://127.0.0.1:8000/ask" `
  -ContentType "application/json" `
  -Body $body

The existing API documentation defines /ask as the question-answering endpoint and returns an answer plus sources.

ngest API
Document the actual schema from your running OpenAPI rather than inventing fields.
Open:
http://127.0.0.1:8000/docs

or:
http://127.0.0.1:8000/openapi.json

API ERROR EXAMPLES
200 → Successful request
400 → Invalid request
404 → Endpoint/resource unavailable
422 → Validation failure
500 → Server error