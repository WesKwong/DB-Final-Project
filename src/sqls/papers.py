import gradio as gr

from .base_sql_class import BaseTable, BaseFunc
from .teachers import TeachersTable
from .publishedpapers import PublishedPapersTable

paper_type_map = [
    ("full paper", 1),
    ("short paper", 2),
    ("poster paper", 3),
    ("demo paper", 4)
]

level_map = [
    ("CCF-A", 1),
    ("CCF-B", 2),
    ("CCF-C", 3),
    ("中文 CCF-A", 4),
    ("中文 CCF-B", 5),
    ("无级别", 6)
]

is_corresponding_map = [
    ("是", 1),
    ("否", 0)
]


class PapersTable(BaseTable):
    """
    CREATE TABLE IF NOT EXISTS `Papers` (
        `PaperID` INTEGER NOT NULL,
        `PaperName` VARCHAR(256) NOT NULL,
        `PublicationSource` VARCHAR(256) NOT NULL,
        `PublicationYear` INTEGER NOT NULL,
        `Type` INTEGER NOT NULL,
        `Level` INTEGER NOT NULL,
        PRIMARY KEY (`PaperID`)
    )
    """

    def __init__(self):
        super().__init__()

    @staticmethod
    def insert():
        sql = """
        INSERT INTO `Papers` (`PaperID`, `PaperName`, `PublicationSource`,
        `PublicationYear`, `Type`, `Level`)
        VALUES (%s, %s, %s, %s, %s, %s);
        """
        return sql

    @staticmethod
    def delete():
        sql = """
        DELETE FROM `Papers`
        WHERE `PaperID` = %s;
        """
        return sql

    @staticmethod
    def update():
        sql = """
        UPDATE `Papers`
        SET
        `PaperName` = %s,
        `PublicationSource` = %s,
        `PublicationYear` = %s,
        `Type` = %s,
        `Level` = %s
        WHERE `PaperID` = %s;
        """
        return sql

    @staticmethod
    def query():
        sql = """
        SELECT * FROM `Papers`
        WHERE `PaperID` = %s;
        """
        return sql

    @staticmethod
    def query_authors():
        sql = """
        SELECT `PublishedPapers`.`TeacherID`, `Name`, `Rank`, `IsCorrespondingAuthor`
        FROM `PublishedPapers`, `Teachers`
        WHERE `PaperID` = %s AND `PublishedPapers`.`TeacherID` = `Teachers`.`TeacherID`;
        """
        return sql


