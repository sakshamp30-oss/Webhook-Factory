from fastapi import FastAPI
from fastapi import Request
from fastapi import Response
import html
from fastapi.responses import HTMLResponse
from db import init_db
from db import log_event
from db import get_events
import base64
from browser_parser import ua_parser
from geoip import get_location
from geoip import org_check
from mint import generate_token
from make_html_trap import get_html_token
from make_credential import get_secret_token

app = FastAPI()
init_db()

PIXEL_BYTES = base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg==")

@app.get("/t/{token_id}")
async def tracker_hit(token_id:str, request:Request):
    if not ((token_id == get_html_token()) or (token_id == get_secret_token())):
        return Response(content= PIXEL_BYTES, status_code=403)
    ip = request.client.host
    ua = request.headers.get("user-agent") or ""
    location_data = get_location(ip)
    city = location_data.get("city")
    country = location_data.get("country")
    tool = ua_parser(ua)
    if "<" in ua:
        ua = "Suspicious Tried planting html injection"
    elif tool == "Suspicious: Unrecognized Client":
        ua = "Suspicious UA probably an exploit: " + ua
    elif "Automated Tool" in tool:
        ua = "Automated tool: "+ ua
    
    organisation = org_check(ip)
    
    
    log_event(token_id, ip, ua, city, country, tool, organisation)
    return Response(content=PIXEL_BYTES, media_type="image/png")
        


randomstr = generate_token()
print(f"Dashboard Path: /dashboard{randomstr}")
@app.get(f"/dashboard{randomstr}", response_class=HTMLResponse)
async def dashboard():
    events = get_events()
    htmll = """<html><body><h1> IP table</h1>
            <table border = '1'>
                <tr><th>ID</th><th>Token ID</th><th>ip</th><th>User Agent</th><th>Timestamp</th><th>city</th><th>country</th><th>tool</th><th>organisation</th></tr>"""

    for event in events:
        htmll+=f"                <tr><td>{event['id']}</td><td>{event['token_id']}</td><td>{event['ip']}</td><td>{html.escape(event['user_agent'])}</td><td>{event['timestamp']}</td><td>{event['city']}</td><td>{event['country']}</td><td>{event['tool']}</td><td>{event['organisation']}</td></tr>"

    htmll+= "</table></body></html>"
    return HTMLResponse(htmll)

