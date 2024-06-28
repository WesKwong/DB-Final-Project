import gradio as gr


from .base_sql_class import BaseTable, BaseFunc
from .teachers import TeachersTable
from .courses import CoursesTable, course_type_map

semester_map = [
    ("春季学期", 1),
    ("夏季学期", 2),
    ("秋季学期", 3),
]

class TaughtCoursesTable(BaseTable):
    """
    CREATE TABLE IF NOT EXISTS `TaughtCourses` (
        `TeacherID` VARCHAR(5) NOT NULL,
        `CourseID` VARCHAR(256) NOT NULL,
        `Year` INTEGER NOT NULL,
        `Semester` INTEGER NOT NULL,
        `HoursTaught` INTEGER NOT NULL,
        FOREIGN KEY (`TeacherID`) REFERENCES `Teachers` (`TeacherID`) ON DELETE CASCADE,
        FOREIGN KEY (`CourseID`) REFERENCES `Courses` (`CourseID`) ON DELETE CASCADE,
        PRIMARY KEY (`TeacherID`, `CourseID`, `Year`, `Semester`)
    )
    """

    def __init__(self):
        super().__init__()

    @staticmethod
    def insert():
        sql = """
        INSERT INTO `TaughtCourses` (`TeacherID`, `CourseID`,
        `Year`, `Semester`, `HoursTaught`)
        VALUES (%s, %s, %s, %s, %s);
        """
        return sql

    @staticmethod
    def delete():
        sql = """
        DELETE FROM `TaughtCourses`
        WHERE `TeacherID` = %s AND `CourseID` = %s AND `Year` = %s
        AND `Semester` = %s;
        """
        return sql

    @staticmethod
    def delete_by_cid_year_semester():
        sql = """
        DELETE FROM `TaughtCourses`
        WHERE `CourseID` = %s AND `Year` = %s AND `Semester` = %s;
        """
        return sql

    @staticmethod
    def update():
        sql = """
        UPDATE `TaughtCourses`
        SET
        `HoursTaught` = %s
        WHERE `TeacherID` = %s AND `CourseID` = %s AND `Year` = %s
        AND `Semester` = %s;
        """
        return sql

    @staticmethod
    def query():
        sql = """
        SELECT * FROM `TaughtCourses`
        WHERE `TeacherID` = %s AND `CourseID` = %s AND `Year` = %s
        AND `Semester` = %s;
        """
        return sql

    @staticmethod
    def query_by_cid_year_semester():
        sql = """
        SELECT * FROM `TaughtCourses`
        WHERE `CourseID` = %s AND `Year` = %s AND `Semester` = %s;
        """
        return sql

    @staticmethod
    def query_teachers():
        sql = """
        SELECT `Teachers`.`TeacherID`, `Name`, `HoursTaught`
        FROM `TaughtCourses`, `Teachers`
        WHERE `TaughtCourses`.`TeacherID` = `Teachers`.`TeacherID`
        AND `CourseID` = %s AND `Year` = %s AND `Semester` = %s;
        """
        return sql

    @staticmethod
    def query_coursename():
        sql = """
        SELECT `CourseName`, `CreditHours`
        FROM `Courses`
        WHERE `CourseID` = %s;
        """
        return sql

