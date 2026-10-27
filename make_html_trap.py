from mint import generate_token
import sys

def create_html_trap(BASEURL):
    global token
    token = generate_token()
    tracker_url = BASEURL + token
    html_content = f''' <html>
                            <h1> BLA BLA Internet portal</h1>
                            <body> <img src="{tracker_url}" style="display:none;"> </body>
                        </html>'''

    with open ("company_login.html", "w") as f:
        f.write(html_content)
    
    print(f"created a html file! URL: {tracker_url}")

def get_html_token():
    return token

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("""Please enter a base url by using the command
                python make_html_trap.py <YOUR BASE URL>""")
        sys.exit(1)
    create_html_trap(sys.argv[1])
