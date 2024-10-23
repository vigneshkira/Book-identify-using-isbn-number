import json
import webbrowser
from pyzbar import pyzbar
import cv2
import requests
from bs4 import BeautifulSoup

# Function to scan barcode (ISBN)
def scan_barcode():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open video source.")
        return None

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Failed to grab frame")
            break

        # Decode barcodes in the frame
        barcodes = pyzbar.decode(frame)

        for barcode in barcodes:
            # Extract the ISBN (barcode data)
            isbn_data = barcode.data.decode('utf-8')
            print(f"Scanned ISBN: {isbn_data}")
            return isbn_data  # Return the scanned ISBN

        # Display the frame with camera feed
        cv2.imshow("Barcode Scanner", frame)

        # Press 'q' to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Function to search Google Books and extract book name
def search_google_books(isbn):
    if isbn:
        # Construct the Google Books search URL using the ISBN number
        google_books_url = f"https://www.google.com/search?q={isbn}+site%3Abooks.google.com"

        # Open the URL in the web browser
        webbrowser.open(google_books_url)

        # Fetch the HTML content of the Google search result
        response = requests.get(google_books_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract the book title from the search result (based on observed patterns)
            title_tag = soup.find('h3')  # Find the first <h3> tag, which often contains the book title
            if title_tag:
                book_title = title_tag.get_text()
                print(f"Book Title: {book_title}")
            else:
                book_title = "Unknown Title"
                print("Book title not found in search results.")
        else:
            book_title = "Unknown Title"
            print("Failed to retrieve Google search results.")

        # Prepare the data to save
        book_data = {
            "isbn": isbn,
            "book_title": book_title,
            "google_books_url": google_books_url
        }

        # Save the details to a local JSON file
        with open('books_data.json', 'a') as json_file:
            json.dump(book_data, json_file, indent=4)
            json_file.write(",\n")  # Add a comma to separate entries

        print(f"Book data saved: {book_data}")

    else:
        print("No ISBN scanned.")

# Example workflow
isbn = scan_barcode()  # Step 1: Scan the ISBN
search_google_books(isbn)  # Step 2: Fetch book name, search Google Books, and save data