class TaughtCoursesFunc(BaseFunc):

    def __init__(self, genner, handler) -> None:
        super().__init__(genner, handler)

    def insert(self, cid: str, year: int, semester: int,
               t_num: int, *t_list: list):
        if cid == "":
            raise gr.Error("课程号不能为空!")

        query_course_sql = self.genner.query_coursename()
        result = self.handler.query(query_course_sql, (cid, ))
        if result[0]:
            if len(result[1]) == 0:
                raise gr.Error("课程号不存在!")
        else:
            raise gr.Error("授课信息增加失败: " + result[1])

        hours = int(result[1][0][1])

        teacher_genner = TeachersTable()
        query_teacher_sql = teacher_genner.query()
        tid_set = set()
        hour_sum = 0
        tlist = []
        for i in range(t_num):
            tid = t_list[i * 2]
            if tid == "":
                raise gr.Error("教师工号不能为空!")
            result = self.handler.query(query_teacher_sql, (tid, ))
            if len(result[1]) == 0:
                raise gr.Error(f"教师工号<{tid}>不存在!")
            if tid in tid_set:
                raise gr.Error(f"教师工号<{tid}>重复!")
            tid_set.add(tid)

            t_hour = t_list[i * 2 + 1]
            hour_sum += t_hour
            teacher = (tid, t_hour)
            tlist.append(teacher)

        if hour_sum != hours:
            raise gr.Error("授课总学时与课程学时不符!")

        insert_sql = self.genner.insert()
        for teacher in tlist:
            result = self.handler.execute(
                insert_sql, (teacher[0], cid, year, semester, teacher[1]))
            if not result[0]:
                raise gr.Error(f"授课信息<工号: {teacher[0]}>增加失败: " + result[1])
            gr.Info(f"授课信息<工号: {teacher[0]}>增加成功!")

        self.handler.commit()
        gr.Info("授课信息增加成功!")

    def delete(self, cid: str, year: int, semester: int):
        query_sql = self.genner.query_by_cid_year_semester()
        query_result = self.handler.query(query_sql, (cid, year, semester))
        if len(query_result[1]) == 0:
            raise gr.Error("删除失败: 未找到该授课信息!")
        sql = self.genner.delete_by_cid_year_semester()
        result = self.handler.execute(sql, (cid, year, semester))
        if result[0]:
            gr.Info("删除成功!")
        else:
            raise gr.Error("删除失败: " + result[1])

    def update(self, cid: str, year: int, semester: int,
               t_num: int, *t_list: list):
        if cid == "":
            raise gr.Error("课程号不能为空!")

        query_course_sql = self.genner.query_coursename()
        result = self.handler.query(query_course_sql, (cid, ))
        if result[0]:
            if len(result[1]) == 0:
                raise gr.Error("课程号不存在!")
        else:
            raise gr.Error("授课信息增加失败: " + result[1])

        hours = int(result[1][0][1])

        teacher_genner = TeachersTable()
        query_teacher_sql = teacher_genner.query()
        tid_set = set()
        hour_sum = 0
        tlist = []
        for i in range(t_num):
            tid = t_list[i * 2]
            if tid == "":
                raise gr.Error("教师工号不能为空!")
            result = self.handler.query(query_teacher_sql, (tid, ))
            if len(result[1]) == 0:
                raise gr.Error(f"教师工号<{tid}>不存在!")
            if tid in tid_set:
                raise gr.Error(f"教师工号<{tid}>重复!")
            tid_set.add(tid)

            t_hour = t_list[i * 2 + 1]
            hour_sum += t_hour
            teacher = (tid, t_hour)
            tlist.append(teacher)

        if hour_sum != hours:
            raise gr.Error("授课总学时与课程学时不符!")

        query_sql = self.genner.query_by_cid_year_semester()
        query_result = self.handler.query(query_sql, (cid, year, semester))
        delete_sql = self.genner.delete_by_cid_year_semester()
        if len(query_result[1]) == 0:
            raise gr.Error("修改失败: 未找到该授课信息!")
        else:
            result = self.handler.execute(delete_sql, (cid, year, semester))
            if not result[0]:
                raise gr.Error("修改失败: " + result[1])

        insert_sql = self.genner.insert()
        for teacher in tlist:
            result = self.handler.execute(
                insert_sql, (teacher[0], cid, year, semester, teacher[1]))
            if not result[0]:
                raise gr.Error(f"授课信息<工号: {teacher[0]}>修改失败: " + result[1])
            gr.Info(f"授课信息<工号: {teacher[0]}>修改成功!")

        self.handler.commit()
        gr.Info("授课信息修改成功!")

    def query(self, cid: str, year: int, semester: int):
        query_sql = self.genner.query_by_cid_year_semester()
        query_result = self.handler.query(query_sql, (cid, year, semester))
        if query_result[0]:
            if len(query_result[1]) == 0:
                gr.Warning("查询失败: 未找到该授课信息!")
                return ([], [])

            courses_genner = CoursesTable()
            course_sql = courses_genner.query()
            course_result = self.handler.query(course_sql, (cid, ))
            if course_result[0]:
                if len(course_result[1]) == 0:
                    gr.Warning("查询失败: 未找到该课程信息!")
                    return ([], [])

                teacher_sql = self.genner.query_teachers()
                teacher_result = self.handler.query(teacher_sql, (cid, year, semester))
                if teacher_result[0]:
                    if len(teacher_result[1]) == 0:
                        gr.Warning("查询失败: 未找到该课程的教师信息!")
                        return ([], [])
                else:
                    raise gr.Error("查询失败: " + teacher_result[1])

                course = [[
                    row[0], row[1], row[2], course_type_map[row[3] - 1][0],
                    year, semester_map[semester - 1][0]
                ] for row in course_result[1]]
                teachers = [[row[0], row[1], row[2]]
                            for row in teacher_result[1]]
                return (course, teachers)

            else:
                raise gr.Error("查询失败: " + course_result[1])
