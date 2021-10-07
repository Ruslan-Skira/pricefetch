# pricefetch
fetch the price of the currencies 



**Backend task:**

Write an API using Django that fetches the price of BTC/USD from the alphavantage
API every hour, and stores it on postgres. This API must be secured which means that
you will need an API key to use it. There should be two endpoints:
GET /api/v1/quotes - returns exchange rate and POST /api/v1/quotes which triggers
force requesting the prices from alphavantage. The API & DB should be
containerized using Docker as well.
- Every part should be implemented as simple as possible.
-The project should be committed to GitHub.
-The technologies to be used: Celery, Redis or RabbitMQ, Docker and Docker
Compose.
- The sensitive data such as alphavantage API key, should be passed from the .env
