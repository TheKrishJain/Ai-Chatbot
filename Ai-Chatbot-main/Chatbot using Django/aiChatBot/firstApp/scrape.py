import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

def scrape_state_universities():
    # Set up the WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get('https://hte.rajasthan.gov.in/state-universities')

    # Wait for the page to load
    driver.implicitly_wait(10)

    # Extract university data
    university_data = []
    try:
        # Find the elements containing university information
        universities = driver.find_elements(By.CSS_SELECTOR, 'table tbody tr')

        # Loop through rows in the table
        for row in universities[:10]:  # Get only the first 10 universities
            cols = row.find_elements(By.TAG_NAME, 'td')
            if len(cols) > 1:  # Ensure there are enough columns
                name = cols[0].text.strip()  # Get university name
                link_element = cols[0].find_element(By.TAG_NAME, 'a') if cols[0].find_elements(By.TAG_NAME, 'a') else None
                
                if link_element:
                    link = link_element.get_attribute('href')  # Get link safely
                else:
                    link = None

                # Get the contact number from the second column, if available
                contact = cols[1].text.strip() if len(cols) > 1 else None

                # Add to the data list
                university_data.append({'name': name, 'link': link, 'contact': contact})

    except Exception as e:
        print(f"An error occurred: {e}")

    # Print or save the scraped data
    print(university_data)

    # Save scraped data to JSON file
    with open('state_universities.json', 'w') as json_file:
        json.dump(university_data, json_file, indent=4)

    driver.quit()

if __name__ == "__main__":
    scrape_state_universities()
