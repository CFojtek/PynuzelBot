# PynuzelBot
Signal Bot for our yearly trip


## Setup
go to the app folder `cd app` and run below docker command to run signal-cli in normal mode
```
docker run -p 8080:8080 \
    -v $(pwd)/signal-cli-config:/home/.local/share/signal-cli \
    -e 'MODE=normal' bbernhard/signal-cli-rest-api:latest
```

Now go to `http://127.0.0.1:8080/v1/qrcodelink?device_name=local` and scan the QR code with the signal app. This can be your phone or a secondary device, and will link the account with the signal rest API.

For further steps, you will need a `secrets.json` file.


### Local development
Now run the server json-rpc mode

```
docker run -p 8080:8080 \
    -v $(pwd)/signal-cli-config:/home/.local/share/signal-cli \
    -e 'MODE=json-rpc' bbernhard/signal-cli-rest-api:latest
```

Install the python dependencies and activate the environment
```
poetry install
evel $(poetry env activate)
```

and run `main.py`
The signal service is running on `127.0.0.1:8080` (localhost)


### Docker

Everythign is handled in the dockerfile, just run `docker compose up` in the rook directory

The signal service is running on `signal-cli:8080` (signal-cli container)


## Infrastructure

The app runs in a containerized instance on Azure.

Infrastructure is handled by Terraform and can be provisioned by running
```
terraform init
terraform plan -out .tfplan
terraform apply .tfplan
```

## Deployment


# TODO
- Fix secrets in docker file
- add terraform code
- run and test on cloud
- get separate signal number (pref BE one)
- write readme