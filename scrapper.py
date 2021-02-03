import requests
from bs4 import BeautifulSoup


#URL을 정해놨었는데, URL이 바뀔 수 있도록 get_jobs에 넣어줌
def get_last_page(url):
    result = requests.get(url)
    soup = BeautifulSoup(result.text, "html.parser")
    pages = soup.find("div", {"class": "pagination"}).find_all("a")
    last_page = pages[-2].get_text(strip=True)
    return int(last_page)  #range에 인자로 넣어주기 위해 int로 형변환


def extract_job(html):
    title = html.find("h2", {"class": "job_tit"}).find("a")["title"]
    print(title)
    company = html.find("strong", {"class": "corp_name"}).find("a")["title"]
    location = html.find("div", {
        "class": "job_condition"
    }).find("a").get_text()
    job_id = html["value"]
    return {
        "title":
        title,
        "company":
        company,
        "location":
        location,
        "apply_link":
        f"https://www.saramin.co.kr/zf_user/jobs/relay/view?isMypage=no&rec_idx={job_id}"
    }


# 페이지의 숫자를 추출하고 가장큰 값을 가져옴
def extract_jobs(last_page, url):
    jobs = []
    for page in range(last_page):
        print(f"Scrapping {page+1}")
        result = requests.get(f"{url}&recruitPage={page+1}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("div", {"class": "item_recruit"})
        for result in results:
            job = extract_job(result)
            jobs.append(job)
    return jobs


def get_jobs(word):
    url = f"https://www.saramin.co.kr/zf_user/search/recruit?searchType=search&searchword={word}"
    last_page = get_last_page(url)
    print(last_page)
    jobs = extract_jobs(last_page, url)
    return jobs
