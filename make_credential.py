from mint import generate_token
import sys
from pathlib import Path

file_exists = Path("tokens.txt").exists()
empty = True
if file_exists:
    with open("tokens.txt", "r") as f:
        first_line = f.readline()
        if first_line.strip():
            empty = False

def create_credential_file(BASE_URL):
    global token
    token = generate_token()
    if BASE_URL[len(BASE_URL)-1] == "/":
        tracker_url = BASE_URL + "t/" + token
    else:
        tracker_url = BASE_URL + "/t/" + token
    content = f"""AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
                AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
                AWS_DEFAULT_REGION=us-east-1
                AWS_BILLING_ALERT_WEBHOOK={tracker_url}"""

    with open("secrets.env", "w") as f:
        f.write(content)

    print(f"Create secrets.env ! Trap URL: {tracker_url}")

def get_secret_token():
    with open("tokens.txt", "r") as f:
        for line in f:
            if line.strip().startswith("Secr") :
                return(line.strip()[5:17])
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("""Please enter a base url by using the command
                python make_credential.py <YOUR BASE URL>""")
        sys.exit(1)
    create_credential_file(sys.argv[1])
    if empty or not file_exists:
        with open("tokens.txt", "w") as f:
            f.write(f"Secr:{token}\n")
    elif file_exists and not empty:
        found = False
        read_count = 0
        lines = []
        with open("tokens.txt", "r") as f:
            for line in f:
                lines.append(line.strip())
                if line.strip()[:4] == "Secr":
                    found = True
                    foundline = read_count
                read_count += 1
                
                
        if found:
            with open("tokens.txt", "w") as f:
                for index in range(read_count):
                    if index == foundline:
                        f.write(f"Secr:{token}\n")
                    else:
                        f.write(lines[index] + "\n")
        else:
            with open("tokens.txt", "a") as f:
                f.write(f"Secr:{token}\n")