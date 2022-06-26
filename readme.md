# DonProxy

Proof-of-concept to intercept and log HTTPS traffic in cleartext.

# Purpose

Suppose you have the certificate and private key to some TLS service. You can use this tool to capture request and response data transparently. An end-user should not know or need to know that this service is running between their browser and the intended endpoint.


# Architecture

A simplified version of the architecture looks something like this. Please note that, in production, port 5000 should be port 443.

```
                               +-----------------------------------+
                               |          DonProxy (app.py)        |
                               +-------------+--------+------------+
                               |             |        |            |
(WAN) --[ Real request ]-->    | Web server  | Logger | Web Client |--[ Fake Request ]--> (Real endpoint)
                               | port 5000   |        |            |                            |
         <--[ Fake response ]--|             |        |            |    <--[ Real Response ]----+
                               +-------------+--------+------------+

```

This architecture requires no real configuration and does not require the user to install a certificate aside from the one issued by the indended endpoint, which the tool is capturing.

# Usage

1. Save the intended endpoint's **certificate** and **private key** as `cert.pem` and `key.pem` in the same directory as the `app.py` script.
1. Run `python3 app.py`.
1. Navigate to `https://127.0.0.1:5000`
1. If you are using a self-signed certificate, accept it and continue.
1. Observe that the response data should look exactly as it would if you had connected to the endpoint directly.

# Considerations

This should go without saying, but the web server should listen on port 443. (Flask defaults to port 5000.)

Flask should not be used in production. One might leverage Express (NodeJS) instead. If Flask must be used, hide it behind Nginx (not covered here).

Take care to rigorously match the request and response data. There should be no evidence of this middleware. At the time of writing, this application does leave artifacts in the response; this should never happen in a production version of this system.

A much better implementation will certainly accept command-line arguments. In Python3, this is accomplished best with `argparse`.

# References

- https://blog.miguelgrinberg.com/post/running-your-flask-application-over-https
- https://stackoverflow.com/questions/16482800/how-to-load-a-public-rsa-key-into-python-rsa-from-a-file
- https://blog.miguelgrinberg.com/post/running-your-flask-application-over-https
- Possible better solution: https://jeffchiu.wordpress.com/2015/07/31/openwrt-and-fiddler-for-http-and-https-transparent-proxy-traffic-capture-part-2/
- Notes about Flask `request`: https://stackoverflow.com/questions/10434599/get-the-data-received-in-a-flask-request
- Bypass SSL verification for requests.get: https://stackoverflow.com/questions/30405867/how-to-get-python-requests-to-trust-a-self-signed-ssl-certificate
- Default paths in Flask: https://stackoverflow.com/questions/45777770/catch-all-routes-for-flask