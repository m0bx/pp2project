import tkinter as tk
from tkinter import ttk
from word_counter import WordCounter
import threading

class WordCounterGUI:
    def __init__(self):
        self.word_counts = None
        self.root = tk.Tk()
        self.root.title("Word Counter")
        self.root.geometry("400x500")
        self.root.resizable(False, False)

        # URL Entry
        self.url_label = ttk.Label(self.root, text="Enter URL:")
        self.url_label.pack()
        self.url_entry = ttk.Entry(self.root, width=40)
        self.url_entry.pack()

        # Buttons
        self.count_button = ttk.Button(self.root, text="Count Words", command=self.count_words)
        self.count_button.pack()

        self.load_button = ttk.Button(self.root, text="Load Word Counts", command=self.load_word_counts)
        self.load_button.pack()

        # Search Entry and Button
        self.search_label = ttk.Label(self.root, text="Search Word:")
        self.search_label.pack()
        self.search_entry = ttk.Entry(self.root, width=40)
        self.search_entry.pack()

        self.search_button = ttk.Button(self.root, text="Search", command=self.search_words)
        self.search_button.pack()

        # Results Display
        self.result_label = tk.Label(self.root, text="", wraplength=350, justify="left", anchor="nw", bg="white", relief="solid")
        self.result_label.pack(pady=10, fill="both", expand=True)

        self.root.mainloop()

    def count_words(self):
        def worker():
            url = self.url_entry.get()
            counter = WordCounter(url)
            self.word_counts = counter.scrape_and_count  # Perform scraping and word counting
            counter.save_wordcounts()  # Save the results to JSON

            # Update the result label to indicate success (but no results shown yet)
            self.result_label.config(text="Operation successful. Click 'Load Word Counts' to view results.")

        self.result_label.config(text="Processing...")  # Show a loading message
        threading.Thread(target=worker, daemon=True).start()

    def load_word_counts(self):
        try:
            counter = WordCounter("")  # URL isn't needed for loading
            counter.load_wordcounts()
            self.word_counts = counter.word_counts  # Store the loaded counts

            if self.word_counts:
                # Prepare the top 10 most frequent words
                top_words = sorted(self.word_counts.items(), key=lambda x: x[1], reverse=True)[:10]
                top_words_text = "\n".join([f"{word}: {count}" for word, count in top_words])

                self.result_label.config(
                    text="Word counts loaded successfully! You can now use the search.\n\nTop 10 Words:\n" + top_words_text
                )
            else:
                self.result_label.config(text="No word counts available.")
        except Exception as e:
            self.result_label.config(text=f"Error loading word counts: {e}")

    def search_words(self):
        if not self.word_counts:
            self.result_label.config(text="No word counts loaded. Click 'Load Word Counts' first.")
            return

        search_term = self.search_entry.get().lower()
        if search_term:
            # Search for words containing the search term
            matching_words = [
                (word, self.word_counts[word])
                for word in self.word_counts
                if search_term in word.lower()
            ]
            if matching_words:
                result_text = "Matching words:\n"
                for word, count in sorted(matching_words, key=lambda x: x[1], reverse=True)[:10]:  # Show top 10 matches
                    result_text += f"{word}: {count}\n"
            else:
                result_text = "No matching words found."
        else:
            # If no search term, show top 10 most frequent words
            top_words = sorted(self.word_counts.items(), key=lambda x: x[1], reverse=True)[:10]
            result_text = "Top 10 Words:\n"
            for word, count in top_words:
                result_text += f"{word}: {count}\n"

        self.result_label.config(text=result_text)


if __name__ == "__main__":
    WordCounterGUI()

