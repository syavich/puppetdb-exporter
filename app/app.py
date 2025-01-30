from flask import Flask, jsonify
import requests, os

app = Flask(__name__)

@app.route("/")
def index():
    return jsonify({ 'name': 'Puppet server metrics exporter', 'version': '0.1' })

@app.route("/metrics")
def metrics():
    url_preffix = "https://" + os.environ['PUPPET_SERVER_PORT_8140_TCP_ADDR'] + ":8140/metrics/v1/mbeans/puppetserver:name=puppetlabs.localhost."
    content = ""

    preffix = ["http-client.experimental.with-metric-id.puppetdb.full-response",
    "http-client.experimental.with-metric-id.puppetdb.command.full-response",
    "http-client.experimental.with-metric-id.puppetdb.command.replace_catalog.full-response",
    "http-client.experimental.with-metric-id.puppetdb.command.store_report.full-response",
    "http-client.experimental.with-metric-id.puppetdb.facts.find.full-response",
    "http-client.experimental.with-metric-id.puppetdb.facts.full-response",
    "http-client.experimental.with-metric-id.puppetdb.command.replace_facts.full-response",
    "jruby.borrow-timer", "jruby.wait-timer"]

    metrics_gauge = [["_1min_rate", "OneMinuteRate"], ["_5min_rate", "FiveMinuteRate"], ["_MeanRate", "MeanRate"],
    ["_Max", "Max"], ["_Mean", "Mean"], ["_StdDev", "StdDev"], ["_count", "Count"]]
    metrics_summary = [["_50", "50thPercentile"],["_75", "75thPercentile"],["_99", "99thPercentile"]]

    for j in preffix:
        r = requests.get(url_preffix + j, verify=False)
        mname = j.replace(".", "_").replace("-", "_")

        content = content + "# HELP " + mname + "\n"
        content = content + "# TYPE " + mname + " gauge\n"
        for i in range (0, len(metrics_gauge)):
            content = content + mname + metrics_gauge[i][0] + " " + str(r.json()[metrics_gauge[i][1]]) + "\n"

        content = content + "# HELP " + mname + "\n"
        content = content + "# TYPE " + mname + " summary\n"
        for i in range (0, len(metrics_summary)):
            content = content + mname + metrics_summary[i][0] + " " + str(r.json()[metrics_summary[i][1]]) + "\n"

    j = "http.active-requests"
    r = requests.get(url_preffix + j, verify=False)
    mname = j.replace(".", "_").replace("-", "_")

    content = content + "# HELP " + mname + "\n"
    content = content + "# TYPE " + mname + " gauge\n"
    content = content + mname + " " + str(r.json()["Count"]) + "\n"

    j = "jruby.free-jrubies-histo"
    metrics_gauge = [["_Max", "Max"], ["_Mean", "Mean"], ["_StdDev", "StdDev"], ["_count", "Count"]]
    r = requests.get(url_preffix + j, verify=False)
    mname = j.replace(".", "_").replace("-", "_")

    content = content + "# HELP " + mname + "\n"
    content = content + "# TYPE " + mname + " gauge\n"
    for i in range (0, len(metrics_gauge)):
        content = content + mname + metrics_gauge[i][0] + " " + str(r.json()[metrics_gauge[i][1]]) + "\n"

    return content

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
