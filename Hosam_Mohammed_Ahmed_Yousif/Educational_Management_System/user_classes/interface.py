from User import User 
from Courses import Course
import sys
import os
from os import path
from Doctor import Doctor
from AdminUser import AdminUser
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from education_db.connect import get_connection
import re
def login():
    username = input("Username: ")
    password = input("Password: ")
    try:
        conn = get_connection()
        if conn:
            cursor = conn.cursor()

            cursor.execute("SELECT userid, username,password,email,role FROM Users WHERE username = ?", (username,))
            user_data = cursor.fetchone()
            if user_data:
                user_id, username,hashed_password,email,role = user_data
                if hashed_password==password:
                    if role == "student":
                      user = User(user_id,username,hashed_password,email,role)
                      return user
                    elif role == "doctor":
                      user = Doctor(user_id,username,hashed_password,email.role)
                      return user
                    elif role == "admin":
                      user = admin_user(user_id,username,hashed_password,email.role)
                      return user
                    else:
                      print(f"Invalid user role: {role}")
                      return None
                else:
                    print("Invalid username or password.")
                    return None
            else:
                print("User not found.")
                return None
        else:
            print("Failed to connect to database.")
            return None
    except Exception as e:
        print(f"Error logging in: {e}")
        return None

def signup():
  username = input("Username: ")
  password = input("Password: ")
  password2 = input("Confirm password: ")
  email=input("email: ")
  email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-]{2,}$"
  if not bool(re.match(email_regex, email)):
    raise ValueError("Invalid email address")
  
  role = input("Role (student, doctor, admin): ")
  user_id=input("user_id : ")
  try:
    conn = get_connection()
    if conn:
      cursor = conn.cursor()
      cursor.execute("SELECT username FROM Users WHERE userid = ?", (user_id,))
      user_data = cursor.fetchone()
      if user_data:
        print("Username already exists.")
        return None
      elif password != password2:
          print("Passwords do not match.")
          return None
      else:
          hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
          cursor.execute("INSERT INTO Users VALUES (?, ?, ?,?,?)", (user_id, username,password,email,role))
          conn.commit()
          if role == "student":
            if hasattr(Student, 'get_all_courses'):  # Check if it's a static method
                courses = Student.get_all_courses()
            else:
              courses = get_all_courses()  # Assuming get_all_courses is a separate function
              user = Student(user_id, username, password, email, courses)  # Pass courses as argument (optional)
    # ... other role checks ...
          elif role=='doctor':
                user = Doctor(user_id,username,password,email.role)
          elif role == "admin":
                user = admin_user(user_id,username,password,email.role)
          else:
                print(f"Invalid user role: {role}")
                return None
          return user 
  except Exception as err:
    conn.rollback()  
  finally:
    conn.close()  

  
def main():
    """Prompts user for login/signup or exit."""
    while True:
        print("\nWelcome to the Education System!")
        print("1. Login")
        print("2. Sign Up")
        print("3. Exit")

        choice = input("Enter your choice (1-3): ")
        if choice == '1':
            user = login()
            if user:
                
                menu = main_menu(user)  
                menu.run()  
                break  
            else:
                print("Login failed.")
        elif choice == '2':
            new_user = signup()
            if new_user:
                print(f"User '{new_user.username}' created successfully.")
                break
            else:
                print("Error creating user.")
                break
        elif choice == '3':
            print("Exiting the system.")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")
def main_menu(user):
    """Presents menu options based on user role and returns the appropriate menu class."""
    try:
      conn = get_connection()
      if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT role FROM Users WHERE userid = ?", (user_id,))
        user_data = cursor.fetchone()
    except Exception as err:
      conn.rollback()  
    finally:
      conn.close() 
    if isinstance(user, User):
        print("\nStudent Menu:")
        print("1. Register for Course")
        print("2. Unregister from Course")
        print("3. View Registered Courses")
        print("4. View Assignments and Grades")
        print("5. Submit Assignment")
        return StudentMenu(user)  # Pass the user to the StudentMenu class
    elif isinstance(user, Doctor):
        print("\nDoctor Menu:")
        print("1. Create Course")
        print("2. View Courses")
        print("3. Edit Course")
        return DoctorMenu(user)  # Pass the user to the DoctorMenu class
    elif isinstance(user, AdminUser):
        print("\nAdmin Menu:")
        print("1. Create User")
        print("2. Delete User")
        return AdminMenu(user)  # Pass the user to the AdminMenu class (implementation required)
    else:
        print("Invalid user role.")
        return None  # Handle invalid user role appropriately

class StudentMenu:
    def __init__(self, user):
        self.user = user

    def run(self):
      """Provides options for student functionalities."""
      while True:
          choice = input("Enter your choice (1-5) or 'q' to quit: ")
          if choice == 'q':
              break
          elif choice == '1':
              course_name=input("input course name ")
              course_code=input("input course code ")
              start_date=input("input start date ")
              end_date=input("input end date ")
              unregister_deadline=input("input unregister deadline ")
              course=Course(course_name,course_code,start_date,end_date,unregister_deadline)
              self.register_for_course(course)
          elif choice == '2':
              course=input("please enter the course ")
              self.unregister_from_course(course)
          elif choice == '3':
              self.get_all_courses()
          elif choice == '4':

              self.get_assignments_and_grades()
          elif choice == '5':
              assignment=input("please enter the assignment ")
              solution=input("please enter the solution")            
              self.submit_assignment(assignment,solution)
          else:
              print("Invalid choice.")
class DoctorMenu:
    def __init__(self, user):
        self.user = user

    def run(self):
        """Provides options for doctor functionalities."""
        while True:
            choice = input("Enter your choice (1-3) or 'q' to quit: ")
            if choice == 'q':
                break
            elif choice == '1':
                course_name=input("please enter the course name")
                course_code=input("pleas enter the course code ")
                start_date=input("enter the start data")
                end_date=input("enter the end date")
                unregister_deadline=input("enter unregister deadline")
                self.create_course( course_name, course_code, start_date, end_date, unregister_deadline)
            elif choice == '2':
                self.view_courses()
            elif choice == '3':
                course_code=input("please enter the course code")
                self.edit_course(course_code)
            else:
                print("Invalid choice.")

class AdminMenu:
    def __init__(self, user):
        self.user = user

    def run(self):
        """Provides options for admin functionalities."""
        while True:
            choice = input("Enter your choice (1-2) or 'q' to quit: ")
            if choice == 'q':
                break
            elif choice == '1':
                user_id=input("enter user id ")
                user_name=input("enter user name ")
                password=input("enter the password")
                email=input("enter the email")
                role=input("enter the role")
                self.create_user(user_id, username, password, email,role)
            elif choice == '2':
                user_id=input("enter user id ")
                self.delete_user(self,user_id)
            else:
                print("Invalid choice.")
if __name__ == "__main__":
    main()