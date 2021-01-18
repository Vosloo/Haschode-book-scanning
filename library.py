class Library:
    def __init__(self, book_count, signup_time, no_books_day, books):
        self.book_count = book_count
        self.signup_time = signup_time
        self.no_books_day = no_books_day
        self.books = books

    def __repr__(self):
        return f"Library: {self.book_count} {self.signup_time} {self.no_books_day}"

    def __len__(self):
        return self.book_count