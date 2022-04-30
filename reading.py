class Reading:
    def __init__(self):
        self.list_url = []
        self.list_region = []

    def read(self, file_name):
        f = open(f"{file_name}.csv", "r", encoding="utf-8")
        f1 = f.readlines()
        for x in f1:
            self.list_url.append(x.strip())
        f.close()

    def read_region(self, file_name):
        f = open(f"{file_name}.csv", "r", encoding="utf-8")
        f1 = f.readlines()
        for x in f1:
            self.list_region.append(x.strip())
        f.close()
