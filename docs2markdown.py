import os
import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md
from urllib.parse import urljoin

def scrape_and_convert_to_markdown(starting_url, output_dir):
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Initialize a list to store visited URLs
    visited_urls = set()

    # Initialize the stack with the starting URL
    stack = [starting_url]

    while stack:
        current_url = stack.pop()
        visited_urls.add(current_url)

        response = requests.get(current_url)
        if response.status_code != 200:
            print(f"Failed to fetch {current_url}. Skipping.")
            continue

        soup = BeautifulSoup(response.text, 'html.parser')

        # Convert HTML content to Markdown
        markdown_content = md(str(soup))

        # Derive the relative path for saving the Markdown file
        relative_path = os.path.relpath(current_url, starting_url).replace('/', os.path.sep)
        markdown_file_path = os.path.join(output_dir, relative_path + '.md')

        # Save the Markdown content to a file
        with open(markdown_file_path, 'w', encoding='utf-8') as markdown_file:
            markdown_file.write(markdown_content)

        # Find and add links to the stack for further processing
        for link in soup.find_all('a'):
            href = link.get('href')
            if href and href.startswith('http') and href not in visited_urls:
                stack.append(href)

if __name__ == '__main__':
    starting_url = '<API documentation starting URL>'
    output_directory = 'output'

    scrape_and_convert_to_markdown(starting_url, output_directory)
