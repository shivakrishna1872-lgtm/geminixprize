#!/bin/bash
# deploy.sh — Deploy AntiGravity to Google Cloud Run
set -e

# Load environment
source .env 2>/dev/null || true

PROJECT_ID=${GCP_PROJECT:?GCP_PROJECT must be set}
REGION=${GCP_REGION:-us-central1}
SERVICE_NAME="antigravity-orchestrator"
IMAGE="gcr.io/${PROJECT_ID}/${SERVICE_NAME}"

echo "🚀 Deploying AntiGravity Orchestrator to Cloud Run..."
echo "   Project: ${PROJECT_ID}"
echo "   Region:  ${REGION}"
echo "   Image:   ${IMAGE}"

# Build and push image
echo "\n📦 Building Docker image..."
docker build -t ${IMAGE} ./backend/orchestrator/
docker push ${IMAGE}

# Deploy to Cloud Run
echo "\n☁️  Deploying to Cloud Run..."
gcloud run deploy ${SERVICE_NAME} \
  --image ${IMAGE} \
  --platform managed \
  --region ${REGION} \
  --allow-unauthenticated \
  --memory 2Gi \
  --cpu 2 \
  --min-instances 0 \
  --max-instances 10 \
  --set-env-vars "GCP_PROJECT=${GCP_PROJECT},GCP_REGION=${GCP_REGION},GEMINI_MODEL=${GEMINI_MODEL},USE_MOCK_INTEGRATIONS=${USE_MOCK_INTEGRATIONS:-true}" \
  --project ${PROJECT_ID}

SERVICE_URL=$(gcloud run services describe ${SERVICE_NAME} \
  --region ${REGION} \
  --project ${PROJECT_ID} \
  --format 'value(status.url)')

echo "\n✅ Orchestrator deployed!"
echo "   URL: ${SERVICE_URL}"

# Update frontend env
echo "\n📝 Updating frontend API URL..."
echo "NEXT_PUBLIC_API_URL=${SERVICE_URL}" >> apps/web/.env.production

echo "\n🎉 Deployment complete!"
echo "   Orchestrator: ${SERVICE_URL}"
echo "   Next step: Deploy frontend with 'firebase deploy' or 'vercel'"
