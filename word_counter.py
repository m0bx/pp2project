import json
import re
from collections import Counter
from bs4 import BeautifulSoup  # lib used for parsing XML and HTML
from htmlreq import HtmlScraper


class WordCounter:
    def __init__(self, url):
        self.word_counts = None
        self.url = url

    @property
    def scrape_and_count(self):
        try:
            html_content = HtmlScraper().scrape_html(self.url)
            soup = BeautifulSoup(html_content, 'html.parser')
            all_text = ' '.join(soup.stripped_strings)
            words = all_text.split()

            # Remove punctuation using regular expressions
            cleaned_words = [re.sub(r'[^\w\s]', '', word).lower() for word in words]
            # Filter out non-alphanumeric characters and empty strings
            cleaned_words1 = [word.lower() for word in cleaned_words]

            # print(cleaned_words) # for debugging
            self.word_counts = Counter(cleaned_words1)  # using Counter from collections
            # print(self.word_counts) # for debugging
            return self.word_counts

        except Exception as e:
            print(f"Failed to retrieve or process HTML content: {e}")
            return None

    def load_wordcounts(self, filename="word_frequencies.json"):
        try:
            with open(filename, 'r') as f:
                self.word_counts = json.load(f)
            print("Word counts loaded successfully!")
        except Exception as e:
            print(f"Failed to load word counts: {e}")
            self.word_counts = {}

    def save_wordcounts(self, filename="word_frequencies.json"):
        if self.word_counts:
            try:
                # Apply filtering to the word_counts dictionary
                filtered_counts = {
                    word: count for word, count in self.word_counts.items()
                    if word and  # Exclude empty strings
                       not any(c.startswith("\\u") for c in word) and  # Remove unicode
                       not any(char.isdigit() for char in word) and  # Exclude words containing any number
                       len(word) > 1  # Exclude single-letter words
                }

                with open(filename, 'w') as f:
                    json.dump(filtered_counts, f, indent=4)
                print("Word counts saved successfully after filtering!")
            except Exception as e:
                print(f"Failed to save word counts: {e}")
        else:
            print("No word counts to save.")
