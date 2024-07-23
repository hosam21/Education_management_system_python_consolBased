import sys
import os
from os import path
from RoleMixin import RoleMixin
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
from education_db.connect import get_connection
class Assignment:
    def __init__(self,name, assignment_id, course_id, due_date):
        self.name=name
        self.assignment_id = assignment_id
        self.description = description
        self.course_id = course_id

    @RoleMixin.role_check("doctor")
    def set_assignment(self, name, assignment_id, course_id, due_date):
        connection = get_connection()
        if not connection:
            raise Exception("Failed to connect to database")

        cursor = connection.cursor()
        try:
            #entered_course_code=input("please enter the course code to set the assignment : ")
            # Check if course exists
            sql_check_course = """
                SELECT course_code
                FROM Courses
                WHERE course_code = ?
            """
            cursor.execute(sql_check_course, (course_code,))
            existing_course = cursor.fetchone()

            if not existing_course:
                raise ValueError(f"Course with code '{course_code}' not found.")

            # Create assignment object (assuming you have an Assignment class)
            assignment = Assignment(name, assignment_id, course_id, due_date)

            # Find students enrolled in the course
            sql_get_students = """
                SELECT user_name
                FROM Courses_Users cu
                WHERE cu.course_code = ? AND role='student'
            """
            cursor.execute(sql_get_students, (course_code,))
            student_usernames = [row[0] for row in cursor.fetchall()]

            # Assign the assignment to each student in the course
            for student_username in student_usernames:
                student = Student.get_user_by_username(connection, student_username)
                student.assignments.append(assignment)
                student.update_user(connection)  # Update student data in database

            print(f"Assignment '{title}' created for course '{course_code}'.")

        except Exception as err:
            print(f"Error setting assignment: {err}")
            connection.rollback()  
        finally:
            if cursor:
                cursor.close()
            connection.close()

    @RoleMixin.role_check("doctor")
    def view_assignments(self, course_code):
        connection = get_connection()
        if not connection:
            raise Exception("Failed to connect to database")

        cursor = connection.cursor()
        try:
            entered_course_code=input("please enter the course code to set the assignment : ")
            sql_check_course = """
                SELECT course_code
                FROM Courses
                WHERE course_code = ?
            """
            cursor.execute(sql_check_course, (course_code))
            existing_course = cursor.fetchone()

            if not existing_course:
                raise ValueError(f"Course with code '{course_code}' not found.")

            # Find all assignments for the course
            sql_get_assignments = """
                SELECT a.name, a.assignment_id, a.course_id,a.due_date
                FROM Assignments a
                INNER JOIN Courses_Assignments ca ON a.assignment_id = ca.assignment_id
                WHERE ca.course_code = ?
            """
            cursor.execute(sql_get_assignments, (course_code,))
            assignments = cursor.fetchall()

            if not assignments:
                print(f"No assignments found for course '{course_code}'.")
                return

            print(f"\nAssignments for course '{course_code}':")
        except Exception as err:
            print(f"Error setting assignment: {err}")
            connection.rollback()  # Rollback changes if an error occurs
        finally:
            if cursor:
                cursor.close()
            connection.close()