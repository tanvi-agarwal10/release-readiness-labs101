# OrderFlow — Release Readiness Documentation

## 1. Release Information

- **Project:** OrderFlow
- **Release Version:** `v2.3.0`
- **Branch:** `investigation/release-readiness`
- **Commit Reference:** `investigation/release-readiness` HEAD
- **Target Environment:** `production` (protected)
- **Application Type:** Node.js Express REST API (`app/server.js`)
- **Container Artifact:** `lab-app:v2.3.0`
- **Release Artifacts & Version Traceability:**
  - Application Container: `lab-app:v2.3.0` (built from Dockerfile using Node.js 18-alpine base)
  - Release Configuration: `release/deployment-config.yml` (`v2.3.0`)
  - Release Metadata: `release/release.json` (`v2.3.0`) and `release/release-summary.yml` (`v2.3.0`)
  - Kubernetes Manifest: `deployment/kubernetes/deployment.yaml` (`v2.3.0`)
  - Rollback Target: `release/rollback.yml` (`v2.2.0`)

---

## 2. Deployment Strategy

The OrderFlow deployment lifecycle follows an automated, gated progression designed to prevent unverified code from reaching production:

1. **Pre-Deployment Validation Gate (`validate-release` job):**
   - Automatically triggered on push to `main` and `investigation/release-readiness`.
   - Checks out the branch using `actions/checkout@v4`.
   - Configures runtime with `actions/setup-node@v4` (Node.js 20 LTS).
   - Installs project dependencies via `npm install --prefix app`.
   - Executes automated tests via `npm test --prefix app`.
   - Downstream deployment strictly depends on this job via GitHub Actions `needs: validate-release`. Any test failure blocks deployment.

2. **Production Gate & Environment Protection (`deploy-production` job):**
   - Explicitly bound to GitHub Environment: `production`.
   - Protected by repository environment governance rules requiring designated human reviewer approval before execution.
   - Verifies release version metadata (`v2.3.0`).

3. **Deployment Restriction (Assignment Guard):**
   - Production deployment is strictly guarded and set to safe dry-run mode.
   - Script execution prevents unintended cloud resource modification (`ALLOW_PRODUCTION_DEPLOY` guard).

---

## 3. Infrastructure Decision

- **Selected Infrastructure:** Containerized Kubernetes Deployment (`deployment/kubernetes/`)
- **Rationale:**
  - OrderFlow is packaged as a lightweight containerized microservice (`Dockerfile`, `docker-compose.yml`).
  - The Kubernetes manifest (`deployment/kubernetes/deployment.yaml`) configures 3 pod replicas for high availability, rolling updates, and automated health monitoring via `deployment/kubernetes/service.yaml` (LoadBalancer).
  - The standalone AWS EC2 instance in `deployment/terraform/` represents legacy, un-orchestrated single-server infrastructure unsuitable for modern container scalability, automatic failover, and zero-downtime rolling deployments.
  - The Kubernetes deployment architecture is selected as the primary, production-ready target for OrderFlow.

---

## 4. Secret Management

- **Zero-Plaintext Policy:** Hardcoded sensitive strings (`password123`, `abcd1234`, `test-secret`, `test-api-key-1234`) have been eliminated from all configuration manifests and source code.
- **Environment Parameterization:** `release/deployment-config.yml` consumes secrets strictly via runtime environment references (`${API_KEY}`, `${DATABASE_PASSWORD}`, `${TOKEN}`, `${AWS_SECRET}`).
- **Kubernetes Secret Store:** `deployment/kubernetes/deployment.yaml` binds container environment variables using Kubernetes `secretKeyRef` objects referencing `orderflow-secrets`.
- **CI/CD Ingestion:** Secrets are injected in GitHub Actions pipelines using repository/environment secrets, ensuring secrets are masked and never printed to build logs.
- **Terraform Hardening:** `deployment/terraform/variables.tf` has the sensitive default removed and is marked `sensitive = true`.

---

## 5. Rollback Strategy

In the event of an anomaly or health check failure during release:

1. **Target Recovery Version:** `v2.2.0` (previous verified stable production baseline).
2. **Execution Mechanism:** Automated rollback using Kubernetes native rollout undo:
   ```bash
   kubectl rollout undo deployment/lab-app
   ```
3. **Health Check Gate:** Post-rollback validation tests the `/health` endpoint:
   - Target HTTP Status: `200 OK`
   - Response validation: `{"status": "ok", "version": "2.2.0"}`
4. **Failure Thresholds:** Max allowed consecutive check failures: 3; verification timeout: 120 seconds.
5. **Abort Condition:** If health checks fail during rollout, the automated pipeline halts progression and triggers an incident alert without advancing traffic to faulty pods.

---

## 6. Production Approval Checklist

- [x] Required validation checks passed (`npm test`, syntax validation, YAML syntax checks)
- [x] Secrets are managed securely (parameterized via environment/vault; no plaintext credentials committed)
- [x] Release version and artifacts are traceable (`v2.3.0` across all metadata, manifests, and configs)
- [x] Infrastructure configuration is verified (Kubernetes containerized deployment selected and validated)
- [x] Production environment protection is configured (`production` environment created in repository)
- [x] Required approval process is documented (manual gate via GitHub environment reviewers required)
- [x] Rollback procedure is documented and reviewed (revert path to `v2.2.0` defined in `release/rollback.yml`)
- [x] Remaining risks are documented (production deployment unexecuted; awaiting production reviewer sign-off)

---

## 7. Validation Summary

- **Node.js Test Suite:** `npm test --prefix app` -> PASSED (`Validation passed: application is stable.`)
- **Server Syntax Check:** `node -c app/server.js` -> PASSED (0 errors)
- **Deployment Script Validation:** `bash -n scripts/deploy.sh` & `bash -n scripts/rollback.sh` -> PASSED (0 syntax errors)
- **YAML Configuration Validation:** 14/14 YAML manifests verified valid.
- **Dry-Run Deployment:** Executed safe dry run; zero modifications made to production infrastructure.
- **Production Status:** Production environment remains protected, unexecuted, and awaiting manual approval.
