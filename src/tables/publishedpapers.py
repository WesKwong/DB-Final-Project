from .base_table import BaseTable


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

    def insert(self, teacher_id: str, paper_id: int, rank: int,
               is_corresponding_author: bool):
        sql = """
        INSERT INTO `PublishedPapers` (`TeacherID`, `PaperID`, `Rank`,
        `IsCorrespondingAuthor`)
        VALUES (%s, %s, %s, %s)
        """
        self.execute(sql,
                     (teacher_id, paper_id, rank, is_corresponding_author))

    def delete(self, teacher_id: str, paper_id: int):
        sql = """
        DELETE FROM `PublishedPapers`
        WHERE `TeacherID` = %s AND `PaperID` = %s
        """
        self.execute(sql, (teacher_id, paper_id))

    def update(self, teacher_id: str, paper_id: int, rank: int,
               is_corresponding_author: bool):
        sql = """
        UPDATE `PublishedPapers`
        SET
        `Rank` = %s,
        `IsCorrespondingAuthor` = %s
        WHERE `TeacherID` = %s AND `PaperID` = %s
        """
        self.execute(sql,
                     (rank, is_corresponding_author, teacher_id, paper_id))
