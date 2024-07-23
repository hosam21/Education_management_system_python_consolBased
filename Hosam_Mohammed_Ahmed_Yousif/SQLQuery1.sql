create database education_system
use education_system

CREATE TABLE Users (
  userid INT ,
  username VARCHAR(50) UNIQUE,
  password VARCHAR(255) NOT NULL,
  email VARCHAR(255) UNIQUE,
  role VARCHAR(50)
  PRIMARY KEY(userid)
);
CREATE TABLE Courses (
  course_code VARCHAR(20) UNIQUE,
  course_name VARCHAR(255),
  description TEXT,
  registration_start DATE,
  registration_end DATE,
  unregister_deadline DATE,
  course_id INT PRIMARY KEY ,
 
);
alter table courses 
add
doctor_username VARCHAR(50) FOREIGN KEY REFERENCES Users(username)

CREATE TABLE Courses_Users (
  role VARCHAR(50),  -- Stores the user's role in the course (e.g., "doctor", "teaching_assistant", "student")

);
alter table Courses_Users 
add
PRIMARY KEY (course_id, userid),
course_id INT FOREIGN KEY REFERENCES Courses(course_id),
userid INT FOREIGN KEY REFERENCES Users(userid)

CREATE TABLE Student_Course (
  student_id INT,
  course_code VARCHAR(20) UNIQUE ,
  PRIMARY KEY (student_id, course_code),
  FOREIGN KEY (student_id) REFERENCES Users(userid),
  FOREIGN KEY (course_code) REFERENCES Courses(course_code)
);

CREATE TABLE Assignments (
  assignment_name VARCHAR(255),
  due_date DATE,
  assignment_id INT PRIMARY KEY 

);
alter table Assignments 
add
 course_id INT FOREIGN KEY REFERENCES Courses(course_id)

CREATE TABLE Grades (

  grade FLOAT,
  grade_id INT PRIMARY KEY 

);
alter table Grades 
add
  userid INT FOREIGN KEY REFERENCES Users(userid),
  assignment_id INT FOREIGN KEY REFERENCES Assignments(assignment_id)

INSERT INTO Users (userid,username, password, email, role)
VALUES (1,'john_doe', 'secret123', 'john.doe@example.com', 'student');
INSERT INTO Users (userid,username, password, email, role)
VALUES (2,'hosam', '123', 'hosam123@example.com', 'student');



select *
from  Users