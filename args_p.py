from sys import argv

class ArgP:
    def __init__(self):
        self.args = []

    def add_arg(self, name, pos=None, choices=None, required=False,
                not_required_in=None, value=False):
        self.args.append({ "name": name, "pos": pos, "choices": choices,
                          "required": required,
                          "not_required_in": not_required_in,
                          "value": value })

    def get_args(self):
        args = {}
        for arg in self.args:
            value = None
            if arg["required"]:
                if arg["pos"] < len(argv):
                    if arg["choices"]:
                        value = argv[arg["pos"]]
                        if value not in arg["choices"]:
                            raise Exception(f"Error: required arg \"{arg['name']}\" value must be one of \"{arg['choices']}\"")
                    else:
                        value = argv[arg["pos"]]
                    args[arg["name"]] = value
                elif arg["not_required_in"] is not None and args["command"] in arg["not_required_in"]:
                    continue
                else:
                    raise Exception(f"Error: Required arg \"{arg['name']}\" not found")
                
            else:
                if arg["name"] in argv:
                    for i, v in enumerate(argv):
                        if arg["name"] == v:
                            if i + 1 < len(argv):
                                value = argv[i + 1]
                                break
                            else:
                                raise Exception(f"Error: Value not provided for \"{arg['name']}\" arg")
                    args[arg["name"]] = value
        return args

if __name__ == "__main__":
    p = ArgP()
    p.add_arg("command", pos=1, choices=["search", "modify", "add", "me", "mal"], required=True)
    p.add_arg("arg", pos=2, required=True, not_required_in=["me", "mal"])
    p.add_arg("--limit", value=True)
    p.add_arg("--offset", value=True)
    p.add_arg("--status", value=True)
    p.add_arg("--num-episodes-watched", value=True)
    p.add_arg("--score", value=True)

    args = p.get_args()
    print(args)
