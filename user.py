from admin import load_library, save_library, find_book


def books_in_category(books, category):
    """Return book IDs that match the given category (case-insensitive, strip spaces)."""
    if category is None:
        return []
    category_lower = category.strip().lower()
    return [
        book_id for book_id, book in books.items()
        if book.get("category", "").strip().lower() == category_lower
    ]


def search_by_title(books, search_text):
    """Return book IDs whose title contains the search text (case-insensitive)."""
    if search_text is None:
        return []
    search_lower = search_text.strip().lower()
    return [
        book_id for book_id, book in books.items()
        if search_lower in book.get("title", "").lower()
    ]


def borrow_book(books, loans, search_text, borrower):
    """Borrow a book. Returns: BOOK_NOT_FOUND, EMPTY_NAME, NOT_AVAILABLE, or OK."""
    if not borrower or not borrower.strip():
        return "EMPTY_NAME"

    book_id = find_book(books, search_text)
    if book_id is None:
        return "BOOK_NOT_FOUND"

    book = books[book_id]
    if not book.get("available", False):
        return "NOT_AVAILABLE"

    book["available"] = False
    loans.append({"book_id": book_id, "borrower": borrower})
    return "OK"


def return_book(books, loans, book_title, borrower):
    """Return a book. Returns: BOOK_NOT_FOUND, EMPTY_NAME, NOT_ON_LOAN, or OK."""
    if not borrower or not borrower.strip():
        return "EMPTY_NAME"

    book_id = find_book(books, book_title)
    if book_id is None:
        return "BOOK_NOT_FOUND"

    loan_entry = None
    for loan in loans:
        if loan.get("book_id") == book_id:
            loan_entry = loan
            break

    if loan_entry is None:
        return "NOT_ON_LOAN"

    loans.remove(loan_entry)
    books[book_id]["available"] = True
    return "OK"


def main():
    """User interface for the library system."""
    filename = "library.json"
    data = load_library(filename)
    books = data.get("books", {})
    loans = data.get("loans", [])

    print("LIBRARY USER SYSTEM")          # ← 改这里
    print("=" * 60)

    while True:
        print("\n=== LIBRARY USER SYSTEM ===")   # ← 改这里
        print("1. Search by title")
        print("2. Search by category")
        print("3. Borrow a book")
        print("4. Return a book")
        print("5. Exit")
        choice = input("Select an option: ").strip()

        if choice == "1":
            text = input("Enter title (or part): ").strip()
            results = search_by_title(books, text)
            if results:
                for book_id in results:
                    b = books[book_id]
                    print(f"{book_id} | {b['title']} | {b['category']}")
            else:
                print("No books found.")

        elif choice == "2":
            cat = input("Enter category: ").strip()
            results = books_in_category(books, cat)
            if results:
                for book_id in results:
                    b = books[book_id]
                    print(f"{book_id} | {b['title']} | {b['category']}")
            else:
                print("No books found in this category.")

        elif choice == "3":
            text = input("Enter book title/ID: ").strip()
            borrower = input("Enter borrower name: ").strip()
            result = borrow_book(books, loans, text, borrower)
            print(f"Result: {result}")

        elif choice == "4":
            title = input("Enter book title/ID: ").strip()
            borrower = input("Enter borrower name: ").strip()
            result = return_book(books, loans, title, borrower)
            print(f"Result: {result}")

        elif choice == "5":
            save_library(data, filename)
            print("Library data saved. Goodbye!")
            break

        else:
            print("Invalid selection. Please try again.")


if __name__ == "__main__":
    main()