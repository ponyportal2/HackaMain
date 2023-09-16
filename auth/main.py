import json
import requests
from authlib.integrations.flask_client import OAuth
from flask import Flask, redirect, url_for, session, render_template, abort


app = Flask(__name__)

appConf = {
    "OAUTH2_CLIENT_ID": "116203304654-fp8noi61ff6kdo5gnu40b7d41nbojn6b.apps.googleusercontent.com",
    "OAUTH2_CLIENT_SECRET": "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",
    "OAUTH2_META_URL": "https://accounts.google.com/.well-known/openid-configuration",
    "FLASK_SECRET": "91db5be4-d545-4a28-9212-5b03b642bbab",
    "FLASK_PORT": 5000
}

app.secret_key = appConf.get("FLASK_SECRET")

oauth = OAuth(app)

oauth.register(
  name="hackmedia",
  client_id=appConf.get("OAUTH2_CLIENT_ID"),
  client_secret=appConf.get("OAUTH2_CLIENT_SECRET"),
  client_kwargs={
    "scope": "openid profile email",
    },
    server_metadata_url=f'{appConf.get("OAUTH2_META_URL")}',
    )

@app.route("/")
def home():
  return render_template("home.html", session=session.get("user"), info=json.dumps(session.get("user"), indent=4))

@app.route("/signin-google")
def googleCallback():
  token = oauth.hackmedia.authorize_access_token()
  session["user"] = token
  return redirect(url_for("home"))


@app.route("/google-login")
def googleLogin():
  if "user" in session:
      abort(404)
  return oauth.hackmedia.authorize_redirect(redirect_uri=url_for("googleCallback", _external=True))
  


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=appConf.get("FLASK_PORT"), debug=True)