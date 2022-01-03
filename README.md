# Test integration scripts
Test python and bash scripts to push data into o11y suite. 

## Setup project 
Create virtual environment

```bash
python3 -m venv venv
```

Activate venv and install dependencies

```bash
. ./venv/bin/activate
pip install -r req.txt
```

You need to create .secrets.yaml file with tokens and endpoints defined for example:

```yaml
SPLUNK_INGEST_TOKEN: "your_access_token"
SPLUNK_API_TOKEN: "your_access_token"
SPLUNK_METRICS_INGEST: "https://{ingest}.{realm}.signalfx.com"
SPLUNK_API: "https://api.{realm}.signalfx.com/v2/integration"

```

## Contributing

Read [how you can contribute](CONTRIBUTING.md)