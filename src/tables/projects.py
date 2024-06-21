from .base_table import BaseTable


class ProjectsTable(BaseTable):
    """
    CREATE TABLE IF NOT EXISTS `Projects` (
        `ProjectID` VARCHAR(256) NOT NULL,
        `ProjectName` VARCHAR(256) NOT NULL,
        `ProjectSource` VARCHAR(256) NOT NULL,
        `ProjectType` INTEGER NOT NULL,
        `TotalFunds` FLOAT NOT NULL,
        `StartDate` INTEGER NOT NULL,
        `EndDate` INTEGER NOT NULL,
        PRIMARY KEY (`ProjectID`)
    )
    """

    def __init__(self):
        super().__init__()

    def insert(self, id: str, name: str, source: str, project_type: int,
               total_funds: float, start_date: int, end_date: int):
        sql = """
        INSERT INTO `Projects` (`ProjectID`, `ProjectName`, `ProjectSource`,
        `ProjectType`, `TotalFunds`, `StartDate`, `EndDate`)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        self.execute(sql, (id, name, source, project_type, total_funds,
                           start_date, end_date))

    def delete(self, id: str):
        sql = """
        DELETE FROM `Projects`
        WHERE `ProjectID` = %s
        """
        self.execute(sql, (id, ))

    def update(self, id: str, name: str, source: str, project_type: int,
               total_funds: float, start_date: int, end_date: int):
        sql = """
        UPDATE `Projects`
        SET
        `ProjectName` = %s,
        `ProjectSource` = %s,
        `ProjectType` = %s,
        `TotalFunds` = %s,
        `StartDate` = %s,
        `EndDate` = %s
        WHERE `ProjectID` = %s
        """
        self.execute(sql, (name, source, project_type, total_funds, start_date,
                           end_date, id))

    def query(self, id: str):
        sql = """
        SELECT * FROM `Projects`
        WHERE `ProjectID` = %s
        """
        return self.fetch(sql, (id, ))
