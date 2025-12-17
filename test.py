import requests,re,json,os
from bs4 import BeautifulSoup
from urllib.parse import urlparse,unquote,parse_qs,quote_plus
from datetime import datetime
import base64
#################################################
class Color:
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    RESET = '\033[0m'
#########################################################################################################
web_movie = "https://www.123hdtv.com/%e0%b8%94%e0%b8%b9%e0%b8%ab%e0%b8%99%e0%b8%b1%e0%b8%87-netflix"
#################################################
f_path = r"C:\playlist\123-hd\\"
os.makedirs(f_path, exist_ok=True)
#################################################
#################################################
date = datetime.now().strftime("%d")
mo = datetime.now().strftime("%m")
month = ['','มกราคม','กุมภาพันธ์','มีนาคม','เมษายน','พฤษภาคม','มิถุนายน','กรกฎาคม','สิงหาคม','กันยายน','ตุลาคม','พฤศจิกายน','ธันวาคม']
timeday = f'วันที่ {date} {month[int(mo)]} {int(datetime.now().strftime("%Y"))+543}'
#################################################
fname = unquote(urlparse(web_movie).path.strip('/').split('/')[-1])
wname = unquote(urlparse(web_movie).netloc.strip('.').split('.')[-2])
f_w3u = f_w3u1 = wname + "_" +fname+ ".w3u"
f_m3u = f_m3u1 = wname + "_" +fname+ ".m3u"
#################################################
W_W3U = 1       # 1 = เขียน ไฟล์ w3u
W_M3U = 1       # 1 = เขียน ไฟล์ m3u
M_S = 1         # 1 = แยก ไฟล์ Movie กับ Series
#################################################
M_f = 1         #ห้ามแก้
S_f = 1         #ห้ามแก้
#################################################
aseries = """{
    "name": "",
    "author": "By luxdo ",
    "info": "",
    "image": "",
    "key": []}"""
#################################################
headers = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
##### Selenium
# -*- coding: UTF-8 -*-
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

options = webdriver.ChromeOptions()
options.add_argument('--headless')        # Head-less 설정
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(options=options)
#################################################
jmovie = json.loads(aseries)
jmovie['stations'] = jmovie.pop('key')
jseries = json.loads(aseries)
jseries['groups'] = jseries.pop('key')
referer = '{uri.scheme}://{uri.netloc}/'.format(uri=urlparse(web_movie))
refer = re.sub("\/$","",referer)
sess = requests.Session()
sess.headers.update({'User-Agent': headers,'referer': referer})
driver.get(web_movie)
#showscreen(driver)
soup = BeautifulSoup(driver.page_source, 'lxml')
#print(str(soup))
#exit()
page = soup.find("ul", {"class": "page-numbers"})
#print(soup)
if page is not None:
    if page.find_all("a"):
        pmax = page.find_all("a")[-2]['href']
        pmax = unquote(urlparse(pmax).path.strip('/').split('/')[-1])
    else:
        pmax = 1
else:
    pmax = 1
