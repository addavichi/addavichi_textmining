import requests
import re
from bs4 import BeautifulSoup
from collections import OrderedDict
from itertools import count
import db_Insert

def naver_content_cralwler(url):
    hrd = {'User-Agent':'Mozilla/5.0', 'referer':'http://naver.com'}
    param = { 'where': 'post' }

    try:
        response = requests.get(url, params=param, headers=hrd)
        soup_temp = BeautifulSoup(response.text, 'html.parser')
        area_temp = soup_temp.find(id='screenFrame')
        url2 = area_temp.get("src")
    except:
        try:
            area_temp = soup_temp.find(id='mainFrame')
            url3 = area_temp.get("src")
            url4 = "https://blog.naver.com" + url3
            return url4
        except:
            return ""
    
    try:
        response = requests.get(url2, params=param, headers=hrd)
        soup_temp = BeautifulSoup(response.text, 'html.parser')
        area_temp = soup_temp.find(id='mainFrame')
        url3 = area_temp.get("src")
        url4 = "https://blog.naver.com" + url3
        return url4
    except:
        return ""

    return ""

def naver_content_text_cralwler(url):
    hrd = {'User-Agent':'Mozilla/5.0', 'referer':'http://naver.com'}
    param = { 'where': 'post' }

    try:
        response = requests.get(url, params=param, headers=hrd)
        soup_temp = BeautifulSoup(response.text, 'html.parser')
        area_temp = soup_temp.find_all("div", {"class" : "sect_dsc"})
        
        for tag2 in area_temp:
            text1 = re.sub('&nbsp; | &nbsp;| \n|\t|\r', '', tag2.text)
            text2 = re.sub('\n\n', '', text1)
            text3 = re.sub('<.+?>', '', text2, 0).strip()
            return " ".join(text3.split())
    except:
        return ""

    try:
        area_temp = soup_temp.find_all("div", {"id" : "postViewArea"})
        
        for tag2 in area_temp:
            text1 = re.sub('&nbsp; | &nbsp;| \n|\t|\r', '', tag2.text)
            text2 = re.sub('\n\n', '', text1)
            text3 = re.sub('<.+?>', '', text2, 0).strip()
            return " ".join(text3.split())
    except:
        return ""

    try:
        area_temp = soup_temp.find_all("div", {"class" : "se-main-container"})
        
        for tag2 in area_temp:
            text1 = re.sub('&nbsp; | &nbsp;| \n|\t|\r', '', tag2.text)
            text2 = re.sub('\n\n', '', text1)
            text3 = re.sub('<.+?>', '', text2, 0).strip()
            return " ".join(text3.split())
    except:
        return ""

    return ""

def naver_cralwler(conn, input_search): #사용자로부터 max_page 받아오기
    url = 'https://search.naver.com/search.naver'
    hrd = {'User-Agent':'Mozilla/5.0', 'referer':'http://naver.com'}
    post_dict = OrderedDict()

    param = {
        'where': 'post',
        'query': input_search
    }
    response = requests.get(url, params=param, headers=hrd)

    # 뷰티풀소프의 인자값 지정
    soup = BeautifulSoup(response.text, 'html.parser')
    page_num = soup.find_all("span", {"class" : "title_num"})

    # 전체 블로그 수 출력
    try:
        for tag in page_num:
            if tag.text in post_dict:
                return post_dict, 0, 0, 0, 0, 0, 0, 0, 0
            
            num = int(tag.text.split('/')[1][:-1].strip().replace(",", ""))
            if(num <= 1):
                return post_dict, 0, 0, 0, 0, 0, 0, 0, 0
            
            print("블로그 수 : " + tag.text.split('/')[1][:-1])
            print("")
            post_dict[tag.text] = tag.text
    except:
        pass

    title_array = []
    link_array = []
    context_array = []
    date_array = []
    nicname_array = []
    img_array = []
    img_numx = []
    data_array = []

    img_num_array = []
    img_num_check = []

    if num > 1002:
        check = 1001
    else:
        check = num - 1

    cnt = 0
    for x in range(1, check, 10):
        param = {
            'query': input_search,
            'where': 'post',
            'start': x,
        }
        print(param)
        response = requests.get(url, params=param, headers=hrd)
        # 뷰티풀소프의 인자값 지정
        soup = BeautifulSoup(response.text, 'html.parser')

        for y in range(1, 11):
            y_id = "sp_blog_" + str(y)
            page_num = soup.find_all("li", {"id" : y_id})
            
            for z in page_num:
                title = z.find_all("a", {"class" : "sh_blog_title"})
                context_ex = z.find_all("dd", {"class" : "sh_blog_passage"})
                date_ex = z.find_all("dd", {"class" : "txt_inline"})
                nicname = z.find_all("a", {"class" : "txt84"})
                img = z.find_all("img", {"class" : "sh_blog_thumbnail"})
                img_num = z.find_all("span")

                for tag2 in title:
                    title_array.append(tag2.text)
                    link_array.append(tag2['href'])

                for tag2 in context_ex:
                    context_array.append(tag2.text)

                for tag2 in date_ex:
                    date_array.append(tag2.text)

                for tag2 in nicname:
                    if(tag2.text != '블로그 내 검색'):
                        nicname_array.append(tag2.text)

                if(not img):
                    img_array.append("null")

                for tag2 in img:
                    img_array.append(tag2['src'])

                for tag2 in img_num:
                    if(tag2.text.count('장의 이미지 더보기')):
                        if(tag2.text.split('장의 이미지 더보기')[0]):
                            img_num_array.append(tag2.text.split('장의 이미지 더보기')[0])
                            cnt = int(x / 10) * 10 + y
                            img_num_check.append(cnt)
                            
    img_num_check.append(0)
    cnt = 0
    for x in range(len(title_array)):
        print("================================================================")
        print("ID : " + str(x))
        print("제목 : " + title_array[x])
        print("링크 : " + link_array[x])
        print("이미지 링크 : " + img_array[x])

        if(x == (img_num_check[cnt] - 1)):
            img_numx.append(img_num_array[cnt])
            cnt = cnt + 1
        else:
            img_numx.append(0)

        print("이미지 개수 : " + str(img_numx[x]))
        print("내용(간략) : " + context_array[x])

        final_url = naver_content_cralwler(link_array[x])
        data_context = naver_content_text_cralwler(final_url)
        data_array.append(data_context)

        # if(data_array[x] != ""):
            # print("내용(상세) : " + data_array[x])
        # else:
            # print("내용(상세) : null")

        print("날짜 : " + date_array[x])
        print("닉네임 : " + nicname_array[x])
        print("")
        db_Insert.db_insert(conn, str(x) + input_search, title_array[x], link_array[x], 
            str(img_numx[x]), context_array[x], date_array[x], nicname_array[x], "미판정", "미판정", "미판정")
    
    return num, title_array, link_array, img_array, img_numx, context_array, data_array, date_array, nicname_array