#!/bin/bash
secrets_file=".secrets.yaml"


read_token_from_yaml() {
    secret=$(grep SPLUNK_INGEST_TOKEN $secrets_file | tr -d '"'); 
    secret=${secret//*SPLUNK_INGEST_TOKEN: /};
}


read_ingest_endpoint() {
    ingest_endpoint=$(grep SPLUNK_METRICS_INGEST $secrets_file | tr -d '"')
    ingest_endpoint=${ingest_endpoint//*SPLUNK_METRICS_INGEST: /}
    ingest_endpoint="${ingest_endpoint}/v2/datapoint"
}


if [ -f "$secrets_file" ]
then
    read_ingest_endpoint
    echo "* Test ingest endpoint: $ingest_endpoint"
    read_token_from_yaml
    value=$(shuf -i 1-100 -n 1)
    host=$(uname -n)
    payload='{"gauge": [{"metric": "heartbeat", "value": "'"$value"'", "dimensions": {"host": "'"$host"'"}}]}'
    echo $payload
    echo "* Send test data: $payload"
    curl -X POST $ingest_endpoint -H "Content-Type: application/json" -H "X-SF-Token: $secret" -d "$payload" -i
else
    echo "$secrets_file not found"
fi


# curl -X POST https://external-ingest.lab0.signalfx.com/v2/datapoint -H "Content-Type: application/json" -H "X-SF-Token: $secret" -d '{"gauge": [{"metric": "heartbeat", "value": 100}]}' -i
