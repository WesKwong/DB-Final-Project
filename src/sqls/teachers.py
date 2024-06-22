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
    def insert():
        sql = """
        INSERT INTO `Teachers` (`TeacherID`, `Name`, `Gender`, `Title`)
        VALUES (%s, %s, %s, %s);
        """
        return sql

    @staticmethod
    def delete():
        sql = """
        DELETE FROM `Teachers`
        WHERE `TeacherID` = %s;
        """
        return sql

    @staticmethod
    def update():
        sql = """
        UPDATE `Teachers`
        SET
        `Name` = %s,
        `Gender` = %s,
        `Title` = %s
        WHERE `TeacherID` = %s;
        """
        return sql

    @staticmethod
    def query():
        sql = """
        SELECT * FROM `Teachers`
        WHERE `TeacherID` LIKE %s AND `Name` LIKE %s;
        """
        return sql


class TeachersFunc(BaseFunc):

    def __init__(self, genner, handler) -> None:
        super().__init__(genner, handler)

    def insert(self, id: str, name: str, gender: int, title: int):
        if id == "":
            raise gr.Error("工号不能为空!")
        if name == "":
            raise gr.Error("姓名不能为空!")
        sql = self.genner.insert()
        result = self.handler.execute(sql, (id, name, gender, title))
        if result[0]:
            gr.Info("增加成功!")
        else:
            raise gr.Error("增加失败: " + result[1])

    def delete(self, id: str):
        query_sql = self.genner.query()
        query_result = self.handler.query(query_sql, (id, ))
        if len(query_result[1]) == 0:
            raise gr.Error("删除失败: 未找到该教师!")
        sql = self.genner.delete()
        result = self.handler.execute(sql, (id, ))
        if result[0]:
            gr.Info("删除成功!")
        else:
            raise gr.Error("删除失败: " + result[1])

    def update(self, id: str, name: str, gender: int, title: int):
        query_sql = self.genner.query()
        query_result = self.handler.query(query_sql, (id, ))
        if len(query_result[1]) == 0:
            raise gr.Error("修改失败: 未找到该教师!")
        sql = self.genner.update()
        result = self.handler.execute(sql, (name, gender, title, id))
        if result[0]:
            gr.Info("修改成功!")
        else:
            raise gr.Error("修改失败: " + result[1])

    def query(self, id: str, name: str):
        sql = self.genner.query()
        id = "%" + id + "%"
        name = "%" + name + "%"
        result = self.handler.query(sql, (id, name))
        if result[0]:
            if len(result[1]) == 0:
                gr.Warning("查询失败: 未找到该教师!")
                return []
            else:
                return [[
                    row[0], row[1], gender_map[row[2] - 1][0],
                    title_map[row[3] - 1][0]
                ] for row in result[1]]
        else:
            raise gr.Error("查询失败: " + result[1])
