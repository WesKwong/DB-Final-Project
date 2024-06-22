import gradio as gr

from .base_sql_class import BaseTable, BaseFunc

course_type_map = [
    ("本科生课程", 1),
    ("研究生课程", 2)
]


class CoursesTable(BaseTable):
    """
    CREATE TABLE IF NOT EXISTS `Courses` (
        `CourseID` VARCHAR(256) NOT NULL,
        `CourseName` VARCHAR(256) NOT NULL,
        `CreditHours` INTEGER NOT NULL,
        `CourseType` INTEGER NOT NULL,
        PRIMARY KEY (`CourseID`)
    )
    """

    @staticmethod
    def insert():
        sql = """
        INSERT INTO `Courses` (`CourseID`, `CourseName`, `CreditHours`, `CourseType`)
        VALUES (%s, %s, %s, %s);
        """
        return sql

    @staticmethod
    def delete():
        sql = """
        DELETE FROM `Courses`
        WHERE `CourseID` = %s;
        """
        return sql

    @staticmethod
    def update():
        sql = """
        UPDATE `Courses`
        SET
        `CourseName` = %s,
        `CreditHours` = %s,
        `CourseType` = %s
        WHERE `CourseID` = %s;
        """
        return sql

    @staticmethod
    def query():
        sql = """
        SELECT * FROM `Courses`
        WHERE `CourseID` = %s;
        """
        return sql


class CoursesFunc(BaseFunc):

    def __init__(self, genner, handler) -> None:
        super().__init__(genner, handler)

    def insert(self, id: str, name: str, credit_hours: int, course_type: int):
        if id == "":
            raise gr.Error("课程号不能为空!")
        if name == "":
            raise gr.Error("课程名不能为空!")
        if credit_hours < 1:
            raise gr.Error("学时数不能小于1!")
        sql = self.genner.insert()
        result = self.handler.execute(sql,
                                      (id, name, credit_hours, course_type))
        if result[0]:
            gr.Info("增加成功!")
        else:
            raise gr.Error("增加失败: " + result[1])

    def delete(self, id: str):
        query_sql = self.genner.query()
        query_result = self.handler.query(query_sql, (id, ))
        if len(query_result[1]) == 0:
            raise gr.Error("删除失败: 未找到该课程!")
        sql = self.genner.delete()
        result = self.handler.execute(sql, (id, ))
        if result[0]:
            gr.Info("删除成功!")
        else:
            raise gr.Error("删除失败: " + result[1])

    def update(self, id: str, name: str, credit_hours: int, course_type: int):
        if id == "":
            raise gr.Error("课程号不能为空!")
        if name == "":
            raise gr.Error("课程名不能为空!")
        query_sql = self.genner.query()
        query_result = self.handler.query(query_sql, (id, ))
        if len(query_result[1]) == 0:
            raise gr.Error("修改失败: 未找到该课程!")
        sql = self.genner.update()
        result = self.handler.execute(sql,
                                      (name, credit_hours, course_type, id))
        if result[0]:
            gr.Info("修改成功!")
        else:
            raise gr.Error("修改失败: " + result[1])

    def query(self, id: str):
        sql = self.genner.query()
        result = self.handler.query(sql, (id, ))
        if result[0]:
            if len(result[1]) == 0:
                gr.Warning("查询失败: 未找到该课程!")
                return []
            else:
                return [[
                    row[0], row[1], row[2], course_type_map[row[3] - 1][0]
                ] for row in result[1]]
        else:
            raise gr.Error("查询失败: " + result[1])
