import requests
import streamlit as st

# 从 URL 获取 CSV 文件
def get_csv_from_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # 确保请求成功
        return response.text
    except Exception as e:
        st.error(f"读取表格时出错：{e}")
        return None

