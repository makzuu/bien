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
    p.add_arg("--num-episodes-watched", value=True)
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

        content, status_code = add(token, anime_id, status)
        print(content)
    elif args["command"] == "modify":
        anime_id = args["arg"]
        status = args.get("--status")
        score = args.get("--score")
        num_watched_episodes = args.get("--num_watched_episodes")

        content, status_code = modify(token, anime_id, status, score, num_watched_episodes)
        print(f"{status_code}\n{content}")
    elif args["command"] == "mal":
        limit = args.get("--limit")
        offset = args.get("--offset")
        status = args.get("--status")

        content, status_code = get_my_anime_list(token, limit, offset, status)
        print(f"{status_code}\n{content}")
    elif args["command"] == "me":
        content, status_code = me(token)
        print(f"{status_code}\n{content}")

def print_search_results(data):
    for node in data:
        anime = node["node"]
        print("---\n"
              f"id: {anime['id']}\n"
              f"title: {anime['title']}\n"
              "alternative titles:\n"
              f"\t> {anime['alternative_titles']['en']}\n"
              f"\t> {anime['alternative_titles']['ja']}\n"
              f"status: {anime['status']}\n"
              f"episodes: {anime['num_episodes']}\n"
              )

def main():
    args = set_args()
    handle_args(args)


main()
