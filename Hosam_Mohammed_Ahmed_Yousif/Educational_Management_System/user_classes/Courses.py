import os
import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
from education_db.connect import get_connection
class Course:
    def __init__(self, course_name, course_code, start_date, end_date, unregister_deadline):
        self.course_name = course_name
        self.course_code = course_code
        self.start_date = start_date
        self.end_date = end_date
        self.unregister_deadline = unregister_deadline

    def create_course(connection, course):
        connection = connect_to_database()
        if not connection:
            raise Exception("Failed to connect to database")
        cursor = connection.cursor()
        try:

            sql = """
                INSERT INTO Courses (course_name, course_code, registration_start, registration_end, unregister_deadline)
                VALUES (?,?,?,?,?)
            """
            cursor.execute(sql, course.to_dict().values())
            connection.commit()
            print("Course created successfully!")
        except Exception as err:
            print(f"Error creating course: {err}")
            connection.rollback()  
        finally:
            cursor.close()  

    @staticmethod
    def get_course(connection, course_code):
        connection = connect_to_database()
        if not connection:
            raise Exception("Failed to connect to database")
        cursor = connection.cursor()
        try:
            #entered_course=input("please enter the course code : ")
            sql = """
                SELECT * FROM Courses
                WHERE course_code = ?
            """
            cursor.execute(sql, (course_code,))
            course_data = cursor.fetchone()
            if course_data:
                return Course.from_dict(course_data)
            else:
                return None
        except Exception as err:
            print(f"Error getting course: {err}")
        finally:
            cursor.close()  