import requests
from bs4 import BeautifulSoup
import csv


class JobScraper:
    def __init__(self, url):
        self.url = url
        self.jobs = []

    def scrape_jobs(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            self.parse_jobs(soup)

    def parse_jobs(self, soup):
        raise NotImplementedError("Subclasses must implement parse_jobs method.")

    def save_to_csv(self, filename):
        fieldnames = ['title', 'department', 'location', 'link']

        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for job in self.jobs:
                writer.writerow(job)


class IQMJobScraper(JobScraper):
    def parse_jobs(self, soup):
        job_cards = soup.find_all('li', class_='border-b border-block-base-text border-opacity-15 last:border-b-0')
        for card in job_cards:
            job = {}
            job['title'] = card.find('span', class_='text-block-base-link company-link-style').get_text().strip()
            job['location'] = card.find('span', class_='location').get_text().strip() if card.find('span', class_='location') else "No data"
            department_element = card.find_previous_sibling('div', class_='department-heading')
            job['department'] = department_element.find('h4').get_text().strip() if department_element else "No data"
            link_element = card.find('a', class_='job-listing')
            job['link'] = "https://iqm.teamtailor.com" + link_element['href'] if link_element else "No link"
            self.jobs.append(job)


class XanaduJobScraper(JobScraper):
    def parse_jobs(self, soup):
        job_list = soup.find('ul', class_='list-group')
        job_items = job_list.find_all('li', class_='list-group-item')
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
            self.jobs.append(job)


# Instantiate and scrape IQM jobs
iqm_scraper = IQMJobScraper('https://iqm.teamtailor.com/jobs')
iqm_scraper.scrape_jobs()
iqm_scraper.save_to_csv('iqm_jobs.csv')
print("IQM job data has been successfully saved to 'iqm_jobs.csv'.")

# Instantiate and scrape Xanadu jobs
xanadu_scraper = XanaduJobScraper('https://xanadu.applytojob.com/apply/')
xanadu_scraper.scrape_jobs()
xanadu_scraper.save_to_csv('xanadu_jobs.csv')
print("Xanadu job data has been successfully saved to 'xanadu_jobs.csv'.")
