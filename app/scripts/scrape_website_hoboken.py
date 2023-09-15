"""Scripts in this file get the current Hoboken municipal street cleaning rules
as raw data and outputs them as a txt file using BeautifulSoup. We will run this 
periodically (until automated with a job schedule) to make sure rules haven't changed.
Also checks to see if there are any changes in rules."""
import requests
from bs4 import BeautifulSoup
from app.main import BASE_DIR


file1 = BASE_DIR / "data_raw" / "current_hoboken_rules_output.txt"
file2 = BASE_DIR / "data_raw" / "new_hoboken_rules_output.txt"

# Installation of BS4 on PythonAnywhere requires this command:
# sudo apt-get install python3-bs4

def create_hoboken_street_cleaning_schedule_file():
    """Use beautifulsoup to scrape the Hoboken municipal website showing
    their street cleaning schedule. This data should not change often, 
    but in case it does run this script every few months to pull new data.
    Be sure to carefully check new rules against the old ones."""
    url = "https://www.hobokennj.gov/resources/street-cleaning-schedule"

    try:
        response = requests.get(url, timeout=10)  # timeout after 10 seconds

        response.raise_for_status()

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")

    except requests.exceptions.ConnectionError as conn_err:
        print(f"Error connecting: {conn_err}")

    except requests.exceptions.Timeout as timeout_err:
        print(f"Timeout error: {timeout_err}")

    except requests.exceptions.RequestException as err:
        print(f"An error occurred: {err}")
    
    else:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the unique container that contains 'table-content'
        container = soup.find_all('div', class_='table-content')

        # Find the divs that contain the table data needed
        table = []
        for div in container:
            links_in_div = div.find_all('div')
            if links_in_div:
                for link in links_in_div:
                    table.append(link.text)

        # Write contents to txt file
        output_path = BASE_DIR / 'data_raw' / 'new_hoboken_rules_output.txt'
        with open(output_path, 'w', encoding='UTF-8') as f:
            for div in table:
                f.write(div + '\n')


class FileComparator:
    def __init__(self, file1, file2):
        self.file1 = file1
        self.file2 = file2

    def compare_files(self):
        """Compares two text files and reports differences."""
        differences = []

        with open(self.file1, 'r') as f1, open(self.file2, 'r') as f2:
            lines1 = f1.readlines()
            lines2 = f2.readlines()

            for i, (line1, line2) in enumerate(zip(lines1, lines2)):
                if line1 != line2:
                    differences.append(f"Line {i + 1}:\nFile 1: {line1.strip()}\nFile 2: {line2.strip()}")

            for i in range(len(lines1), len(lines2)):
                differences.append(f"Line {i + 1} is present in File 2 but not in File 1: {lines2[i].strip()}")
            for i in range(len(lines2), len(lines1)):
                differences.append(f"Line {i + 1} is present in File 1 but not in File 2: {lines1[i].strip()}")

        return differences

    def report(self):
        diffs = self.compare_files()
        if diffs:
            output = "\nDifferences found:\n"
            for diff in diffs:
                output += ('-' * 40) + "\n" + diff + "\n"
            return output
        else:
            return "The two files are identical."

# create_hoboken_street_cleaning_schedule_file()
print(FileComparator(file1, file2).report())