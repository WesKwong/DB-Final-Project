import os

import gradio as gr
from md2pdf.core import md2pdf

from .base_sql_class import BaseTable, BaseFunc
from .teachers import TeachersTable, gender_map, title_map
from .courses import CoursesTable, course_type_map
from .taughtcourses import TaughtCoursesTable, semester_map
from .papers import PapersTable, level_map, paper_type_map, is_corresponding_map
from .projects import ProjectsTable, project_type_map


class SummaryTable(object):

    @staticmethod
    def query_teacher_info():
        sql = """
        SELECT * FROM `Teachers`
        WHERE `TeacherID` = %s;
        """
        return sql

    @staticmethod
    def query_taught_courses():
        sql = """
        SELECT `TaughtCourses`.`CourseID`, `CourseName`, `CourseType`,
        `HoursTaught`, `CreditHours`, `Year`, `Semester`
        FROM `TaughtCourses`, `Courses`
        WHERE `TeacherID` = %s
        AND `TaughtCourses`.`CourseID` = `Courses`.`CourseID`
        AND `Year` >= %s AND `Year` <= %s;
        """
        return sql

    @staticmethod
    def query_published_papers():
        sql = """
        SELECT `PaperName`, `PublicationSource`, `PublicationYear`,
        `Level`, `Rank`, `IsCorrespondingAuthor`
        FROM `PublishedPapers`, `Papers`
        WHERE `TeacherID` = %s
        AND `PublishedPapers`.`PaperID` = `Papers`.`PaperID`
        AND `PublicationYear` >= %s AND `PublicationYear` <= %s;
        """
        return sql

    @staticmethod
    def query_undertaken_projects():
        sql = """
        SELECT `ProjectName`, `ProjectSource`, `ProjectType`,
        `StartDate`, `EndDate`, `FundsUndertaken`,
        `TotalFunds`, `Rank`
        FROM `UndertakenProjects`, `Projects`
        WHERE `TeacherID` = %s
        AND `UndertakenProjects`.`ProjectID` = `Projects`.`ProjectID`
        AND `EndDate` >= %s AND `StartDate` <= %s;
        """
        return sql


class MarkdownFormat(object):

    def __init__(self) -> None:
        self.init_md()

    def init_md(self) -> None:
        self.md = ""

    def add_title(self, title: str, center: bool = True) -> None:
        if center:
            self.md += "<center><h1>" + title + "</h1></center>\n\n"
        else:
            self.md += "# " + title + "\n\n"

    def add_subtitle(self, subtitle: str) -> None:
        self.md += "## " + subtitle + "\n\n"

    def add_text(self, text: str) -> None:
        self.md += text + "\n\n"

    def add_table(self, headers: list, data: list[list]) -> None:
        # headers
        self.md += "|"
        for header in headers:
            self.md += header + "|"
        self.md += "\n"
        # split line
        self.md += "|"
        for _ in headers:
            self.md += ":---:|"
        self.md += "\n"
        # data
        for row in data:
            self.md += "|"
            for cell in row:
                self.md += cell + "|"
            self.md += "\n"
        self.md += "\n"

    def add_enumerate(self, data: list) -> None:
        for i, item in enumerate(data):
            self.md += str(i + 1) + ". " + item + "\n\n"

    def get_md(self) -> str:
        return self.md


class SummaryFunc(object):

    def __init__(self, genner, handler) -> None:
        self.genner = genner
        self.handler = handler
        self.md = None

    def query_summary(self, tid: str, start_year: int, end_year: int) -> str:
        if tid == "":
            raise gr.Error("工号不能为空!")
        if start_year > end_year:
            raise gr.Error("起始年份不能大于结束年份!")

        t_info_sql = self.genner.query_teacher_info()
        c_info_sql = self.genner.query_taught_courses()
        p_info_sql = self.genner.query_published_papers()
        pf_info_sql = self.genner.query_undertaken_projects()

        t_info = self.handler.query(t_info_sql, (tid, ))
        if not t_info[0]:
            raise gr.Error("查询失败: " + t_info[1])
        if len(t_info[1]) == 0:
            raise gr.Error("查询失败: 未找到该教师!")

        self.md = MarkdownFormat()
        # title
        self.md.add_title(f"教师教学科研工作统计({start_year}-{end_year})", center=True)

        # teacher info
        t_info_list = [[
            row[0], row[1], gender_map[row[2] - 1][0], title_map[row[3] - 1][0]
        ] for row in t_info[1]]
        self.md.add_subtitle("教师基本信息")
        self.md.add_text(
            f"<b>工号: </b>{t_info_list[0][0]}    " +
            f"<b>姓名: </b>{t_info_list[0][1]}    " +
            f"<b>性别: </b>{t_info_list[0][2]}    " +
            f"<b>职称: </b>{t_info_list[0][3]}    "
        )

        # courses info
        self.md.add_subtitle("教授课程信息")
        c_info = self.handler.query(c_info_sql, (tid, start_year, end_year))
        if not c_info[0]:
            raise gr.Error("查询失败: " + c_info[1])
        if len(c_info[1]) != 0:
            c_info_list = [[
                row[0],
                row[1],
                course_type_map[row[2] - 1][0],
                str(row[3]) + "/" + str(row[4]),
                str(row[5]) + " " + semester_map[row[6] - 1][0]
            ] for row in c_info[1]]
            self.md.add_table(["课程号", "课程名", "课程类型", "授课学时/总学时", "学期"], c_info_list)
        else:
            self.md.add_text("无")

        # papers info
        self.md.add_subtitle("发表论文信息")
        p_info = self.handler.query(p_info_sql, (tid, start_year, end_year))

        def get_cor_str(is_corresponding: bool) -> str:
            if is_corresponding:
                return ", 通信作者"
            return ""

        if not p_info[0]:
            raise gr.Error("查询失败: " + p_info[1])
        if len(p_info[1]) != 0:
            p_info_list = [
                f"{row[0]}, " + \
                f"{row[1]}, " + \
                f"{str(row[2])}, " + \
                f"{level_map[row[3]-1][0]}, " + \
                f"第{str(row[4])}作者" + \
                f"{get_cor_str(row[5])}"
                for row in p_info[1]
            ]
            self.md.add_enumerate(p_info_list)
        else:
            self.md.add_text("无")

        # projects info
        self.md.add_subtitle("承担项目信息")
        pf_info = self.handler.query(pf_info_sql, (tid, start_year, end_year))
        if not pf_info[0]:
            raise gr.Error("查询失败: " + pf_info[1])
        if len(pf_info[1]) != 0:
            pf_info_list = [
                f"{row[0]}, " + \
                f"{row[1]}, " + \
                f"{project_type_map[row[2]-1][0]}, " + \
                f"{str(row[3])}~{str(row[4])}, " + \
                f"(承担经费/总经费):({str(row[5])}/{str(row[6])}), " + \
                f"第{str(row[7])}负责人"
                for row in pf_info[1]
            ]
            self.md.add_enumerate(pf_info_list)
        else:
            self.md.add_text("无")

        return self.md.get_md()

    def export_summary(self, tid: str, start_year: int, end_year: int, path: str="./export") -> None:
        if self.md is None:
            self.query_summary(tid, start_year, end_year)
        if not os.path.exists(path):
            os.makedirs(path)
        path = os.path.join(path, f"{tid}_summary_{start_year}-{end_year}.pdf")
        md2pdf(pdf_file_path=path, md_content=self.md.get_md())
        return path
