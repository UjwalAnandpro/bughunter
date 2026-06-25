from lmstudio import LMStudio

ai = LMStudio()

print("Server:", ai.check_server())

cmd = ai.generate_command("show current user")

print(cmd)

analysis = ai.analyze_output(
    cmd,
    "ujwal"
)

print()
print(analysis)