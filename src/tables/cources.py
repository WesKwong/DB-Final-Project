from .base_table import BaseTable


class CourcesTable(BaseTable):
    """
    CREATE TABLE IF NOT EXISTS `Courses` (
        `CourseID` VARCHAR(256) NOT NULL,
        `CourseName` VARCHAR(256) NOT NULL,
        `CreditHours` INTEGER NOT NULL,
        `CourseType` INTEGER NOT NULL,
        PRIMARY KEY (`CourseID`)
    )
    """

    def __init__(self):
        super().__init__()

    def insert(self, id: str, name: str, credit_hours: int, course_type: int):
        sql = """
        INSERT INTO `Courses` (`CourseID`, `CourseName`, `CreditHours`, `CourseType`)
        VALUES (%s, %s, %s, %s)
        """
        self.execute(sql, (id, name, credit_hours, course_type))

    def delete(self, id: str):
        sql = """
        DELETE FROM `Courses`
        WHERE `CourseID` = %s
        """
        self.execute(sql, (id, ))

    def update(self, id: str, name: str, credit_hours: int, course_type: int):
        sql = """
        UPDATE `Courses`
        SET
        `CourseName` = %s,
        `CreditHours` = %s,
        `CourseType` = %s
        WHERE `CourseID` = %s
        """
        self.execute(sql, (id, name, credit_hours, course_type))

    def query(self, id: str):
        sql = """
        SELECT * FROM `Courses`
        WHERE `CourseID` = %s
        """
        return self.fetch(sql, (id, ))
