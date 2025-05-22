# -*- coding: utf-8 -*-
import jieba
import numpy as np
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA


# 设置中文字体（根据实际系统字体名称调整）
plt.rcParams['font.sans-serif'] = ['SimHei']  # Windows常用黑体
plt.rcParams['axes.unicode_minus'] = False    # 解决负号"-"显示为方块的问题

# 1. 读取数据
with open('data for clustering.txt', 'r', encoding='utf-8') as f:
    names = eval(f.read())  # 直接读取列表

# 2. 中文分词（精确模式）
def tokenize(text):
    return ' '.join(jieba.lcut(text))

corpus = [tokenize(name) for name in names]

# 3. 生成词频矩阵
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(corpus)
print("词袋特征:", vectorizer.get_feature_names_out())

# 4. 计算TF-IDF权重
transformer = TfidfTransformer()
tfidf = transformer.fit_transform(X)
weight = tfidf.toarray()

# 5. KMeans聚类（分为3类，可根据数据调整）
n_clusters = 4
kmeans = KMeans(n_clusters=n_clusters, random_state=42)
y_pred = kmeans.fit_predict(weight)

# 6. PCA降维可视化
pca = PCA(n_components=2)
new_data = pca.fit_transform(weight)
x = new_data[:, 0]
y = new_data[:, 1]

# 7. 绘制聚类结果
plt.figure(figsize=(10, 6))
plt.scatter(x, y, c=y_pred, s=100, cmap='viridis', marker='o')
plt.title(f'KMeans聚类结果 (n_clusters={n_clusters})')
plt.xlabel('PCA Component 1')
plt.ylabel('PCA Component 2')

# 添加标签
for i, name in enumerate(names):
    plt.annotate(name, (x[i], y[i]), fontsize=8, alpha=0.7)

plt.show()

# 8. 输出聚类分组
clusters = {}
for idx, label in enumerate(y_pred):
    if label not in clusters:
        clusters[label] = []
    clusters[label].append(names[idx])

print("\n聚类结果:")
for label, items in clusters.items():
    print(f"\n类别 {label}:")
    print("\n".join(items))