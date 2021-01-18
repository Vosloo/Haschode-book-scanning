from library import Library


class Storage:
    def __init__(self, file_name, init_sort=True):
        self.file_name = file_name
        self.book_count = None
        self.lib_count = None
        self.no_days = None
        self.book_scores = None
        self.libraries: list[Library] = list()
        self.init_sort = init_sort
        self.read_file()

    def __getitem__(self, key):
        return self.libraries[key]

    def read_file(self):
        with open(self.file_name, "r") as f:
            data = f.readlines()

        self.book_count, self.lib_count, self.no_days = list(
            map(int, data[0].strip().split())
        )
        self.book_scores = list(map(int, data[1].strip().split()))

        if self.init_sort:
            for line in range(2, len(data), 2):
                if not data[line].strip():
                    break

                lib_info = list(map(int, data[line].strip().split()))
                books = sorted(
                    list(map(int, data[line + 1].strip().split())),
                    key=lambda x: self.book_scores[x],
                    reverse=True,
                )
                self.libraries.append(Library(*lib_info, books))
        else:
            for line in range(2, len(data), 2):
                if not data[line].strip():
                    break

                lib_info = list(map(int, data[line].strip().split()))
                books = list(map(int, data[line + 1].strip().split()))
                self.libraries.append(Library(*lib_info, books))