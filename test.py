import requests
from bs4 import BeautifulSoup as soup, BeautifulSoup
from requests_html import AsyncHTMLSession
import pyppdf.patch_pyppeteer
import asyncio
target = ["title", "itemDetailUrl", "imagePath"]


async def main():
    header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'}
    #HTML = 'https://de.aliexpress.com/item/1005003462345537.html?spm=a2g0o.productlist.0.0.5b5d7f3eP7WT2w&algo_pvid=acc27bba-a787-46dd-a4f5-48ffc27e1706&aem_p4p_detail=2022031107115612782986930137560023687702&algo_exp_id=acc27bba-a787-46dd-a4f5-48ffc27e1706-4&pdp_ext_f=%7B%22sku_id%22%3A%2212000025899459854%22%7D&pdp_pi=-1%3B30948.0%3B-1%3B-1%40salePrice%3BKRW%3Bsearch-mainSearch'
    HTML = "https://ko.aliexpress.com/item/1005001299588690.html?spm=a2g0o.new_user_benefits.0.0.49f9BcK2BcK2G4&pdp_ext_f=%7B%22ship_from%22:%22CN%22,%22sku_id%22:%2212000025048220927%22%7D&scm=1007.34914.273009.0&scm_id=1007.34914.273009.0&scm-url=1007.34914.273009.0&pvid=7e2addeb-4a47-4ecd-ae7a-5c7d6e056971&utparam=%257B%2522process_id%2522%253A%2522401%2522%252C%2522x_object_type%2522%253A%2522product%2522%252C%2522pvid%2522%253A%25227e2addeb-4a47-4ecd-ae7a-5c7d6e056971%2522%252C%2522belongs%2522%253A%255B%257B%2522floor_id%2522%253A%252222234693%2522%252C%2522id%2522%253A%2522782032%2522%252C%2522type%2522%253A%2522dataset%2522%257D%252C%257B%2522id_list%2522%253A%255B%25221000094891%2522%255D%252C%2522type%2522%253A%2522gbrain%2522%257D%255D%252C%2522pageSize%2522%253A%252224%2522%252C%2522language%2522%253A%2522ko%2522%252C%2522scm%2522%253A%25221007.34914.273009.0%2522%252C%2522countryId%2522%253A%2522KR%2522%252C%2522tpp_buckets%2522%253A%252221669%25230%2523265320%252379_21669%25234190%252319159%2523107_24914%25230%2523273009%252318%2522%252C%2522x_object_id%2522%253A%25221005001299588690%2522%257D"
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
        print(priceStr)

        # '#root>div>.product-main>div>.product-info>.product-sku>div>div:nth-child(1)>ul li>div' //국가
        # '#root>div>.product-main>div>.product-info>.product-sku>div>div:nth-child(2)>ul li>div' // 옵션 이미지
        # .product-info>.product-sku>div>.sku-property:nth-child(3)>ul li:nth-child(1)>div //옵션 텍스트
        property = '.product-info>.product-sku>div>.sku-property:nth-child(3)>ul li>.sku-property-text>span'
        t = request.html.find(property)
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