import os
import yaml
import requests
from bs4 import BeautifulSoup

# Define the input file containing the list of websites
input_file = 'websites.txt'

# Define the output file for the YAML data
output_file = 'websites.yaml'

# Read the input file and parse the URLs
with open(input_file, 'r') as f:
    urls = [line.strip() for line in f]

# Define a function to extract the title from a web page
def get_title(url):
    try:
        res = requests.get(url)
        soup = BeautifulSoup(res.text, 'html.parser')
        title = soup.title.string.strip() if soup.title else url
        return title
    except Exception as e:
        print("Error fetching title for {}: {}".format(url, e))
        return url

# Define the YAML data structure
data = []

# Loop through the URLs and add them to the data structure
for url in urls:
    title = get_title(url)
    data.append({'url': url, 'title': title})

# Append the YAML data to the output file
if os.path.exists(output_file):
    with open(output_file, 'r') as f:
        existing_data = yaml.safe_load(f) or []
    data = existing_data + data

with open(output_file, 'w') as f:
    yaml.dump(data, f)
