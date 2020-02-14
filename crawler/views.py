import json
import requests
import time

from django.http import JsonResponse
from django.views import View

from bs4 import BeautifulSoup

class CrawlerView(View):
    def get(self, request):
        start_time = time.time()
        keyword         = str(request.GET.get('keyword', None))
        limit           = int(request.GET.get('limit', 36))
        target_page     = f"""https://www.coupang.com/np/search"""
        payload         = {
            "q"         : keyword,
            "channel"   : "user",
            "listSize"  : limit,
        }
        ##proxies = {
        ##    "http": 'http://255.255.255.252',
        ##    "https": 'https://121.134.83.111'
        ##} ##for the case to use proxies, left the code. But it didn't work properly when I tried before.
        headers          = {
            "user-agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36"
        }
        response         = requests.get(target_page, headers = headers, params = payload)#, proxies = proxies)
        html             = response.text
        soup             = BeautifulSoup(html, 'html.parser')
        get_names        = soup.select("a > dl > dd > div > div.name")
        names            = [name.text for name in get_names]
        get_images       = soup.select("a > dl > dt > img")
        images           = []
        for image in get_images:
            if image['src'] == "//img1a.coupangcdn.com/image/coupang/search/blank1x1.gif":
                images.append("http:" + image['data-img-src'])
            else : 
                images.append("http:" + image['src'])
        get_prices       = soup.select("a > dl > dd > div > div.price-area > div > div.price > em > strong")
        str_prices       = [price.text for price in get_prices]
        prices           = [int(price.replace(",","")) for price in str_prices]
        get_infos        = soup.find(id="productList")
        get_ids          = json.loads(get_infos["data-products"])
        ids              = get_ids["indexes"]
        urls             = [f"""https://www.coupang.com/vp/products/{id}"""for id in ids]
        result           = {
            "landingUrl": f"""https://www.coupang.com/np/search?q={keyword}&channel=user&listSize={limit}""",
            "productData": [
                {
                    
                    "num" : i,
                    "productId": ids[i],
                    "productName": names[i],
                    "productPrice": prices[i],
                    "productImage": images[i],
                    "productUrl": urls[i],
                    "keyword": keyword
                } for i in range(0,len(names))
            ]
        }
        print("duration : ", time.time() - start_time)
        return JsonResponse(result, status = 200)

    

