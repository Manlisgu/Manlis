from langchain.chains import ConversationChain
from langchain_openai import ChatOpenAI
from langchain_community.chat_models.tongyi import ChatTongyi
# from langchain_community.chat_models.moonshot import MoonshotChat
# from langchain_community.chat_models.volcengine_maas import VolcEngineMaasChat

import os
from langchain.memory import ConversationBufferMemory


def get_chat_response(openai_api_model, openai_api_key, prompt, memory):
    if "qwen" in openai_api_model:
        model = ChatTongyi(model=openai_api_model, dashscope_api_key=openai_api_key)
    # elif "moonshot" in openai_api_model:
    #    model = MoonshotChat(model=openai_api_model, moonshot_api_key=openai_api_key)
    # elif "ep" in openai_api_model:
    #    model = VolcEngineMaasChat(model=openai_api_model, api_key=openai_api_key)
    else:
        model = ChatOpenAI(model=openai_api_model, openai_api_key=openai_api_key)

    chain = ConversationChain(llm=model, memory=memory)

    response = chain.invoke({"input": prompt})
    return response["response"]


# memory = ConversationBufferMemory(return_messages=True)
# print(get_chat_response("牛顿提出过哪些知名的定律？", memory, os.getenv("OPENAI_API_KEY")))
# print(get_chat_response("我上一个问题是什么？", memory, os.getenv("OPENAI_API_KEY")))