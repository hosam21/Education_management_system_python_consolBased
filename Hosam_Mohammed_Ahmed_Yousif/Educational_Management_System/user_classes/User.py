# from RoleMixin import RoleMixin
import sys
import os
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
from education_db.connect import get_connection
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
from user_classes.RoleMixin import RoleMixin
class User( RoleMixin):
    def __init__(self, user_id, username, password, email,role):
        self.user_id = user_id
        self.username = username
        self.password = password 
        self.email = email
        self.role = role
    import bcrypt
    import re
    @RoleMixin.role_check("admin")
    def create_user(user_id, username, password, email,role):
        email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-]{2,}$"
        if not bool(re.match(email_regex, email)):
          raise ValueError("Invalid email address")
    
        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password_bytes, salt)
        connection = connect_to_database()  # Get the connection
        if not connection:
            raise Exception("Failed to connect to database")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO users (user_id, username, email, hashed_password, role) VALUES (?, ?, ?, ?, ?)",
                       (user_id, username, email, hashed_password, role))
        connection.commit()
        connection.close()
        print("User created successfully!")
    @RoleMixin.role_check("admin")
    def delete_user(self,user_id):
        connection = connect_to_database()  # Get the connection
        if not connection:
            raise Exception("Failed to connect to database")
        cursor = connection.cursor()
        # Execute the delete query using the user's ID for safety
        cursor.execute("DELETE FROM users WHERE user_id = ?", (self.user_id,))
        connection.commit()
        connection.close()
        print("User deleted successfully!")
    @classmethod
    def get_user_by_username(cls, connection, username):
        cursor = connection.cursor()
        try:
            #entered_user=input("please enter the user name : ")
            sql = """
                SELECT userid, username, password, email, role
                FROM Users
                WHERE username = ?
            """
            cursor.execute(sql, (username,))
            user_data = cursor.fetchone()

            if not user_data:
                return None

            user = User(user_data[0], user_data[1], user_data[2], user_data[3], user_data[4])
            return user

        except Exception as err:
            print(f"Error retrieving user by username: {err}")
            return None
        finally:
            if cursor:
                cursor.close()
    @RoleMixin.role_check("student")
    def register_for_course(self, course):
    
        if not isinstance(course, Course):
            raise ValueError("Invalid course provided. Please provide a Course object.")

        existing_course = Course.get_course(course.course_code)
        if not existing_course:
            raise ValueError(f"Course with code '{course.course_code}' not found.")

        current_date = datetime.date.today() 
        if current_date < existing_course.registration_start or current_date > existing_course.registration_end:
            raise ValueError(f"Registration for '{existing_course.course_name}' (code: {existing_course.course_code}) is closed.")
        else:
            print(f"You have successfully registered for '{existing_course.course_name}' (code: {existing_course.course_code}).")
    @RoleMixin.role_check("student")  # Assuming this restricts access to admins
    def get_all_courses(self):
        connection = connect.get_connection()
        if not connection:
            raise Exception("Failed to connect to database")

        cursor = connection.cursor()
        try:
            sql = "SELECT course_name , course_code FROM Courses"  
            cursor.execute(sql)
            course_data = cursor.fetchall()

            if not course_data:
                print("No courses found in the database.")
                return []

            courses = []  # Initialize an empty list to store courses

            for course_name, course_code in course_data:
                course = {"course_name": course_name, "course_code": course_code}
                courses.append(course)  # Append course dictionary to the list

            return courses  # Return the list of courses

        except Exception as err:
            print(f"Error retrieving courses: {err}")
        finally:
            if cursor:
                cursor.close()
            connection.close()

    @RoleMixin.role_check("student")
    def unregister_from_course(self, course):

        if not isinstance(course, Course):
            raise ValueError("Invalid course provided. Please provide a Course object.")

        existing_course = Course.get_course(course.course_code)
        if not existing_course:
            raise ValueError(f"Course with code '{course.course_code}' not found.")

        current_date = datetime.date.today()  
        if current_date > existing_course.unregister_deadline:
            raise ValueError(f"The deadline to unregister from '{existing_course.course_name}' (code: {existing_course.course_code}) has passed.")

        connection = connect.get_connection()
        if not connection:
            raise Exception("Failed to connect to database")

        try:
            sql = """
                DELETE FROM Courses_Users
                WHERE userid = ? AND course_id = ?
                """
            cursor.execute(sql, (self.username, existing_course.course_code))
            connection.commit()
            print(f"You have successfully unregistered from '{existing_course.course_name}' (code: {existing_course.course_code}).")
        except Exception as err:
            print(f"Error unregistering from course: {err}")
            connection.rollback()  
        finally:
            connection.close()  


    @RoleMixin.role_check("student")
    def view_courses(self):

        registered_courses = Course.get_student_registered_courses(self.username)

        if not registered_courses:
            print("You are currently not registered for any courses.")
            return

        print("\nYour Registered Courses:")
        for course in registered_courses:
            print(f"- '{course.course_name}' (code: {course.course_code})")

    @RoleMixin.role_check("student")
    def get_assignments_and_grades(self, course_code):
        connection = connect.get_connection()
        if not connection:
            raise Exception("Failed to connect to database")

        cursor = connection.cursor()
        try:
            sql = """
                    SELECT a.assignment_name, a.due_date, g.grade
                    FROM Assignments , Grades

                    """
            cursor.execute(sql, (self.username, course_code))
            assignment_data = cursor.fetchall()

            if not assignment_data:
                print(f"No assignments found for course '{course_code}'.")
                return

            print(f"\nAssignments and Grades for Course '{course_code}':")
            for assignment, due_date, grade in assignment_data:
                print(f"- {assignment_name} (due: {due_date}):")
                if grade is not None:
                    print(f"  - Grade: {grade}")
                else:
                    print(f"  - Grade: Not Yet Graded")

        except Exception as err:
            print(f"Error retrieving assignments and grades: {err}")
        finally:
            if cursor:
                cursor.close()
            connection.close()

    @RoleMixin.role_check("student")
    def submit_assignment(self, assignment, solution):
        connection = connect.get_connection()
        if not connection:
            raise Exception("Failed to connect to database")
    
        cursor = connection.cursor()
        try:
            sql_check = """
                    SELECT assignment_id
                    FROM Assignments
                    WHERE assignment_name = ? AND course_id = ?
                    """
            cursor.execute(sql_check, (assignment.name, assignment.course_code))
            existing_assignment = cursor.fetchone()
    
            if not existing_assignment:
                raise ValueError(f"Assignment '{assignment.name}' not found in course '{assignment.course_code}'.")
    
            current_date = datetime.date.today()
            if current_date > assignment.deadline:
                raise ValueError(f"The deadline to submit '{assignment.name}' has passed.")
    
            sql_submit = """
                    INSERT INTO Student_Submissions (assignment_name, due_date, assignment_id, course_id)
                    VALUES (?, ?, ?, ?)
                    """
            cursor.execute(sql_submit, (self.username, existing_assignment[0], solution))
            connection.commit()
            print(f"Assignment '{assignment.name}' submitted successfully!")
    
        except Exception as err:
            print(f"Error submitting assignment: {err}")
            connection.rollback() 
        finally:
            if cursor:
                cursor.close()
            connection.close()
    