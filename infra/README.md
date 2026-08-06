# infra — Terraform for Azure

Provisions the Azure resources required to host the file-upload application.

## Resources created

| Resource | Purpose |
|----------|---------|
| Resource Group | Logical container for all resources |
| Storage Account + Container | Stores uploaded blobs |
| Key Vault | Holds the storage connection string; referenced by App Service at runtime |
| App Service Plan (Linux B1) | Compute for the FastAPI backend |
| App Service (Linux) | Runs the FastAPI backend with Python 3.12 |
| Static Web App (Free) | Hosts the React SPA |

## Prerequisites

| Tool | Version |
|------|---------|
| [Terraform](https://developer.hashicorp.com/terraform) | ≥ 1.8 |
| [Azure CLI](https://learn.microsoft.com/en-us/cli/azure/) | ≥ 2.60 |

You must be logged in to the Azure CLI and have **Contributor** access on the
target subscription before running Terraform:

```bash
az login
az account set --subscription "<subscription-id>"
```

### Provider registration preflight

This stack requires these Azure resource providers to be registered on the
target subscription:

- `Microsoft.Web`
- `Microsoft.Storage`
- `Microsoft.KeyVault`

Check registration state:

```bash
az provider show --namespace Microsoft.Web --query registrationState -o tsv
az provider show --namespace Microsoft.Storage --query registrationState -o tsv
az provider show --namespace Microsoft.KeyVault --query registrationState -o tsv
```

If either command does not return `Registered`, run:

```bash
az provider register --namespace Microsoft.Web
az provider register --namespace Microsoft.Storage
az provider register --namespace Microsoft.KeyVault
```

Then re-check until all are `Registered`.

### Backend plan SKU

The backend App Service Plan SKU is configurable via `backend_service_plan_sku`:

- `F1` (default): free tier, useful for quota-constrained subscriptions.
- `B1`: basic paid tier, requires available App Service VM quota.

When `F1` is selected, `always_on` is automatically disabled because it is not
supported on the free tier.

## Usage

```bash
cd infra

# 1. Copy and populate the example variables file.
cp terraform.tfvars.example terraform.tfvars

# 2. Initialise providers and modules.
terraform init

# 3. Preview the changes.
terraform plan

# 4. Apply.
terraform apply
```

After apply, retrieve useful output values with:

```bash
terraform output backend_url
terraform output frontend_url
terraform output key_vault_name
```

The Static Web App deployment API key (used by GitHub Actions) is marked
`sensitive` — retrieve it with:

```bash
terraform output -raw static_web_app_api_key
```

## Remote state

Terraform state can contain sensitive data.  Before production use, configure
the `azurerm` backend block in `main.tf` and follow the
[Azure remote state guide](https://developer.hashicorp.com/terraform/language/settings/backends/azurerm).

## Secrets

The storage connection string is written to Key Vault by Terraform and
referenced by the App Service via a
[Key Vault reference](https://learn.microsoft.com/en-us/azure/app-service/app-service-key-vault-references)
in Application Settings. Key Vault uses RBAC authorization, so Terraform grants
the backend managed identity the `Key Vault Secrets User` role and grants the
deployer the `Key Vault Secrets Officer` role. The secret is **never** stored
in plain text in App Service configuration or in Terraform state outputs.

> **Important:** `terraform.tfvars` is git-ignored.  Never commit it.

## Tagging

Every resource is tagged with `environment`, `project`, and `managed_by=terraform`.

## Troubleshooting

- `MissingSubscriptionRegistration` for `Microsoft.Web`:
	register `Microsoft.Web` and wait for `Registered`.
- `MissingSubscriptionRegistration` for `Microsoft.Storage`:
	register `Microsoft.Storage` and wait for `Registered`.
- `MissingSubscriptionRegistration` for `Microsoft.KeyVault`:
	register `Microsoft.KeyVault` and wait for `Registered`.
- `LocationNotAvailableForResourceType` for Static Web App:
	use a supported region for `location` (default is `eastus2`).
- Key Vault name validation errors:
	ensure generated vault names stay within Azure constraints (3-24 chars,
	alphanumeric and dashes).
- App Service Plan quota errors (`Current Limit (Total VMs): 0`):
	use `backend_service_plan_sku = "F1"` or request quota and use `B1`.
- Key Vault secret 403 errors right after role assignment:
	this stack waits for RBAC propagation before creating the secret; if you still
	see a transient 403, re-run `terraform apply`.
