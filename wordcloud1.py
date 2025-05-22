import requests
from bs4 import BeautifulSoup
import re

def fetch_zhihu_posts(keyword, max_posts=10):
    """
    爬取知乎上与关键词相关的帖子
    :param keyword: 老年人 社交媒体
    :param max_posts: 1000
    :return: 帖子标题和链接列表
    """
    url = f"https://www.zhihu.com/search?q={keyword}&type=content"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    posts = []
    for item in soup.find_all('div', class_='ContentItem', limit=max_posts):
        title = item.find('meta', itemprop='name')
        link = item.find('meta', itemprop='url')
        if title and link:
            posts.append({
                "title": title['content'],
                "link": link['content']
            })
    return posts

def fetch_post_comments(post_link):
    """
    爬取单个帖子的评论
    :param post_link: 帖子链接
    :return: 评论内容列表
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(post_link, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    comments = []
    for comment in soup.find_all('div', class_='RichText'):
        text = comment.get_text(strip=True)
        if text:
            comments.append(text)
    return comments

# 示例：爬取与“武汉市老年人社交媒体”相关的帖子与评论
keyword = "武汉市老年人社交媒体"
posts = fetch_zhihu_posts(keyword, max_posts=5)
all_comments = []
for post in posts:
    print(f"爬取帖子: {post['title']}")
    comments = fetch_post_comments(post['link'])
    all_comments.extend(comments)

# 保存评论数据
with open("zhihu_comments.txt", "w", encoding="utf-8") as f:
    for comment in all_comments:
        f.write(comment + "\n")

import jieba
from wordcloud import WordCloud
import matplotlib.pyplot as plt

def analyze_text(file_path):
    """
    对文本进行分析并生成词云
    :param file_path: 文本文件路径
    """
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    # 使用jieba进行分词
    words = jieba.lcut(text)
    word_count = {}
    for word in words:
        if len(word) > 1:  # 过滤单字
            word_count[word] = word_count.get(word, 0) + 1

    # 生成词云
    wordcloud = WordCloud(
        font_path="simhei.ttf",  # 使用中文字体
        width=800,
        height=400,
        background_color="white"
    ).generate_from_frequencies(word_count)

    # 显示词云
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.show()

# 示例：分析爬取的评论并生成词云
analyze_text("zhihu_comments.txt")