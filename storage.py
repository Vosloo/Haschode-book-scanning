from library import Library


class Storage:
    def __init__(self, file_name) -> None:
        self.file_name = file_name
        self.book_count = 0
        self.library_count = 0
        self.days = 0
        self.weights = []
        self.scanned = []
        self.libraries = []
        self.read_input()

    def read_input(self):
        
        with open(self.file_name, "r") as f:
            # Scanning info
            self.book_count, self.library_count, self.days = list(
                map(int, f.readline().split())
            )
            self.weights = list(map(int, f.readline().split()))
            self.scanned = [False] * len(self.weights)

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
