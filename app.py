import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import pygwalker as pyg

from langchain.memory import ConversationBufferMemory
from csv_utils import dataframe_agent
from csv_classify_utils import classify_agent
from pdf_utils import qa_agent
from chatgpt_utils import get_chat_response

import base64
from wordfreq_utils import generate_wordcloud
import matplotlib.pyplot as plt # 图像展示库，以便在notebook中显示图片


# 页面配置
st.set_page_config(page_title="AutoDataAnalyzer", layout="wide")

# 应用标题
st.title("AutoDataAnalyzer - AI大数据分析与可视化")

# 侧边栏导航
st.sidebar.title("导航")
app_mode = st.sidebar.selectbox("选择页面", ["AI车辆性能大数据分析", "AI智能CSV数据分析工具", "AI智能PDF问答工具", "AI智能对话问答工具", "重点议题管理"
    #, "问题管理", "报告生成"
                                             ])

def sidebar_bg(side_bg):
    side_bg_ext = 'png'
    st.markdown(
        f"""
        <style>
        [data-testid="stSidebar"] > div:first-child {{
            background: url(data:image/{side_bg_ext};base64,{base64.b64encode(open(side_bg, "rb").read()).decode()});
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )
# 调用
sidebar_bg('./pics/siderbackground2.jpg')

def background_bg(main_bg):
    main_bg_ext = "png"
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: url(data:image/{main_bg_ext};base64,{base64.b64encode(open(main_bg, "rb").read()).decode()});
            background-size: cover
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
# 调用
background_bg('./pics/background.jpg')

with st.sidebar:
    openai_api_model = st.text_input("请输入ChatAI Model：", type="password")
    st.markdown("[获取OpenAI Model: gpt-3.5-turbo(默认，需要魔法)]()")
    st.markdown("[查阅Qwen Model: qwen-plus(默认)](https://help.aliyun.com/zh/dashscope/developer-reference/tongyi-thousand-questions-metering-and-billing?spm=a2c4g.11186623.help-menu-610100.d_3_5.72785120xkOrE4&scm=20140722.H_2399482._.OR_help-T_cn-DAS-zh-V_1)")
    #st.markdown("[默认kiMi Model: moonshot-v1-8k(默认)](https://www.volcengine.com/docs/82379/1099320)")
    st.markdown("[默认doubao Model: doubao-pro-32k(默认)](https://www.volcengine.com/docs/82379/1099320)")
    openai_api_key = st.text_input("请输入ChatAI API密钥：", type="password")
    st.markdown("[获取OpenAI API key(需要魔法)](https://platform.openai.com/account/api-keys)")
    st.markdown("[获取Qwen API key](https://bailian.console.aliyun.com/?apiKey=1#/api-key)")
    #st.markdown("[获取kiMi API key](https://platform.moonshot.cn/console/api-keys)")
    st.markdown("[获取doubao API key](https://console.volcengine.com/ark/region:ark+cn-beijing/apiKey?apikey=%7B%7D&projectName=undefined)")

def csv_main():
    st.header("💡 AI智能CSV数据分析工具")
    data = st.file_uploader("上传你的数据文件（CSV格式）：", type="csv")
    if data:
        st.session_state["df"] = pd.read_csv(data)
        with st.expander("原始数据"):
            st.dataframe(st.session_state["df"])
    query = st.text_area("请输入你关于以上表格的问题，或数据提取请求，或可视化要求（支持散点图、折线图、条形图）：")
    button = st.button("生成回答")
    def create_chart(input_data, chart_type):
        df_data = pd.DataFrame(input_data["data"], columns=input_data["columns"])
        df_data.set_index(input_data["columns"][0], inplace=True)
        if chart_type == "bar":
            st.bar_chart(df_data)
        elif chart_type == "line":
            st.line_chart(df_data)
        elif chart_type == "scatter":
            st.scatter_chart(df_data)
    if button and not openai_api_model:
        st.info("请输入你的ChatAI Model")
    if button and not openai_api_key:
        st.info("请输入你的ChatAI API密钥")
    if button and "df" not in st.session_state:
        st.info("请先上传数据文件")
    if button and openai_api_model and openai_api_key and "df" in st.session_state:
        with st.spinner("AI正在思考中，请稍等..."):
            response_dict = dataframe_agent(openai_api_model, openai_api_key, st.session_state["df"], query)
            if "answer" in response_dict:
                st.write(response_dict["answer"])
            if "table" in response_dict:
                st.table(pd.DataFrame(response_dict["table"]["data"],
                                      columns=response_dict["table"]["columns"]))
            if "bar" in response_dict:
                create_chart(response_dict["bar"], "bar")
            if "line" in response_dict:
                create_chart(response_dict["line"], "line")
            if "scatter" in response_dict:
                create_chart(response_dict["scatter"], "scatter")

def pdf_main():
    st.header("📑 AI智能PDF问答工具")
    if "memory" not in st.session_state:
        st.session_state["memory"] = ConversationBufferMemory(
            return_messages=True,
            memory_key="chat_history",
            output_key="answer"
        )
    uploaded_file = st.file_uploader("上传你的PDF文件：", type="pdf")
    question = st.text_input("对PDF的内容进行提问", disabled=not uploaded_file)
    if uploaded_file and question and not openai_api_model:
        st.info("请输入你的ChatAI Model")
    if uploaded_file and question and not openai_api_key:
        st.info("请输入你的ChatAI API密钥")
    if uploaded_file and question and openai_api_model and openai_api_key:
        with st.spinner("AI正在思考中，请稍等..."):
            response = qa_agent(openai_api_model, openai_api_key, st.session_state["memory"],
                                uploaded_file, question)
        st.write("### 答案")
        st.write(response["answer"])
        st.session_state["chat_history"] = response["chat_history"]
    if "chat_history" in st.session_state:
        with st.expander("历史消息"):
            for i in range(0, len(st.session_state["chat_history"]), 2):
                human_message = st.session_state["chat_history"][i]
                ai_message = st.session_state["chat_history"][i + 1]
                st.write(human_message.content)
                st.write(ai_message.content)
                if i < len(st.session_state["chat_history"]) - 2:
                    st.divider()

def chatgpt_main():
    st.header("💬 AI智能对话问答工具")
    if "memory" not in st.session_state:
        st.session_state["memory"] = ConversationBufferMemory(return_messages=True)
        st.session_state["messages"] = [{"role": "ai",
                                         "content": "你好，我是你的AI助手，有什么可以帮你的吗？"}]
    for message in st.session_state["messages"]:
        st.chat_message(message["role"]).write(message["content"])
    prompt = st.chat_input()
    if prompt:
        if not openai_api_model:
            st.info("请输入你的ChatAI Model")
            st.stop()
        if not openai_api_key:
            st.info("请输入你的ChatAI API Key")
            st.stop()
        st.session_state["messages"].append({"role": "human", "content": prompt})
        st.chat_message("human").write(prompt)
        with st.spinner("AI正在思考中，请稍等..."):
            response = get_chat_response(openai_api_model, openai_api_key,
                                         prompt, st.session_state["memory"])
        msg = {"role": "ai", "content": response}
        st.session_state["messages"].append(msg)
        st.chat_message("ai").write(response)


def analyze_performance():
    st.header("📊 AI车辆性能大数据分析")
    data_files = st.file_uploader("上传车辆性能数据文件（CSV格式）", type=["csv"], accept_multiple_files=True)
    if data_files:
        for uploaded_file in data_files:
            try:
                st.session_state["df"] = pd.read_csv(uploaded_file)
                st.subheader(f"数据预览 - {uploaded_file.name}")
                with st.expander("原始数据"):
                    st.dataframe(st.session_state["df"])
                st.subheader("故障清单 - 故障描述分类")
                text_input = st.text_input("将需要分类的列，按照格式填写关键词。字段名：异响|漏水|油漆|...")
                button = st.button("生成分类")
                if not button and not text_input:
                    # 使用PyGWalker进行可视化
                    st.subheader("数据可视化")
                    # pyg.walk(data)
                    # 使用PyGWalker生成HTML
                    pyg_html = pyg.to_html(st.session_state["df"])
                    # 将HTML嵌入到Streamlit应用程序中
                    components.html(pyg_html, height=1000, scrolling=True)
                elif button and not text_input:
                    st.info("请先输入分类需求")
                elif button and text_input:
                    if not openai_api_model:
                        st.info("请输入你的ChatAI Model")
                    elif not openai_api_key:
                        st.info("请输入你的ChatAI API密钥")
                    elif "df" not in st.session_state:
                        st.info("请先上传数据文件")
                    elif openai_api_model and openai_api_key and "df" in st.session_state:
                        text_list = text_input.split('：')
                        df_data = pd.DataFrame(st.session_state["df"])
                        question_list = list(df_data[text_list[0].strip()])
                        categories_list = [item.strip() for item in text_list[1].split('|')]
                        if question_list and categories_list:
                            with st.spinner("AI正在思考中，请稍等..."):
                                response_list = []
                                for q in question_list:
                                    response = classify_agent(openai_api_model, openai_api_key, categories_list, q)
                                    response_list += [response]
                                df_data.loc[:,"Classify"] = response_list
                                # 使用image进行词云可视化
                                st.subheader("分类词云")
                                with st.expander("下面是根据分类数据和自定义背景图生成的词云："):
                                    wordcloud = generate_wordcloud(df_data["Classify"])
                                    plt.figure(figsize=(10, 5))
                                    plt.imshow(wordcloud, interpolation='bilinear')
                                    plt.axis('off')  # 不显示坐标轴
                                    st.pyplot(plt)
                                st.subheader("分类数据预览")
                                with st.expander("类别数据"):
                                    st.dataframe(df_data)
                                # 使用PyGWalker进行可视化
                                st.subheader("数据可视化")
                                # pyg.walk(df_data)
                                # 使用PyGWalker生成HTML
                                pyg_html = pyg.to_html(df_data)
                                # 将HTML嵌入到Streamlit应用程序中
                                components.html(pyg_html, height=1000, scrolling=True)
                        else:
                            st.info("请正确输入分类需求")
            except Exception as e:
                st.error(f"加载文件 {uploaded_file.name} 失败：{e}")


def manage_keyissues():
    st.header("📝‍ 重点议题管理平台")
    st.subheader("1️⃣️ 议题创建提交")
    # 问题列表
    # audio_url = "https://www.example.com/audio.mp3"
    # st.audio(audio_url)
    # video_url = "https://www.example.com/video.mp4"
    # st.video(video_url, start_time=0)
    url = "https://forms.office.com/pages/responsepage.aspx?id=RKcqmrK53U-tlatSW_OXlkaV6-0kIfVIiZjfnst8pVJUOFQxUVdQV0k3WkM2UkNIVUFPTUhTNVdEMS4u&origin=lprLink&route=shorturl"
    components.iframe(url, width=1400, height=800)
    # 主界面
    st.subheader("2️⃣ 议题摘要概览")
    # 用户输入 CSV 文件的 URL
    list_url = "https://forms.office.com/Pages/AnalysisPage.aspx?AnalyzerToken=NVXeNdjxe7TrNnMywwkSCP9lqAeAXoeu&id=RKcqmrK53U-tlatSW_OXlkaV6-0kIfVIiZjfnst8pVJUOFQxUVdQV0k3WkM2UkNIVUFPTUhTNVdEMS4u"
    components.iframe(list_url, width=1400, height=800)
    st.subheader("3️⃣ 议题编辑修改")
    edit_url = "https://pbi1u-my.sharepoint.com/:x:/g/personal/guyizhe_pbi1u_onmicrosoft_com/EWoRjmTh3SNOmpnsME1uTHgBqH4OP7sUx3KThEhcly0uhg?e=OXUYeR"
    components.iframe(edit_url, width=1400, height=800)


# 根据导航选择展示不同页面
if app_mode == "AI车辆性能大数据分析":
    analyze_performance()
elif app_mode == "AI智能CSV数据分析工具":
    csv_main()
elif app_mode == "AI智能PDF问答工具":
    pdf_main()
elif app_mode == "AI智能对话问答工具":
    chatgpt_main()
elif app_mode == "重点议题管理":
    manage_keyissues()
