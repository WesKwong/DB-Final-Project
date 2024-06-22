import gradio as gr

from .base_sql_class import BaseTable, BaseFunc
from .teachers import TeachersTable
from .undertakenprojects import UndertakenProjectsTable

project_type_map = [
    ("国家级项目", 1),
    ("省部级项目", 2),
    ("市厅级项目", 3),
    ("企业合作项目", 4),
    ("其它类型项目", 5)
]


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

    @staticmethod
    def insert():
        sql = """
        INSERT INTO `Projects` (`ProjectID`, `ProjectName`, `ProjectSource`,
        `ProjectType`, `TotalFunds`, `StartDate`, `EndDate`)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        return sql

    @staticmethod
    def delete():
        sql = """
        DELETE FROM `Projects`
        WHERE `ProjectID` = %s
        """
        return sql

    @staticmethod
    def update():
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
        return sql

    @staticmethod
    def query():
        sql = """
        SELECT * FROM `Projects`
        WHERE `ProjectID` = %s
        """
        return sql

    @staticmethod
    def query_members():
        sql = """
        SELECT `UndertakenProjects`.`TeacherID`, `Name`, `Rank`, `FundsUndertaken`
        FROM `UndertakenProjects`, `Teachers`
        WHERE `UndertakenProjects`.`TeacherID` = `Teachers`.`TeacherID`
        AND `ProjectID` = %s
        """
        return sql


class ProjectsFunc(BaseFunc):

    def __init__(self, genner, handler) -> None:
        super().__init__(genner, handler)

    def insert(self, id: str, name: str, source: str, type: int, funds: float,
               start_date: int, end_date: int, member_num: int, *member_list: list):
        if id == "":
            raise gr.Error("项目编号不能为空!")
        if name == "":
            raise gr.Error("项目名称不能为空!")
        if source == "":
            raise gr.Error("项目来源不能为空!")
        if funds < 0:
            raise gr.Error("项目经费不能为负数!")
        if start_date > end_date:
            raise gr.Error("项目开始年份不能晚于结束年份!")

        teacher_genner = TeachersTable()
        query_teacher_sql = teacher_genner.query()
        tid_set = set()
        rank_set = set()
        funds_total = 0.0
        mlist = []
        for i in range(member_num):
            tid = member_list[i * 3]
            if tid == "":
                raise gr.Error("成员工号不能为空!")
            result = self.handler.query(query_teacher_sql, (tid, ))
            if len(result[1]) == 0:
                raise gr.Error(f"成员工号<{tid}>不存在!")
            if tid in tid_set:
                raise gr.Error(f"成员工号<{tid}>重复!")
            tid_set.add(tid)

            rank = member_list[i * 3 + 1]
            if rank in rank_set:
                raise gr.Error(f"成员排名<{rank}>重复!")
            rank_set.add(rank)

            funds_undertaken = member_list[i * 3 + 2]
            funds_total += funds_undertaken
            member = (tid, rank, funds_undertaken)
            mlist.append(member)

        if abs(funds_total - funds) > 1e-6:
            raise gr.Error("成员承担经费总和与项目经费不符!")

        under_genner = UndertakenProjectsTable()
        sql = self.genner.insert()
        under_sql = under_genner.insert()
        result = self.handler.execute(
            sql, (id, name, source, type, funds, start_date, end_date),
            autocommit=False)
        if result[0]:
            gr.Info("项目增加成功!")
        else:
            raise gr.Error("项目增加失败: " + result[1])

        for member in mlist:
            result = self.handler.execute(
                under_sql, (member[0], id, member[1], member[2]),
                autocommit=False)
            if not result[0]:
                raise gr.Error("项目成员增加失败: " + result[1])
            gr.Info(f"项目成员<工号: {member[0]}>增加成功!")
        self.handler.commit()
        gr.Info("增加成功!")

    def delete(self, id: str):
        query_sql = self.genner.query()
        query_result = self.handler.query(query_sql, (id, ))
        if len(query_result[1]) == 0:
            raise gr.Error("删除失败: 未找到该项目!")
        sql = self.genner.delete()
        result = self.handler.execute(sql, (id, ))
        if result[0]:
            gr.Info("删除成功!")
        else:
            raise gr.Error("删除失败: " + result[1])

    def update(self, id: str, name: str, source: str, type: int, funds: float,
               start_date: int, end_date: int, member_num: int, *member_list: list):
        if id == "":
            raise gr.Error("项目编号不能为空!")
        if name == "":
            raise gr.Error("项目名称不能为空!")
        if source == "":
            raise gr.Error("项目来源不能为空!")
        if funds < 0:
            raise gr.Error("项目经费不能为负数!")
        if start_date > end_date:
            raise gr.Error("项目开始年份不能晚于结束年份!")

        teacher_genner = TeachersTable()
        query_teacher_sql = teacher_genner.query()
        tid_set = set()
        rank_set = set()
        funds_total = 0.0
        mlist = []
        for i in range(member_num):
            tid = member_list[i * 3]
            if tid == "":
                raise gr.Error("成员工号不能为空!")
            result = self.handler.query(query_teacher_sql, (tid, ))
            if len(result[1]) == 0:
                raise gr.Error(f"成员工号<{tid}>不存在!")
            if tid in tid_set:
                raise gr.Error(f"成员工号<{tid}>重复!")
            tid_set.add(tid)

            rank = member_list[i * 3 + 1]
            if rank in rank_set:
                raise gr.Error(f"成员排名<{rank}>重复!")
            rank_set.add(rank)

            funds_undertaken = member_list[i * 3 + 2]
            funds_total += funds_undertaken
            member = (tid, rank, funds_undertaken)
            mlist.append(member)

        if abs(funds_total - funds) > 1e-6:
            raise gr.Error("成员承担经费总和与项目经费不符!")

        query_sql = self.genner.query()
        query_result = self.handler.query(query_sql, (id, ))
        delete_sql = self.genner.delete()
        if len(query_result[1]) == 0:
            raise gr.Error("修改失败: 未找到该项目!")
        else:
            result = self.handler.execute(delete_sql, (id, ))
            if not result[0]:
                raise gr.Error("修改失败: " + result[1])

        under_genner = UndertakenProjectsTable()
        sql = self.genner.insert()
        under_sql = under_genner.insert()
        result = self.handler.execute(
            sql, (id, name, source, type, funds, start_date, end_date),
            autocommit=False)
        if result[0]:
            gr.Info("项目修改成功!")
        else:
            raise gr.Error("项目修改失败: " + result[1])

        for member in mlist:
            result = self.handler.execute(
                under_sql, (member[0], id, member[1], member[2]),
                autocommit=False)
            if not result[0]:
                raise gr.Error(f"项目成员<工号: {member[0]}>修改失败, 已回滚: " + result[1])
            gr.Info(f"项目成员<工号: {member[0]}>修改成功!")

        self.handler.commit()
        gr.Info("修改成功!")

    def query(self, id: str):
        sql = self.genner.query()
        result = self.handler.query(sql, (id, ))
        if result[0]:
            if len(result[1]) == 0:
                gr.Warning("查询失败: 未找到该项目!")
                return ([], [])

            member_sql = self.genner.query_members()
            member_result = self.handler.query(member_sql, (id, ))
            if member_result[0]:
                if len(member_result[1]) == 0:
                    gr.Warning("查询失败: 未找到该项目成员!")
                    return ([], [])
            else:
                raise gr.Error("查询失败: " + member_result[1])

            project = [[
                row[0], row[1], row[2], project_type_map[row[3] - 1][0],
                row[4], row[5], row[6]
            ] for row in result[1]]
            members = [[row[0], row[1], row[2], row[3]]
                       for row in member_result[1]]
            return (project, members)
        else:
            raise gr.Error("查询失败: " + result[1])
