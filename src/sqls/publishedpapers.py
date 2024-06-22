from .base_sql_class import BaseTable


class PublishedPapersTable(BaseTable):
    """
    CREATE TABLE IF NOT EXISTS `PublishedPapers` (
        `TeacherID` VARCHAR(5) NOT NULL,
        `PaperID` INTEGER NOT NULL,
        `Rank` INTEGER NOT NULL,
        `IsCorrespondingAuthor` BOOLEAN NOT NULL,
        FOREIGN KEY (`TeacherID`) REFERENCES `Teachers` (`TeacherID`) ON DELETE CASCADE,
        FOREIGN KEY (`PaperID`) REFERENCES `Papers` (`PaperID`) ON DELETE CASCADE,
        PRIMARY KEY (`TeacherID`, `PaperID`)
    )
    """

    def __init__(self):
        super().__init__()

    @staticmethod
    def insert():
        sql = """
        INSERT INTO `PublishedPapers` (`TeacherID`, `PaperID`, `Rank`,
        `IsCorrespondingAuthor`)
        VALUES (%s, %s, %s, %s);
        """
        return sql

    @staticmethod
    def delete():
        sql = """
        DELETE FROM `PublishedPapers`
        WHERE `TeacherID` = %s AND `PaperID` = %s;
        """
        return sql

    @staticmethod
    def update():
        sql = """
        UPDATE `PublishedPapers`
        SET
        `Rank` = %s,
        `IsCorrespondingAuthor` = %s
        WHERE `TeacherID` = %s AND `PaperID` = %s;
        """
        return sql

    @staticmethod
    def query():
        sql = """
        SELECT * FROM `PublishedPapers`
        WHERE `TeacherID` = %s AND `PaperID` = %s;
        """
        return sql
