import json

import json5

with open("./settings.json", mode="r") as fp:
    settings = json5.load(fp)

json.dumps(({k: settings.get(k) for k in sorted(settings.keys())}))
