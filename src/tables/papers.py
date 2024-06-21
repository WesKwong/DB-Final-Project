from .base_table import BaseTable


class PapersTable(BaseTable):
    """
    CREATE TABLE IF NOT EXISTS `Papers` (
        `PaperID` INTEGER NOT NULL,
        `PaperName` VARCHAR(256) NOT NULL,
        `PublicationSource` VARCHAR(256) NOT NULL,
        `PublicationYear` DATE NOT NULL,
        `Type` INTEGER NOT NULL,
        `Level` INTEGER NOT NULL,
        PRIMARY KEY (`PaperID`)
    )
    """

    def __init__(self):
        super().__init__()

    def insert(self, id: int, name: str, publication_source: str,
               publication_year: str, type: int, level: int):
        sql = """
        INSERT INTO `Papers` (`PaperID`, `PaperName`, `PublicationSource`,
        `PublicationYear`, `Type`, `Level`)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        self.execute(
            sql, (id, name, publication_source, publication_year, type, level))

    def delete(self, id: int):
        sql = """
        DELETE FROM `Papers`
        WHERE `PaperID` = %s
        """
        self.execute(sql, (id, ))

    def update(self, id: int, name: str, publication_source: str,
               publication_year: str, type: int, level: int):
        sql = """
        UPDATE `Papers`
        SET
        `PaperName` = %s,
        `PublicationSource` = %s,
        `PublicationYear` = %s,
        `Type` = %s,
        `Level` = %s
        WHERE `PaperID` = %s
        """
        self.execute(
            sql, (name, publication_source, publication_year, type, level, id))

    def query(self, id: int):
        sql = """
        SELECT * FROM `Papers`
        WHERE `PaperID` = %s
        """
        return self.fetch(sql, (id, ))
