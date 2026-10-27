from mint import generate_token
import sys
def create_credential_file(BASE_URL):
    global token
    token = generate_token()
    tracker_url = BASE_URL + token
    content = f"""AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
                AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
                AWS_DEFAULT_REGION=us-east-1
                AWS_BILLING_ALERT_WEBHOOK={tracker_url}"""

    with open("secrets.env", "w") as f:
        f.write(content)

    print(f"Create secrets.env ! Trap URL: {tracker_url}")

def get_secret_token():
    return token
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("""Please enter a base url by using the command
                python make_credential.py <YOUR BASE URL>""")
        sys.exit(1)
    create_credential_file(sys.argv[1])