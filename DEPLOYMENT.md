# DEPLOYMENT.md

## Docker Containerization Documentation

This document describes the containerization process for the Lab 3 Penguin Classification API using Docker.

## Build and Run Commands

### Build the Docker Image
```bash
docker build -t lab3-penguin-api .
```

### Run the Container
```bash
docker run -p 8080:8080 lab3-penguin-api
```

### Monitor Container Resources
```bash
# Single snapshot of resource usage
docker stats --no-stream

# Continuous monitoring (press Ctrl+C to stop)
docker stats
```

### Inspect Image Details
```bash
docker inspect lab3-penguin-api
```

### List Local Images
```bash
docker images
```

## Issues Encountered and Solutions

### 1. **Initial Requirements.txt Error**
- **Issue**: Docker build failed during `pip install -r requirements.txt` with exit code 1
- **Cause**: The generated requirements.txt had 251 packages with potential conflicts
- **Solution**: Created a minimal requirements file (`requirements-minimal.txt`) with only essential packages:
  ```
  fastapi==0.116.1
  uvicorn==0.35.0
  xgboost==3.0.2
  pandas==2.3.1
  scikit-learn==1.7.1
  pydantic==2.11.7
  google-cloud-storage==2.18.0
  python-dotenv==1.0.1
  ```

### 2. **Image Name Mismatch**
- **Issue**: `docker run` command failed with "image not found" error
- **Cause**: Typo in image name (`lab3-penguin-apk` vs `lab3-penguin-api`)
- **Solution**: Used correct image name that was actually built: `lab3-penguin_apk`

### 3. **Container Access Issues**
- **Issue**: Initial confusion about Docker pull vs build
- **Cause**: Trying to pull non-existent image from registry instead of building locally
- **Solution**: Used `docker build` to create image locally first

## Performance Observations

### Container Resource Usage
Based on `docker stats` monitoring:

```
CONTAINER ID   NAME          CPU %     MEM USAGE / LIMIT   MEM %     NET I/O         BLOCK I/O     PIDS
61a177413e23   gifted_pike   0.21%     113MiB / 7.57GiB    1.46%     1.17kB / 126B   52.1MB / 0B   39
```

**Performance Summary:**
- **CPU Usage**: 0.21% (very efficient, low CPU overhead)
- **Memory Usage**: 113 MiB (~113 MB)
- **Memory Percentage**: 1.46% of available system RAM
- **Network I/O**: Minimal (1.17kB in / 126B out)
- **Process Count**: 39 processes running in container

**Analysis:**
- Excellent resource efficiency for a ML API
- Low memory footprint suitable for cloud deployment
- Minimal CPU usage when idle
- Fast startup time with uvicorn

## Security Observations

### Dockerfile Security Features
1. **Minimal Base Image**: Uses `python:3.10-slim` for reduced attack surface
2. **Environment Variables**: Proper Python configuration for container environment
3. **System Cleanup**: Removes apt cache and build dependencies after installation
4. **Health Checks**: Includes health endpoint monitoring
5. **Non-Root Consideration**: Initially included non-root user (removed for simplicity)

### Security Recommendations for Production
- Consider adding non-root user back for production deployment
- Use multi-stage builds to further reduce image size
- Scan image for vulnerabilities with tools like `docker scan`
- Implement proper secrets management for GCS credentials

## Docker Image Analysis

### Image Summary from `docker inspect`

**Basic Information:**
- **Image ID**: `sha256:b052ecb7d56763fe7f8dfdd16d4aba136d7e41b01b4072d6a33fdfccf94504ad`
- **Size**: 1,496,542,744 bytes (≈ 1.5 GB)
- **Architecture**: amd64
- **OS**: linux
- **Created**: 2025-08-06T20:46:09.239509853Z

### Image Layers Analysis

The image consists of **8 layers**:

