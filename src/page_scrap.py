from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd


def web_scraping():
    options = webdriver.ChromeOptions()
    options.add_argument("headless")

    driver = webdriver.Chrome(executable_path="chromedriver", options=options)
    driver.implicitly_wait(3)
    driver.get(url="https://finance.naver.com/sise/etf.nhn")

    soup = BeautifulSoup(driver.page_source, "lxml")
    table = soup.find_all("table", class_="type_1 type_etf")
    df = pd.read_html(str(table), header=0)[0]
    driver.close()

    df = df.drop(columns=["Unnamed: 9"]).dropna()
    df.index = range(1, len(df) + 1)
    df.to_csv("etf_list.csv", mode="w")
    print(df)

    etf_table = soup.find_all("td", class_="ctg")
    etfs = dict()
    for etf in etf_table:
        stock = str(etf.a["href"]).split("=")
        code = stock[-1]
        etfs[etf.a.text] = code
    print("ETFs :", etfs)


if __name__ == "__main__":
    web_scraping()
