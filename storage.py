from library import Library


class Storage:
    def __init__(self, file_name) -> None:
        self.file_name = file_name
        self.book_count = 0
        self.lib_count = 0
        self.days_avail = 0
        self.weights = []

        self.cur_day = 0
        # Library currently_signing
        self.currently_signing = -1
        
        # TODO:
        # signed libraries, cur day, scanned should all be local to a given population...

        self.scanned = []
        self.signed_libs = []
        self.libraries: list[Library] = []
        self.read_input()

    def __getitem__(self, key):
        return self.libraries[key]

    def read_input(self):
        with open(self.file_name, "r") as f:
            # Scanning info
            self.book_count, self.lib_count, self.days_avail = list(
                map(int, f.readline().split())
            )
            self.weights = list(map(int, f.readline().split()))
            # self.scanned = [False] * len(self.weights)

            library_ind = 0
            for line in f:
                if not line.strip():
                    # Empty line
                    break

                # Library info
                self.libraries.append(Library(*list(map(int, line.split()))))

                # Books in library
                self.libraries[library_ind].set_books(
                    list(map(int, f.readline().split()))
                )
                library_ind += 1

    def add_scanned_book(self, book):
        self.scanned.append(book)