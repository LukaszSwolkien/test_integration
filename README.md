# Test integration scripts
Test python and bash scripts to push data into o11y suite. 

## Usage examples:

Create your organisation using Splunk API (see ```create_org.sh```), setup access tokens and you can create test chart/dashboard to see test data.
Remember to set all necessery secrets in the ```.secrets.yaml``` file

```bash
./test_ingest.sh
./test_integrations.sh
./market_cap.py ethereum
```

market_cap python script collect publicly available market data on a given cryptocurrency and send selected metrics to the o11y suite
## Setup project 
You need to create .secrets.yaml file with tokens and endpoints defined, for example:

```yaml
SPLUNK_INGEST_TOKEN: "your_access_token"
SPLUNK_API_TOKEN: "your_access_token"
SPLUNK_METRICS_INGEST: "https://{ingest}.{realm}.signalfx.com"
SPLUNK_API: "https://api.{realm}.signalfx.com/v2/integration"

```
### Note: you can skip below step if you don't want to play with python script
Create virtual environment

```bash
python3 -m venv venv
```

Activate venv and install dependencies

```bash
. ./venv/bin/activate
pip install -r req.txt
```
## Contributing

Read [how you can contribute](CONTRIBUTING.md)