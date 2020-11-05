class Library:
    def __init__(self, book_count, sign_proc, daily_scans):
        self.book_count = book_count
        self.sign_proc = sign_proc
        self.daily_scans = daily_scans
        self.books = []

    def set_books(self, books):
        self.books = books