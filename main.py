import secrets
from dotenv import client_id
import requests
import json
from bridge import *

def get_new_code_verifier():
    token = secrets.token_urlsafe(100)
    return token[:128]

def print_auth_url(code_challenge):
    base_url = "https://myanimelist.net/v1/oauth2/authorize"
    response_type = "code"
    url = f"{base_url}?response_type={response_type}&client_id={client_id}&code_challenge={code_challenge}"

    print(f"click here to login: {url}")

def get_token():
    code_verifier = code_challenge = get_new_code_verifier()
    print_auth_url(code_challenge)
    auth_code = input("insert auth code: ")
    
    base_url = "https://myanimelist.net/v1/oauth2/token"
    data = { "client_id": client_id, "code": auth_code, "code_verifier": code_verifier, "grant_type": "authorization_code" }
    r = requests.post(base_url, data=data)
    token = r.json()

    return token

def save_token(token, file_name="token.json"):
    with open(file_name, "w") as f:
        json.dump(token, f)

def load_token(file_name="token.json"):
    with open(file_name, "r") as f:
        token = json.load(f)
    return token

if __name__ == "__main__":
    try:
        token = load_token()
    except FileNotFoundError:
        token = get_token()
        save_token(token)

    data, status_code = me(token)
    if data is not None:
        print(f"Welcome! {data['name']}")

    data, status_code = get_anime_list(token)
    if status_code == 200:
        print("Anime List:")
        for element in data["data"]:
            node = element["node"]
            status = element["list_status"]["status"]
            print(f"\t({node['id']}) |{status}| {node['title']}")
