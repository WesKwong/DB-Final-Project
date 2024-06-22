from datetime import date

import gradio as gr
from loguru import logger

from sqls import *

handler = SQLHandler()
current_year = date.today().year

with gr.Blocks() as demo:
    gr.Markdown("""
<center> <h1> 🏫 教师教学科研登记系统 </h1> </center>
""")
    with gr.Tab("👨‍🏫 教师信息"):
        teacher_genner = TeachersTable()
        teacher_func = TeachersFunc(teacher_genner, handler)
        with gr.Tab("✂️ 信息增删改"):
            tid = gr.Textbox(label="工号", placeholder="请输入工号", value="T0001")
            tname = gr.Textbox(label="姓名", placeholder="请输入姓名", value="张三")
            tgender = gr.Dropdown(gender_map, label="性别", value=1)
            ttitle = gr.Dropdown(title_map, label="职称", value=1)
            with gr.Row():
                tinsert_button = gr.Button("💡 增加")
                tdelete_button = gr.Button("🗑️ 删除")
                tupdate_button = gr.Button("✏️ 修改")
            tinsert_button.click(fn=teacher_func.insert,
                                 inputs=[tid, tname, tgender, ttitle])
            tdelete_button.click(fn=teacher_func.delete, inputs=[tid])
            tupdate_button.click(fn=teacher_func.update,
                                 inputs=[tid, tname, tgender, ttitle])
        with gr.Tab("📊 信息查询"):
            with gr.Row():
                tquery_id = gr.Textbox(label="工号",
                                       placeholder="请输入工号")
                tquery_name = gr.Textbox(label="姓名",
                                         placeholder="请输入姓名")
                tquery_button = gr.Button("🔍 查询")
            tquery_output = gr.Dataframe(headers=["工号", "姓名", "性别", "职称"])
            tquery_button.click(fn=teacher_func.query,
                                inputs=[tquery_id, tquery_name],
                                outputs=[tquery_output])
    with gr.Tab("📚 课程信息"):
        course_genner = CoursesTable()
        course_func = CoursesFunc(course_genner, handler)
        with gr.Tab("✂️ 信息增删改"):
            cid = gr.Textbox(label="课程号", placeholder="请输入课程号", value="C0001")
            cname = gr.Textbox(label="课程名",
                               placeholder="请输入课程名",
                               value="数据库原理")
            chours = gr.Number(label="学时数", precision=0, value=1, minimum=1)
            ctype = gr.Dropdown(course_type_map, label="课程性质", value=1)
            with gr.Row():
                cinsert_button = gr.Button("💡 增加")
                cdelete_button = gr.Button("🗑️ 删除")
                cupdate_button = gr.Button("✏️ 修改")
            cinsert_button.click(fn=course_func.insert,
                                 inputs=[cid, cname, chours, ctype])
            cdelete_button.click(fn=course_func.delete, inputs=[cid])
            cupdate_button.click(fn=course_func.update,
                                 inputs=[cid, cname, chours, ctype])
        with gr.Tab("📊 信息查询"):
            with gr.Row():
                cquery_id = gr.Textbox(label="课程号",
                                       placeholder="请输入课程号")
                cquery_name = gr.Textbox(label="课程名",
                                         placeholder="请输入课程名")
                cquery_button = gr.Button("🔍 查询")
            cquery_output = gr.Dataframe(headers=["课程号", "课程名", "学时数", "课程性质"])
            cquery_button.click(fn=course_func.query,
                                inputs=[cquery_id, cquery_name],
                                outputs=[cquery_output])
    with gr.Tab("📝 发表论文"):
        paper_genner = PapersTable()
        paper_func = PapersFunc(paper_genner, handler)
        with gr.Tab("✂️ 信息增删改"):
            gr.Markdown("<center> <h2> 📝 论文信息 </h2> </center>")
            with gr.Row():
                pid = gr.Number(label="论文编号",
                                precision=0,
                                value=1,
                                minimum=1,
                                interactive=True)
                pname = gr.Textbox(label="论文名称",
                                   placeholder="请输入论文名称",
                                   value="数据库论文",
                                   interactive=True)
                psource = gr.Textbox(label="发表源",
                                     placeholder="请输入发表源",
                                     value="数据库学报",
                                     interactive=True)
            with gr.Row():
                pdate = gr.Number(label="发表年份",
                                  value=current_year,
                                  minimum=1900,
                                  maximum=current_year,
                                  interactive=True,
                                  precision=0)
                ptype = gr.Dropdown(paper_type_map,
                                    label="论文类型",
                                    value=1,
                                    interactive=True)
                plevel = gr.Dropdown(level_map,
                                     label="论文级别",
                                     value=1,
                                     interactive=True)

            gr.Markdown("<center> <h2> 👨‍🏫 作者信息 </h2> </center>")
            author_num = gr.State(value=1)
            with gr.Row():
                add_author_btn = gr.Button("➕ 增加作者")
                del_author_btn = gr.Button("➖ 删除作者")
            add_author_btn.click(lambda x: x + 1, author_num, author_num)
            del_author_btn.click(lambda x: x - 1
                                 if x > 1 else 1, author_num, author_num)

            @gr.render(inputs=author_num)
            def add_author(num):
                boxes = []
                for i in range(num):
                    gr.Markdown(f"<h3> 作者{i+1} </h3>")
                    with gr.Row():
                        id_box = gr.Textbox(label="作者工号",
                                            placeholder="请输入作者工号",
                                            value=f"T{i+1:04d}",
                                            key=i)
                        rank_box = gr.Number(label="作者排名",
                                             value=i + 1,
                                             minimum=1,
                                             precision=0,
                                             interactive=True,
                                             key=i + 1e9 + 7)
                        cor_box = gr.Checkbox(label="是否通讯作者",
                                              value=False,
                                              key=i + 2 * (1e9 + 7))
                        boxes.append(id_box)
                        boxes.append(rank_box)
                        boxes.append(cor_box)

                pinsert_button.click(fn=paper_func.insert,
                                     inputs=[
                                         pid, pname, psource, pdate, ptype,
                                         plevel, author_num, *boxes
                                     ])
                pupdate_button.click(fn=paper_func.update,
                                     inputs=[
                                         pid, pname, psource, pdate, ptype,
                                         plevel, author_num, *boxes
                                     ])

            with gr.Row():
                pinsert_button = gr.Button("💡 增加")
                pdelete_button = gr.Button("🗑️ 删除")
                pupdate_button = gr.Button("✏️ 修改")

            pdelete_button.click(fn=paper_func.delete, inputs=[pid])

        with gr.Tab("📊 信息查询"):
            with gr.Row():
                pquery_id = gr.Number(label="论文编号",
                                      precision=0,
                                      value=1,
                                      minimum=1)
                pquery_button = gr.Button("🔍 查询")
            gr.Markdown("<h3> 📝 论文信息 </h3>")
            paper_df = gr.Dataframe(
                headers=["论文编号", "论文名称", "发表源", "发表年份", "论文类型", "论文级别"])
            gr.Markdown("<h3> 👨‍🏫 作者信息 </h3>")
            authors_df = gr.Dataframe(
                headers=["作者工号", "作者姓名", "作者排名", "是否通讯作者"])
            pquery_button.click(fn=paper_func.query,
                                inputs=[pquery_id],
                                outputs=[paper_df, authors_df])

    with gr.Tab("💰 承担项目"):
        project_genner = ProjectsTable()
        project_func = ProjectsFunc(project_genner, handler)
        with gr.Tab("✂️ 信息增删改"):
            gr.Markdown("<center> <h2> 💼 项目信息 </h2> </center>")
            with gr.Row():
                pjid = gr.Textbox(label="项目编号",
                                  placeholder="请输入项目编号",
                                  value="P0001",
                                  interactive=True)
                pjname = gr.Textbox(label="项目名称",
                                    placeholder="请输入项目名称",
                                    value="数据库项目",
                                    interactive=True)
                pjsource = gr.Textbox(label="项目来源",
                                      placeholder="请输入项目来源",
                                      value="数据库学院",
                                      interactive=True)
            with gr.Row():
                pjtype = gr.Dropdown(project_type_map,
                                     label="项目类型",
                                     value=1,
                                     interactive=True)
                pjfunds = gr.Number(label="项目经费",
                                    value=0.0,
                                    minimum=0.0,
                                    interactive=True,
                                    precision=2)
            with gr.Row():
                pjstart = gr.Number(label="开始年份",
                                    value=current_year,
                                    minimum=1900,
                                    maximum=current_year,
                                    interactive=True,
                                    precision=0)
                pjend = gr.Number(label="结束年份",
                                  value=current_year,
                                  minimum=1900,
                                  maximum=current_year,
                                  interactive=True,
                                  precision=0)

            gr.Markdown("<center> <h2> 👩‍💻‍ 成员信息 </h2> </center>")
            member_num = gr.State(value=1)
            with gr.Row():
                add_member_btn = gr.Button("➕ 增加成员")
                del_member_btn = gr.Button("➖ 删除成员")
            add_member_btn.click(lambda x: x + 1, member_num, member_num)
            del_member_btn.click(lambda x: x - 1
                                 if x > 1 else 1, member_num, member_num)

            @gr.render(inputs=member_num)
            def add_member(num):
                boxes = []
                for i in range(num):
                    gr.Markdown(f"<h3> 成员{i+1} </h3>")
                    with gr.Row():
                        id_box = gr.Textbox(label="成员工号",
                                            placeholder="请输入成员工号",
                                            value=f"T{i+1:04d}",
                                            key=i)
                        rank_box = gr.Number(label="成员排名",
                                             value=i + 1,
                                             minimum=1,
                                             precision=0,
                                             interactive=True,
                                             key=i + 1e9 + 7)
                        funds_box = gr.Number(label="成员承担经费",
                                              value=0.0,
                                              minimum=0.0,
                                              precision=2,
                                              interactive=True,
                                              key=i + 2 * (1e9 + 7))
                        boxes.append(id_box)
                        boxes.append(rank_box)
                        boxes.append(funds_box)

                pjinsert_button.click(fn=project_func.insert,
                                      inputs=[
                                          pjid, pjname, pjsource, pjtype,
                                          pjfunds, pjstart, pjend, member_num,
                                          *boxes
                                      ])
                pjupdate_button.click(fn=project_func.update,
                                      inputs=[
                                          pjid, pjname, pjsource, pjtype,
                                          pjfunds, pjstart, pjend, member_num,
                                          *boxes
                                      ])

            with gr.Row():
                pjinsert_button = gr.Button("💡 增加")
                pjdelete_button = gr.Button("🗑️ 删除")
                pjupdate_button = gr.Button("✏️ 修改")

            pjdelete_button.click(fn=project_func.delete, inputs=[pjid])

        with gr.Tab("📊 信息查询"):
            with gr.Row():
                pjquery_id = gr.Textbox(label="项目编号",
                                        placeholder="请输入项目编号",
                                        value="P0001",
                                        interactive=True)
                pjquery_button = gr.Button("🔍 查询")
            gr.Markdown("<h3> 💼 项目信息 </h3>")
            project_df = gr.Dataframe(headers=[
                "项目编号", "项目名称", "项目来源", "项目类型", "项目经费", "开始年份", "结束年份"
            ])
            gr.Markdown("<h3> 👩‍💻‍ 成员信息 </h3>")
            members_df = gr.Dataframe(
                headers=["成员工号", "成员姓名", "成员排名", "成员承担经费"])
            pjquery_button.click(fn=project_func.query,
                                 inputs=[pjquery_id],
                                 outputs=[project_df, members_df])

    with gr.Tab("🎓 主讲课程"):
        taught_genner = TaughtCoursesTable()
        taught_func = TaughtCoursesFunc(taught_genner, handler)
        with gr.Tab("✂️ 信息增删改"):
            gr.Markdown("<center> <h2> 📚 课程信息 </h2> </center>")
            with gr.Row():
                tcid = gr.Textbox(label="课程编号",
                                  placeholder="请输入课程编号",
                                  value="C0001",
                                  interactive=True)
                tcyear = gr.Number(label="学年",
                                   value=current_year,
                                   minimum=1900,
                                   maximum=current_year,
                                   interactive=True,
                                   precision=0)
                tcsemester = gr.Dropdown(semester_map,
                                         label="学期",
                                         value=1,
                                         interactive=True)
                tchours = gr.Number(label="课程学时",
                                    value=1,
                                    minimum=1,
                                    precision=0,
                                    interactive=True)

            gr.Markdown("<center> <h2> 👨‍🏫 教师信息 </h2> </center>")
            tc_num = gr.State(value=1)
            with gr.Row():
                add_teacher_btn = gr.Button("➕ 增加教师")
                del_teacher_btn = gr.Button("➖ 删除教师")
            add_teacher_btn.click(lambda x: x + 1, tc_num, tc_num)
            del_teacher_btn.click(lambda x: x - 1
                                  if x > 1 else 1, tc_num, tc_num)

            @gr.render(inputs=tc_num)
            def add_teacher(num):
                boxes = []
                for i in range(num):
                    gr.Markdown(f"<h3> 教师{i+1} </h3>")
                    with gr.Row():
                        id_box = gr.Textbox(label="教师工号",
                                            placeholder="请输入教师工号",
                                            value=f"T{i+1:04d}",
                                            key=i)
                        hours_box = gr.Number(label="授课学时",
                                              value=1,
                                              minimum=1,
                                              precision=0,
                                              interactive=True,
                                              key=i + 1e9 + 7)
                        boxes.append(id_box)
                        boxes.append(hours_box)

                tcinsert_button.click(
                    fn=taught_func.insert,
                    inputs=[tcid, tcyear, tcsemester, tchours, tc_num, *boxes])
                tcupdate_button.click(
                    fn=taught_func.update,
                    inputs=[tcid, tcyear, tcsemester, tchours, tc_num, *boxes])

            with gr.Row():
                tcinsert_button = gr.Button("💡 增加")
                tcdelete_button = gr.Button("🗑️ 删除")
                tcupdate_button = gr.Button("✏️ 修改")

            tcdelete_button.click(fn=taught_func.delete,
                                  inputs=[tcid, tcyear, tcsemester])

        with gr.Tab("📊 信息查询"):
            with gr.Row():
                tcquery_id = gr.Textbox(label="课程编号",
                                        placeholder="请输入课程编号",
                                        value="C0001",
                                        interactive=True)
                tcquery_year = gr.Number(label="学年",
                                         value=current_year,
                                         minimum=1900,
                                         maximum=current_year,
                                         interactive=True,
                                         precision=0)
                tcquery_semester = gr.Dropdown(semester_map,
                                               label="学期",
                                               value=1,
                                               interactive=True)
                tcquery_button = gr.Button("🔍 查询")
            gr.Markdown("<h3> 📚 课程信息 </h3>")
            course_df = gr.Dataframe(
                headers=["课程编号", "课程名称", "学时数", "课程性质", "学年", "学期"])
            gr.Markdown("<h3> 👨‍🏫 教师信息 </h3>")
            teachers_df = gr.Dataframe(headers=["教师工号", "教师姓名", "授课学时"])
            tcquery_button.click(
                fn=taught_func.query,
                inputs=[tcquery_id, tcquery_year, tcquery_semester],
                outputs=[course_df, teachers_df])

    with gr.Tab("📊 查询统计"):
        summary_genner = SummaryTable()
        summary_func = SummaryFunc(summary_genner, handler)
        with gr.Row():
            summary_tid = gr.Textbox(label="工号",
                                        placeholder="请输入工号",
                                        value="T0001",
                                        interactive=True)
            summary_start_year = gr.Number(label="起始年份",
                                        value=current_year,
                                        minimum=1900,
                                        maximum=current_year,
                                        interactive=True,
                                        precision=0)
            summary_end_year = gr.Number(label="结束年份",
                                        value=current_year,
                                        minimum=1900,
                                        maximum=current_year,
                                        interactive=True,
                                        precision=0)
            summary_button = gr.Button("🔍 查询")
            export_button = gr.Button("📜 导出")
        export_file = gr.File(label="导出文件", type="filepath")
        summary_md = gr.Markdown("")
        summary_button.click(
            fn=summary_func.query_summary,
            inputs=[summary_tid, summary_start_year, summary_end_year],
            outputs=[summary_md])
        export_button.click(
            fn=summary_func.export_summary,
            inputs=[summary_tid, summary_start_year, summary_end_year],
            outputs=[export_file])

@logger.catch
def main():
    demo.launch()


if __name__ == "__main__":
    main()
