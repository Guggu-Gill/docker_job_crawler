import time,re,os,json
from bs4 import BeautifulSoup
from datetime import datetime
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

i=os.environ['CHUNK_ID']

chrome_options = Options()
chrome_options.add_argument('--headless') 
chrome_options.add_argument('--no-sandbox') 
chrome_options.add_argument('--disable-dev-shm-usage') 


selenium_server_url = "http://selenium_chromium_container:4444/wd/hub"
driver = webdriver.Remote(
    command_executor=selenium_server_url,
    options=chrome_options  # Use options instead of desired_capabilities
)

def scarp_jd(id,delay=0.6):
    """
    this function returns dictionary of data scrapped from jobbank.ca

    Args:
        job_id (int): it must be correct as per records on jobbank.ca

    Returns:
        {dictionary of features}
        
    Raises:
        ValueError
    """

    url=f"https://www.jobbank.gc.ca/jobsearch/jobposting/{id}".format(id)
    # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    try:
        driver.get(url)
    except ValueError as e:
        return None

    try:
        button = driver.find_element(By.ID, "applynowbutton")
        button.click()
        time.sleep(delay)
        updated_html=driver.page_source
        soup = BeautifulSoup(updated_html, 'html.parser')
    except:
        return None

    #####################
    date_pattern=r'\b([A-Z][a-z]+ \d{1,2}, \d{4})\b'
    pay_pattern = r'\b(\d+\.\d{2})\s?\$'
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    phone_pattern = r'\(?\b[2-9][0-9]{2}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4}\b'
    url_pattern = r'https?://(?:www\.)?[a-zA-Z0-9-]+\.[a-zA-Z]{2,}(?:/[a-zA-Z0-9._%+-]*)*'

    ##############################
    company_tag=soup.find("p",class_="date-business")
    date_tag=company_tag.find('span',class_='date') if company_tag else None
    date=re.search(date_pattern,date_tag.get_text()).group(0) if date_tag else None
    date=datetime.strptime(date, "%B %d, %Y").date().isoformat()



    company_name_tag=company_tag.find('span',class_='business').find('span',attrs={"property":"name"}) if company_tag else None
    company_name=company_name_tag.get_text().strip() if company_name_tag else None


    ####################
    noc_tag=soup.find("div",class_="job-posting-details-menu").find("div",class_="row col-md-12 job-posting-details-jmi-wrapper info-wrapper")

    noc_title_tag=noc_tag.find('span',class_="noc-title") if noc_tag else None
    noc_title=noc_title_tag.get_text() if noc_tag else None

    noc_no_tag=noc_tag.find('span',class_="noc-no") if noc_tag else None
    noc_no=noc_no_tag.get_text()[4:] if noc_no_tag else None

    try:
        median_wage_tag=noc_tag.find('a',id="j_id_2y_3_jx") if noc_tag else None
        median_wage=re.search(pay_pattern,median_wage_tag.get_text()).group(0)[:-2] if median_wage_tag else None
    except:
        median_wage=None


    ############
    list=soup.find("ul",class_="job-posting-brief colcount-lg-2").find('li')

    street_tag=list.find('span',attrs={"property":"streetAddress"}) if list else None
    street=street_tag.get_text() if street_tag else None

    locality_tag=list.find('span',attrs={"property":"addressLocality"}) if list else None
    locality=locality_tag.get_text() if locality_tag else None

    region_tag=list.find('span',attrs={"property":"addressRegion"}) if list else None
    region=region_tag.get_text() if region_tag else None

    postal_tag=list.find('span',attrs={"property":"postalCode"}) if list else None
    postal=postal_tag.get_text() if postal_tag else None



    ##########
    job_div=soup.find('div',id='howtoapply')
 

    email_tag=job_div.find('h4',id='htaemail') if job_div else None
    email=re.search(email_pattern,email_tag.find_next('a').get_text()).group(0) if email_tag else None

    phone_tag=job_div.find('h4',id='htaphone') if job_div else None
    phone=re.search(phone_pattern,phone_tag.find_next('p').get_text()).group(0) if phone_tag else None

    link_tag=job_div.find('h4',id='htaonline') if job_div else None
    link=re.search(url_pattern,link_tag.find_next('p').get_text()).group(0) if link_tag else None

    hta_street_tag=job_div.find('span',class_='block_street') if job_div else None
    hta_street=hta_street_tag.get_text() if hta_street_tag else None

    hta_city_tag=job_div.find('span',class_='block_city') if job_div else None
    hta_city=hta_city_tag.get_text() if hta_city_tag else None

    hta_postalcode_tag=job_div.find('span',class_='block_postalcode') if job_div else None
    hta_postalcode=hta_postalcode_tag.get_text() if hta_postalcode_tag else None

    hta_validity_tag=soup.find('body').find('p',attrs={'property':'validThrough'}) if job_div else None

    hta_validity=hta_validity_tag.get_text().rstrip() if hta_validity_tag else None

    d={}
    d['id']=id
    d['date_published']=date
    d['company_name']=company_name
    d['noc_no']=noc_no
    d['noc_title']=noc_title
    d['median_wage']=median_wage
    d['company_street']=street
    d['company_locality']=locality
    d['company_region']=region 
    d['company_postal_code']=postal
    # d['email_to_apply']=email
    # d['phone_to_apply']=phone
    d['to_apply_street']=hta_street
    d['to_apply_city']=hta_city
    d['to_apply_postal']=hta_postalcode
    d['to_apply_link']=link
    d['last_date']=hta_validity
    return d


if __name__ == "__main__":
    arr_job_id=np.load(f"/data/job_id_split_{i}.npy")

    arr_output=[]

    os.makedirs('/data/job_description', exist_ok=True)


    for x in arr_job_id:
        jd=scarp_jd(x)
        if jd is not None:
            arr_output.append(jd)

    with open(f'/data/job_description/{i}.json', 'w') as f:
        json.dump(arr_output, f)





    

