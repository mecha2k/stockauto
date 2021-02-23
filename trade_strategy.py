import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import marketDB


def get_stock_data(stocks):
    market = marketDB.MarketDB()
    dataframe = pd.DataFrame()
    for stock in stocks:
        dataframe[stock] = market.getDailyPrice(stock, "2016-01-04", "2018-04-27")["close"]
    return dataframe


def eff_frontier(df):
    daily_ret = df.pct_change()
    annual_ret = daily_ret.mean() * 252
    daily_cov = daily_ret.cov()
    annual_cov = daily_cov * 252

    port_ret = []
    port_risk = []
    port_weights = []
    for _ in range(20000):
        weights = np.random.random(len(stocks))
        weights /= np.sum(weights)
        returns = np.dot(weights, annual_ret)
        risk = np.sqrt(np.dot(weights.T, np.dot(annual_cov, weights)))
        port_ret.append(returns)
        port_risk.append(risk)
        port_weights.append(weights)

    portfolio = {"Returns": port_ret, "Risk": port_risk}
    for i, s in enumerate(stocks):
        portfolio[s] = [weight[i] for weight in port_weights]
    df = pd.DataFrame(portfolio)
    df = df[["Returns", "Risk"] + [s for s in stocks]]

    df.plot.scatter(x="Risk", y="Returns", figsize=(8, 6), grid=True)
    plt.title("Efficient Frontier")
    plt.xlabel("Risk")
    plt.ylabel("Expected Returns")
    plt.show()


def portfolio_optimize(df):
    daily_ret = df.pct_change()
    annual_ret = daily_ret.mean() * 252
    daily_cov = daily_ret.cov()
    annual_cov = daily_cov * 252

    port_ret = []
    port_risk = []
    port_weights = []
    sharpe_ratio = []
    for _ in range(20000):
        weights = np.random.random(len(stocks))
        weights /= np.sum(weights)
        returns = np.dot(weights, annual_ret)
        risk = np.sqrt(np.dot(weights.T, np.dot(annual_cov, weights)))
        port_ret.append(returns)
        port_risk.append(risk)
        port_weights.append(weights)
        sharpe_ratio.append(returns / risk)

    portfolio = {"Returns": port_ret, "Risk": port_risk, "Sharpe": sharpe_ratio}
    for i, s in enumerate(stocks):
        portfolio[s] = [weight[i] for weight in port_weights]
    df = pd.DataFrame(portfolio)
    df = df[["Returns", "Risk", "Sharpe"] + [s for s in stocks]]

    max_sharpe = df.loc[df["Sharpe"] == df["Sharpe"].max()]
    min_risk = df.loc[df["Risk"] == df["Risk"].min()]

    df.plot.scatter(
        x="Risk",
        y="Returns",
        c="Sharpe",
        cmap="viridis",
        edgecolors="k",
        figsize=(11, 7),
        grid=True,
    )
    plt.scatter(x=max_sharpe["Risk"], y=max_sharpe["Returns"], c="r", marker="*", s=300)
    plt.scatter(x=min_risk["Risk"], y=min_risk["Returns"], c="r", marker="X", s=200)
    plt.title("Portfolio Optimization")
    plt.xlabel("Risk")
    plt.ylabel("Expected Returns")
    plt.show()


