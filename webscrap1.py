from bs4 import BeautifulSoup
import requests

url = "https://boston.craigslist.org/search/sof"
jobs_number = 0 

while True:
    response = requests.get(url)    #creating response object
    data = response.text            #getting sourse code of page into memory
    #Passing the code to BeautifulSoup
    soup = BeautifulSoup(data,'html.parser')
    tags = soup.find_all('a')
    """for tag in tags:
        print(tag.get())"""         #get all the links(just remove comment)
    titles = soup.find_all("a",{'class':"result-title"})    # "a" is tag which contains the rqd info
    """for title in titles:
        print(title.text)"""    #find all job titles
    addresses = soup.find_all("span",{'class':'result-hood'})
    """for address in addresses:
        print(address.text)"""      #checking for another class
    jobs = soup.find_all("p",{'class':'result-info'})
    for job in jobs:
        title = job.find("a",{'class':'result-title'}).text         #extract each job detail
        location_tag =  job.find("span",{'class':'result-hood'})    #use find as only first occurance of tag is needed
        location = location_tag.text[2:-1] if location_tag else "locaion_tag : N/A "    #slicing is done as there will be brackets in the code
        date = job.find("time",{'class':'result-date'}).text
        link = job.find('a',{'class':'result-title'}).get('href')
        job_response = requests.get(link)
        job_data = job_response.text
        job_soup = BeautifulSoup(job_data,'html.parser')
        job_description = job_soup.find('section',{"id":'postingbody'}).text
        job_attribute_tag = job_soup.find('p',{'class':'attrgroup'})
        job_attribute = job_attribute_tag.text if job_attribute_tag else 'N/A'
        jobs_number+=1
        print('Job Title:',title, '\n Location',location,'\ndate',date,'\nlink',link, '\njob_description',job_description, '\njob_attribute',job_attribute, '\n---')
    url_tag = soup.find('a',{'title':'next page'})
    if url_tag.get('href'):
        url = 'https://boston.craigslist.org' + url_tag.get('href')
        print (url)
    else:
        break
print("Total Jobs:",jobs_number)