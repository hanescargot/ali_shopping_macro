import datetime
import shutil
import time

import requests
import wget
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




def getDescripImg(driver):
    # 스크롤 기능
    driver.execute_script('window.scrollTo(0, 800);')
    time.sleep(1)
    print('====success=====')
    items = driver.find_elements_by_css_selector('#product-description img')
    resultList = []
    for i in items:
        resultList.append(i.get_attribute("src"))
    print(resultList)
    return resultList

def getImgOptionText(driver):
    # 이미지로 된 옵션
    driver.execute_script('window.scrollTo(0, 800);')
    time.sleep(1)
    path = '.product-info>.product-sku>div>.sku-property>ul'
    uls = driver.find_elements_by_css_selector(path)
    resultStringList = []
    for i in uls:
        img = i.find_elements_by_css_selector("li img")
        tmpList = []
        for s in img:
            data = s.get_attribute("alt")
            tmpList.append(data)
        resultStringList.append(", ".join(tmpList))

    return "\n".join(resultStringList)

def getAlloptionName(driver):
    path = '.product-info>.product-sku>div>.sku-property:nth-child(n+2)>ul'#:nth-child(n+2)
    uls = driver.find_elements_by_css_selector(path)
    resultStringList = []
    for i in uls:
        span = i.find_elements_by_css_selector("li>div>span")
        tmpList = []
        for s in span:
            data = s.text
            tmpList.append(data)
        resultStringList.append(", ".join(tmpList))
    return "\n".join(resultStringList)

async def main(type, maginPercent, categoryCode):
    print(type)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9'}
    HTML = 'https://ko.aliexpress.com/item/1005003321002994.html'
    driver = webdriver.Chrome('C:/Users/pyrio/pythonProject/shopping_macro/chromedriver_win32/chromedriver.exe')
    driver.get(HTML)

    defPath = "C:/Users/pyrio/pythonProject/shopping_macro/"

    # 대표, sub사진 저장 & 제목
    imgSavePoint = defPath + "img_res/"
    imgList = driver.find_elements_by_css_selector('.images-view-list img')
    strSite = imgList[0].get_attribute('src').replace("_50x50.jpg_.webp", "")
    strFileName = strSite.split("/")[-1]
    # product.mainImgFileName = strFileName
    print(strSite)
    print(imgSavePoint + strFileName)
    if os.path.exists(imgSavePoint + strFileName) != True:
        # wget.download(strSite)
        #헤더 없으면 403에러 남
        r = requests.get(strSite, stream=True, headers={'User-agent': 'Mozilla/5.0'})
        print(r.status_code)
        if r.status_code == 200:
            with open(imgSavePoint+strFileName, 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)
    print("===file downloaded===")
    # subFileList = []
    # for img in imgList[1:]:
    #     strFile = img.get_attribute('src').replace("_50x50.jpg_.webp", "").split("/")[-1]
    #     subFileList.append(strFile)
    #     wget.download(strFile, imgSavePoint + strFile)
    # product.subImgFileName = "\n".join(subFileList)
    try:
        response = requests.get(HTML, headers=headers)
        # soup = BeautifulSoup(response.text, 'lxml')#'html.parser'    'lxml'
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
        product.name = title[:100]

        rating_count = html.find('.product-reviewer-reviews')
        rating = rating_count[0].text
        print(rating)
        # .uniform-banner-box-price
        # .product-price-value
        priceList = html.find('.product-price-value')

        if len(priceList)<1:
            priceList = html.find('.uniform-banner-box-price')
        price = priceList[0].text
        print(price)
        price = int(price.replace(",","").split(" ")[-1])
        product.price= round(price + price/100*maginPercent, -2)
        print(price)
        print(product.price)

        #옵션 아이템 목록
        product.optionName = (getImgOptionText(driver)+getAlloptionName(driver)).strip()
        print(product.optionName)

        print('카테고리!!')
        #옵션 카테고리 타이틀
        categoryList = []
        categoryPath = '.sku-property .sku-title'
        for i in html.find(categoryPath):
            t = i.text[:-1]
            if not( t == '수량' or t == '배송지'):
                categoryList.append(t)

        product.optionCategory += "\n".join(categoryList)
        print(product.optionCategory)

        #설명 URL
        # product.imgUrl = "\n".join(getDescripImg(driver))
        descriptionTag = driver.find_elements_by_css_selector('#product-description')
        product.imgUrl = descriptionTag[0].get_attribute('innerHTML')

        # 배송비
        deliverySearch = driver.find_elements_by_css_selector('.product-shipping-price span')
        priceStr = deliverySearch[0].text
        if priceStr == "무료 배송":
            delivery = 0
        else:
            won = round(int(priceStr.split(" ")[2].replace(",","")),-3)
            delivery=won

        product.deliveryPrice =delivery
        product.deliveryRefund =delivery
        product.deliveryExchange =delivery
        print(delivery)












        #엑셀 작성
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
                      '스토어찜회원 전용여부':product.vip,
                      'url':HTML
        }
        if(os.path.isfile(defPath+"result.xlsx")):
            print("excel from result")
            df = pd.read_excel(defPath+"result.xlsx",engine='openpyxl')
        else:
            print("excel from template")
            df = pd.read_excel(defPath+"Template.xlsx", engine='openpyxl')



        result = df.append(columns, ignore_index=True)

        for i in range(len(result.index)):
            #7자리 맞춰서 앞에 0 추가
            value = str(result['원산지 코드'][i]).zfill(7)
            result.loc[i,'원산지 코드'] = value

        result.to_excel(defPath+"result.xlsx", sheet_name="New", index=False)
        #
        #
        # copyResult = df.append({'url' : HTML})
        # copyResult.to_excel(defPath + "result_copy.xlsx", sheet_name="New", index=False)
        #
        #


        driver.close()
        await html.browser.close()
    except:
        print("error")
        driver.close()
        await html.browser.close()



# randerType
CONVERT_DB = 1

if __name__ == "__main__":
    # text()
    asyncio.run(main(CONVERT_DB, 30, 50006675))
