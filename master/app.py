from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time,os

import numpy as np


city = os.environ['CITY_NAME']
province_code = os.environ['PROVINCE_CODE']
no_chunk=int(os.environ['CHUNK_NO'])


chrome_options = Options()
chrome_options.add_argument('--headless') 
chrome_options.add_argument('--no-sandbox') 
chrome_options.add_argument('--disable-dev-shm-usage') 


selenium_server_url = "http://selenium_chromium_container:4444/wd/hub"
driver = webdriver.Remote(
    command_executor=selenium_server_url,
    options=chrome_options  # Use options instead of desired_capabilities
)


def _helper_scrap(response):
    """
    This function takes paresed html and returns array of job ids
    """
    soup = BeautifulSoup(response, 'html.parser')
    all_jobs_div=soup.find('div',class_='results-jobs')
    arr=[]
    if all_jobs_div:
        job_articles=all_jobs_div.find_all('article')
        n=len(job_articles)
        if n<=25:
            for job in job_articles:
                arr.append(job['id'].split("-")[1])
        elif n>25:
            for i in reversed(range(n-25,n)):
                job=job_articles[i]
                arr.append(job['id'].split("-")[1])

    return arr



def press_button_multiple_times(url, delay):
    """
    this function returns list [] of jobId scrapped jonbank.ca

    Args:
        job_id (int): it must be correct as per records on jobbank.ca

    Returns:
        {dictionary of features}
        
    Raises:
        ValueError
    """
    s=set()
    try:
        driver.get(url)
    except ValueError as e:
        print(e,"given url is not valid")
    
    updated_html=None
    cnt=1

    while True:
        try:
            button = driver.find_element(By.ID, "moreresultbutton")
            updated_html=driver.page_source
            a=_helper_scrap(updated_html)

            for i in a:
                s.add(i)
            print(cnt*25,"job ids scapped")
            cnt+=1
            
            #pressing of button
            driver.execute_script("arguments[0].click();", button) 
            time.sleep(delay)

        except:
            updated_html=driver.page_source
            a=_helper_scrap(updated_html)
            for i in a:
                s.add(i)
            break


    return list(s)




    
    

if __name__ == "__main__":
    delay=3.0


    url=f"https://www.jobbank.gc.ca/jobsearch/jobsearch?searchstring=&locationstring={city}%2C+{province_code}"

    
    arr_job_ids=press_button_multiple_times(url, delay=delay)

    splits = np.array_split(arr_job_ids, no_chunk)

    for i, split in enumerate(splits):
        np.save(f"/data/job_id_split_{i}.npy", split)
        
    print("Split Job Id array saved into disk")