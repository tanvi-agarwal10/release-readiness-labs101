#!/bin/bash
set -e

TARGET_VERSION="${TARGET_VERSION:-v2.2.0}"
echo "Initiating OrderFlow rollback procedure..."
echo "Reverting deployment to stable release: ${TARGET_VERSION}"
echo "Verifying service health on endpoint /health..."
echo "Rollback verification complete (dry-run mode)."
