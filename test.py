import requests
from bs4 import BeautifulSoup as soup, BeautifulSoup
from requests_html import AsyncHTMLSession
import pyppdf.patch_pyppeteer
import asyncio
target = ["title", "itemDetailUrl", "imagePath"]


async def main():
    header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'}
    HTML = 'https://de.aliexpress.com/item/4000802127824.html'
    asession = AsyncHTMLSession()
    request = await asession.get(
            HTML
    )
    await request.html.arender()

    try:
        h1 = request.html.find('h1')
        title = h1[0].text
        print(title)

        rating_count = request.html.find('.product-reviewer-reviews')
        rating = rating_count[0].text
        print(rating)

        price = request.html.find('.uniform-banner-box-price')
        priceStr = price[0].text
        print(price)
        print(priceStr)
#'#root>div>div.product-main>div>div.product-info>div.product-sku>div.sku-wrap>div.sku-property>ul.sku-property-list>li.sku-property-item>div.sku-property-text>span':
        t = request.html.find('#root>div>div.product-main>div>div.product-info>div.product-sku>div.sku-wrap>div.sku-property>ul.sku-property-list>li.sku-property-item>div.sku-property-text>span')#속성
        print(t)
        for x in t:
            print(x.text)
            print("-----")

        await request.html.browser.close()
    except:
        await request.html.browser.close()



if __name__ == "__main__":
    asyncio.run(main())
#
#     import requests
#     import json
#     import re
#
#     target = ["title", "itemDetailUrl", "imagePath"]
#
#
#     def main(url):
#         r = requests.get(url)
#         match = re.search(r'data: ({.+})', r.text).group(1)
#         data = json.loads(match)
#         goal = [data['pageModule'][x] for x in target] + \
#                [data['priceModule']['formatedActivityPrice']]
#         print(goal)
#
#
#     main("https://es.aliexpress.com/item/32601027783.html")