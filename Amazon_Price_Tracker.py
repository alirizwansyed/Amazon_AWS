# Amazon product price tracker using Python
  
# importing libraries
import bs4 as bs
import sys
import schedule
import time
import urllib.request
from PyQt5.QtWebEngineWidgets import QWebEnginePage
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QUrl
  
import winsound
frequency = 2500  # Set Frequency To 2500 Hertz
duration = 1000  # Set Duration To 1000 ms == 1 second
  
  
class Page(QWebEnginePage):
  
    def __init__(self, url):
        self.app = QApplication(sys.argv)
        QWebEnginePage.__init__(self)
        self.html = ''
        self.loadFinished.connect(self._on_load_finished)
        self.load(QUrl(url))
        self.app.exec_()
  
    def _on_load_finished(self):
        self.html = self.toHtml(self.Callable)
        print('Load finished')
  
    def Callable(self, html_str):
        self.html = html_str
        self.app.quit()
  
def exact_url(url):
    index = url.find("B0")
    index = index + 10
    current_url = ""
    current_url = url[:index]
    return current_url
      
  
def mainprogram():
    url = "https://www.amazon.in/dp/B08V99QQ47"
    exacturl = exact_url(url) # main url to extract data
    page = Page(exacturl)
    print("I am page")
    # print(page)
    soup = bs.BeautifulSoup(page.html, 'html.parser')
    # print(soup)
    js_test = soup.find('span', id ='priceblock_ourprice')  
    mrp_save=([x.text for x in soup.find_all("span",attrs={"class":"a-price a-text-price a-size-base"})])
    print(mrp_save)
    mrp=mrp_save[0][:len(mrp_save[0])//2]
    savings=mrp_save[1][:len(mrp_save[1])//2]
    print("MRP=",mrp,"Save=",savings)
    # vars=(soup.find_all("span",attrs={"class":"a-price a-text-price a-size-base"}))
    # for var in vars:
    #     print(var.text)
    # print(soup.find(id='corePrice_desktop'))
    # print(soup.find(id='tp-tool-tip-subtotal-price-value').get_text())
    selling_price=soup.find(id='tp-tool-tip-subtotal-price-value').get_text().replace('₹','').strip()
    print(selling_price[:len(selling_price)//2])



    # if js_test is None:
    #     js_test = soup.find('span', id ='priceblock_dealprice')        
    # str = ""
    # for line in js_test.stripped_strings :
    #     str = line
  
    # # convert to integer
    # str = str.replace(", ", "")
    # current_price = int(float(str))
    # your_price = 600
    # if current_price < your_price :
    #     print("Price decreased book now")
    #     winsound.Beep(frequency, duration)
    # else:
    #     print("Price is high please wait for the best deal")
      
# def job():
#     print("Tracking....")    
#     mainprogram()
  
# # main code
# schedule.every(1).minutes.do(job)
  
# while True:
mainprogram()
    # schedule.run_pending()
    # time.sleep(1)