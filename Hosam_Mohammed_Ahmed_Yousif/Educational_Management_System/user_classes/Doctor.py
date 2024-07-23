from Courses import Course
from RoleMixin import  RoleMixin
import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
from education_db.connect import get_connection
from User import User
class Doctor(User):
    def __init__(self, user_id, username, password, email,role, courses=[]):
        super().__init__(user_id, username, password, email)
        self.courses = courses

    @RoleMixin.role_check("doctor")
    def create_course(self, course_name, course_code, start_date, end_date, unregister_deadline):
        connection = connect.get_connection()
        if not connection:
            raise Exception("Failed to connect to database")

        existing_course = Course.get_course(connection, course_code)
        if existing_course:
            raise ValueError(f"Course code '{course_code}' already exists.")

        if not course_name:
            raise ValueError("Course name cannot be empty.")

        course = Course(course_name, course_code, start_date, end_date, unregister_deadline)
        course.create_course(connection, course)

        connection.close()
        print(f"Course '{course_name}' (code: {course_code}) created successfully!")

    
    @RoleMixin.role_check("doctor")
    def view_courses(self):
        connection = connect.get_connection()
        if not connection:
            raise Exception("Failed to connect to database")

        cursor = connection.cursor()
        try:
            #enter_user_name=input("please enter the user name : ")
            sql = """
                    SELECT c.course_name, c.course_code
                    FROM Courses c
                    INNER JOIN Courses_Users dc ON c.course_code = dc.course_code
                    WHERE dc.user_name =?
                    """
            cursor.execute(sql, (self.username,))
            course_data = cursor.fetchall()

            if not course_data:
                print("You are currently not assigned to any courses.")
                return

            print(f"\nYour Courses:")
            for course_name, course_code in course_data:
                print(f"- {course_name} (code: {course_code})")

        except Exception as err:
            print(f"Error retrieving assigned courses: {err}")
        finally:
            if cursor:
                cursor.close()
            connection.close()

    @RoleMixin.role_check("doctor") 
    def edit_course(self, course_code, new_course_name=None):
        connection = connect.get_connection()
        if not connection:
            raise Exception("Failed to connect to database")

        cursor = connection.cursor()
        try:
            #entered_course_code=input("please enter the course code : ")
            
            sql_check = """
                    SELECT course_code
                    FROM Courses
                    WHERE course_code = ?
                    """
            cursor.execute(sql_check, (course_code,))
            existing_course = cursor.fetchone()

            if not existing_course:
                raise ValueError(f"Course with code '{course_code}' not found.")

          
            if new_course_name:
                sql_update = """
                        UPDATE Courses
                        SET course_name = ?
                        WHERE course_code = ?
                        """
                cursor.execute(sql_update, (new_course_name, course_code))
                connection.commit()
                print(f"Course '{course_code}' name updated to '{new_course_name}'.")
            else:
                print(f"No new course name provided. Course '{course_code}' remains unchanged.")

        except Exception as err:
            print(f"Error editing course: {err}")
            connection.rollback()  
        finally:
            if cursor:
                cursor.close()
            connection.close()

 