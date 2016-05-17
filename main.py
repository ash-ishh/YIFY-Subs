# Ash-Ishh.. <mr.akc@outlook.com>

import requests
from bs4 import BeautifulSoup
from urllib.request import quote
import zipfile
import os


#To Make Directory Of Query
def make_subs_dir(query):
    global subspath
    subspath = "c:\subs\"+query+'\'
    if not os.path.exists(subspath):
        os.makedirs(subspath)


#Search For Query and Return Titles And Links
def search_and_return_result(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content,"html.parser")

    titles = [title.get_text() for title in soup.find_all('span',{'class':'title'})]
    links = [link['href'] for link in soup.find_all('a') if 'imdb' in link['href']]
    #eg : <span class="title" itemprop="name">Batman: Bad Blood</span>
    return titles,links


#Get All Links of Selected Subtitle.
def get_links_of_selected_sub(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content,"html.parser")
    return soup.find_all('a')


#Get Zip File Links Of 'English' Subtitle
def get_zip_links(all_links):
    for each_link in all_links:
        if 'english' in each_link['href']:        
            sub_req = requests.get(base_url+each_link['href'])
            sub_soup = BeautifulSoup(sub_req.content)
     
            dwnld_links = [link['href'] for link in sub_soup.find_all('a')]
            for link in dwnld_links:
                if 'zip' in link:                   
                    yield link         
           
 
#Download Zip Files Of Subtitle.
def dwnld_zip_files(link):
    name = link.split('/')[-1]
    zipfile_path = subspath+name
                
    print(name)
    print("\nDownloading..\n")
                
    with open(zipfile_path,"wb") as foo:              
        final_file = requests.get(link)
        for chunk in final_file.iter_content(chunk_size=1024):
            if chunk:
                foo.write(chunk)
                foo.flush()
    print("Downloaded!\n\n")
    return zipfile_path


#Unzip and Removed Zip File                  
def unzip_file(zipfile_path):
    print("Unzipping File..\n\n")
    try:
        z = zipfile.ZipFile(zipfile_path)
        z.extractall(path=subspath)
        z.close()
        os.remove(zipfile_path)
        print("Unzipped! :)\n\n")
        print('-'*40)                
    except Exception as e:
        print(str(e))
        print("\nFailed To Unzip..\n")
        print("-"*40)
                   



## ## ## ## ## ## ## ## ## ##
def main():
    query = quote(input("Enter Query:\n>> "))
    make_subs_dir(query)
    
    global base_url
    base_url = "http://www.yifysubtitles.com"
    url = base_url + "/search?q=" + query    

    titles,links = search_and_return_result(url)
    
    if len(titles) == 0:
        print("\nSubtitles Not Found!\nTry Again\n\n")
        main()
    else: #Print Available Subs
        print('\n\n')
        for num,i in enumerate(titles):
            print("Token : {}".format(num+1))
            print(i,"\n")
            print(".x"*20)
            print("\n")

    token = int(input("Enter Token Number :\n>> "))
    selected_sub_url = base_url + links[token-1]
    
    all_links = get_links_of_selected_sub(selected_sub_url)
    dwnld_link = get_zip_links(all_links)           
    
    num = int(input("\nHow Many Subs You Want?\n>> "))
    
    for i in range(num):
        try:
            zip_path = dwnld_zip_files(next(dwnld_link))       
            unzip_file(zip_path) 
        except:
            print("No More Available :(")
            break
    action = input("\n* Do you want to Quit? (y/n)\n>> ").lower()
    
    if action == ('n' or 'no'):
        main()
    else:
        exit(0)
if __name__ == '__main__':  
    print("YIFY-Subs".center(40,'-'))    
    main()
