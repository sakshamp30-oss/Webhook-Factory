import geoip2.database
import ipaddress

city_DB_PATH = "data/GeoLite2-City.mmdb"
proxy_DB_PATH = "data/GeoLite2-ASN.mmdb"

def get_location(ip):
    if ipaddress.ip_address(ip).is_private:
        return {"city": "Localhost", "country": "Local"}
        
    try:
        with geoip2.database.Reader(city_DB_PATH) as reader:
            response = reader.city(ip)
            city = response.city.name or "Unknown"
            country = response.country.name or "Unknown"
            return {"city": city, "country": country}
    except Exception as e:
        return {"city": "Unknown", "country": "Unknown"}

def org_check(ip):
    try:
        with geoip2.database.Reader(proxy_DB_PATH) as reader:
            response = reader.asn(ip)
            org = response.autonomous_system_organization or "Unknown"
            return f"This ip is from {org}"
    except Exception as e:
        return "Unknown"


    
