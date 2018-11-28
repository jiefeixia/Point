from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd


def crawl(file):
    names = []
    course_id = []
    units = []
    description = []
    learning_outcome = []

    driver = webdriver.Chrome()
    driver.get("https://api.heinz.cmu.edu/courses_api/course_list/")

    course_urls = [url.get_attribute("href") for url in driver.find_elements_by_css_selector(
        "#container-fluid > div > div.col-md-10 > table a")]

    driver.close()

    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options=options)

    for url in course_urls:
        driver.get(url)
        names.append(driver.find_elements_by_css_selector(
            "#container-fluid > div > div.col-md-10 > h1 > p")[0].text)
        course_id.append(driver.find_elements_by_css_selector(
            "#container-fluid > div > div.col-md-10 > h4")[0].text)
        units.append(driver.find_elements_by_css_selector(
            "#container-fluid > div > div.col-md-10 > p")[0].text)
        try:
            description.append(driver.find_elements_by_css_selector(
                "#container-fluid > div > div.col-md-10 > p")[1].text)
        except IndexError:
            description.append(None)
        finally:
            try:
                if driver.find_elements_by_css_selector(
                        "#container-fluid > div > div.col-md-10 > p")[2].find_elements_by_css_selector("span")[0].text \
                        == "Learning Outcomes:":
                    learning_outcome.append(driver.find_elements_by_css_selector(
                        "#container-fluid > div > div.col-md-10 > p")[2].text)
                else:
                    learning_outcome.append(None)
            except IndexError:
                learning_outcome.append(None)
            print("finish", url, len(names), ",", len(learning_outcome))

    driver.get("https://api.heinz.cmu.edu/courses_api/course_detail/90-725")
    driver.find_elements_by_css_selector(
        "#container-fluid > div > div.col-md-10 > p")[2].find_elements_by_css_selector("span")[0].text

    df = pd.DataFrame({"names": names, "course_id": course_id, "units": units, "description": description,
                       "learning_outcome": learning_outcome})
    df.to_csv(file, index=False)
