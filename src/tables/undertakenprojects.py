from .base_table import BaseTable


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

    def insert(self, teacher_id: str, project_id: str, rank: int,
               funds_undertaken: float):
        sql = """
        INSERT INTO `UndertakenProjects` (`TeacherID`, `ProjectID`, `Rank`,
        `FundsUndertaken`)
        VALUES (%s, %s, %s, %s)
        """
        self.execute(sql, (teacher_id, project_id, rank, funds_undertaken))

    def delete(self, teacher_id: str, project_id: str):
        sql = """
        DELETE FROM `UndertakenProjects`
        WHERE `TeacherID` = %s AND `ProjectID` = %s
        """
        self.execute(sql, (teacher_id, project_id))

    def delete_by_teacher_id(self, teacher_id: str):
        sql = """
        DELETE FROM `UndertakenProjects`
        WHERE `TeacherID` = %s
        """
        self.execute(sql, (teacher_id, ))

    def delete_by_project_id(self, project_id: str):
        sql = """
        DELETE FROM `UndertakenProjects`
        WHERE `ProjectID` = %s
        """
        self.execute(sql, (project_id, ))

    def update(self, teacher_id: str, project_id: str, rank: int,
               funds_undertaken: float):
        sql = """
          UPDATE `UndertakenProjects`
          SET
          `Rank` = %s,
          `FundsUndertaken` = %s
          WHERE `TeacherID` = %s AND `ProjectID` = %s
          """
        self.execute(sql, (rank, funds_undertaken, teacher_id, project_id))

    def query(self, teacher_id: str, project_id: str):
        sql = """
        SELECT * FROM `UndertakenProjects`
        WHERE `TeacherID` = %s AND `ProjectID` = %s
        """
        return self.fetch(sql, (teacher_id, project_id))
