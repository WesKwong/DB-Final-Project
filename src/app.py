import gradio as gr
from sqls import *

handler = SQLHandler()

with gr.Blocks() as demo:
    gr.Markdown("""
<center> <h1> 🏫 教师教学科研登记系统 </h1> </center>
""")
    with gr.Tab("👨‍🏫 教师信息"):
        teacher_genner = TeachersTable()
        teacher_func = TeacherFunc(teacher_genner, handler)
        with gr.Tab("查询信息"):
            tid = gr.Textbox(label="工号", placeholder="请输入工号")
            tquery_button = gr.Button("查询")
            tquery_output = gr.Dataframe(headers=["工号", "姓名", "性别", "职称"])
            tquery_button.click(fn=teacher_func.query,
                                inputs=[tid],
                                outputs=[tquery_output])
        with gr.Tab("修改信息"):
            tid = gr.Textbox(label="工号", placeholder="请输入工号")
            tquery_button = gr.Button("查询")
            tquery_output = gr.Dataframe(headers=["工号", "姓名", "性别", "职称"])
            tquery_button.click(fn=teacher_func.query,
                                inputs=[tid],
                                outputs=[tquery_output])

            tname = gr.Textbox(label="姓名", placeholder="请输入姓名")
            tgender = gr.Dropdown(gender_map, label="性别")
            ttitle = gr.Dropdown(title_map, label="职称")
            tinsert_button = gr.Button("确认修改")
            tinsert_button.click(fn=teacher_func.update,
                                 inputs=[tid, tname, tgender, ttitle])
        with gr.Tab("删除信息"):
            tid = gr.Textbox(label="工号", placeholder="请输入工号")
            tquery_button = gr.Button("查询")
            tquery_output = gr.Dataframe(headers=["工号", "姓名", "性别", "职称"])
            tquery_button.click(fn=teacher_func.query,
                                inputs=[tid],
                                outputs=[tquery_output])

            tinsert_button = gr.Button("确认删除")
            tinsert_button.click(fn=teacher_func.delete,
                                 inputs=[tid])

        with gr.Tab("添加信息"):
            tid = gr.Textbox(label="工号", placeholder="请输入工号")
            tname = gr.Textbox(label="姓名", placeholder="请输入姓名")
            tgender = gr.Dropdown(gender_map, label="性别", value=1)
            ttitle = gr.Dropdown(title_map, label="职称", value=1)
            tinsert_button = gr.Button("确认添加")
            tinsert_button.click(fn=teacher_func.insert,
                                 inputs=[tid, tname, tgender, ttitle])
    with gr.Tab("📚 课程信息"):
        with gr.Tab("添加信息"):
            pass
        with gr.Tab("删除信息"):
            pass
        with gr.Tab("修改信息"):
            pass
        with gr.Tab("查询信息"):
            pass
    with gr.Tab("📝 发表论文"):
        with gr.Tab("添加信息"):
            pass
        with gr.Tab("删除信息"):
            pass
        with gr.Tab("修改信息"):
            pass
        with gr.Tab("查询信息"):
            pass
    with gr.Tab("💰 承担项目"):
        with gr.Tab("添加信息"):
            pass
        with gr.Tab("删除信息"):
            pass
        with gr.Tab("修改信息"):
            pass
        with gr.Tab("查询信息"):
            pass
    with gr.Tab("🎓 主讲课程"):
        with gr.Tab("添加信息"):
            pass
        with gr.Tab("删除信息"):
            pass
        with gr.Tab("修改信息"):
            pass
        with gr.Tab("查询信息"):
            pass
    with gr.Tab("📊 查询统计"):
        pass

if __name__ == "__main__":
    demo.launch()
