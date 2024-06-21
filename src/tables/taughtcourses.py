from .base_table import BaseTable


class TaughtCoursesTable(BaseTable):
    """
    CREATE TABLE IF NOT EXISTS `TaughtCourses` (
        `TeacherID` VARCHAR(5) NOT NULL,
        `CourseID` VARCHAR(256) NOT NULL,
        `Year` INTEGER NOT NULL,
        `Semester` INTEGER NOT NULL,
        `HoursTaught` INTEGER NOT NULL,
        FOREIGN KEY (`TeacherID`) REFERENCES `Teachers` (`TeacherID`) ON DELETE CASCADE,
        FOREIGN KEY (`CourseID`) REFERENCES `Courses` (`CourseID`) ON DELETE CASCADE,
        PRIMARY KEY (`TeacherID`, `CourseID`, `Year`, `Semester`)
    )
    """

    def __init__(self):
        super().__init__()

    def insert(self, teacher_id: str, course_id: str, year: int, semester: int,
               hours_taught: int):
        sql = """
          INSERT INTO `TaughtCourses` (`TeacherID`, `CourseID`,
          `Year`, `Semester`, `HoursTaught`)
          VALUES (%s, %s, %s, %s, %s)
          """
        self.execute(sql,
                     (teacher_id, course_id, year, semester, hours_taught))

    def delete(self, teacher_id: str, course_id: str, year: int,
               semester: int):
        sql = """
            DELETE FROM `TaughtCourses`
            WHERE `TeacherID` = %s AND `CourseID` = %s AND `Year` = %s
            AND `Semester` = %s
            """
        self.execute(sql, (teacher_id, course_id, year, semester))

    def update(self, teacher_id: str, course_id: str, year: int, semester: int,
               hours_taught: int):
        sql = """
        UPDATE `TaughtCourses`
        SET
        `HoursTaught` = %s
        WHERE `TeacherID` = %s AND `CourseID` = %s AND `Year` = %s
        AND `Semester` = %s
        """
        self.execute(sql,
                     (hours_taught, teacher_id, course_id, year, semester))

    def query(self, teacher_id: str, course_id: str, year: int, semester: int):
        sql = """
        SELECT * FROM `TaughtCourses`
        WHERE `TeacherID` = %s AND `CourseID` = %s AND `Year` = %s
        AND `Semester` = %s
        """
        return self.fetch(sql, (teacher_id, course_id, year, semester))
