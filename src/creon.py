import pandas as pd
import win32com.client


def get_stock_lists():
    # 종목코드 리스트 구하기
    objCpCodeMgr = win32com.client.Dispatch("CpUtil.CpCodeMgr")
    codeList = objCpCodeMgr.GetStockListByMarket(1)  # 거래소
    codeList2 = objCpCodeMgr.GetStockListByMarket(2)  # 코스닥

    print("거래소 종목코드", len(codeList))
    for i, code in enumerate(codeList):
        secondCode = objCpCodeMgr.GetStockSectionKind(code)
        name = objCpCodeMgr.CodeToName(code)
        stdPrice = objCpCodeMgr.GetStockStdPrice(code)
        print(i, code, secondCode, stdPrice, name)

    print("코스닥 종목코드", len(codeList2))
    for i, code in enumerate(codeList2):
        secondCode = objCpCodeMgr.GetStockSectionKind(code)
        name = objCpCodeMgr.CodeToName(code)
        stdPrice = objCpCodeMgr.GetStockStdPrice(code)
        print(i, code, secondCode, stdPrice, name)

    print("거래소 + 코스닥 종목코드 ", len(codeList) + len(codeList2))


def get_stock_price(code):
    # 현재가 객체 구하기
    objStockMst = win32com.client.Dispatch("DsCbo1.StockMst")
    objStockMst.SetInputValue(0, code)  # 종목 코드 - 삼성전자
    objStockMst.BlockRequest()

    # 현재가 통신 및 통신 에러 처리
    rqStatus = objStockMst.GetDibStatus()
    rqRet = objStockMst.GetDibMsg1()
    print("통신상태", rqStatus, rqRet)
    if rqStatus != 0:
        exit()

    # 현재가 정보 조회
    code = objStockMst.GetHeaderValue(0)  # 종목코드
    name = objStockMst.GetHeaderValue(1)  # 종목명
    time = objStockMst.GetHeaderValue(4)  # 시간
    cprice = objStockMst.GetHeaderValue(11)  # 종가
    diff = objStockMst.GetHeaderValue(12)  # 대비
    open = objStockMst.GetHeaderValue(13)  # 시가
    high = objStockMst.GetHeaderValue(14)  # 고가
    low = objStockMst.GetHeaderValue(15)  # 저가
    offer = objStockMst.GetHeaderValue(16)  # 매도호가
    bid = objStockMst.GetHeaderValue(17)  # 매수호가
    vol = objStockMst.GetHeaderValue(18)  # 거래량
    vol_value = objStockMst.GetHeaderValue(19)  # 거래대금

    # 예상 체결관련 정보
    exFlag = objStockMst.GetHeaderValue(58)  # 예상체결가 구분 플래그
    exPrice = objStockMst.GetHeaderValue(55)  # 예상체결가
    exDiff = objStockMst.GetHeaderValue(56)  # 예상체결가 전일대비
    exVol = objStockMst.GetHeaderValue(57)  # 예상체결수량

    print("코드", code)
    print("이름", name)
    print("시간", time)
    print("종가", cprice)
    print("대비", diff)
    print("시가", open)
    print("고가", high)
    print("저가", low)
    print("매도호가", offer)
    print("매수호가", bid)
    print("거래량", vol)
    print("거래대금", vol_value)

    if exFlag == ord("0"):
        print("장 구분값: 동시호가와 장중 이외의 시간")
    elif exFlag == ord("1"):
        print("장 구분값: 동시호가 시간")
    elif exFlag == ord("2"):
        print("장 구분값: 장중 또는 장종료")

    print("예상체결가 대비 수량")
    print("예상체결가", exPrice)
    print("예상체결가 대비", exDiff)
    print("예상체결수량", exVol)


