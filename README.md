# Assignment 2
# Penguin Species Classification API

A production-ready FastAPI application that predicts penguin species (Adelie, Chinstrap, Gentoo) based on physical measurements using XGBoost machine learning with Google Cloud Storage integration and containerized deployment.

## Project Overview

This project implements a machine learning API that classifies penguin species using the Palmer Penguins dataset. The API accepts penguin physical measurements and returns species predictions with high accuracy.

### Key Features

- ** High Accuracy ML Model**: XGBoost classifier trained on Palmer Penguins dataset
- ** FastAPI REST API**: Modern, fast, and automatic documentation generation
- ** Cloud Integration**: Google Cloud Storage for model storage and retrieval
- ** Docker Containerized**: Production-ready container for consistent deployment
- ** Comprehensive Testing**: 77% code coverage with 49+ unit tests
- ** Load Testing**: Locust integration for performance validation
- ** Production Ready**: Health checks, error handling, and monitoring

###  Tech Stack

- **Backend**: FastAPI, Python 3.10, Uvicorn
- **ML Framework**: XGBoost, Scikit-learn, Pandas, NumPy
- **Cloud Platform**: Google Cloud Storage, Cloud Run
- **Containerization**: Docker with multi-layer optimization
- **Testing**: Pytest (unit), Locust (load testing)

## Setup Instructions

### Prerequisites

- Python 3.10+
- Docker Desktop
- Google Cloud SDK (gcloud CLI)
- Git

### Local Development Setup

1. **Clone and Navigate**
```bash
git clone <repository-url>
cd lab3_Rozy_Patel
```

2. **Setup Virtual Environment**
```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate
```

3. **Install Dependencies**
```bash
pip install -r requirements-minimal.txt
```

4. **Train Model (Optional)**
```bash
python train.py
```

5. **Run API Locally**
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

6. **Access Endpoints**
- **API Root**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health


###  Docker Deployment

```bash
# Build the Docker image
docker build -t penguin-api .

# Run container with GCS integration
docker run -d -p 8080:8080 \
  --name penguin-api-container \
  -v "${PWD}/app/data/penguin-ml-api-*.json:/gcp/sa-key.json:ro" \
  -e GOOGLE_APPLICATION_CREDENTIALS=/gcp/sa-key.json \
  -e GCS_BUCKET_NAME=penguin-models \
  -e GCS_BLOB_NAME=pen_model.json \
  penguin-api
```

###  Cloud Run Deployment

```bash
# Tag for Artifact Registry
docker tag penguin-api us-central1-docker.pkg.dev/penguin-ml-api/penguin-api-repo/penguin-api:latest

# Push to registry
docker push us-central1-docker.pkg.dev/penguin-ml-api/penguin-api-repo/penguin-api:latest

# Deploy to Cloud Run
gcloud run deploy penguin-api \
  --image us-central1-docker.pkg.dev/penguin-ml-api/penguin-api-repo/penguin-api:latest \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 8080 \
  --memory 2Gi \
  --cpu 1 \
  --max-instances 100
```

## API Documentation

### Available Endpoints

#### `GET /` - Root Endpoint
Returns API information and status.

**Response:**
```json
{
  "message": "Penguin Species Classification API",
  "version": "1.0.0"
}
```

#### `GET /health` - Health Check
Monitoring endpoint for container orchestration.

**Response:**
```json
{
  "status": "ok"
}
```

#### `POST /predict` - Species Prediction
Main endpoint for penguin species classification.

### 🐧 Complete Species Examples

#### Adelie Penguin (Smallest Species)
**Request:**
```json
{
  "bill_length_mm": 39.1,
  "bill_depth_mm": 18.7,
  "flipper_length_mm": 181,
  "body_mass_g": 3750,
  "year": 2007,
  "sex": "male",
  "island": "Torgersen"
}
```

**Response:**
```json
{
  "prediction": "Adelie"
}
```

