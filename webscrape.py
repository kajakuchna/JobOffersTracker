import csv

job_offer = {
    'company': 'Company Name',
    'title': 'Job Title',
    'department': 'Department Name',
    'location': 'Location',
    'experience': 'Experience Level',
    'responsibilities': 'Responsibilities',
    'basic_requirements': 'Basic Qualifications and Experience',
    'preferred_requirements': 'Preferred Qualifications and Experience'
}


def save_jobs_to_csv(jobs, filename):
    fieldnames = ['company', 'title', 'department', 'location', 'experience', 'responsibilities', 'basic_requirements',
                  'preferred_requirements']

    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for job in jobs:
            writer.writerow(job)