def get_stock_chart_num(code, num=10):
    # 차트 객체 구하기
    objStockChart = win32com.client.Dispatch("CpSysDib.StockChart")

    objStockChart.SetInputValue(0, code)  # 종목 코드 - 삼성전자
    objStockChart.SetInputValue(1, ord("2"))  # 개수로 조회
    objStockChart.SetInputValue(4, num)  # 최근 10일 치
    objStockChart.SetInputValue(5, [0, 2, 3, 4, 5, 8])  # 날짜,시가,고가,저가,종가,거래량
    objStockChart.SetInputValue(6, ord("D"))  # '차트 주가 - 일간 차트 요청
    objStockChart.SetInputValue(9, ord("1"))  # 수정주가 사용

    objStockChart.BlockRequest()
    len = objStockChart.GetHeaderValue(3)

    data = []
    for i in range(len):
        date = objStockChart.GetDataValue(0, i)
        open1 = objStockChart.GetDataValue(1, i)
        high = objStockChart.GetDataValue(2, i)
        low = objStockChart.GetDataValue(3, i)
        close = objStockChart.GetDataValue(4, i)
        vol = objStockChart.GetDataValue(5, i)
        data.append([date, open1, high, low, close, vol])

    return data


def get_stock_chart_period(code, num=1000000):
    # 차트 객체 구하기
    objStockChart = win32com.client.Dispatch("CpSysDib.StockChart")
    objStockChart.SetInputValue(0, code)  # 종목 코드 - 삼성전자
    objStockChart.SetInputValue(1, ord("2"))  # 개수로 조회
    objStockChart.SetInputValue(4, num)  # 1000000개 = 모든 구간
    objStockChart.SetInputValue(5, [0, 2, 3, 4, 5, 8, 9])  # 날짜,시가,고가,저가,종가,거래량
    objStockChart.SetInputValue(6, ord("D"))  # '차트 주가 - 일간 차트 요청
    objStockChart.SetInputValue(9, ord("1"))  # 수정주가 사용

    data = []
    while True:
        objStockChart.BlockRequest()
        cnt = objStockChart.GetHeaderValue(3)  # 3은 요청 개수
        for i in range(cnt):  # => 매일매일의 데이터를 하루씩 처리
            date = objStockChart.GetDataValue(0, i)  # 날짜
            open1 = objStockChart.GetDataValue(1, i)  # 시가
            high = objStockChart.GetDataValue(2, i)  # 고가
            low = objStockChart.GetDataValue(3, i)  # 저가
            close = objStockChart.GetDataValue(4, i)  # 종가
            volume = objStockChart.GetDataValue(5, i)  # 거래량
            amount = objStockChart.GetDataValue(6, i)  # 거래대금
            data.append([date, open1, high, low, close, volume])
        if objStockChart.Continue == False:  # 더 요청할 데이터가 없으면 break, 있으면 계속 요청
            break

    # date, open, high, low, close, volume = zip(*data)
    # print(list(date))
    df = pd.DataFrame(data, columns=["date", "open", "high", "low", "close", "volume"])
    df["date"] = pd.to_datetime(df["date"].astype(object), format="%Y%m%d")

    return df

    # # 딕셔너리를 만들어 데이터 프레임으로 변환
    # dict1 = {
    #     "day": day_list,
    #     "open": open_list,
    #     "high": high_list,
    #     "low": low_list,
    #     "close": close_list,
    #     "vol": vol_list,
    #     "amount": amount_list,
    # }

    # df = pd.DataFrame(
    #     dict1, columns=["day", "open", "high", "low", "close", "vol", "amount"]
    # )  # 2. 데이터프레임으로 만들기
    # df = df.sort_index(ascending=False)  # 내림차순 정렬

    # df.to_csv("{}.csv".format(stockcode), index=False)  # csv로 삼성전자 전구간 일봉을 저장


if __name__ == "__main__":
    # 연결 여부 체크
    objCpCybos = win32com.client.Dispatch("CpUtil.CpCybos")
    bConnect = objCpCybos.IsConnect
    if bConnect == 0:
        print("PLUS가 정상적으로 연결되지 않음. ")
        exit()

    # get_stock_lists()
    # get_stock_price(code="A005930")
    # data = get_stock_chart_num(code="A005930", num=10)
    # print("date", "open", "high", "low", "close", "volume")
    # print("===============================================")
    # for i in range(len(data)):
    #     stock = data[i]
    #     print(stock[0], stock[1], stock[2], stock[3], stock[4], stock[5])

    df = get_stock_chart_period(code="A005930")
    df.info()
    print(df.head())
    print(df.describe())
