import json


def load_library(filename):
    """Load library data from a JSON file and return it as a Python data structure."""
    with open(filename, "r") as f:
        return json.load(f)


def save_library(data, filename):
    """Save the library data to a JSON file."""
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)


def find_book(books, search_text):
    """Find a book by its title, author, or ID. Return the book ID or None."""
    if search_text is None:
        return None
    search_text = search_text.strip()
    if search_text in books:
        return search_text
    search_lower = search_text.lower()
    for book_id, book in books.items():
        if (
            book_id.lower() == search_lower
            or book.get("title", "").strip().lower() == search_lower
            or book.get("author", "").strip().lower() == search_lower
        ):
            return book_id
    return None


def display_books(books):
    """Display the list of books in a user-friendly format."""
    print("BOOK CATALOGUE")
    print("-" * 60)
    for book_id, book in books.items():
        status = "AVAILABLE" if book.get("available", False) else "ON LOAN"
        print(f"{book_id} | {book.get('title', '')} | {book.get('category', '')} | {status}")


def display_loans(loans, books):
    """Display the list of current loans in a user-friendly format."""
    print("CURRENT LOANS")
    print("-" * 60)
    for loan in loans:
        book_id = loan.get("book_id")
        borrower = loan.get("borrower", "")
        book = books.get(book_id, {})
        title = book.get("title", "")
        print(f"{book_id} | {title} | Borrower: {borrower}")


def library_statistics(books):
    """Return total, available, and borrowed counts."""
    total = len(books)
    available = sum(1 for b in books.values() if b.get("available", False))
    borrowed = total - available
    return total, available, borrowed


def main():
    """Admin interface: load data, display catalogue, loans, and statistics."""
    data = load_library("library.json")
    books = data.get("books", {})
    loans = data.get("loans", [])
    library_info = data.get("library", {})
    categories = data.get("categories", [])

    print("LIBRARY ADMINISTRATION")
    print("=" * 60)
    print(f"Library: {library_info.get('name', '')}")
    print(f"Branch: {library_info.get('branch', '')}")
    print(f"Year: {library_info.get('year', '')}")
    print(f"Categories: {', '.join(categories)}")
    print()

    display_books(books)
    print()

    display_loans(loans, books)
    print()

    total, available, borrowed = library_statistics(books)
    print("STATISTICS")
    print("-" * 60)
    print(f"Total books: {total}")
    print(f"Available: {available}")
    print(f"Borrowed: {borrowed}")


if __name__ == "__main__":
    main()