#### Gentoo Penguin (Largest Species)
**Request:**
```json
{
  "bill_length_mm": 50.0,
  "bill_depth_mm": 15.2,
  "flipper_length_mm": 230,
  "body_mass_g": 6050,
  "year": 2008,
  "sex": "male",
  "island": "Biscoe"
}
```

**Response:**
```json
{
  "prediction": "Gentoo"
}
```

#### Chinstrap Penguin (Medium Species)
**Request:**
```json
{
  "bill_length_mm": 46.5,
  "bill_depth_mm": 17.9,
  "flipper_length_mm": 192,
  "body_mass_g": 3500,
  "year": 2009,
  "sex": "female",
  "island": "Dream"
}
```

**Response:**
```json
{
  "prediction": "Chinstrap"
}
```

### Input Validation Schema

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `bill_length_mm` | float | 30.0 - 60.0 | Bill length in millimeters |
| `bill_depth_mm` | float | 10.0 - 25.0 | Bill depth in millimeters |
| `flipper_length_mm` | int | 170 - 240 | Flipper length in millimeters |
| `body_mass_g` | int | 2500 - 7000 | Body mass in grams |
| `year` | int | 2007 - 2009 | Year of observation |
| `sex` | enum | "male", "female" | Penguin sex |
| `island` | enum | "Torgersen", "Biscoe", "Dream" | Island location |

---

##  Production Questions & Answers

### 1. What edge cases might break your model in production that aren't in your training data?

Climate Change Effects: The training data is from 2007-2009, but climate change could make penguins smaller or larger due to environmental stress, different food sources, or habitat loss. The model has never seen these climate-adapted penguins.

Injured or Sick Penguins: Training data likely only includes healthy penguins. In production, you might encounter penguins with broken bills, damaged flippers, or diseases that make them much lighter or heavier than normal ranges.

New Geographic Locations: The model only knows 3 islands (Torgersen, Biscoe, Dream). Penguins from unexplored islands, different climates, or even captive penguins in zoos might have completely different physical characteristics.

Hybrid Species: Training assumes pure species, but real penguins sometimes interbreed. A hybrid between Adelie and Chinstrap would have mixed characteristics that don't match any pure species the model learned.

Measurement Errors: Real-world data isn't perfect - you might get impossible values like negative weights, equipment failures, human recording errors, or confusion between metric and imperial units.

