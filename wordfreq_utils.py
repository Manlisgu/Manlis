import numpy as np
from collections import Counter
from wordcloud import WordCloud # 词云库
from PIL import Image # 图像处理库，用于读取背景图片



def generate_wordcloud(data):
    word_freq = Counter(data)
    background_image_path = "./pics/wordfreq.PNG"
    background_image = Image.open(background_image_path) # 定义词频背景图
    background_array = np.array(background_image)
    # 定义词云样式
    wordcloud = WordCloud(
        font_path='C:/Windows/Fonts/simhei.ttf',  # 设置字体
        width=100,
        height=100,
        background_color='white',
        mask=background_array,  # 使用自定义背景图
        contour_color='black',  # 添加轮廓线
        contour_width=5,  # 轮廓宽度
        max_words=500,  # 最多显示词数
        max_font_size=100  # 字号最大值
    ).generate_from_frequencies(word_freq)  # 从字典生成词云

    return wordcloud