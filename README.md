# Barcode Book Scanning System (No API Key Required)

This project allows users to scan a book's barcode (ISBN) from an image file, search for the book on Google Books without using an API key, and store the ISBN and book details in a JSON file. The system processes the image using pyzbar to extract the ISBN, then opens the Google Books search in a browser. Additionally, the system can scrape the book title from the search results using web scraping with BeautifulSoup and Requests. The book details (ISBN and title) are saved locally in a book_data.json file. This setup uses Python, OpenCV for image handling, and a local SQLite/JSON database to store transaction records. The process offers an efficient, API-free solution for managing books with minimal manual input.





