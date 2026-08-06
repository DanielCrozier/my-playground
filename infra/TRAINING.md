# Terraform Training: infra Package

This training is designed to get a new developer productive and confident in this repository's Terraform package. It progresses from foundations to project-specific implementation details and then to advanced concepts and pitfalls.

## Learning Path

1. Basic: Terraform concepts used directly in this package.
2. Intermediate: How this project implements those concepts in Azure.
3. Advanced: The trickiest design and operational details.
4. Knowledge Check: Test your understanding with scenario-based questions.

---

## Section 1: Basic

### 1.1 What Terraform is doing in this repo

In this project, Terraform defines Azure infrastructure as code under `infra/`. Terraform reads all `.tf` files in the directory as one configuration and creates a dependency graph from references between resources.

Primary outcomes:

- Create the resource group, storage, key vault, backend app service, and static web app.
- Configure app settings and runtime behavior for the backend.
- Expose useful values via outputs after deployment.

### 1.2 Core Terraform building blocks in this package

You will see these fundamentals throughout the files:

- `terraform` block: pins Terraform and provider versions (`main.tf`).
- `provider` block: configures AzureRM provider features (`main.tf`).
- `resource` blocks: define Azure resources to create (`*.tf`).
- `data` blocks: read existing info from Azure (e.g., current tenant/object id).
- `variable` blocks: project inputs with types/defaults (`variables.tf`).
- `locals` blocks: reusable computed values like naming/tag maps (`main.tf`).
- `output` blocks: print values after apply (`outputs.tf`).

### 1.3 Implicit dependency graph

Terraform infers resource order when one resource references another. Example:

- `azurerm_storage_container.uploads` references `azurerm_storage_account.uploads.id`.
- Terraform will create storage account before the container.

If references form a loop, plan fails with a cycle error.

### 1.4 Naming, uniqueness, and tags

This package standardizes naming with:

- `local.name_prefix` = sanitized `${var.project}-${var.environment}`.
- `random_string.suffix` for globally unique names where Azure requires it.

It also enforces consistent metadata via `local.common_tags` on resources:

- `environment`
- `project`
- `managed_by=terraform`

### 1.5 Inputs and defaults

Key inputs from `variables.tf`:

- `project` (required)
- `environment` (default `dev`)
- `location` (default `eastus`)
- `allowed_origins` (default `*`)
- `max_upload_size_bytes` (default 10 MB)

These values are usually set through `terraform.tfvars` (git-ignored).

### 1.6 Standard workflow in this package

Typical commands:

1. `terraform init`
2. `terraform plan`
3. `terraform apply`
4. `terraform output <name>`

Support commands you should know:

- `terraform validate` checks configuration semantics.
- `terraform fmt -recursive` enforces formatting.

---

## Section 2: Intermediate

This section maps concepts to specific implementation decisions in this repository.

### 2.1 Resource-by-resource mental model

Infrastructure components and why they exist:

1. Resource Group: top-level container for lifecycle and access.
2. Storage Account + private `uploads` container: destination for user files.
3. Key Vault + secret: stores storage connection string securely.
4. App Service Plan + Linux Web App: hosts FastAPI backend on Python 3.12.
5. Static Web App: hosts frontend SPA.

### 2.2 How backend config is assembled

The backend app settings combine values from different resource outputs and variables:

- `AZURE_STORAGE_CONNECTION_STRING`: Key Vault reference string.
- `AZURE_STORAGE_CONTAINER_NAME`: from storage container resource.
- `ALLOW_ORIGINS`: from Terraform variable.
- `MAX_UPLOAD_SIZE_BYTES`: numeric input converted via `tostring(...)`.

Important implementation detail:

- Even when Key Vault references are used at runtime, Terraform still tracks dependencies from interpolated references in the string.

### 2.3 Key Vault access policies and identities

This package grants:

- Deploying principal: manage secrets.
- Backend managed identity: read secrets.

The managed identity principal ID is only known after the web app exists. This can create ordering complexity (covered in Advanced).

### 2.4 Sensitive outputs and operational use

`static_web_app_api_key` is marked `sensitive = true`. This means:

- Terraform hides it in standard output views.
- You must use `terraform output -raw static_web_app_api_key` to retrieve it for CI/CD secrets.

### 2.5 Security posture implemented here

Project-specific controls encoded in Terraform:

- Storage container is private.
- Nested/public blob access disabled on account.
- Backend uses HTTPS only.
- Secret is stored in Key Vault and referenced by app setting.
- Tags for ownership and environment tracking.

### 2.6 How to safely customize for environments

When promoting from dev to prod:

1. Set `environment` and `allowed_origins` appropriately.
2. Keep project naming consistent to avoid accidental parallel stacks.
3. Configure remote state backend (recommended before production).
4. Review plan carefully for replacements/destruction.

---

## Section 3: Advanced

