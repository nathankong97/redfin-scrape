from models import *
import json

if __name__ =="__main__":
    p = Proxy()
    r = Redfin(zip_code="19035", proxy=p.ip_proxies)
    urls = r.property_urls
    for url in urls:
        pro = Property(url=url, proxy=p.ip_proxies)
        print(pro.detail)