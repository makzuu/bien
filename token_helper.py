import requests
import json
from dotenv import client_id
import secrets
import os
import time
import webbrowser
from server import get_code

def get_new_code_verifier():
    token = secrets.token_urlsafe(100)
    return token[:128]

def get_auth_code(code_challenge):
    base_url = "https://myanimelist.net/v1/oauth2/authorize"
    response_type = "code"
    auth_url = f"{base_url}?response_type={response_type}&client_id={client_id}&code_challenge={code_challenge}"

    webbrowser.open(auth_url)
    return get_code()

def request_user_access_token(auth_code, code_verifier):
    base_url = "https://myanimelist.net/v1/oauth2/token"
    data = { "client_id": client_id, "code": auth_code, "code_verifier": code_verifier, "grant_type": "authorization_code" }
    r = requests.post(base_url, data=data)
    if r.status_code != 200:
        raise Exception("Error: Could not retrieve user access token")

    return r.json()

def refresh_user_access_token(refresh_token):
    base_url = "https://myanimelist.net/v1/oauth2/token"
    data = { "client_id": client_id, "grant_type": "refresh_token", "refresh_token": refresh_token }
    r = requests.post(base_url, data=data)
    if r.status_code != 200:
        raise Exception("Error: Could not refresh user access token")
    return r.json()

def get_access_token_status(expires_in, file_path="token.json"):
    last_m = os.path.getmtime(file_path)
    time_now = time.time()
    time_left = last_m + expires_in
    if time_left > time_now:
        days_left = (time_left - time_now) / 60 / 60 / 24
        if days_left < 10:
            expired = False
            must_refresh = True
        else:
            expired = False
            must_refresh = False
    else:
        expired = True
        must_refresh = False

    return expired, must_refresh

def get_token():
    try:
        token = load_token()
        expired, must_refresh = get_access_token_status(token["expires_in"])
        if expired:
            code_verifier = code_challenge = get_new_code_verifier()
            auth_code = get_auth_code(code_challenge)
            token = request_user_access_token(auth_code, code_verifier)
            save_token(token)
        elif must_refresh:
            token = refresh_user_access_token(token["refresh_token"])
            save_token(token)
        else:
            return token

        return token

    except FileNotFoundError:
        code_verifier = code_challenge = get_new_code_verifier()
        auth_code = get_auth_code(code_challenge)
        token = request_user_access_token(auth_code, code_verifier)
        save_token(token)
        return token
    raise Exception("Error: You're not supposed to be here")

def save_token(token, file_name="token.json"):
    with open(file_name, "w") as f:
        json.dump(token, f)

def load_token(file_name="token.json"):
    with open(file_name, "r") as f:
        token = json.load(f)
    return token

if __name__ == "__main__":
    token = get_token()
    print(token)
