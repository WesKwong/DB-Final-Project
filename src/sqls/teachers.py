import gradio as gr
from .base_sql_class import BaseTable, BaseFunc


gender_map = [
    ("男", 1),
    ("女", 2)
]

title_map = [
    ("博士后", 1),
    ("助教", 2),
    ("讲师", 3),
    ("副教授", 4),
    ("特任教授", 5),
    ("教授", 6),
    ("助理研究员", 7),
    ("特任副研究员", 8),
    ("副研究员", 9),
    ("特任研究员", 10),
    ("研究员", 11)
]

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

    @staticmethod
    def insert(id: str, name: str, gender: int, title: int):
        sql = """
        INSERT INTO `Teachers` (`TeacherID`, `Name`, `Gender`, `Title`)
        VALUES (%s, %s, %s, %s)
        """
        return sql

    @staticmethod
    def delete(id: str):
        sql = """
        DELETE FROM `Teachers`
        WHERE `TeacherID` = %s
        """
        return sql

    @staticmethod
    def update(id: str, name: str, gender: int, title: int):
        sql = """
        UPDATE `Teachers`
        SET
        `Name` = %s,
        `Gender` = %s,
        `Title` = %s
        WHERE `TeacherID` = %s
        """
        return sql

    @staticmethod
    def query(id: str):
        sql = """
        SELECT * FROM `Teachers`
        WHERE `TeacherID` = %s
        """
        return sql


class TeacherFunc(BaseFunc):

    def __init__(self, genner, handler) -> None:
        super().__init__(genner, handler)

    def insert(self, id: str, name: str, gender: int, title: int):
        if id == "":
            raise gr.Error("工号不能为空！")
        if name == "":
            raise gr.Error("姓名不能为空！")
        sql = self.genner.insert(id, name, gender, title)
        result = self.handler.execute(sql, (id, name, gender, title))
        if result[0]:
            gr.Info("添加成功！")
        else:
            raise gr.Error("添加失败！" + result[1])


    def delete(self, id: str):
        sql = self.genner.delete(id)
        result = self.handler.execute(sql, (id,))
        if result[0]:
            gr.Info("删除成功！")
        else:
            raise gr.Error("删除失败！" + result[1])

    def update(self, id: str, name: str, gender: int, title: int):
        sql = self.genner.update(id, name, gender, title)
        result = self.handler.execute(sql, (name, gender, title, id))
        if result[0]:
            gr.Info("修改成功！")
        else:
            raise gr.Error("修改失败！" + result[1])

    def query(self, id: str):
        sql = self.genner.query(id)
        result = self.handler.query(sql, (id,))
        try:
            id_, name, gender, title = result[1][0]
            return [[id_, name, gender_map[gender-1][0], title_map[title-1][0]]]
        except Exception as e:
            raise gr.Error("查询失败")