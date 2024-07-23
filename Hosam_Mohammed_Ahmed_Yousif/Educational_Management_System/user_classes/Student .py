from User import User
from Courses import Course
from RoleMixin import  RoleMixin
import sys
class Student(User):
    def __init__(self, user_id, username, password, email,role,courses=[]):
        super().__init__(user_id, username, password, email)
        self.courses = courses

    