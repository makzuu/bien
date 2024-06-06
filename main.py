from bridge import *

def main():
    p = ArgP()
    p.add_arg("command", pos=1, choices=["search", "modify", "add", "me", "mal"], required=True)
    p.add_arg("arg", pos=2, required=True, not_required_in=["me", "mal"])
    p.add_arg("--limit", value=True)
    p.add_arg("--offset", value=True)
    p.add_arg("--status", value=True)
    p.add_arg("--num-episodes-watched", value=True)
    p.add_arg("--score", value=True)

    args = p.get_args()