Seasonal Variations: The model might not have seen penguins during molting season (when they're lighter), breeding season (different body conditions), or migration periods when their measurements change significantly.


### 2. What happens if your model file becomes corrupted?

If my model file gets corrupted, the penguin API would crash during startup when it tries to load the XGBoost model. The application would fail with a 500 Internal Server Error, and since the health check at /health probably depends on the model being loaded, Cloud Run would keep restarting the container over and over in a crash loop.

My current setup has a basic fallback where it tries to download the model from Google Cloud Storage first, and if that fails, it uses a local backup copy in the container. But if both files are corrupted, the whole service goes down. There's no graceful handling right now - it just crashes hard and users get error pages.

The recovery process would be pretty manual - I'd need to either fix the corrupted model file in GCS, redeploy the container with a fresh model, or roll back to a previous working version. Cloud Run's health checks would eventually mark the service as unhealthy, but there's no automatic recovery mechanism built in.

A better approach would be to validate the model file before loading it, keep multiple backup versions, and maybe serve a "service temporarily unavailable" message instead of just crashing when the model can't load.


### 3. What's a realistic load for a penguin classification service?

A realistic load really depends on who's using the penguin classification service. For a research institution or university, I'd expect maybe 50-200 requests per day during active research periods, with bursts of 10-20 requests per hour when students are working on assignments or researchers are processing field data. That's pretty light load - maybe 1-5 requests per minute at peak.

If it's serving a educational platform or public API, the load could be much higher. Think about a biology class where 30 students are all submitting penguin data for homework - you might get 100-500 requests in a short burst, then nothing for hours. During exam periods or project deadlines, it could spike to 1000+ requests in a day.

For a commercial API service, I'd plan for maybe 10-50 requests per second during business hours if it's popular, scaling down to almost nothing overnight. The tricky part is handling those burst periods - like when a research paper gets published and suddenly everyone wants to try penguin classification.

My current Cloud Run setup can handle maybe 50-100 requests per second with auto-scaling, which is probably overkill for most realistic penguin research scenarios. The bigger challenge is likely the unpredictable burst patterns rather than sustained high volume, since penguin research isn't exactly a 24/7 high-traffic use case

### 4. How would you optimize if response times are too slow?

If my penguin API is running slow, the first thing I'd do is bump up the resources in Cloud Run - increase from 1 CPU to 2-4 CPUs and maybe double the memory to 4GB since machine learning predictions can be CPU intensive. I'd also set minimum instances to 2 or 3 so there are always warm containers ready instead of waiting for cold starts every time.

The biggest optimization would be keeping the XGBoost model loaded in memory at startup instead of loading it fresh for each request. Right now the model gets loaded from either Google Cloud Storage or local file every time someone makes a prediction, which adds unnecessary delay. Loading it once and caching it in memory could cut response times in half.

If that's still not fast enough, I'd add Redis caching for predictions since penguin measurements probably repeat often in research scenarios, and consider reducing the number of concurrent requests per container so each one gets more dedicated resources to process faster.


### 5. What metrics matter most for ML inference APIs?

For ML inference APIs like my penguin classifier, the most critical metrics are response time and accuracy. Response time matters because users expect fast predictions - ideally under 200ms for real-time applications. I track P50, P95, and P99 percentiles since average response time can hide problems when some requests take much longer than others.

Model accuracy metrics are equally important since wrong predictions defeat the purpose. I monitor prediction confidence scores to catch when the model is uncertain, and watch for data drift by tracking the distribution of species predictions over time. If suddenly 80% of predictions are Adelie instead of the expected 44%, something's probably wrong with the input data.

Availability and error rates are also crucial - the API needs to stay up and handle edge cases gracefully. I track 4xx errors (bad user input) separately from 5xx errors (my system problems), and monitor throughput to ensure the service can handle the expected load without degrading.

Finally, resource utilization metrics like memory and CPU usage help with capacity planning and cost optimization, especially on Cloud Run where you pay for what you use. Keeping an eye on these prevents the containers from running out of resources and crashing during high traffic periods.

### 6. Why is Docker layer caching important for build speed? (Did you leverage it?)

Docker layer caching is crucial because it saves tons of time during development and deployment. When you rebuild a Docker image, Docker is smart enough to reuse layers that haven't changed, so you don't have to reinstall everything from scratch every time.

Looking at my Dockerfile, I partially leveraged caching but missed some opportunities. The good news is that my base image python:3.10-slim gets cached, and my system dependencies like build-essential and gcc only reinstall when the Dockerfile changes. However, I made a mistake by copying all my application files with COPY . . before installing Python dependencies. This means every time I change a single line of code, Docker has to reinstall all my Python packages again, which can take 2-3 minutes.

A better approach would have been to copy just the requirements-minimal.txt file first, install the dependencies, and then copy the application code. That way, I only reinstall packages when the requirements actually change, not when I modify my Python code. With proper layer caching, a code change rebuild could drop from 3 minutes to just 30 seconds, which really adds up during development when you're rebuilding constantly.

### 7. What security risks exist with running containers as root?

Running containers as root is a major security risk because if an attacker manages to break out of the container, they'd have full administrator privileges on the host system. My current Dockerfile doesn't specify a user, which means it runs as root by default - that's definitely not ideal for production.

The biggest danger is container escape attacks. If there's a vulnerability in Docker or the kernel, a root user inside the container could potentially access the host file system, read sensitive files, install malware, or even take control of other containers running on the same machine. It's like giving a burglar the master key to your entire building instead of just one room.

Another risk is that root can bind to privileged network ports (under 1024), access any mounted volumes with full permissions, and potentially interfere with system processes if the container shares the host's process namespace. Even simple mistakes like mounting the wrong directory could expose sensitive host files.

The fix is pretty straightforward - I should add a non-root user to my Dockerfile with something like RUN adduser --disabled-password appuser and then USER appuser before the CMD line. Cloud Run provides additional protection with gVisor sandboxing, but it's still best practice to follow the principle of least privilege and not run as root unless absolutely necessary.


### 8. How does cloud auto-scaling affect your load test results?

Cloud auto-scaling really messes with load test results because you're not testing a static system - you're testing a system that's constantly changing during the test. When I run my Locust tests against Cloud Run, the first few minutes show terrible performance with response times of 2-3 seconds because new containers are cold starting. Then performance suddenly improves as instances warm up and reach steady state.

The biggest issue is that my load test results don't represent real-world performance. If I'm testing 50 concurrent users ramping up over 2 minutes, most of that test time is spent watching Cloud Run scramble to spin up new instances rather than measuring actual application performance. The average response time gets skewed by all those cold starts, so a test might show 800ms average when the steady-state performance is actually 150ms.

It also makes it hard to find the true capacity limits. My stress tests might show the system "failing" at 30 concurrent users, but that's really just the auto-scaler not keeping up with the ramp rate, not the actual application bottleneck. If I had pre-warmed instances, the same system could probably handle 100+ users easily.

The solution is to either pre-warm the system before testing by sending gradual traffic for 5-10 minutes, or set minimum instances to avoid cold starts entirely. Otherwise, you're testing the auto-scaling behavior more than the application performance, which gives misleading results for capacity planning.


### 9. What would happen with 10x more traffic?
If my penguin API suddenly got 10x more traffic, Cloud Run would aggressively start spinning up new containers to handle the load, but there'd be a painful period where users experience really slow response times or timeouts. My current setup handles maybe 50-100 requests per second comfortably, so 10x would mean 500-1000 RPS hitting the system.

The auto-scaler would frantically create new instances, but each one takes 2-3 seconds to cold start, so during that ramp-up period, a lot of requests would queue up or fail with timeouts. I'd probably see my error rate spike to 10-20% for the first few minutes as the system struggles to catch up. Even with my max instances set to 100, it might not scale fast enough to handle the sudden surge.

The bigger problem is that each container can probably only handle 10-20 concurrent requests efficiently given the machine learning processing, so I'd need 25-50 instances running simultaneously. That means potentially 50-100GB of total memory usage across all containers, which would get expensive fast on Cloud Run's pay-per-use pricing.

My GCS model downloads could also become a bottleneck if all those new containers try to fetch the model file at once, though the caching should help. The system would eventually stabilize and handle the load fine, but those first few minutes would be rough for users. I'd definitely need to set minimum instances and maybe implement request queuing to handle traffic spikes more gracefully.

### 10. How would you monitor performance in production?
For monitoring my penguin API in production, I'd set up multiple layers of monitoring to catch issues before users notice them. First, I'd add custom metrics directly in the FastAPI app to track response times, prediction confidence scores, and error rates for each endpoint. Something simple like logging every request duration and whether predictions have low confidence scores.

Cloud Run already provides basic infrastructure metrics like CPU usage, memory consumption, and request counts, which I can view in Google Cloud Console. I'd set up alerts for things like response times over 1 second, error rates above 5%, or memory usage approaching the 2GB limit. These would send notifications to Slack or email when something's wrong.

For deeper application monitoring, I'd integrate Prometheus metrics and create a dashboard showing business-specific metrics like the distribution of penguin species predictions over time. If suddenly 90% of predictions are Adelie instead of the normal 44%, that's a sign something's wrong with the input data or model. I'd also track model confidence trends to spot potential data drift.

The most important thing is setting up proper alerting for the stuff that actually matters - like if the service goes down, response times get terrible, or the model starts making obviously wrong predictions. I'd rather get woken up at 2am for a real problem than miss an issue that affects researchers trying to use the API during their field work.


### 11. How would you implement blue-green deployment?
For blue-green deployment with my penguin API on Cloud Run, I'd deploy the new version (green) alongside the current one (blue) without sending any traffic to it initially. I'd use Cloud Run's traffic splitting feature to gradually shift users from the old version to the new one.

First, I'd deploy the green version with a specific tag like gcloud run deploy penguin-api --image my-new-image:v2 --tag green --no-traffic. This creates the new version but keeps 100% of traffic on the current blue version. Then I'd run automated tests against the green URL to make sure it's working - checking that all three penguin species predictions work correctly, response times are reasonable, and the health endpoint responds properly.

Once I'm confident the green version is stable, I'd gradually shift traffic using Cloud Run's built-in traffic management. Start with 10% traffic to green and 90% to blue, monitor for 10-15 minutes watching error rates and response times. If everything looks good, bump it to 50-50, then eventually 100% to green. The whole process might take 30-60 minutes to be safe.

The beauty of this approach is that if anything goes wrong during the transition, I can instantly roll back to 100% blue traffic with a single command. Cloud Run handles all the load balancing automatically, so users don't experience any downtime. Once I'm confident the green deployment is successful, I can delete the old blue revision to clean up resources and save costs.

### 12. What would you do if deployment fails in production?
If my penguin API deployment fails in production, my first priority is getting the service back online as quickly as possible, then figuring out what went wrong. I'd immediately roll back to the previous working version using Cloud Run's traffic splitting - just run gcloud run services update-traffic penguin-api --to-revisions previous-stable=100 to route all traffic back to the last known good deployment.

Looking at my Dockerfile, the most likely failure points are during the container startup - maybe the health check at /health is failing, the model file can't be loaded from GCS, or there's a dependency issue in requirements-minimal.txt. Cloud Run's logs would tell me exactly where it's crashing, whether it's a Python import error, missing environment variables, or the uvicorn server not starting properly.

Once I've rolled back and users can access the service again, I'd investigate the root cause by checking the deployment logs, testing the new image locally with docker run, and making sure all the environment variables and GCS credentials are set correctly. Common issues might be a corrupted model file, version conflicts in the Python dependencies, or the health check endpoint returning errors.

For future deployments, I'd implement better safeguards like running automated tests against the new version before switching traffic, using blue-green deployment to test alongside the current version, and having monitoring alerts that automatically trigger rollbacks if error rates spike above 5% or response times exceed reasonable thresholds. The key is having a tested rollback plan so you can recover quickly rather than scrambling to debug while the service is down.

### 13. What happens if your container uses too much memory?

If my penguin API container uses too much memory, it gets killed by Cloud Run with an "Out of Memory" (OOM) error and automatically restarts. Since I've set the memory limit to 2GB in my Cloud Run configuration, once the container tries to use more than that, the system forcefully terminates it to protect other services running on the same host.

When this happens, users would see 503 Service Unavailable errors while the container restarts, which usually takes 10-15 seconds. The health check in my Dockerfile would fail during this restart period since the /health endpoint wouldn't be accessible. Cloud Run would keep trying to restart the container, but if the memory issue persists, it could get stuck in a crash loop.

The most likely culprit in my case would be the XGBoost model and machine learning libraries eating up memory, especially if multiple requests are being processed simultaneously. Each prediction might load additional data into memory, and if I'm not properly cleaning up after requests or if there's a memory leak, the container could gradually consume more RAM until it hits the limit.

To fix this, I'd first increase the memory limit to 4GB or 8GB in the Cloud Run deployment settings, then reduce the number of concurrent requests per container so each one gets more dedicated memory. I could also add memory monitoring to track usage over time and implement request-level cleanup to free memory after each prediction. The key is balancing memory allocation with cost, since more memory means higher Cloud Run bills.



