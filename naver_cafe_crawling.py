
import requests
from bs4 import BeautifulSoup
import konlpy
from konlpy.tag import Twitter

def get_total(keyword) :
    url = "https://m.cafe.naver.com/ArticleSearchList.nhn?search.query=%" + keyword +  \
    "&search.menuid=&search.searchBy=1&search.sortBy=date&search.clubid=10258021&search.option=0&search.defaultValue="
    response = requests.get(url)
    dom = BeautifulSoup(response.content, "html.parser")
    return dom.select_one("#ct > div.search_contents > div.search_sort > div.sort_l > span").text

def get_list(keyword, page) : 
    url = "https://m.cafe.naver.com/ArticleSearchListAjax.nhn?search.query=" + keyword + \
    "&search.menuid=&search.searchBy=0&search.sortBy=date&search.clubid=10258021&search.option=0&search.defaultValue=&search.page=" + \
    str(page)
    response = requests.get(url)
    dom = BeautifulSoup(response.content, "html.parser")
    return dom.select("a")


def get_all_texts(keyword) :
    total = get_total(keyword)
    pages = int(total) // 20 + 1
    text_sets = []
    for page in range(1, pages + 1) :
        text = get_list(keyword, page)
        link_ls = get_link(text)
        for link in link_ls :
            all_text = get_text(link)
            all_text = twitter.nouns(all_text)
            text_sets.extend(all_text)
    return text_sets


def get_link(dom): 
    ls = []
    for i in range(0, len(dom)) :
        link = dom[i].get('href')
        if len(link) > 2 and "Comment" not in link and "javascript" not in link :
            link = "http://m.cafe.naver.com"+link
            ls.append(link)
    return ls


def get_text(link):
    headers = {
        "Referer"  : "YOUR IFORMATION",
        "User-Agent" : "YOUR IFORMATION",
    }
    response = requests.get(link, headers = headers)
    dom = BeautifulSoup(response.content, "html.parser")
    text = dom.select_one("#postContent").text
    return text


def get_all_texts(keyword):
    total = get_total(keyword)
    pages = int(total)
    text_sets = []
    for page in range(1, pages + 1) :
        text = get_list(keyword, page)
        link_ls = get_link(text)
        for link in link_ls :
            all_text = get_text(link)
            all_text = twitter.nouns(all_text) 
            text_sets.extend(all_text)
    return text_sets


if __name__ == '__main__':

    input_text = "여행"

    data = get_all_texts(input_text)

    print(data)