This section covers the hardest concepts in this package.

### 3.1 Dependency cycles (the most common hard failure)

A cycle happens when resources depend on each other in a loop.

Real pattern from this repo:

1. Key Vault access policy reads backend identity principal ID.
2. Backend app setting references Key Vault secret and Key Vault name.
3. Key Vault secret needs Key Vault ID.

That can produce:

- Key Vault -> Backend -> Key Vault Secret -> Key Vault

Terraform requires a Directed Acyclic Graph (DAG), so it errors.

How to break the cycle cleanly:

1. Keep `azurerm_key_vault.main` independent of backend identity.
2. Create backend app and key vault secret separately.
3. Grant backend identity access with a separate `azurerm_key_vault_access_policy` resource that depends on both existing resources.

### 3.2 String interpolation can still create dependencies

Even if a value looks like a plain string (for example Key Vault reference syntax), if that string interpolates resource attributes, Terraform adds graph edges.

Takeaway:

- Treat interpolated strings as dependency declarations.

### 3.3 State security and remote backend strategy

State may contain sensitive values (such as secret material inside resource state). For team workflows:

1. Use remote backend (Azure Storage) before production.
2. Enable state locking/concurrency controls.
3. Restrict who can read state blobs.

### 3.4 Drift, reconciliation, and blast radius

If someone manually edits Azure resources:

- Next plan may show drift.
- Terraform will try to reconcile to code-defined state.

Best practices:

1. Avoid portal/manual changes for managed resources.
2. Use plans in pull requests.
3. Understand when a change forces replacement.

### 3.5 Provider behavior and lifecycle nuance

The AzureRM provider `features.key_vault` options here influence destroy/recreate behavior for soft-delete recovery and purge semantics.

Advanced implication:

- Destroy/apply behavior for vaults can differ from naive expectations due to Azure soft-delete mechanics.

---

## Knowledge Check

Answer these without looking at the code first. Then verify.

### Part A: Core understanding

1. Why does this package use a random suffix in resource names?
2. Which variable is required with no default, and why is that useful?
3. Why is `max_upload_size_bytes` converted with `tostring(...)` for app settings?
4. What is the difference between a `data` block and a `resource` block in this repo?

### Part B: Project implementation

5. Name the Azure resource that hosts the frontend and the one that hosts the backend.
6. Where does the backend get its storage connection string from at runtime?
7. Why is `static_web_app_api_key` marked sensitive, and how do you retrieve it when needed?
8. Which settings in this package directly improve security posture?

### Part C: Advanced reasoning

9. Explain, in your own words, how the Key Vault/Backend cycle can happen.
10. Why can interpolation inside a quoted string still affect Terraform's resource order?
11. If a teammate updates a Terraform-managed resource in the Azure Portal, what do you expect on the next `terraform plan`?
12. What is the operational risk of keeping local state for a team production environment?

### Part D: Practical scenario

13. You need production CORS restrictions. What variable changes should you make, and where?
14. You are asked to add a new tag across all resources. Where is the most maintainable place to implement this?
15. You get a cycle error involving backend, key vault, and key vault secret. Describe a refactor strategy that preserves least privilege and breaks the cycle.

---

## Answer Key (Self-Assessment)

1. To satisfy global uniqueness constraints (notably storage account naming) and avoid collisions.
2. `project`; it forces explicit naming context and reduces accidental generic deployments.
3. App settings are strings; explicit conversion avoids type mismatch and clarifies intent.
4. `data` reads existing external info (current client config); `resource` creates/manages infrastructure.
5. Frontend: Static Web App. Backend: Linux Web App on App Service Plan.
6. From a Key Vault secret referenced in App Service app settings.
7. It is a deployment credential; sensitive avoids accidental display. Retrieve with `terraform output -raw static_web_app_api_key`.
8. Private container, disabled nested public access, HTTPS-only backend, Key Vault secret storage/reference, consistent tagging.
9. Key Vault references backend identity while backend references key vault/secret values, and secret references key vault, forming a loop.
10. Interpolation expressions introduce references, and references create graph edges.
11. Plan shows drift and proposed reconciliation changes.
12. State access/concurrency risk, potential secret exposure, no shared locking process.
13. Set `allowed_origins` in `terraform.tfvars` to the frontend production origin(s).
14. `local.common_tags` in `main.tf`.
15. Move backend identity policy out of Key Vault resource into separate access-policy resource created after both resources exist.

---

## Suggested Practice Lab (Optional)

1. Run `terraform validate` and explain any warnings or failures.
2. Run `terraform plan` and trace one dependency chain from resource group to backend app settings.
3. Implement a harmless tag change in `local.common_tags` and inspect planned changes.
4. Simulate an environment change by updating `allowed_origins` and compare plan output.
5. Sketch a no-cycle refactor for Key Vault policy handling before implementing it.
