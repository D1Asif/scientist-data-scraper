from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import pandas as pd

columns = ["World Rank", "National Rank", "Name", "D-Index", "Citations", "Publications", "Affiliation", "Country", "Image URL"]

def get_row_data(row):
    row_data = row.text.split("\n")

    # Affiliation and country comes in one string. So, splitting it into 2 fields
    country = row_data[3].split(", ")[len(row_data[3].split(", ")) - 1]
    affiliation = row_data[3].replace(f", {country}", "")
    row_data.extend([affiliation, country])
    del row_data[3]
    
    # Retrieving the image url
    img_url = row.find_element(By.CLASS_NAME, "lazyload").get_attribute("src")
    row_data.append(img_url)

    row_data_dict = {columns[index]: item.strip() for index, item in enumerate(row_data)}

    return row_data_dict


def main():
    data = []

    for page in range(1, 21):
        url = f"https://research.com/scientists-rankings/computer-science?page={page}"

        driver = webdriver.Chrome()
        driver.get(url)

        time.sleep(5)
    
        rankingItems = driver.find_element(By.ID, "rankingItems")
        rows = rankingItems.find_elements(By.CLASS_NAME, "scientist-item")

        for i in range(0, len(rows)):
            row_content = get_row_data(rows[i])
            data.append(row_content)

        driver.close()

    print(len(data))

    df = pd.DataFrame(data=data, columns=columns)
    df.to_csv("best_cs_scientist_data.csv", index=False)

    return

if __name__ == "__main__":
    main()