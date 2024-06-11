from bridge import *
from args_p import ArgP
from token_helper import get_token

def set_args():
    p = ArgP()
    p.add_arg("command", pos=1, choices=["search", "modify", "add", "me", "mal"], required=True)
    p.add_arg("arg", pos=2, required=True, not_required_in=["me", "mal"])
    p.add_arg("--limit", value=True)
    p.add_arg("--offset", value=True)
    p.add_arg("--status", value=True)
    p.add_arg("--num-watched-episodes", value=True)
    p.add_arg("--score", value=True)

    return p.get_args()

def handle_args(args):
    token = get_token()

    if args["command"] == "search":
        anime_name = args["arg"]
        limit = args.get("--limit", 3)
        offset = args.get("--offset", 0)

        content, status_code = search(token, anime_name, limit, offset)
        data = content["data"]

        print_search_results(data)


    elif args["command"] == "add":
        anime_id = args["arg"]
        status = args.get("--status")

        new, status_code = add(token, anime_id, status)
        print(f"id: {anime_id}\n"
              f"status: {new['status']}\n"
              f"score: {new['score']}\n"
              f"num episodes watched: {new['num_episodes_watched']}\n")
    elif args["command"] == "modify":
        anime_id = args["arg"]
        status = args.get("--status")
        score = args.get("--score")
        num_watched_episodes = args.get("--num-watched-episodes")

        modified, status_code = modify(token, anime_id, status, score, num_watched_episodes)
        print(f"id: {anime_id}\n"
              f"status: {modified['status']}\n"
              f"score: {modified['score']}\n"
              f"num episodes watched: {modified['num_episodes_watched']}\n")
         
    elif args["command"] == "mal":
        limit = args.get("--limit")
        offset = args.get("--offset")
        status = args.get("--status")

        mal, status_code = get_my_anime_list(token, limit, offset, status)
        print_mal_results(mal)

    elif args["command"] == "me":
        user, status_code = me(token)
        print(f"Welcome! {user["name"]}")

def print_search_results(data):
    for node in data:
        anime = node["node"]
        print("---\n"
              f"id: {anime['id']}\n"
              f"title: {anime['title']}\n"
              "alternative titles:\n"
              f"\t(en) {anime['alternative_titles']['en']}\n"
              f"\t(ja) {anime['alternative_titles']['ja']}\n"
              f"status: {anime['status']}\n"
              f"episodes: {anime['num_episodes']}\n")

def print_mal_results(mal):
    for data in mal["data"]:
        anime = data["node"]
        list_status = data["list_status"]
        print("---\n"
              f"id: {anime['id']}\n"
              f"title: {anime['title']}\n"
              f"alternative titles:\n"
              f"\t(en) {anime['alternative_titles']['en']}\n"
              f"\t(ja) {anime['alternative_titles']['ja']}\n"
              f"status: {list_status['status']}\n"
              f"num episodes watched: {list_status['num_episodes_watched']}\n"
              f"score: {list_status['score']}\n")

def main():
    args = set_args()
    handle_args(args)


main()
