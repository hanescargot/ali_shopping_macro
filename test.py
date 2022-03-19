import datetime
import time

import requests
from bs4 import BeautifulSoup as soup, BeautifulSoup
from requests_html import AsyncHTMLSession
import pyppdf.patch_pyppeteer
import asyncio
import re

from selenium import webdriver
from selenium.webdriver.common.by import By

from ProductDto import Product
import os
import pandas as pd
target = ["title", "itemDetailUrl", "imagePath"]
from dataclasses import asdict, dataclass






async def getDescripImg():
    HTML = 'https://de.aliexpress.com/item/1005003624117637.html'
    driver = webdriver.Chrome('C:/Users/pyrio/pythonProject/shopping_macro/chromedriver_win32/chromedriver.exe')
    driver.get(HTML)

    # 스크롤 기능
    driver.execute_script('window.scrollTo(0, 800);')
    time.sleep(1)
    print('====success=====')
    items = driver.find_elements_by_css_selector('#product-description>div>p>img')

    for i in items:
        print(i.get_attribute("src"))

    await driver.close()
    return

async def main(type, maginPercent, categoryCode):
    print(type)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9'}
    HTML = 'https://de.aliexpress.com/item/1005003624117637.html'

    try:
        response = requests.get(HTML, headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')#'html.parser'    'lxml'
        print(soup)
        print("===================================")


        asession = AsyncHTMLSession()
        request = await asession.get(
            HTML
        )
        await request.html.arender()
        html = request.html

        #start
        product = Product()
        product.categoryCode = categoryCode


        h1 = html.find("title")
        title = h1[0].text
        print(title)
        product.name = title

        rating_count = html.find('.product-reviewer-reviews')
        rating = rating_count[0].text
        print(rating)
        # .uniform-banner-box-price
        # .product-price-value
        price = html.find('.product-price-value')[0].text
        print(price)
        price = int(price.replace(",","").split(" ")[-1])
        product.price= round(price + price/100*maginPercent, -2)
        print(price)
        print(product.price)

        # '#root>div>.product-main>div>.product-info>.product-sku>div>div:nth-child(1)>ul li>div' //국가
        # '#root>div>.product-main>div>.product-info>.product-sku>div>div:nth-child(2)>ul li>div' // 옵션 이미지
        # .product-info>.product-sku>div>.sku-property:nth-child(3)>ul li:nth-child(1)>div //옵션 텍스트
        # '.product-info>.product-sku>div>.sku-property:nth-child(3)>ul li>.sku-property-text>span'
        propertyPath = '.product-info>.product-sku li>.sku-property-text>span'
        property = html.find(propertyPath)
        for p in property:
            print(p.text)
        print("===pass property==")


        getDescripImg()

        defPath = "C:/Users/pyrio/pythonProject/shopping_macro/"
        # df = pd.json_normalize(asdict(Product()))
        columns = {'상품상태':product.state,
                      '카테고리ID': product.categoryCode,
                      '상품명':product.name,
                      '판매가':product.price,
                      '재고수량':product.count,
                      'A/S 안내내용':product.asMsg,
                      'A/S 전화번호':product.asPhoneNumber,
                      '대표 이미지 파일명':product.mainImgFileName,
                      '추가 이미지 파일명':product.subImgFileName,
                      '상품 상세정보':product.imgUrl,
                      '부가세':product.bugase,
                      '미성년자 구매':product.kidAble,
                      '구매평 노출여부':product.reviewVisible,
                      '원산지 코드':product.countryCode,
                      '수입사':product.shipCompany,
                      '복수원산지 여부':product.shipDuplicated,
                      '배송방법':product.delivery,
                      '배송비 유형':product.deliveryPriceType,
                      '기본배송비':product.defaultDeliveryPrice,
                      '배송비 결제방식':product.deliveryPayment,
                      '수량별부과-수량':product.deliveryPriceItemCount,
                      '반품배송비':product.deliveryRefund,
                      '교환배송비':product.deliveryExchange,
                      '옵션형태':product.optionType,
                      '옵션명':product.optionCategory,
                      '옵션값':product.optionName,
                      '옵션가':product.optionPrice,
                      '옵션 재고수량':product.optionCount,
                      '스토어찜회원 전용여부':product.vip
        }
        if(os.path.isfile(defPath+"result.xlsx")):
            print("excel from result")
            df = pd.read_excel(defPath+"result.xlsx",engine='openpyxl')
        else:
            print("excel from template")
            df = pd.read_excel(defPath+"ProductTemplate.xls", engine='openpyxl')



        result = df.append(columns, ignore_index=True)

        for i in range(len(result.index)):
            #7자리 맞춰서 앞에 0 추가
            value = str(result['원산지 코드'][i]).zfill(7)
            result.loc[i,'원산지 코드'] = value

        result.to_excel(defPath+"result.xlsx", sheet_name="New", index=False)

        # await html.browser.close()
    except:
        print("error")

        # await html.browser.close()



# randerType
CONVERT_DB = 1

if __name__ == "__main__":
    # text()
    asyncio.run(main(CONVERT_DB, 30, 50006675))
