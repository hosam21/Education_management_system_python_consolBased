from User import User
class TeachingAssistant(User):
    def __init__(self, user_id, username, password, email,role, courses=[]):
        super().__init__(user_id, username, password, email)
        self.courses = courses

