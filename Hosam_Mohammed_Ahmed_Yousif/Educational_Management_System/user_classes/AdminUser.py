
from User import User
from RoleMixin import  RoleMixin
class AdminUser(User):
    @RoleMixin.role_check(["admin"])
    def access_admin_panel(self):
        print("Accessing admin panel...")
