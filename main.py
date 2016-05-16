#Ash-Ishh.. <mr.akc@outlook.com>

import requests
from bs4 import BeautifulSoup

print("YIFY-Subs".center(40,'-'))

base_url = "http://www.yifysubtitles.com"
query = input("Enter Query:\n>> ")
url = base_url + "/search?q=" + query

r = requests.get(url)

soup = BeautifulSoup(r.content,"html.parser")

titles = [title.get_text() for title in soup.find_all('span',{'class':'title'})]
links = [link['href'] for link in soup.find_all('a') if 'imdb' in link['href']]
#eg : <span class="title" itemprop="name">Batman: Bad Blood</span>


for num,i in enumerate(titles):
    print("Token : {}".format(num+1))
    print(i,"\n")
    print(".x"*20)
    print("\n")

token = int(input("Enter Token Number :\n>> "))
url = base_url + links[token-1]

r = requests.get(url)
soup = BeautifulSoup(r.content,"html.parser")

selected_link = soup.find_all('a')

for link in selected_link:
    if 'english' in link['href']:        
        sub_req = requests.get(base_url+link['href'])
        soup = BeautifulSoup(sub_req.content)
     
        dwnld_links = [link['href'] for link in soup.find_all('a')]
        for link in dwnld_links:
            if 'zip' in link:     
                name = link.split('/')[-1]
                with open("sdcard/subs/"+name,"wb") as foo:              
                    final_file = requests.get(link)
                    for chunk in final_file.iter_content(chunk_size=1024):
                        if chunk:
                            foo.write(chunk)
                            foo.flush()
                    print(name + " Done!\n")           
       
