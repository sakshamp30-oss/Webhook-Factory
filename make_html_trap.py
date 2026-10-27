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
        
def create_html_trap(BASEURL):
    global token
    token = generate_token()
    if BASEURL[len(BASEURL)-1] == "/":
        tracker_url = BASEURL + "t/" + token
    else:
        tracker_url = BASEURL + "/t/" + token

    html_content = f''' <html>
                            <h1> BLA BLA Internet portal</h1>
                            <body> <img src="{tracker_url}" style="display:none;"> </body>
                        </html>'''

    with open ("company_login.html", "w") as f:
        f.write(html_content)
    
    print(f"created a html file! URL: {tracker_url}")

def get_html_token():
    with open("tokens.txt", "r") as f:
        for line in f:
            if line.strip().startswith("Html") :
                return(line.strip()[5:17])


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("""Please enter a base url by using the command
                python make_html_trap.py <YOUR BASE URL>""")
        sys.exit(1)
    create_html_trap(sys.argv[1])
    if empty or not file_exists:
        with open("tokens.txt", "w") as f:
            f.write(f"Html:{token}\n")
    elif file_exists and not empty:
        found = False
        read_count = 0
        lines = []
        with open("tokens.txt", "r") as f:
            for line in f:
                lines.append(line.strip())
                if line.strip()[:4] == "Html":
                    found = True
                    foundline = read_count
                read_count += 1
                
                
        if found:
            with open("tokens.txt", "w") as f:
                for index in range(read_count):
                    if index == foundline:
                        f.write(f"Html:{token}\n")
                    else:
                        f.write(lines[index] + "\n")
        else:
            with open("tokens.txt", "a") as f:
                f.write(f"Html:{token}\n")
                 

        
