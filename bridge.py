import requests

base_url = "https://api.myanimelist.net/v2/"

def me(token):
    headers = { "Authorization": f"Bearer {token['access_token']}" }
    r = requests.get("https://api.myanimelist.net/v2/users/@me", headers=headers)
    if r.status_code == 200:
        return r.json(), r.status_code
    return None, r.status_code

def get_my_anime_list(token, limit=100, offset=0, status=""):
    headers = { "Authorization": f"Bearer {token['access_token']}"}
    params = { "limit": limit, "offset": offset, "status": status,
              "fields": "list_status,alternative_titles,score" }
    r = requests.get(base_url + "users/@me/animelist", headers=headers, params=params)
    return r.json(), r.status_code

def search(token, anime_name, limit=100, offset=0):
    headers = { "Authorization": f"Bearer {token['access_token']}"}
    params = { "q": anime_name, "limit": limit, "offset": offset,
              "fields": "my_list_status,status,alternative_titles,num_episodes" }
    r = requests.get(base_url + "anime", headers=headers, params=params)
    return r.json(), r.status_code

def update_my_anime_list(token, anime_id, status=None, score=None, num_watched_episodes=None):
    url = base_url + f"anime/{anime_id}/my_list_status"
    headers = { "Authorization": f"Bearer {token['access_token']}"}
    data = { "status": status, "score": score, "num_watched_episodes": num_watched_episodes }
    r = requests.put(url, headers=headers, data=data)
    return r.json(), r.status_code

def add(token, anime_id, status="plan_to_watch"):
    return update_my_anime_list(token, anime_id, status)
    
def modify(token, anime_id, status=None, score=None, num_watched_episodes=None):
    return update_my_anime_list(token, anime_id, status, score, num_watched_episodes)
