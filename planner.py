import json

from tools.whatweb import WhatWeb
from tools.subfinder import Subfinder
from tools.httpx import Httpx
from tools.katana import Katana
from tools.nuclei import Nuclei
from tools.ffuf import Ffuf


class Planner:

    def __init__(self, ssh):

        self.ssh = ssh

        self.tools = {
            "whatweb": WhatWeb(),
            "subfinder": Subfinder(),
            "httpx": Httpx(),
            "katana": Katana(),
            "nuclei": Nuclei(),
            "ffuf": Ffuf(),
        }

    def execute(self, plan):

        if isinstance(plan, str):
            plan = json.loads(plan)

        results = []

        for step in plan:

            tool_name = step["tool"].lower()

            target = step["target"]

            if tool_name not in self.tools:

                results.append({
                    "tool": tool_name,
                    "status": False,
                    "output": "Tool not found"
                })

                continue

            tool = self.tools[tool_name]

            command = tool.command(target)

            ok, output = self.ssh.run_command(command)

            results.append({

                "tool": tool_name,

                "command": command,

                "status": ok,

                "output": output

            })

        return results