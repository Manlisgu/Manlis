from openai import OpenAI

classify_prompt_template = """
你的任务是为用户对产品的疑问进行分类。
请仔细阅读用户的问题内容，给出所属类别。类别应该是这些里面的其中一个：{categories}。
直接输出所属类别，不要有任何额外的描述或补充内容。
用户的问题内容会以三个#符号进行包围。

###
{question}
###
"""


def classify_agent(openai_api_model, openai_api_key, category_list, q):
    if "qwen" in openai_api_model:
        client = OpenAI(api_key=openai_api_key, base_url="https://dashscope.aliyuncs.com/compatible-mode/v1")
    elif "moonshot" in openai_api_model:
        client = OpenAI(api_key=openai_api_key, base_url="https://api.moonshot.cn/v1")
    elif "ep" in openai_api_model:
        client = OpenAI(api_key=openai_api_key, base_url="https://ark.cn-beijing.volces.com/api/v3")
    else:
        client = OpenAI()

    formatted_prompt = classify_prompt_template.format(categories="，".join(category_list), question=q)

    response = client.chat.completions.create(
        model=openai_api_model,
        messages=[{"role": "user", "content": formatted_prompt}],
    )
    return response.choices[0].message.content


