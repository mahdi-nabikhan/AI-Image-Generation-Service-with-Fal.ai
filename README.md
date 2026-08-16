# AI Image Generation Service

A FastAPI service for asynchronous AI image generation using Fal.ai.
The service handles generation requests, manages user AI balance, and processes generation results through webhook callbacks.

## Installation

Install dependencies:

pip install -r src/requirements.txt


## Environment Variables

Create a `.env` file inside `src`:

FAL_KEY=your_fal_api_key

WEBHOOK_URL=https://your-public-url/generate/image/callback


## Run

Start the application:

uvicorn main:app --app-dir src --reload


API documentation:

http://localhost:8000/docs


## Docker

Run the application using Docker Compose:

docker compose up --build


## Webhook Development

Fal.ai requires a publicly accessible callback URL.

For local development, ngrok can be used:

ngrok http 8000


Set the generated URL as:

WEBHOOK_URL=https://your-ngrok-url/generate/image/callback


## Design Decisions

### Webhook instead of polling

The service uses Fal.ai webhook callbacks instead of polling the generation status.

After submitting a generation request, Fal.ai sends the result to the callback endpoint.
This reduces unnecessary API requests and provides event-driven processing.


### Idempotency

Webhook providers may send the same callback multiple times.

To prevent duplicate processing:

- Each generation request is stored with a unique request_id.
- The callback checks the current generation status before applying changes.
- Database row locking is used to prevent concurrent duplicate processing.

This ensures that:
- Generation results are not processed more than once.
- User balance is not refunded multiple times.


### Balance Management

The user's AI balance is checked before submitting a generation request.

The generation cost is deducted before sending the request to Fal.ai.

If submitting the request fails, the deducted amount is refunded.

If generation fails, the refund is performed only once using the is_refunded flag to prevent duplicate refunds.