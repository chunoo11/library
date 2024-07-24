class Book:
    def __init__(self, category, isbn, title, gn, author, publisher, price):
        self.category = category
        self.isbn = isbn
        self.title = title
        self.gn = gn
        self.author = author
        self.publisher = publisher
        self.price = price

    def to_tuple(self):
        return (self.category, self.isbn, self.title, self.gn, self.author, self.publisher, self.price)

    @classmethod
    def from_tuple(cls, data):
        return cls(*data)
