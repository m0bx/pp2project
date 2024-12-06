import requests
from bs4 import BeautifulSoup


class HtmlScraper:
	def __init__(self):
		pass

	def scrape_html(self, url):
		try:
			response = requests.get(url)
			response.raise_for_status()  # Raise an exception for bad status codes
			soup = BeautifulSoup(response.content, 'html.parser')
			return str(soup)
		except requests.exceptions.RequestException as e:
			print(f"Error fetching URL: {e}")
			return None


# Example usage:
if __name__ == "__main__":
	scraper = HtmlScraper()
	url = "https://cs.wikipedia.org/wiki/Slovensko"  # test url
	html_content = scraper.scrape_html(url)

	if html_content:
		print(html_content)
