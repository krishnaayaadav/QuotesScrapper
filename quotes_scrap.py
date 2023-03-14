import requests, re, os, time
from bs4 import BeautifulSoup

from csvfiles_hanlder import CSVHandlers





class QuotesScrapping:
   
    def __init__(self,targeted_url:str):
        self.url = targeted_url

    def get_soup_data(self,url=None):
        """This method will return beautiful soup object of requested page.
           Which is parsed as lxml ok.
        """

        if url is None:
            url = self.url 

        # user client headers
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'}
        
        # making request and getting response as html page
        try:
            web_page = requests.get(url = url, headers = headers)
        except:
            print('Error: While making request to targeted url')
        else:
            # data parsing using beautifulsoup
            soup     = BeautifulSoup(web_page.content, 'lxml') 
            return soup
        
    def image_downloader(self,filename:str, images_url=None, site=None):
         
         for url in images_url:
                time.sleep(2)
                filename = re.search(r'/([\w_-]+[.](jpg|gif|png))$', url)
                if not filename:
                    print("Regex didn't match with the url: {}".format(url))
                    continue
                with open(filename.group(1), 'wb') as f:
                    if 'http' not in url:
                        # sometimes an image source can be relative 
                        # if it is provide the base url which also happens 
                        # to be the site variable atm. 
                        
                        url = '{}{}'.format(site, url)
                    response = requests.get(url)
                    f.write(response.content)
        
    def quetes_extractor(self, soup=None):

        if soup is None:
            soup = self.get_soup_data()


            all_quotes_div = soup.find_all('div', attrs= {'class':"col-6 col-lg-4 text-center margin-30px-bottom sm-margin-30px-top"})

            
            all_quotes = [] # blank list to store quotes
           
            for i in range(len(all_quotes_div)):
                quote = all_quotes_div[i]
                imgage = quote.find('img')

                # motivatoinal lines
                motivn_lines = imgage['alt'][0:-29]

                # images src
                src          = imgage['src']

                # qt category
                category     = quote.find('h5', class_="value_on_red").find('a').text 

                qt = {
                    'Motivation_lines': motivn_lines,
                    'Images_src':       src,
                    'Quotes_category':  category
                }

                all_quotes.append(qt)
            
            return all_quotes
            


def no_pages_of_quotes(page_no:int):
    
    URL = 'https://www.passiton.com/inspirational-quotes?page=' # target url
    csvfilename = 'motivational_quotes.csv'                     # csv filename
   
    q1 = QuotesScrapping(targeted_url=URL)                # obj creation
    csvobj = CSVHandlers(filename=csvfilename, mode='a')  # obj creation

    keys = ['Motivation_lines', 'Quotes_category', 'Images_src'] # dict keys

    for i in range(1,page_no+1):
        URL += f'{i}' # making  new page url 
        soup  = q1.get_soup_data(url=URL)           # getting soup data 
        all_quotes = q1.quetes_extractor(soup=soup) # extracting data from soup

        initial = False

        if i == 1: # initial here
            initial = True

        # writtingt into csvfile
        csvobj.dict_csv_writer(dict_datas=all_quotes, keys=keys, is_initial=initial)


def scrappe_pages(no_page:int):
    for i in range(1,no_page+1):
            
        URL = 'https://www.passiton.com/inspirational-quotes?page=' # target url
        csvfilename = 'motivational_quotes.csv'                     # csv filename

        URL += f'{i}'
   
        q1 = QuotesScrapping(targeted_url=URL)                # obj creation
        dictdata = q1.quetes_extractor(soup=q1.get_soup_data())
        csvobj = CSVHandlers(filename=csvfilename, mode='a')  # obj creation

        keys = ['Motivation_lines', 'Quotes_category', 'Images_src'] # dict keys

        initial = False
        if i == 1:
            initial = True

        # csv = CSVHandlers(filename=csvfilename, mode='a')
        # csv.dict_csv_writer(keys=keys, dict_datas=dictdata, is_initial=initial)

        print()
        print(dictdata)
        time.sleep(7)

# scrappe_pages(10)


def quote_getter(no_quote:int):

    URL = 'https://www.passiton.com/inspirational-quotes?page=' # target url
    q1 = QuotesScrapping(URL)

    for i in range(1,no_quote+1):
        URL += f'{i}'
        soup = q1.get_soup_data()
        all_quotes = q1.quetes_extractor(soup=soup)
        print( '\n \n', all_quotes ,'\n \n', )
        time.sleep(5)

# quote_getter(1)

# q1 = QuotesScrapping(URL)
# print(q1.quetes_extractor())

for i in range(1, 7):
    URL = f'https://www.passiton.com/inspirational-quotes?page={i}' # target url

    q1 = QuotesScrapping(URL)
    print()
    dictdata = (q1.quetes_extractor())


    if dictdata is not None:
        csvfilename = 'motivational_quotes.csv'                     # csv filename
        keys = ['Motivation_lines', 'Quotes_category', 'Images_src'] # dict keys
        initial =False

        if i == 1:
            initial =True


        csvobj = CSVHandlers(filename=csvfilename, mode='a')
        csvobj.dict_csv_writer(dict_datas=dictdata, keys=keys, is_initial=initial)
    

    print()
    time.sleep(7+i)

