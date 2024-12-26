import requests
import streamlit as st

# 将修改后的表格上传到指定地址
def upload_csv_to_url(upload_url, csv_data):
    try:
        files = {'file': ('modified_table.csv', csv_data, 'text/csv')}
        response = requests.post(upload_url, files=files)
        response.raise_for_status()
        return response.json()  # 返回响应内容
    except Exception as e:
        st.error(f"上传表格时出错：{e}")
        return None
