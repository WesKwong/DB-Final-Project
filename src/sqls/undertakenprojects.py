from .base_sql_class import BaseTable


class UndertakenProjectsTable(BaseTable):
    """
    CREATE TABLE IF NOT EXISTS `UndertakenProjects` (
        `TeacherID` VARCHAR(5) NOT NULL,
        `ProjectID` VARCHAR(256) NOT NULL,
        `Rank` INTEGER NOT NULL,
        `FundsUndertaken` FLOAT NOT NULL,
        FOREIGN KEY (`TeacherID`) REFERENCES `Teachers` (`TeacherID`) ON DELETE CASCADE,
        FOREIGN KEY (`ProjectID`) REFERENCES `Projects` (`ProjectID`) ON DELETE CASCADE,
        PRIMARY KEY (`TeacherID`, `ProjectID`)
    )
    """

    def __init__(self):
        super().__init__()

    @staticmethod
    def insert():
        sql = """
        INSERT INTO `UndertakenProjects` (`TeacherID`, `ProjectID`, `Rank`,
        `FundsUndertaken`)
        VALUES (%s, %s, %s, %s);
        """
        return sql

    @staticmethod
    def delete():
        sql = """
        DELETE FROM `UndertakenProjects`
        WHERE `TeacherID` = %s AND `ProjectID` = %s;
        """
        return sql

    @staticmethod
    def update():
        sql = """
          UPDATE `UndertakenProjects`
          SET
          `Rank` = %s,
          `FundsUndertaken` = %s
          WHERE `TeacherID` = %s AND `ProjectID` = %s;
          """
        return sql

    @staticmethod
    def query():
        sql = """
        SELECT * FROM `UndertakenProjects`
        WHERE `TeacherID` = %s AND `ProjectID` = %s;
        """
        return sql
