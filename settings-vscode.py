import json5, json

with open("./settings.json", mode="r") as fp:
    settings = json5.load(fp)

json.dumps(({k: settings.get(k) for k in sorted(settings.keys())}))
