import requests
import subprocess

LM_URL = "http://localhost:1234/v1/chat/completions"

KALI_IP = "192.168.137.190"
KALI_USER = "ujwal"

COMMAND_PROMPT = """
You are a Linux command generator.

Rules:
- Return ONLY the command.
- No markdown.
- No explanations.
- No code blocks.
- One command only.
"""

ANALYSIS_PROMPT = """
You are a cybersecurity and Linux analyst.

Analyze the command output.

Explain:
1. What the command output means
2. Important findings
3. Potential issues
4. Recommendations

Use simple language.
"""

while True:

    user_prompt = input("\\nYou: ")

    if user_prompt.lower() in ["exit", "quit"]:
        break

    try:

        data = {
            "messages": [
                {
                    "role": "system",
                    "content": COMMAND_PROMPT
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ],
            "temperature": 0.1
        }

        response = requests.post(
            LM_URL,
            json=data,
            timeout=120
        ).json()

        command = response["choices"][0]["message"]["content"]

        command = command.replace("```bash", "")
        command = command.replace("```sh", "")
        command = command.replace("```", "")
        command = command.strip()

        print("\\nAI Command:")
        print(command)

        confirm = input("\\nRun command? (y/n): ")

        if confirm.lower() != "y":
            continue

        ssh_cmd = f'ssh {KALI_USER}@{KALI_IP} "{command}"'

        result = subprocess.getoutput(ssh_cmd)

        print("\\n====================")
        print("RAW OUTPUT")
        print("====================\\n")
        print(result)

        analysis_request = {
            "messages": [
                {
                    "role": "system",
                    "content": ANALYSIS_PROMPT
                },
                {
                    "role": "user",
                    "content": f"""
User Request:
{user_prompt}

Command:
{command}

Output:
{result}
"""
                }
            ],
            "temperature": 0.2
        }

        analysis_response = requests.post(
            LM_URL,
            json=analysis_request,
            timeout=180
        ).json()

        analysis = analysis_response["choices"][0]["message"]["content"]

        print("\\n====================")
        print("AI ANALYSIS")
        print("====================\\n")
        print(analysis)

    except Exception as e:
        print("\\nERROR:")
        print(e)