def bollinger_band(df):
    df["MA20"] = df["close"].rolling(window=20).mean()
    df["stddev"] = df["close"].rolling(window=20).std()
    df["upper"] = df["MA20"] + (df["stddev"] * 2)
    df["lower"] = df["MA20"] - (df["stddev"] * 2)
    df = df[19:]

    plt.figure(figsize=(9, 5))
    plt.plot(df.index, df["close"], color="#0000ff", label="Close")
    plt.plot(df.index, df["upper"], "r--", label="Upper band")
    plt.plot(df.index, df["MA20"], "k--", label="Moving average 20")
    plt.plot(df.index, df["lower"], "c--", label="Lower band")
    plt.fill_between(df.index, df["upper"], df["lower"], color="0.9")
    plt.legend(loc="best")
    plt.title("NAVER Bollinger Band (20 day, 2 std)")
    plt.show()

    #
    # def get_rltv_momentum(self, start_date, end_date, stock_count):
    #     """특정 기간 동안 수익률이 제일 높았던 stock_count 개의 종목들 (상대 모멘텀)
    #         - start_date  : 상대 모멘텀을 구할 시작일자 ('2020-01-01')
    #         - end_date    : 상대 모멘텀을 구할 종료일자 ('2020-12-31')
    #         - stock_count : 상대 모멘텀을 구할 종목수
    #     """
    #     connection=pymysql.connect(host='localhost', port=3306,
    #                                db='INVESTAR', user='root', passwd='******', autocommit=True)
    #     cursor=connection.cursor()
    #
    #     # 사용자가 입력한 시작일자를 DB에서 조회되는 일자로 보정
    #     sql=f"select max(date) from daily_price where date <= '{start_date}'"
    #     cursor.execute(sql)
    #     result=cursor.fetchone()
    #     if (result[0] is None):
    #         print("start_date : {} -> returned None".format(sql))
    #         return
    #     start_date=result[0].strftime('%Y-%m-%d')
    #
    #     # 사용자가 입력한 종료일자를 DB에서 조회되는 일자로 보정
    #     sql=f"select max(date) from daily_price where date <= '{end_date}'"
    #     cursor.execute(sql)
    #     result=cursor.fetchone()
    #     if (result[0] is None):
    #         print("end_date : {} -> returned None".format(sql))
    #         return
    #     end_date=result[0].strftime('%Y-%m-%d')
    #
    #     # KRX 종목별 수익률을 구해서 2차원 리스트 형태로 추가
    #     rows=[]
    #     columns=['code', 'company', 'old_price', 'new_price', 'returns']
    #     for _, code in enumerate(self.mk.codes):
    #         sql=f"select close from daily_price " \
    #             f"where code='{code}' and date='{start_date}'"
    #         cursor.execute(sql)
    #         result=cursor.fetchone()
    #         if (result is None):
    #             continue
    #         old_price=int(result[0])
    #         sql=f"select close from daily_price " \
    #             f"where code='{code}' and date='{end_date}'"
    #         cursor.execute(sql)
    #         result=cursor.fetchone()
    #         if (result is None):
    #             continue
    #         new_price=int(result[0])
    #         returns=(new_price / old_price - 1) * 100
    #         rows.append([code, self.mk.codes[code], old_price, new_price,
    #                      returns])
    #
    #     # 상대 모멘텀 데이터프레임을 생성한 후 수익률순으로 출력
    #     df=pd.DataFrame(rows, columns=columns)
    #     df=df[['code', 'company', 'old_price', 'new_price', 'returns']]
    #     df=df.sort_values(by='returns', ascending=False)
    #     df=df.head(stock_count)
    #     df.index=pd.Index(range(stock_count))
    #     connection.close()
    #     print(df)
    #     print(f"\nRelative momentum ({start_date} ~ {end_date}) : " \
    #           f"{df['returns'].mean():.2f}% \n")
    #     return df
    #
    # def get_abs_momentum(self, rltv_momentum, start_date, end_date):
    #     """특정 기간 동안 상대 모멘텀에 투자했을 때의 평균 수익률 (절대 모멘텀)
    #         - rltv_momentum : get_rltv_momentum() 함수의 리턴값 (상대 모멘텀)
    #         - start_date    : 절대 모멘텀을 구할 매수일 ('2020-01-01')
    #         - end_date      : 절대 모멘텀을 구할 매도일 ('2020-12-31')
    #     """
    #     stockList=list(rltv_momentum['code'])
    #     connection=pymysql.connect(host='localhost', port=3306,
    #                                db='INVESTAR', user='root', passwd='******', autocommit=True)
    #     cursor=connection.cursor()
    #
    #     # 사용자가 입력한 매수일을 DB에서 조회되는 일자로 변경
    #     sql=f"select max(date) from daily_price " \
    #         f"where date <= '{start_date}'"
    #     cursor.execute(sql)
    #     result=cursor.fetchone()
    #     if (result[0] is None):
    #         print("{} -> returned None".format(sql))
    #         return
    #     start_date=result[0].strftime('%Y-%m-%d')
    #
    #     # 사용자가 입력한 매도일을 DB에서 조회되는 일자로 변경
    #     sql=f"select max(date) from daily_price " \
    #         f"where date <= '{end_date}'"
    #     cursor.execute(sql)
    #     result=cursor.fetchone()
    #     if (result[0] is None):
    #         print("{} -> returned None".format(sql))
    #         return
    #     end_date=result[0].strftime('%Y-%m-%d')
    #
    #     # 상대 모멘텀의 종목별 수익률을 구해서 2차원 리스트 형태로 추가
    #     rows=[]
    #     columns=['code', 'company', 'old_price', 'new_price', 'returns']
    #     for _, code in enumerate(stockList):
    #         sql=f"select close from daily_price " \
    #             f"where code='{code}' and date='{start_date}'"
    #         cursor.execute(sql)
    #         result=cursor.fetchone()
    #         if (result is None):
    #             continue
    #         old_price=int(result[0])
    #         sql=f"select close from daily_price " \
    #             f"where code='{code}' and date='{end_date}'"
    #         cursor.execute(sql)
    #         result=cursor.fetchone()
    #         if (result is None):
    #             continue
    #         new_price=int(result[0])
    #         returns=(new_price / old_price - 1) * 100
    #         rows.append([code, self.mk.codes[code], old_price, new_price,
    #                      returns])
    #
    #     # 절대 모멘텀 데이터프레임을 생성한 후 수익률순으로 출력
    #     df=pd.DataFrame(rows, columns=columns)
    #     df=df[['code', 'company', 'old_price', 'new_price', 'returns']]
    #     df=df.sort_values(by='returns', ascending=False)
    #     connection.close()
    #     print(df)
    #     print(f"\nAbasolute momentum ({start_date} ~ {end_date}) : " \
    #           f"{df['returns'].mean():.2f}%")
    #     return


if __name__ == "__main__":
    stocks = ["삼성전자", "SK하이닉스", "현대자동차", "NAVER"]
    dataframe = get_stock_data(stocks)

    eff_frontier(dataframe)
    portfolio_optimize(dataframe)
    bollinger_band(dataframe["NAVER"])
