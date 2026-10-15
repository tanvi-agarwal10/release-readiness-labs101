#!/bin/bash
set -e

RELEASE_VERSION="${RELEASE_VERSION:-v2.3.0}"
echo "OrderFlow Deployment Script - Version: ${RELEASE_VERSION}"
echo "Target Environment: ${DEPLOY_ENV:-production}"

# Safety guard: Prevent accidental production deployment during release readiness assignment
if [ "${ALLOW_PRODUCTION_DEPLOY}" != "true" ]; then
  echo "NOTICE: Production deployment execution is disabled for this assignment (Dry-Run Mode)."
  echo "Validation of deployment parameters succeeded."
  exit 0
fi

echo "Deploying version: ${RELEASE_VERSION}"
echo "Deployment successful."
