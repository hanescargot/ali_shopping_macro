from dataclasses import dataclass
@dataclass
class Product:
    state: str = "신상품"
    categoryCode: int = 50006675
    name: str = "아이템 명 오류"
    price : int = 1000000
    count : int = 1
    asMsg : str = "제품 상세 내역 조회"
    asPhoneNumber : str = "01044890709"
    mainImgFileName : str = "snail.png"
    subImgFileName: str = "snail.png"
    imgUrl : str = "test"
    bugase : str = "과세상품"
    kidAble : str = "Y"
    reviewVisible : str = "Y"
    countryCode : str = "0200037"
    shipCompany : str = "DogPy"
    shipDuplicated : str = "N"
    delivery : str = "택배‚ 소포‚ 등기"
    deliveryPriceType : str = "수량별" #무료 조건부무료 유료
    defaultDeliveryPrice : int = 60000
    deliveryPayment : str = "선결제"
    deliveryPriceItemCount : int = 1
    deliveryRefund : int = 60000
    deliveryExchange : int = 60000
    optionType : str = "단독형"
    optionCategory : str = "" #줄바꿈으로 구분
    optionName : str = "" # 이름은,로 카테고리는 줄바꿈으로 구반
    optionPrice : str = "" #,로 구분 없으면 0원
    optionCount : str = "" #재고수량 ,로 구분
    vip : str = "N"