1. **Layer 1** (`sha256:7cc7fe68...`): Base Python 3.10-slim layer
2. **Layer 2** (`sha256:d379451f...`): System package updates and dependencies
3. **Layer 3** (`sha256:3ba4af07...`): Build tools (gcc, build-essential)
4. **Layer 4** (`sha256:f6dc80d9...`): curl installation for health checks
5. **Layer 5** (`sha256:5256c89b...`): Python pip upgrade and package installation
6. **Layer 6** (`sha256:2cb03b7f...`): Application code copy
7. **Layer 7** (`sha256:ee2658d0...`): Additional configuration
8. **Layer 8** (`sha256:204453f4...`): Final layer with CMD and metadata

### Configuration Details

**Runtime Configuration:**
```json
{
  "Cmd": ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"],
  "ExposedPorts": {"8080/tcp": {}},
  "WorkingDir": "/app",
  "Env": [
    "PYTHONDONTWRITEBYTECODE=1",
    "PYTHONUNBUFFERED=1"
  ]
}
```

**Health Check Configuration:**
- **Interval**: 30 seconds
- **Timeout**: 30 seconds
- **Retries**: 3
- **Start Period**: 5 seconds
- **Command**: `curl -f http://localhost:8080/health || exit 1`

## Size Optimization Opportunities

### Current Size Analysis
- **Total Size**: ~1.5 GB
- **Base Image**: Python 3.10-slim (~100 MB)
- **Dependencies**: ML libraries (pandas, scikit-learn, xgboost) add significant size
- **Build Tools**: gcc and build-essential needed for compilation

### Optimization Recommendations
1. **Multi-stage Build**: Use builder stage for compilation, copy only runtime artifacts
2. **Alpine Base**: Consider python:3.10-alpine for smaller base (with compilation complexity)
3. **Layer Optimization**: Combine RUN commands to reduce layer count
4. **Dependency Pruning**: Remove development dependencies after installation

## Production Readiness Checklist

**Completed:**
- [x] Production-ready Dockerfile with minimal base image
- [x] Proper environment variable configuration
- [x] Health check implementation
- [x] Port 8080 exposure for Cloud Run compatibility
- [x] Efficient resource usage
- [x] FastAPI with uvicorn server setup

**Recommended for Production:**
- [ ] Multi-stage build implementation
- [ ] Non-root user configuration
- [ ] Vulnerability scanning
- [ ] Secrets management integration
- [ ] Logging configuration optimization
- [ ] Container registry setup

## Deployment Commands Summary

```bash
# Build the image
docker build -t lab3-penguin-api .

# Run locally for testing
docker run -p 8080:8080 lab3-penguin-api

# Test endpoints
curl http://localhost:8080/health
curl http://localhost:8080/

# Monitor performance
docker stats --no-stream

# Clean up
docker stop <container_id>
docker rm <container_id>
```

## Next Steps for Cloud Deployment

1. **Tag for Registry**: `docker tag lab3-penguin-api gcr.io/PROJECT_ID/lab3-penguin-api`
2. **Push to Registry**: `docker push gcr.io/PROJECT_ID/lab3-penguin-api`
3. **Deploy to Cloud Run**: Use Google Cloud Console or gcloud CLI
4. **Configure Environment Variables**: Set GCS credentials and bucket information
5. **Test Production Endpoints**: Verify health checks and prediction functionality

## Live Cloud Run Deployment - SUCCESS! 

### Final Deployment URLs
- **Live API**: https://penguin-api-87331348082.us-central1.run.app
- **Swagger Docs**: https://penguin-api-87331348082.us-central1.run.app/docs
- **Health Check**: https://penguin-api-87331348082.us-central1.run.app/health

### Deployment Verification Results
-  Service deployed successfully to Cloud Run
-  Health endpoint returns {"status": "ok"}
-  Interactive Swagger documentation accessible
-  Prediction endpoint working with sample data
-  Model loading from GCS successful
-  Public access enabled and working

### Cloud Run Configuration
- **Region**: us-central1
- **Memory**: 2Gi
- **CPU**: 1
- **Port**: 8080
- **Max Instances**: 10
- **Authentication**: Public (unauthenticated access)
