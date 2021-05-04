from cloudbot import hook
from cloudbot.util import formatting
import urllib
import requests
from bs4 import BeautifulSoup

api_url = 'https://www.goodreads.com/search?utf8=%E2%9C%93&query={}'
base_url = 'https://www.goodreads.com{}'


@hook.command("goodreads", "gr", autohelp=False)
def goodreads(text):

    index = 0
    getindex = text.split(',')
    if len(getindex) > 1 and getindex[-1].strip().isdigit():
        index = int(getindex[-1])-1
        title = ' '.join(getindex[:len(getindex)-1])
    else:
        title = text

    r = requests.get(api_url.format(urllib.parse.quote(title,safe='')))
    
    soup = BeautifulSoup(r.text,'html.parser')
    
    books = soup.find_all('tr',{'itemtype':'http://schema.org/Book'})
    
    results = len(books)
    
    if results == 0:
        return 'No results.'
    else:
        try:
            book = books[index];
            book_name = book.find_all('span',{'itemprop':'name'},limit=1)[0].text
            book_url = book.find_all('a',{'class':'bookTitle','itemprop':'url'})[0]['href']
            book_url = base_url.format(book_url)
            shortened = requests.get('https://is.gd/create.php?format=simple&url={}'.format(book_url)).text
            book_author = book.find_all('a',{'class':'authorName'})[0].text
            ratings = book.find_all('span',{'class':'minirating'})[0].text.strip()

            book_link = book.find_all('a', {'class':'bookTitle'})[0]['href'];

            r = requests.get(base_url.format(book_link));
            soup = BeautifulSoup(r.text,'html.parser');
            book_pages = soup.find(itemprop="numberOfPages").text;
            book_format = soup.find(itemprop="bookFormat").text;

            details = soup.find('div', {'id':'details'}).findAll('div',{'class':'row'});
            book_details = '';
            details_list = [];
            for detail in details:
                details_list.append(' '.join(detail.text.split()))
            book_details = '. '.join(details_list);

            return '[{}/{}] {} - by {} ({}) {}, {} {}: {}'.format(index+1,results, book_name, book_author, ratings, book_format, book_pages, book_details, shortened)
        except IndexError:
            return 'No results.'
