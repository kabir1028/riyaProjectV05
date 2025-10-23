class User:
    def __init__(self, id, email, is_guest=False):
        self.id = id
        self.email = email
        self.is_guest = is_guest
