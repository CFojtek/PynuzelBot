# PynuzelBot

A Signal bot for our yearly trip. It serves help and released intel from Airtable, picks jokes by subject, and lets admins send messages to the user group.

## Requirements

- Docker with the Compose plugin
- Python 3.12+ and Poetry 2.x for local Python development
- An Airtable base and personal access token
- A Signal account to link to `signal-cli`

## Configure

Create `app/.env` with the bot's settings:

```dotenv
PHONE_NUMBER=+1234567890
USER_GROUP=<signal-user-group-id>
ADMIN_GROUP=<signal-admin-group-id>
AIRTABLE_TOKEN=<airtable-personal-access-token>
AIRTABLE_BASE_ID=<airtable-base-id>
```

`SIGNAL_SERVICE` defaults to `127.0.0.1:8080` when running Python directly. Docker Compose sets it to `signal-cli:8080` automatically.

The Airtable base must contain these tables and fields:

| Table | Fields used |
| --- | --- |
| `Help` | `Id`, `Text` |
| `Intel` | `Id`, `ReleaseDate`, `Text` |
| `Joke` | `Id`, `Text`, `Subject` |

Intel is selected from records whose `ReleaseDate` is in the past, with the latest release returned. Joke subjects are matched against `General` and the sender's first name.

## Link Signal

From the repository root, start `signal-cli` in account-linking mode:

```sh
docker compose run --rm --service-ports -e MODE=normal signal-cli
```

Open `http://127.0.0.1:8080/v1/qrcodelink?device_name=local` and scan the QR code with Signal. The configuration is persisted under `app/signal-cli-config`. Stop the linking container after the account is linked.

## Run Locally

To run the Python process on the host, first start `signal-cli` in JSON-RPC mode:

```sh
docker compose up -d signal-cli
```

Then install dependencies and start the bot:

```sh
cd app
poetry install
poetry run python main.py
```

The bot connects to `127.0.0.1:8080`. Stop the service from the repository root with `docker compose down`.

To run both containers instead, use the Compose build from the repository root:

```sh
docker compose up --build
```

The bot accepts `/help`, `/intel`, and `/joke` in the user group. The admin group can use those commands and `/push <message>`; bot responses and pushed messages are sent to the user group.

## Azure Deployment

The Terraform configuration in `infra/` creates an Azure resource group, container registry, Key Vault, storage account/file share, Log Analytics workspace, and Linux container group. The container group runs the bot and `signal-cli` together; they communicate over `localhost:8080`.

Requirements: Terraform `~> 1.13.0`, Azure CLI, and an Azure identity authorized to provision the resources and read the Key Vault secrets. In `infra/terraform.tfvars`, set the required Terraform variables:

```hcl
project_slug          = "<lowercase-project-slug>"
tenant_id             = "<azure-tenant-id>"
subscription_id       = "<azure-subscription-id>"
object_id             = "<deployment-identity-object-id>"
image_name_signal_cli = "bbernhard/signal-cli-rest-api:latest"
image_name_signal_bot = "signal-bot:latest"
```

`location`, `env`, and `tags` have defaults. Use a lowercase alphanumeric project slug; it is used to derive Azure resource names, including the registry name (`<project_slug>cr`).

Bootstrap the Key Vault and registry first, since the full deployment expects the secrets and images to exist:

```sh
cd infra
terraform init
terraform apply -target=azurerm_key_vault.key_vault -target=azurerm_container_registry.container_registry
terraform apply -target=azurerm_key_vault_access_policy.access_policy
```

Add these secrets to the created Key Vault using the Azure portal or Azure CLI:

| Secret name | Value |
| --- | --- |
| `phone-number` | Signal account phone number |
| `user-group` | Signal user group ID |
| `admin-group` | Signal admin group ID |
| `airtable-token` | Airtable personal access token |
| `airtable-base-id` | Airtable base ID |

Build and push the bot image and Signal REST API image to the registry. Set `PROJECT_SLUG` to the same value used in `infra/terraform.tfvars`:

```sh
cd ..
PROJECT_SLUG="replace-with-project-slug"
REGISTRY_NAME="${PROJECT_SLUG}cr"
docker build --target runtime -t signal-bot:latest -f dockerfile .
az acr login --name "$REGISTRY_NAME"
docker tag signal-bot:latest "${REGISTRY_NAME}.azurecr.io/signal-bot:latest"
docker push "${REGISTRY_NAME}.azurecr.io/signal-bot:latest"
docker pull bbernhard/signal-cli-rest-api:latest
docker tag bbernhard/signal-cli-rest-api:latest "${REGISTRY_NAME}.azurecr.io/bbernhard/signal-cli-rest-api:latest"
docker push "${REGISTRY_NAME}.azurecr.io/bbernhard/signal-cli-rest-api:latest"
```

Upload the contents of `app/signal-cli-config` to the `signal-cli-config` Azure file share. Then apply the complete configuration:

```sh
cd infra
terraform plan -out .tfplan
terraform apply .tfplan
```

Terraform state contains infrastructure details and should be stored and protected accordingly.

## Future Works
- Add tests
- Add exception handling when airtable does not return anything, or no information could be found
- Put Azure infra in Virtual Network with private endpoints to not expose public container IP

## License

Released under the [MIT License](LICENSE).

Author: Christian Fojtek