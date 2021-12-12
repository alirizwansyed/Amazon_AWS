
from sqlalchemy.engine import url
from PyQt5.QtCore import pyqtSignal, QUrl
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebEngineWidgets import QWebEnginePage
import pandas as pd
import bs4 as bs

mrp_lst=[]
savings_lst=[]
selling_price_lst=[]
html_length_lst=[]

# with open(r"C:\Users\alis\OneDrive - Dun and Bradstreet\Desktop\Personal-Local\AmazonSearchTerm\files\Step1_4_Output_After_BadKeywords20211210-122229AM_highconvasin_output.csv",'w') as fp:
#     fp.write(""+str("MRP")+","+str("Savings")+","+str("Selling Price")+","+"URL"+","+str("Length of HTML"))

class WebPage(QWebEnginePage):
    htmlReady = pyqtSignal(str, str)

    def __init__(self, verbose=False):
        super().__init__()
        self._verbose = verbose
        self.loadFinished.connect(self.handleLoadFinished)

    def process(self, urls):
        self._urls = iter(urls)
        self.fetchNext()

    def fetchNext(self):
        try:
            url = next(self._urls)
        except StopIteration:
            return False
        else:
            self.load(QUrl(url))
        return True

    def processCurrentPage(self, html):
        self.htmlReady.emit(html, self.url().toString())
        if not self.fetchNext():
            QApplication.instance().quit()

    def handleLoadFinished(self):
        self.toHtml(self.processCurrentPage)

    def javaScriptConsoleMessage(self, *args, **kwargs):
        if self._verbose:
            super().javaScriptConsoleMessage(*args, **kwargs)

def read_input(filename):
    df=pd.read_csv(filename)
    # print(df.columns)
    df['Amazon_url']='https://www.amazon.in/dp/'
    if 'High Conversion ASIN' in list(df.columns):
        df['High Conversion ASIN']=df['Amazon_url']+df['High Conversion ASIN']
        return df
    # df['#1 Conversion Share'] = df['#1 Conversion Share'].apply(lambda x: x.replace('%',''))
    # df['#2 Conversion Share'] = df['#2 Conversion Share'].apply(lambda x: x.replace('%',''))
    # df['#3 Conversion Share'] = df['#3 Conversion Share'].apply(lambda x: x.replace('%',''))
    # df['#1 Conversion Share']=pd.to_numeric(df['#1 Conversion Share'], errors='coerce')
    # df['#2 Conversion Share']=pd.to_numeric(df['#2 Conversion Share'], errors='coerce')
    # df['#3 Conversion Share']=pd.to_numeric(df['#3 Conversion Share'], errors='coerce')
    df['High Conversion ASIN'] = df[['#1 Conversion Share','#1 Clicked ASIN','#2 Conversion Share','#2 Clicked ASIN','#3 Conversion Share','#3 Clicked ASIN']].apply(lambda x: get_sublist(*x), axis=1)
    df=df[df['High Conversion ASIN']!="None"]
    df['High Conversion ASIN']=df['Amazon_url']+df['High Conversion ASIN']
    df.to_csv(filename.replace('.csv','_highconvasin.csv'),index=False)
    return df

def get_sublist(conv1,conv_asin1,conv2,conv_asin2,conv3,conv_asin3):
    var1=100
    if conv1>=var1:
        return conv_asin1
    elif conv2>=var1:
        return conv_asin2
    elif conv3>=var1:
        return conv_asin3
    return "None"

def my_html_processor(html, url):
    try:
        print('loaded: [%d chars] %s' % (len(html), url))
        # print(html)
        soup = bs.BeautifulSoup(html, 'html.parser')
        # print(soup)
        mrp_save=([x.text for x in soup.find_all("span",attrs={"class":"a-price a-text-price a-size-base"})])
        # print(mrp_save)
        mrp=float(mrp_save[0][:len(mrp_save[0])//2].replace('₹','').replace(',','').strip())
        savings=float(mrp_save[1][:len(mrp_save[1])//2].replace('₹','').replace(',','').strip())
        print("MRP=",mrp,"Save=",savings,"Selling Price=",mrp-savings)
        # with open(r"C:\Users\alis\OneDrive - Dun and Bradstreet\Desktop\Personal-Local\AmazonSearchTerm\files\Step1_4_Output_After_BadKeywords20211210-122229AM_highconvasin_output.csv",'a') as fp:
        #     fp.write("\n"+str(mrp)+","+str(savings)+","+str(mrp-savings)+","+url+","+str(len(html)))
        mrp_lst.append(mrp)
        savings_lst.append(savings)
        selling_price_lst.append(mrp-savings)
        html_length_lst.append(len(html))
    except:
        # with open(r"C:\Users\alis\OneDrive - Dun and Bradstreet\Desktop\Personal-Local\AmazonSearchTerm\files\Step1_4_Output_After_BadKeywords20211210-122229AM_highconvasin_output.csv",'a') as fp:
        #     fp.write("\n"+"-1,-1,-1"+","+url+","+str(len(html)))
        mrp_lst.append(-1)
        savings_lst.append(-1)
        selling_price_lst.append(-1)
        html_length_lst.append(len(html))
        

import sys
app = QApplication(sys.argv)
webpage = WebPage(verbose=False)
webpage.htmlReady.connect(my_html_processor)

filename=r"C:\Users\alis\OneDrive - Dun and Bradstreet\Desktop\Personal-Local\AmazonSearchTerm\files\Step1_4_Output_After_BadKeywords20211210-122229AM.csv"
df1=read_input(filename)
urls=list(df1['High Conversion ASIN'])
# print(urls)

print('Processing list of urls...')
# webpage.process(urls[0:3])
# df1=df1[0:3]
webpage.process(urls)
app.exec_()
df1['MRP']=mrp_lst
df1['Savings']=savings_lst
df1['Selling Price']=selling_price_lst
df1['Length of HTML']=html_length_lst
df1.to_csv(r"C:\Users\alis\OneDrive - Dun and Bradstreet\Desktop\Personal-Local\AmazonSearchTerm\files\Step1_4_Output_After_BadKeywords20211210-122229AM_highconvasin_output.csv",index=False)
print("Processing Done")
