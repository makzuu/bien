import requests

base_url = "https://api.myanimelist.net/v2/"

def get_anime_list(token, status="", limit=100, offset=0):
    headers = { "Authorization": f"Bearer {token['access_token']}"}
    params = { "fields": ["list_status"], "status": status, "limit": limit,
              "offset": offset }
    r = requests.get(base_url + "users/@me/animelist", headers=headers, params=params)
    if r.status_code == 200:
        return r.json(), r.status_code
    return None, r.status_code

def me(token):
    headers = { "Authorization": f"Bearer {token['access_token']}" }
    r = requests.get("https://api.myanimelist.net/v2/users/@me", headers=headers)
    if r.status_code == 200:
        return r.json(), r.status_code
    return None, r.status_code