class PapersFunc(BaseFunc):

    def __init__(self, genner, handler) -> None:
        super().__init__(genner, handler)

    def insert(self, id: int, name: str, source: str, year: int, type: int,
               level: int, author_num: int, *author_list):
        if name == "":
            raise gr.Error("论文名称不能为空!")
        if source == "":
            raise gr.Error("发表源不能为空!")

        teacher_genner = TeachersTable()
        query_teacher_sql = teacher_genner.query()
        tid_set = set()
        rank_set = set()
        cor_flag = False
        alist = []
        for i in range(author_num):
            tid = author_list[i * 3]
            if tid == "":
                raise gr.Error(f"作者工号不能为空!")
            result = self.handler.query(query_teacher_sql, (tid, ))
            if len(result[1]) == 0:
                raise gr.Error(f"作者工号<{tid}>不存在!")
            if tid in tid_set:
                raise gr.Error(f"作者工号<{tid}>重复!")
            tid_set.add(tid)

            rank = author_list[i * 3 + 1]
            if rank in rank_set:
                raise gr.Error(f"作者排名<{rank}>重复!")
            rank_set.add(rank)

            cor = author_list[i * 3 + 2]
            if cor:
                if cor_flag:
                    raise gr.Error("只能有一个通讯作者!")
                cor_flag = True
            author = (tid, rank, cor)
            alist.append(author)

        pub_genner = PublishedPapersTable()
        sql = self.genner.insert()
        pub_sql = pub_genner.insert()
        result = self.handler.execute(sql,
                                      (id, name, source, year, type, level),
                                      autocommit=False)
        if result[0]:
            gr.Info("论文增加成功!")
        else:
            raise gr.Error("论文增加失败: " + result[1])

        for author in alist:
            result = self.handler.execute(
                pub_sql, (author[0], id, author[1], author[2]),
                autocommit=False)
            if not result[0]:
                raise gr.Error(f"作者<工号: {author[0]}>增加失败, 已回滚: " + result[1])
            gr.Info(f"作者<工号: {author[0]}>增加成功!")
        self.handler.commit()
        gr.Info("增加成功!")

    def delete(self, id: str):
        query_sql = self.genner.query()
        query_result = self.handler.query(query_sql, (id, ))
        if len(query_result[1]) == 0:
            raise gr.Error("删除失败: 未找到该论文!")
        sql = self.genner.delete()
        result = self.handler.execute(sql, (id, ))
        if result[0]:
            gr.Info("删除成功!")
        else:
            raise gr.Error("删除失败: " + result[1])

    def update(self, id: int, name: str, source: str, year: int, type: int,
               level: int, author_num: int, *author_list):
        if name == "":
            raise gr.Error("论文名称不能为空!")
        if source == "":
            raise gr.Error("发表源不能为空!")

        teacher_genner = TeachersTable()
        query_teacher_sql = teacher_genner.query()
        tid_set = set()
        rank_set = set()
        cor_flag = False
        alist = []
        for i in range(author_num):
            tid = author_list[i * 3]
            if tid == "":
                raise gr.Error(f"作者工号不能为空!")
            result = self.handler.query(query_teacher_sql, (tid, ))
            if len(result[1]) == 0:
                raise gr.Error(f"作者工号<{tid}>不存在!")
            if tid in tid_set:
                raise gr.Error(f"作者工号<{tid}>重复!")
            tid_set.add(tid)

            rank = author_list[i * 3 + 1]
            if rank in rank_set:
                raise gr.Error(f"作者排名<{rank}>重复!")
            rank_set.add(rank)

            cor = author_list[i * 3 + 2]
            if cor:
                if cor_flag:
                    raise gr.Error("只能有一个通讯作者!")
                cor_flag = True
            author = (tid, rank, cor)
            alist.append(author)

        query_sql = self.genner.query()
        query_result = self.handler.query(query_sql, (id, ))
        delete_sql = self.genner.delete()
        if len(query_result[1]) == 0:
            raise gr.Error("修改失败: 未找到该论文!")
        else:
            result = self.handler.execute(delete_sql, (id, ))
            if not result[0]:
                raise gr.Error("修改失败: " + result[1])

        pub_genner = PublishedPapersTable()
        sql = self.genner.insert()
        pub_insert_sql = pub_genner.insert()
        result = self.handler.execute(sql,
                                      (id, name, source, year, type, level),
                                      autocommit=False)
        if result[0]:
            gr.Info("论文修改成功!")
        else:
            raise gr.Error("论文修改失败: " + result[1])

        for author in alist:
            result = self.handler.execute(
                pub_insert_sql, (author[0], id, author[1], author[2]),
                autocommit=False)
            if not result[0]:
                raise gr.Error(f"作者<工号: {author[0]}>修改失败, 已回滚: " + result[1])
            gr.Info(f"作者<工号: {author[0]}>修改成功!")

        self.handler.commit()
        gr.Info("修改成功!")

    def query(self, id: str):
        sql = self.genner.query()
        result = self.handler.query(sql, (id, ))
        if result[0]:
            if len(result[1]) == 0:
                gr.Warning("查询失败: 未找到该论文!")
                return ([], [])

            author_sql = self.genner.query_authors()
            author_result = self.handler.query(author_sql, (id, ))
            if author_result[0]:
                if len(author_result[1]) == 0:
                    gr.Warning("查询失败: 未找到作者信息!")
                    return ([], [])
            else:
                raise gr.Error("查询失败: " + author_result[1])

            paper = [[
                row[0], row[1], row[2], row[3], paper_type_map[row[4] - 1][0],
                level_map[row[5] - 1][0]
            ] for row in result[1]]
            authors = [[
                row[0], row[1], row[2], is_corresponding_map[row[3] - 1][0]
            ] for row in author_result[1]]
            return (paper, authors)
        else:
            raise gr.Error("查询失败: " + result[1])
