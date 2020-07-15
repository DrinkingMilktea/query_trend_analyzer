from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
import re
from time import sleep
newsQuaryfront = "https://search.naver.com/search.naver?query="
newsQuaryend = "&where=news&ie=utf8&sm=nws_hty"

newsTitlefront1 = "/html/body/div[3]/div[2]/div/div[1]/div[1]/ul/li["
newsTitlefront2 = "/html/body/div[3]/div[2]/div/div[1]/div/ul/li["
newsTitleend = "]/dl/dt/a"
newsTabfront = "/html/body/div[3]/div[2]/div/div[1]/div[1]/div[2]/a["

option = webdriver.ChromeOptions()
#option.add_argument("headless")
option.add_argument("window-size=1920x1080")
option.add_argument("disable-gpu")
newsTab = [1,3,4,5,6,6,6,6,6]
hangul = re.compile('[^ 0-9ㄱ-ㅣ가-힣]+')

def newcollactor(quary):
    driver = webdriver.Chrome('./data/chrome83.14/chromedriver', options=option)
    driver.implicitly_wait(3)
    data = pd.DataFrame(columns=["crawled"])
    driver.get(newsQuaryfront + quary + newsQuaryend)
    main_tab = driver.current_window_handle
    for tab in newsTab:
        for news in range(1, 11):
            try:
                driver.find_element_by_xpath(newsTitlefront1 + str(news) + newsTitleend).click()
            except:
                driver.find_element_by_xpath(newsTitlefront2 + str(news) + newsTitleend).click()
            driver.switch_to.window(driver.window_handles[1])
            html = driver.page_source
            only_hangul = hangul.sub('', html)
            only_meaningful = re.sub('[0-9]{5,}', ' ', only_hangul)
            #print(only_meaningful)
            data = data.append({"crawled":only_meaningful}, ignore_index=True)
            sleep(0.1)
            driver.close()
            driver.switch_to.window(main_tab)
        driver.find_element_by_xpath(newsTabfront + str(tab) + "]").click()
    data.to_csv("./data/"+quary+"data.csv", encoding='utf-8')
    driver.quit()
    return data



if __name__ == "__main__":
    newcollactor("CJ제일제당")