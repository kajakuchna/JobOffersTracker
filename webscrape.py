import requests
from bs4 import BeautifulSoup
import csv


def scrape_iqm_jobs(url):
    jobs = []

    # Fetching the webpage content
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        # Finding all job listings
        job_cards = soup.find_all('li', class_='border-b border-block-base-text border-opacity-15 last:border-b-0')

        # Parsing each job listing
        for card in job_cards:
            job = {}
            job['title'] = card.find('span', class_='text-block-base-link company-link-style').get_text().strip()
            job['location'] = card.find('span', class_='location').get_text().strip() if card.find('span',
                                                                                                   class_='location') else "No data"
            department_element = card.find_previous_sibling('div', class_='department-heading')
            job['department'] = department_element.find('h4').get_text().strip() if department_element else "No data"
            link_element = card.find('a', class_='job-listing')
            job['link'] = "https://iqm.teamtailor.com" + link_element['href'] if link_element else "No link"
            jobs.append(job)

    return jobs


def scrape_xanadu_jobs(url):
    jobs = []

    # Fetching the webpage content
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        # Finding all job listings
        job_list = soup.find('ul', class_='list-group')
        job_items = job_list.find_all('li', class_='list-group-item')

        # Parsing each job listing
        for item in job_items:
            job = {}
            title_element = item.find('h4', class_='list-group-item-heading')
            job['title'] = title_element.get_text().strip()
            location_element = item.find('ul', class_='list-inline').find('li')
            job['location'] = location_element.get_text().strip() if location_element else "No data"
            department_element = item.find_previous('div', class_='department-heading')
            job['department'] = department_element.find('h4').get_text().strip() if department_element else "No data"
            link_element = title_element.find('a')
            job['link'] = link_element['href'] if link_element else "No link"
            jobs.append(job)

    return jobs


def save_jobs_to_csv(jobs, filename):
    fieldnames = ['title', 'department', 'location', 'link']

    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for job in jobs:
            writer.writerow(job)


# URL for the IQM job listings page
iqm_url = 'https://iqm.teamtailor.com/jobs'
iqm_jobs = scrape_iqm_jobs(iqm_url)
save_jobs_to_csv(iqm_jobs, 'iqm_jobs.csv')
print("IQM job data has been successfully saved to 'iqm_jobs.csv'.")

# URL for the Xanadu job listings page
xanadu_url = 'https://xanadu.applytojob.com/apply/'
xanadu_jobs = scrape_xanadu_jobs(xanadu_url)
save_jobs_to_csv(xanadu_jobs, 'xanadu_jobs.csv')
print("Xanadu job data has been successfully saved to 'xanadu_jobs.csv'.")
