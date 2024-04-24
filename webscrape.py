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
            soup = BeautifulSoup(response.content, "html.parser")
            self.parse_jobs(soup)

    def parse_jobs(self, soup):
        raise NotImplementedError("Subclasses must implement parse_jobs method.")

    def save_to_csv(self, filename):
        fieldnames = ["title", "department", "location", "link",
                      "role_responsibilities", "basic_qualifications",
                      "preferred_qualifications", "extra_info"]
        with open(filename, "w", newline="", encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for job in self.jobs:
                writer.writerow(job)

    def scrape_additional_info(self, link):
        raise NotImplementedError("Subclasses must implement scrape_additional_info method.")


class IQMJobScraper(JobScraper):
    def parse_jobs(self, soup):
        job_cards = soup.find_all("li", class_="border-b border-block-base-text border-opacity-15 last:border-b-0")
        for card in job_cards:
            job = {}
            job["title"] = card.find("span", class_="text-block-base-link company-link-style").get_text().strip()
            department_span = card.find("span", class_="text-base").find("span")
            job["department"] = department_span.get_text().strip() if department_span else "No department"
            location_span = card.find("span", class_="text-base").find_all("span")[-1]
            job["location"] = location_span.get_text().strip() if location_span else "No location"
            link_element = card.find("a", class_="hover:bg-block-base-text hover:bg-opacity-3 flex flex-col py-2 px-4")
            job["link"] = link_element["href"] if link_element else "No link"

            # Get additional info
            additional_info = self.scrape_additional_info(job["link"])
            job.update(additional_info)
            self.jobs.append(job)

    def scrape_additional_info(self, link):
        response = requests.get(link)
        soup = BeautifulSoup(response.content, 'html.parser')
        additional_info = {
            "role_responsibilities": "Information not available",
            "basic_qualifications": "Information not available",
            "preferred_qualifications": "Information not available",
            "extra_info": "Information not available"
        }

        sections = [
            ("role_responsibilities", "Role and Responsibilities"),
            ("basic_qualifications", "Basic Qualifications"),
            ("preferred_qualifications", "Preferred Qualifications"),
            ("extra_info", "Extra Information")
        ]

        for key, section in sections:
            section_heading = soup.find('h3', string=section)
            if section_heading:
                content_text = section_heading.find_next('p').text.strip() if section_heading.find_next(
                    'p') else "Information not available"
                additional_info[key] = content_text

        return additional_info


class XanaduJobScraper(JobScraper):
    def parse_jobs(self, soup):
        job_list = soup.find("ul", class_="list-group")
        job_items = job_list.find_all("li", class_="list-group-item")
        for item in job_items:
            job = {}
            title_element = item.find("h4", class_="list-group-item-heading")
            job["title"] = title_element.get_text().strip()
            location_element = item.find("ul", class_="list-inline").find("li")
            job["location"] = location_element.get_text().strip() if location_element else "No data"
            department_element = item.find_previous("div", class_="department-heading")
            job["department"] = department_element.find("h4").get_text().strip() if department_element else "No data"
            link_element = title_element.find("a")
            job["link"] = link_element["href"] if link_element else "No link"

            # Get additional info
            additional_info = self.scrape_additional_info(job["link"])
            job.update(additional_info)
            self.jobs.append(job)

    def scrape_additional_info(self, link):
        response = requests.get(link)
        soup = BeautifulSoup(response.content, 'html.parser')
        additional_info = {
            "role_responsibilities": "Information not available",
            "basic_qualifications": "Information not available",
            "preferred_qualifications": "Information not available",
            "extra_info": "Information not available"
        }

        sections = [
            ("role_responsibilities", "Role and Responsibilities"),
            ("basic_qualifications", "Basic Qualifications"),
            ("preferred_qualifications", "Preferred Qualifications"),
            ("extra_info", "Extra Information")
        ]

        for key, section in sections:
            section_heading = soup.find('h3', string=section)
            if section_heading:
                content_text = section_heading.find_next('p').text.strip() if section_heading.find_next(
                    'p') else "Information not available"
                additional_info[key] = content_text

        return additional_info


# Example usage:
iqm_scraper = IQMJobScraper("https://iqm.teamtailor.com/jobs")
iqm_scraper.scrape_jobs()
iqm_scraper.save_to_csv("iqm_jobs.csv")

xanadu_scraper = XanaduJobScraper("https://xanadu.applytojob.com/apply/")
xanadu_scraper.scrape_jobs()
xanadu_scraper.save_to_csv("xanadu_jobs.csv")
