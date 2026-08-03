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
