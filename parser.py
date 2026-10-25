from user_agents import parse

def ua_parser(ua_string):
    if ua_string == "":
        return "Suspicious: Empty UA"
        
    automated_tools = ["python-requests", "curl", "wget", "sqlmap", "nmap", "masscan", "go-http-client", "zgrab", "nikto", "aiohttp"]
    
    for tool in automated_tools:
        if tool in ua_string.lower():
            return f"Automated Tool: {tool}"

    parsed_ua = parse(ua_string)
    
    if parsed_ua.browser.family == "Other":
        return "Suspicious: Unrecognized Client"
        
    return f"{parsed_ua.browser.family} on {parsed_ua.os.family}"
