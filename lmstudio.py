import requests

LM_STUDIO_URL = "http://127.0.0.1:1234/v1/chat/completions"
MODEL = "qwen2.5-coder-14b-instruct"

MAX_OUTPUT_CHARS = 8000


class LMStudio:

    def check_server(self):
        try:
            r = requests.get(
                "http://127.0.0.1:1234/v1/models",
                timeout=5
            )
            return r.status_code == 200
        except:
            return False

    def ask(self, prompt, system="You are a helpful assistant."):

        payload = {
            "model": MODEL,
            "messages": [
                {
                    "role": "system",
                    "content": system
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.2,
            "max_tokens": 1024
        }

        try:

            r = requests.post(
                LM_STUDIO_URL,
                json=payload,
                timeout=300
            )

            if r.status_code != 200:
                raise Exception(
                    f"LM Studio Error {r.status_code}\n\n{r.text}"
                )

            data = r.json()

            return data["choices"][0]["message"]["content"].strip()

        except requests.exceptions.RequestException as e:
            return f"Connection Error:\n{e}"

        except Exception as e:
            return str(e)

    def generate_command(self, prompt):

        system = """
You are an expert Linux assistant.

Convert the user request into ONE Linux command.

Rules:

Return ONLY the command.

No markdown.

No explanation.

No ```bash

No extra text.
"""

        return self.ask(prompt, system)

    def analyze_output(self, command, output):

        if len(output) > MAX_OUTPUT_CHARS:
            output = (
                output[:MAX_OUTPUT_CHARS]
                + "\n\n...[Output Truncated]..."
            )

        system = """
You are a Linux expert.

Explain:

1. What command executed.

2. What the output means.

3. Mention errors if present.

4. Keep answer under 200 words.

5. Use bullet points.
"""

        prompt = f"""
Command

{command}

Output

{output}
"""

        return self.ask(prompt, system)