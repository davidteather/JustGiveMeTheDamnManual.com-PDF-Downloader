import selenium
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import requests
from bs4 import BeautifulSoup
import time

options = Options()
options.headless = False
driver = webdriver.Firefox(options=options)


driver.get("https://justgivemethedamnmanual.com/")

makes = driver.find_elements_by_xpath("//div[@id='listLink']/a/span[@class='hyperSpan']/span[not(contains(@class, 'ownersManualsCount'))]")
makeUrls = []

for make in makes:
    makeUrls.append(make.text.strip())

index = 0
print(makeUrls)
for makeUrl in makeUrls:

    driver.get("https://justgivemethedamnmanual.com/category/" + makeUrls[index]  + "/page/" + str(0) + "/")
    time.sleep(1)

    loop = True
    articleArray = []

    validPages = True
    while validPages:
        articles = driver.find_elements_by_xpath("//a[@class='entry-link']")
        for article in articles:
            articleArray.append(article.get_attribute('href'))

        try:
            nextUrl = driver.find_element_by_xpath('//a[@class="next page-numbers"]').get_attribute('href')
            driver.get(nextUrl)
            time.sleep(1)
        except:
            validPages = False


    for article in articleArray:
        save = False
        driver.get(article)
        time.sleep(1)
        try:
            pdfLink = driver.find_element_by_xpath("//li[@class='post-attachment mime-application-pdf']/a").get_attribute("href")
            save = True
        except:
            try:
                pdfLink = driver.find_element_by_xpath("//li[@class='post-attachment mime-application-pdf']/a").get_attribute("href")
                save = True
            except:
                print(nextUrl)
        
        if save == True:
            pdfRes = requests.get(pdfLink)
            with open('downloads/' + pdfLink.split("/")[4] + ".pdf", 'wb') as pdf:
                pdf.write(pdfRes.content)

    index += 1