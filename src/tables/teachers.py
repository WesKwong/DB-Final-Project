from .base_table import BaseTable


class TeachersTable(BaseTable):
    """
    CREATE TABLE IF NOT EXISTS `Teachers` (
        `TeacherID` VARCHAR(5) NOT NULL,
        `Name` VARCHAR(256) NOT NULL,
        `Gender` INTEGER NOT NULL,
        `Title` INTEGER NOT NULL,
        PRIMARY KEY (`TeacherID`)
    )
    """

    def __init__(self):
        super().__init__()

    def insert(self, id: str, name: str, gender: int, title: int):
        sql = """
        INSERT INTO `Teachers` (`TeacherID`, `Name`, `Gender`, `Title`)
        VALUES (%s, %s, %s, %s)
        """
        self.execute(sql, (id, name, gender, title))

    def delete(self, id: str):
        sql = """
        DELETE FROM `Teachers`
        WHERE `TeacherID` = %s
        """
        self.execute(sql, (id, ))

    def update(self, id: str, name: str, gender: int, title: int):
        sql = """
        UPDATE `Teachers`
        SET
        `Name` = %s,
        `Gender` = %s,
        `Title` = %s
        WHERE `TeacherID` = %s
        """
        self.execute(sql, (id, name, gender, title))

    def query(self, id: str):
        sql = """
        SELECT * FROM `Teachers`
        WHERE `TeacherID` = %s
        """
        return self.fetch(sql, (id, ))
