import pandas as pd
import re
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# 定义一个停用词列表
stopwords = set([
    'a', 'about', 'above', 'after', 'again', 'against', 'all', 'am', 'an', 'and', 'any', 'are', "aren't", 'as', 'at',
    'be', 'because', 'been', 'before', 'being', 'below', 'between', 'both', 'but', 'by',
    'can', "can't", 'cannot', 'could', "couldn't", 'did', "didn't", 'do', 'does', "doesn't", 'doing', "don't", 'down', 'during',
    'each', 'few', 'for', 'from', 'further', 'had', "hadn't", 'has', "hasn't", 'have', "haven't", 'having', 'he', "he'd", "he'll", "he's", 'her', 'here', "here's", 'hers', 'herself', 'him', 'himself', 'his', 'how', "how's",
    'i', "i'd", "i'll", "i'm", "i've", 'if', 'in', 'into', 'is', "isn't", 'it', "it's", 'its', 'itself',
    "let's", 'me', 'more', 'most', "mustn't", 'my', 'myself',
    'no', 'nor', 'not', 'of', 'off', 'on', 'once', 'only', 'or', 'other', 'ought', 'our', 'ours', 'ourselves', 'out', 'over', 'own',
    'same', "shan't", 'she', "she'd", "she'll", "she's", 'should', "shouldn't", 'so', 'some', 'such',
    'than', 'that', "that's", 'the', 'their', 'theirs', 'them', 'themselves', 'then', 'there', "there's", 'these', 'they', "they'd", "they'll", "they're", "they've", 'this', 'those', 'through', 'to', 'too',
    'under', 'until', 'up', 'very', 'was', "wasn't", 'we', "we'd", "we'll", "we're", "we've", 'were', "weren't", 'what', "what's", 'when', "when's", 'where', "where's", 'which', 'while', 'who', "who's", 'whom', 'why', "why's", 'with', "won't", 'would', "wouldn't",
    'you', "you'd", "you'll", "you're", "you've", 'your', 'yours', 'yourself', 'yourselves',
    'bitcoin', 'crypto', 'btc' # 添加特定领域的停用词
])

def analyze_headlines(file_path, source_name):
    """
    读取CSV文件，分析'Headlines'列的词频，
    并生成条形图和词云。
    """
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"文件未找到: {file_path}")
        return

    if 'Headlines' not in df.columns:
        print(f"在 {file_path} 中未找到 'Headlines' 列")
        return

    # 将所有标题合并为单个字符串
    text = ' '.join(df['Headlines'].dropna())

    # 清理文本
    text = re.sub(r'[^\w\s]', '', text).lower()

    # 分词并移除停用词
    words = text.split()
    words = [word for word in words if word not in stopwords and len(word) > 2]

    # 计算词频
    word_counts = Counter(words)
    most_common_words = word_counts.most_common(50)

    print(f"\n{source_name} 新闻中前50个最常见的词:")
    print(most_common_words)

    # 创建并保存条形图
    if most_common_words:
        most_common_df = pd.DataFrame(most_common_words, columns=['Word', 'Frequency'])
        plt.figure(figsize=(12, 15))
        plt.barh(most_common_df['Word'], most_common_df['Frequency'])
        plt.xlabel('Frequency')
        plt.title(f'Top 50 Most Common Words in {source_name} Bitcoin News')
        plt.gca().invert_yaxis()
        plt.savefig(f'most_common_{source_name.lower()}_words.png')
        plt.show()

    # 创建并保存词云
    if text:
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.title(f'Word Cloud of {source_name} Bitcoin News')
        plt.savefig(f'{source_name.lower()}_wordcloud.png')
        plt.show()

# --- 主执行 ---
if __name__ == "__main__":
    # 分析CNBC标题
    analyze_headlines('cnbc_headlines.csv', 'CNBC')

    # 分析Guardian标题
    analyze_headlines('guardian_headlines.csv', 'Guardian')

    # 分析Reuters标题
    analyze_headlines('reuters_headlines.csv', 'Reuters')