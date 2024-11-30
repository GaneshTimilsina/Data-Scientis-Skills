import requests
import logging
import re
from bs4 import BeautifulSoup

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

data_URL = "https://www.seek.com.au/data-scientist-jobs/in-All-Australia"
jobTitle = []
jobCompanyName = []
jobType = []
jobLocation = []
jobSalary = []
jobClassificaton = []
jobKeyInfo = []
    
try:
    read_url = requests.get(data_URL)
    read_url.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
    logging.info("URL is working properly")

    content = read_url.content
    soup = BeautifulSoup(content, 'html.parser')

    #Getting the total jobs available 
    total_jobs = soup.find('div', class_='_1tghpaf0 _1bnjhlpgj _1bnjhlp5b _1bnjhlph3 _1bnjhlphn _6za4j60')
    content = total_jobs.find('span', attrs={'data-automation':"totalJobsCount"})

    # Find all job cards (adjust selector if needed based on Seek's HTML changes)
    job_cards = soup.find_all('article', {'data-automation': 'normalJob'})

    for job_card in job_cards:
        try:
            # Extract job title
            job_title = job_card.find('a', {'data-automation': 'jobTitle'}).text.strip()

            # Extract company
            job_company = job_card.find('a', {'data-automation': 'jobCompany'}).text.strip()

            # Extract job type (Full time, Part time, etc.)
            job_type_element = job_card.find('p') #This might need to be adapted depending on how Seek structures the job type
            job_type = job_type_element.text.strip() if job_type_element else "Not specified"

            # Extract location
            job_location = job_card.find('a', {'data-automation': 'jobLocation'}).text.strip()

            # Extract salary (handle variations in format)
            salary_element = job_card.find('span', {'data-automation': 'jobSalary'})
            job_salary = salary_element.text.strip() if salary_element else "Not specified"

            # Extract classification (Science & Technology, etc.)
            classification_element = job_card.find('a', {'data-automation': 'jobClassification'})
            job_classification = classification_element.text.strip() if classification_element else "Not specified"

            # Extract key information (this might need more specific selectors)
            key_info_elements = job_card.find_all('li')
            key_info = [li.text.strip() for li in key_info_elements]


            # logging.info(f"Job Title: {job_title}")
            # logging.info(f"Company: {job_company}")
            # logging.info(f"Job Type: {job_type}")
            # logging.info(f"Location: {job_location}")
            # logging.info(f"Salary: {job_salary}")
            # logging.info(f"Classification: {job_classification}")
            # logging.info(f"Key Information: {key_info}")
            # logging.info("-" * 20)

            jobTitle.append(job_title)
            jobCompanyName.append(job_company)
            jobType.append(job_type)
            jobLocation.append(job_location)
            jobSalary.append(job_salary)
            jobClassificaton.append(job_classification)
            jobKeyInfo.append(key_info)
        except AttributeError as e:
            logging.error(f"Error processing job card: {e}")
            # Consider adding more sophisticated error handling here
except requests.exceptions.RequestException as e:
    logging.error(f"Error fetching URL: {e}")
except Exception as e:
    logging.exception(f"An unexpected error occurred: {e}")

with open('URL_Data.txt', 'w') as file:
    for i in range(len(jobTitle)):
        file.write(f"Job Title: {jobTitle[i]}")
        file.write(f"\nCompany: {jobCompanyName[i]}")
        file.write(f"\nJob Type: {jobType[i]}")
        file.write(f"\nLocation: {jobLocation[i]}")
        file.write(f"\nSalary: {jobSalary[i]}")
        file.write(f"\nClassification: {jobClassificaton[i]}")
        file.write(f"\nKey Information: {jobKeyInfo[i]}\n")
        file.write("_"*30)
        file.write("\n\n\n")
    file.close()