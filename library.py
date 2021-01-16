class Library:
    def __init__(self, book_count, sign_proc, daily_scans):
        self.book_count = book_count
        self.days_to_sign = sign_proc
        self.daily_scans = daily_scans
        self.books = []

    def __repr__(self):
        return f"Library: {self.book_count} {self.sign_proc} {self.daily_scans}"

    def __len__(self):
        return len(self.books)

    def set_books(self, books):
        self.books = books