jmovie['name'] = jseries['name'] = soup.find("h3", {"class": "section-title"}).get_text().strip()
jmovie['image'] = jseries['image'] = "https://www.123-hdd.com/wp-content/uploads/2019/10/testa7.png"
jmovie['author'] = jseries['author'] = jseries['author'] + timeday
print(jseries['name'])
#print(pmax)
#exit()
###### แก้สำหรับทดสอบ##
pcurrent = 1
#pmax = 1
###############
pbak = web_movie
for num in range(int(pcurrent), int(pmax)+1):
    if num == 1:
        plink = pbak = web_movie
        #sess.headers.update(headers)
        sess.headers.update({'User-Agent': headers,'referer': referer})
    else:
        plink = "/page/%s" % (num)
        #sess.headers.update(headers)
        sess.headers.update({'User-Agent': headers,'referer': pbak})
        plink = pbak = web_movie + plink
    eprint = "Pages [%s/%s] %s" % (num,pmax,plink)
    print(eprint)
    #home_page = sess.get(plink)
    #soup = BeautifulSoup(home_page.content, "lxml")
    driver.get(plink)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    div = soup.find("div", {"class": "halim_box"})

    try:
        smax = len(div.find_all("div",{"class": "halim-item"}))
    except:
        if smax is not None:
            print("ข้าม")
        continue

    #print("--")
    #exit()
    for i,link in enumerate(div.find_all("div",{"class": "halim-item"}), start=1):
        #print(link)
        purl = link.find("a")['href']
        pname = link.find("a")['title']
        #print(pname)
        try:
            pinfo = link.find("span", {"class": "soundsub"}).get_text().strip() + "(" + link.find("span", {
                "class": "status"}).get_text().strip() + ")"
            #print(pinfo)
        except:
            if pinfo is not None:
                print("ข้าม")
                continue
        ppic = re.sub('/$','',referer) + link.find("img")['data-src']
        eprint = "[Pages : %s/No. : %s/%s] %s" % (num,i,smax,pname)
        print(eprint)
        #จบหน้าหลัก
        #print(pinfo)
        #print(ppic)
        #exit()
        #purl = "https://www.123-hdd.com/x-men-1-%e0%b8%a8%e0%b8%b6%e0%b8%81%e0%b8%a1%e0%b8%99%e0%b8%b8%e0%b8%a9%e0%b8%a2%e0%b9%8c%e0%b8%9e%e0%b8%a5%e0%b8%b1%e0%b8%87%e0%b9%80%e0%b8%ab%e0%b8%99%e0%b8%b7%e0%b8%ad%e0%b9%82%e0%b8%a5%e0%b8%81"
        #print(purl)
        pbak = purl
        home_page = sess.get(purl, allow_redirects=False)
        home_page.encoding = home_page.apparent_encoding
        soup = BeautifulSoup(home_page.content, "lxml")
        #-------แยกประเภท
        if soup.find("table", {"id": "Sequel"}): #Series 1
            table = soup.find("table", {"id": "Sequel"})
            ckfirst = table.find_all("tr")[1]   #, {"style": re.compile("^background-color")}
            if re.search("background-color",str(ckfirst)):
                pass
            else:
                continue
            tbody = table.find("tbody")
            #print("Series 1")
            pagetype = 1
        elif soup.find("select", {"name": "Sequel_select"}): #Series 2
            table = soup.find("select", {"name": "Sequel_select"})
            tbody = table.find_all("option")
            for header in tbody:
                header.name = "a"
                header['href'] = header['value']
                del header['value']
            tbody = BeautifulSoup(str(tbody), "lxml")
            #print("Series 2")
            pagetype = 1
        else: #Movie
            #print("Movie")
            pagetype = 0
        if pagetype == 1:
            epmax = len(table.find_all("a"))
            #jseries['groups'].append({"name":pname,"image":ppic,"groups":[]})
            jseries['groups'].append({"name":pname,"image":ppic,"info":pinfo,"stations":[]})
            for j,eplink in enumerate(tbody.find_all("a"), start=1):
                epname = eplink.get_text().strip()
                purl = eplink['href']
                eprint = f"     [EP name : {j}/{epmax}] {epname}"
                print(eprint)
                home_page = sess.get(purl, allow_redirects=False)
                home_page.encoding = home_page.apparent_encoding
                insoup = BeautifulSoup(home_page.content, "lxml")
                csub = insoup.find_all("th", {"class": re.compile("^lmselect")})
                submax = len(csub)
                if submax > 0:
                    for k,lsub in enumerate(csub, start=1):
                        tsub = lsub.get_text().strip()
                        # if j==1 and k==1:
                            # g1 = len(jseries['groups'])-1
                            # jseries['groups'][g1]['groups'].append({"name":tsub,"image":ppic,"stations":[]})
                        # elif j==1 and k==2:
                            # g1 = len(jseries['groups'])-1
                            # jseries['groups'][g1]['groups'].append({"name":tsub,"image":ppic,"stations":[]})
                        try:
                            inpic = insoup.find("meta", {"property": "og:image"})['content']
                        except:
                            if inpic is not None:
                                print("ข้าม")
                                continue
                        #print(inpic)
                        data_embed = lsub.find("span")['data-embed']
                        data_episode = lsub.find("span")['data-episode']
                        data_post_id = lsub.find("span")['data-post-id']
                        data_server = lsub.find("span")['data-server']
                        data_type = lsub.find("span")['data-type']
                        pnonce = re.search('ajax_player(.+?)"nonce":"(.+?)"',str(insoup)).group(2)
                        data = {'action':'halim_ajax_player','nonce': pnonce,'episode': data_episode,'server': data_server,'postid': data_post_id}
                        #print(data)
                        sess.headers.update({'Content-Type': 'application/x-www-form-urlencoded','referer': pbak})
                        #print(sess.headers)
                        home_page = sess.post("https://www.123hdtv.com/api/get.php", data=data)
                        soup = BeautifulSoup(home_page.content, "lxml")
                        #print(pbak)
                        #print(str(soup))
                        try:
                            elink = soup.find("iframe")['src']
                        except:
                            continue
                        if elink != "https://www.123hdtv.com/api/fileprocess.html":
                            try:
                                cid = parse_qs(urlparse(elink).query)['id'][0]
                            except:
                                if cid is not None:
                                    print("ข้าม")
                                    continue


                            purl = '{uri.scheme}://{uri.netloc}/'.format(uri=urlparse(elink))
                            if re.search('main\.24playerhd\.com',elink):
                                try:
                                    backup = parse_qs(elink)['backup'][0]
                                except:
                                    backup = 0
                                try:
                                    ptype = parse_qs(elink)['ptype'][0]
                                except:
                                    ptype = 0
                                if backup == 1:
                                    elink = purl + 'newplaylist_g/' + cid + '/' + cid + '.m3u8'
                                else:
                                    if ptype == 2:
                                        elink = purl + 'newplaylist/' + cid + '/' + cid + '.m3u8'
                                    else:
                                        elink = purl + 'newplaylist/' + cid + '/' + cid + '.m3u8'
                            if re.search('hot\.24playerhd\.com',elink):
                                try:
                                    ptype = parse_qs(elink)['ptype'][0]
                                except:
                                    ptype = 0
                                if ptype == 2:
                                    elink = purl + 'newplaylist/' + cid + '/' + cid + '.m3u8'
                                else:
                                    elink = purl + 'autoplaylist/' + cid + '/' + cid + '.m3u8'
                                    #elink = purl + 'iosplaylist/' + cid + '/' + cid + '.m3u8'
                                    #https://xxx.77player.xyz/iosplaylist/5fc7a74c21c0ec8660ea10c85a5b2b95/5fc7a74c21c0ec8660ea10c85a5b2b95.m3u8
                        else:
                            continue
                        view_page = sess.get(elink)
                        regex_pattern = re.compile('RESOLUTION=(.+)*\n(.+[-a-zA-Z0-9()@:%_\+.~#?&//=])')
                        result = regex_pattern.findall(str(view_page.text))
                        try:
                            result1 = result[-1]
                            purl2 = result1[-1]
                            purl2 = re.sub(r'^/', '', purl2)
                            elink = purl + purl2
                        except:
                            print("error")
                            #print(elink)
                            #purl2 = result[-1][-1]
                        print("         Playlist : ",elink)
                        g1 = len(jseries['groups'])-1
                        #jseries['groups'][g1]['groups'][k-1]['stations'].append({"name":epname,"info":pinfo,"image":ppic,"url":elink,"referer": referer})
                        jseries['groups'][g1]['stations'].append({"name":epname,"info":tsub,"image":ppic,"url":elink,"referer": ''})
                        if W_W3U:
                            #f_w3u = "Series_"+f_w3u1
                            with open(f_path+f_w3u, 'w',encoding='utf-8') as f:
                                json.dump(jseries, f, indent=2, ensure_ascii=False)
                        if W_M3U:
                            #f_m3u = "Series_"+f_m3u1
                            if S_f:
                                with open(f_path+f_m3u, 'w',encoding='utf-8') as f:
                                    f.write("#EXTM3U\n")
                                    f.close()
                                    S_f = 0
                            with open(f_path+f_m3u, 'a',encoding='utf-8') as f:
                                f.write(f'#EXTINF:-1 tvg-logo="{ppic}" group-title="{pname}" ,{epname}\n')
                                f.write(f'{elink}\n')
                                f.close()
                else:
                    try:
                        data_post_id = insoup.find(class_="halim-btn")['data-post-id']
                    except:
                        continue
                    inpic = insoup.find("meta", {"property": "og:image"})['content']
                    #print(inpic)
                    data_episode = insoup.find(class_="halim-btn")['data-episode']
                    data_server = insoup.find(class_="halim-btn")['data-server']
                    tsub = insoup.find(class_="halim-btn").get_text().strip()
                    pnonce = re.search('ajax_player(.+?)"nonce":"(.+?)"',str(insoup)).group(2)
                    data = {'action':'halim_ajax_player','nonce': pnonce,'episode': data_episode,'server': data_server,'postid': data_post_id}
                    #print(data)
                    sess.headers.update({'Content-Type': 'application/x-www-form-urlencoded','referer': pbak})
                    #print(sess.headers)
                    home_page = sess.post("https://www.123hdtv.com/api/get.php", data=data)
                    soup = BeautifulSoup(home_page.content, "lxml")
                    #print(pbak)
                    #print(str(soup))
                    try:
                        elink = soup.find("iframe")['src']
                    except:
                        continue
                    if elink != "https://www.123hdtv.com/api/fileprocess.html":
                        try:
                            cid = parse_qs(urlparse(elink).query)['id'][0]
                        except:
                            if cid  is not None:
                                print("ข้าม")
                                continue
                        # print(lang_select)
                        purl = '{uri.scheme}://{uri.netloc}/'.format(uri=urlparse(elink))
                        if re.search('main\.24playerhd\.com',elink):
                            try:
                                backup = parse_qs(elink)['backup'][0]
                            except:
                                backup = 0
                            try:
                                ptype = parse_qs(elink)['ptype'][0]
                            except:
                                ptype = 0
                            if backup == 1:
                                elink = purl + 'newplaylist_g/' + cid + '/' + cid + '.m3u8'
                            else:
                                if ptype == 2:
                                    elink = purl + 'newplaylist/' + cid + '/' + cid + '.m3u8'
                                else:
                                    elink = purl + 'newplaylist/' + cid + '/' + cid + '.m3u8'
                        if re.search('main\.abcplays\.com', elink):
                            try:
                                backup = parse_qs(elink)['backup'][0]
                            except:
                                backup = 0
                            try:
                                ptype = parse_qs(elink)['ptype'][0]
                            except:
                                ptype = 0
                            if backup == 1:
                                elink = purl + 'newplaylist_g/' + cid + '/' + cid + '.m3u8'
                            else:
                                if ptype == 2:
                                    elink = purl + 'newplaylist/' + cid + '/' + cid + '.m3u8'
                                else:
                                    elink = purl + 'newplaylist/' + cid + '/' + cid + '.m3u8'
                        if re.search('hot\.24playerhd\.com',elink):
                            try:
                                ptype = parse_qs(elink)['ptype'][0]
                            except:
                                ptype = 0
                            if ptype == 2:
                                elink = purl + 'newplaylist/' + cid + '/' + cid + '.m3u8'
                            else:
                                elink = purl + 'autoplaylist/' + cid + '/' + cid + '.m3u8'
                                #elink = purl + 'iosplaylist/' + cid + '/' + cid + '.m3u8'
                                #https://xxx.77player.xyz/iosplaylist/5fc7a74c21c0ec8660ea10c85a5b2b95/5fc7a74c21c0ec8660ea10c85a5b2b95.m3u8
                    else:
                        continue
                    view_page = sess.get(elink)
                    regex_pattern = re.compile('RESOLUTION=(.+)*\n(.+[-a-zA-Z0-9()@:%_\+.~#?&//=])')
                    result = regex_pattern.findall(str(view_page.text))
                    #print(view_page.text)
                    try:
                        result1 = result[-1]
                        purl2 = result1[-1]
                        purl2 = re.sub(r'^/', '', purl2)
                        elink = purl + purl2
                    except:
                        print("error")
                        #print(elink)
                        #purl2 = result[-1][-1]
                    print("         Playlist : ",elink)
                    #g1 = len(jseries['groups'])-1
                    #jseries['groups'][g1]['groups'][0]['stations'].append({"name":epname,"info":pinfo,"image":ppic,"url":elink,"referer": referer})
                    g1 = len(jseries['groups'])-1
                    jseries['groups'][g1]['stations'].append({"name":epname,"info":tsub,"image":ppic,"url":elink,"referer": ''})
                    if W_W3U:
                        #f_w3u = "Series_"+f_w3u1
                        with open(f_path+f_w3u, 'w',encoding='utf-8') as f:
                            json.dump(jseries, f, indent=2, ensure_ascii=False)
                    if W_M3U:
                        #f_m3u = "Series_"+f_m3u1
                        if S_f:
                            with open(f_path+f_m3u, 'w',encoding='utf-8') as f:
                                f.write("#EXTM3U\n")
                                f.close()
                                S_f = 0
                        with open(f_path+f_m3u, 'a',encoding='utf-8') as f:
                            f.write(f'#EXTINF:-1 tvg-logo="{ppic}" group-title="{pname}" ,{epname}\n')
                            f.write(f'#EXTVLCOPT:{referer}\n')
                            f.write(f'{elink}\n')
                            f.close()
        else:#movie
            insoup = soup
            csub = insoup.find_all("th", {"class": re.compile("^lmselect")})
            submax = len(csub)
            jseries['groups'].append({"name":pname,"image":ppic,"info":pinfo,"stations":[]})
            if submax > 0:
                for j,lsub in enumerate(csub, start=1):
                    inpic = insoup.find("meta", {"property": "og:image"})['content']
                    #print(inpic)
                    tsub = lsub.get_text().strip()
                    data_embed = lsub.find("span")['data-embed']
                    data_episode = lsub.find("span")['data-episode']
                    data_post_id = lsub.find("span")['data-post-id']
                    data_server = lsub.find("span")['data-server']
                    data_type = lsub.find("span")['data-type']
                    pnonce = re.search('ajax_player(.+?)"nonce":"(.+?)"',str(insoup)).group(2)
                    data = {'action':'halim_ajax_player','nonce': pnonce,'episode': data_episode,'server': data_server,'postid': data_post_id}
                    #print(data)
                    sess.headers.update({'Content-Type': 'application/x-www-form-urlencoded','referer': pbak})
                    #print(sess.headers)
                    home_page = sess.post("https://www.123hdtv.com/api/get.php", data=data)
                    soup = BeautifulSoup(home_page.content, "lxml")
                    #print(pbak)
                    #print(str(soup))
                    try:
                        elink = soup.find("iframe")['src']
                    except:
                        continue
                    if elink != "https://www.123hdtv.com/api/fileprocess.html":
                        try:
                            cid = parse_qs(urlparse(elink).query)['id'][0]
                            # print(pinfo)
                        except:
                            if cid is not None:
                                print("ข้าม")
                                continue


                        purl = '{uri.scheme}://{uri.netloc}/'.format(uri=urlparse(elink))
                        if re.search('main\.24playerhd\.com',elink):
                            try:
                                backup = parse_qs(elink)['backup'][0]
                            except:
                                backup = 0
                            try:
                                ptype = parse_qs(elink)['ptype'][0]
                            except:
                                ptype = 0
                            if backup == 1:
                                elink = purl + 'newplaylist_g/' + cid + '/' + cid + '.m3u8'
                            else:
                                if ptype == 2:
                                    elink = purl + 'newplaylist/' + cid + '/' + cid + '.m3u8'
                                else:
                                    elink = purl + 'newplaylist/' + cid + '/' + cid + '.m3u8'
                        if re.search('hot\.24playerhd\.com',elink):
                            try:
                                ptype = parse_qs(elink)['ptype'][0]
                            except:
                                ptype = 0
                            if ptype == 2:
                                elink = purl + 'newplaylist/' + cid + '/' + cid + '.m3u8'
                            else:
                                elink = purl + 'autoplaylist/' + cid + '/' + cid + '.m3u8'
                                #elink = purl + 'iosplaylist/' + cid + '/' + cid + '.m3u8'
                                #https://xxx.77player.xyz/iosplaylist/5fc7a74c21c0ec8660ea10c85a5b2b95/5fc7a74c21c0ec8660ea10c85a5b2b95.m3u8
                    else:
                        continue
                    view_page = sess.get(elink)
                    regex_pattern = re.compile('RESOLUTION=(.+)*\n(.+[-a-zA-Z0-9()@:%_\+.~#?&//=])')
                    result = regex_pattern.findall(str(view_page.text))
                    try:
                        result1 = result[-1]
                        purl2 = result1[-1]
                        purl2 = re.sub(r'^/', '', purl2)
                        elink = purl + purl2
                    except:
                        print("error")
                        #print(elink)
                        #purl2 = result[-1][-1]
                    print("         Playlist : ",elink)
                    g1 = len(jseries['groups'])-1
                    jseries['groups'][g1]['stations'].append({"name":pname,"info":tsub,"image":ppic,"url":elink,"referer": ''})
                    if W_W3U:
                        #f_w3u = "Series_"+f_w3u1
                        with open(f_path+f_w3u, 'w',encoding='utf-8') as f:
                            json.dump(jseries, f, indent=2, ensure_ascii=False)
                    if W_M3U:
                        #f_m3u = "Series_"+f_m3u1
                        if S_f:
                            with open(f_path+f_m3u, 'w',encoding='utf-8') as f:
                                f.write("#EXTM3U\n")
                                f.close()
                                S_f = 0
                        with open(f_path+f_m3u, 'a',encoding='utf-8') as f:
                            f.write(f'#EXTINF:-1 tvg-logo="{ppic}" group-title="" ,{pname}\n')
                            f.write(f'#EXTVLCOPT:{referer}\n')
                            f.write(f'{elink}\n')
                            f.close()
            else:
                try:
                    data_post_id = insoup.find(class_="halim-btn")['data-post-id']
                except:
                    continue
                inpic = insoup.find("meta", {"property": "og:image"})['content']
                #print(inpic)
                data_episode = insoup.find(class_="halim-btn")['data-episode']
                data_server = insoup.find(class_="halim-btn")['data-server']
                tsub = insoup.find(class_="halim-btn").get_text().strip()
                pnonce = re.search('ajax_player(.+?)"nonce":"(.+?)"',str(insoup)).group(2)
                data = {'action':'halim_ajax_player','nonce': pnonce,'episode': data_episode,'server': data_server,'postid': data_post_id}
                #print(data)
                sess.headers.update({'Content-Type': 'application/x-www-form-urlencoded','referer': pbak})
                #print(sess.headers)
                home_page = sess.post("https://www.123hdtv.com/api/get.php", data=data)
                soup = BeautifulSoup(home_page.content, "lxml")
                #print(pbak)
                #print(str(soup))
                try:
                    elink = soup.find("iframe")['src']
                except:
                    continue
                if elink != "https://www.123hdtv.com/api/fileprocess.html":
                    try:
                        cid = parse_qs(urlparse(elink).query)['id'][0]
                    except:
                        if cid is not None:
                            print("ข้าม")
                            continue
                    purl = '{uri.scheme}://{uri.netloc}/'.format(uri=urlparse(elink))
                    if re.search('main\.24playerhd\.com',elink):
                        try:
                            backup = parse_qs(elink)['backup'][0]
                        except:
                            backup = 0
                        try:
                            ptype = parse_qs(elink)['ptype'][0]
                        except:
                            ptype = 0
                        if backup == 1:
                            elink = purl + 'newplaylist_g/' + cid + '/' + cid + '.m3u8'
                        else:
                            if ptype == 2:
                                elink = purl + 'newplaylist/' + cid + '/' + cid + '.m3u8'
                            else:
                                elink = purl + 'newplaylist/' + cid + '/' + cid + '.m3u8'
                    if re.search('hot\.24playerhd\.com',elink):
                        try:
                            ptype = parse_qs(elink)['ptype'][0]
                        except:
                            ptype = 0
                        if ptype == 2:
                            elink = purl + 'newplaylist/' + cid + '/' + cid + '.m3u8'
                        else:
                            elink = purl + 'autoplaylist/' + cid + '/' + cid + '.m3u8'
                            #elink = purl + 'iosplaylist/' + cid + '/' + cid + '.m3u8'
                            #https://xxx.77player.xyz/iosplaylist/5fc7a74c21c0ec8660ea10c85a5b2b95/5fc7a74c21c0ec8660ea10c85a5b2b95.m3u8
                else:
                    continue
                view_page = sess.get(elink)
                regex_pattern = re.compile('RESOLUTION=(.+)*\n(.+[-a-zA-Z0-9()@:%_\+.~#?&//=])')
                result = regex_pattern.findall(str(view_page.text))
                #print(view_page.text)
                try:
                    result1 = result[-1]
                    purl2 = result1[-1]
                    purl2 = re.sub(r'^/', '', purl2)
                    elink = purl + purl2
                except:
                    print("error")
                    # print(elink)
                    # purl2 = result[-1][-1]
                print("         Playlist : ", elink)
                g1 = len(jseries['groups']) - 1
                jseries['groups'][g1]['stations'].append({"name":pname,"info":tsub,"image":ppic,"url":elink,"referer": ''})
                if W_W3U:
                    #f_w3u = "Series_"+f_w3u1
                    with open(f_path+f_w3u, 'w',encoding='utf-8') as f:
                        json.dump(jseries, f, indent=2, ensure_ascii=False)
                if W_M3U:
                    #f_m3u = "Series_"+f_m3u1
                    if S_f:
                        with open(f_path+f_m3u, 'w',encoding='utf-8') as f:
                            f.write("#EXTM3U\n")
                            f.close()
                            S_f = 0
                    with open(f_path+f_m3u, 'a',encoding='utf-8') as f:
                        f.write(f'#EXTINF:-1 tvg-logo="{ppic}" group-title="" ,{pname}\n')
                        f.write(f'#EXTVLCOPT:{referer}\n')
                        f.write(f'{elink}\n')
                        f.close()
print("THE END")
if W_W3U:
    out  = f_path+f_w3u
    re.sub(r' ', '', out)
    out  = "W3u Go to " + out
    print(out)
if W_M3U:
    out  = f_path+f_m3u
    re.sub(r' ', '', out)
    out  = "M3u Go to " + out
    print(out)
