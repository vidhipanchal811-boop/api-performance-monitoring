# API Performance Testing & Automated Deployment Monitoring

A DevOps-focused project for testing API performance, evaluating performance against defined thresholds, and monitoring historical performance results.

## Project Overview

This project provides a REST API that can execute performance tests against HTTP/HTTPS endpoints and generate structured performance reports.

The system measures response time, success rate, throughput, and percentile-based performance metrics. It also evaluates the results against configurable performance thresholds and maintains a history of previous performance tests.

## Current Features

- REST API built with FastAPI
- User CRUD operations
- Sequential API performance testing
- Concurrent API performance testing
- Response time measurement
- Average response time
- Minimum response time
- Maximum response time
- P95 response time
- P99 response time
- Successful and failed request tracking
- Success rate calculation
- Requests-per-second calculation
- Structured performance reports
- Performance threshold evaluation
- Automatic PASS/FAIL performance status
- Performance test history
- Performance history API
- Automated testing with pytest

## API Endpoints

### Basic Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Check that the API is running |
| GET | `/health` | Health check |
| GET | `/users` | Get all users |
| GET | `/users/{user_id}` | Get a specific user |
| POST | `/users` | Create a user |
| PUT | `/users/{user_id}` | Update a user |
| DELETE | `/users/{user_id}` | Delete a user |

### Performance Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/performance-test` | Run an API performance test |
| GET | `/performance-history` | View previous performance test reports |

## Performance Testing

The `/performance-test` endpoint supports two modes:

### Sequential

Requests are executed one after another.

```json
{
  "url": "https://httpbin.org/get",
  "number_of_requests": 5,
  "mode": "sequential"
}
