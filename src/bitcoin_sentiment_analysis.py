import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import re
from collections import Counter
import numpy as np
import matplotlib

# 加载数据
file_path = './bitcoin_sentiments_21_24.csv'
df = pd.read_csv(file_path)

# 数据预处理
df['Date'] = pd.to_datetime(df['Date'])
df = df.sort_values(by='Date')

# 定义情绪分类函数
def classify_sentiment(score):
    if score > 0:
        return 'positive'
    elif score < 0:
        return 'negative'
    else:
        return 'neutral'

df['Sentiment_Type'] = df['Accurate Sentiments'].apply(classify_sentiment)

# 情绪分布
sentiment_counts = df['Sentiment_Type'].value_counts()
sentiment_percentage = df['Sentiment_Type'].value_counts(normalize=True) * 100

print("情绪分布:")
print(sentiment_counts)
print("\n情绪分布百分比:")
print(sentiment_percentage)

# 绘制情绪分布饼图
plt.figure(figsize=(8, 8))
plt.pie(sentiment_counts, labels=sentiment_counts.index, autopct='%1.1f%%', startangle=140)
plt.title('Sentiment Distribution of Bitcoin News')
plt.ylabel('')
plt.savefig('sentiment_distribution.png')
plt.show()

# 情绪随时间变化的趋势
df.set_index('Date', inplace=True)
sentiment_over_time = df['Accurate Sentiments'].resample('M').mean()

plt.figure(figsize=(12, 6))
sentiment_over_time.plot(title='Monthly Average Sentiment of Bitcoin News')
plt.xlabel('Date')
plt.ylabel('Average Sentiment')
plt.grid(True)
plt.savefig('sentiment_over_time.png')
plt.show()

# 高频词分析
all_text = ' '.join(df['Short Description'].dropna())

# 清理文本
all_text = re.sub(r'[^\w\s]', '', all_text).lower()

# 分词
words = all_text.split()

# 移除停用词
stopwords = set(WordCloud().stopwords)
words = [word for word in words if word not in stopwords and len(word) > 2]

# 统计词频
word_counts = Counter(words)
most_common_words = word_counts.most_common(20)

print("\n最常见的20个词:")
print(most_common_words)

# 绘制高频词条形图
most_common_df = pd.DataFrame(most_common_words, columns=['Word', 'Frequency'])
plt.figure(figsize=(12, 8))
plt.barh(most_common_df['Word'], most_common_df['Frequency'])
plt.xlabel('Frequency')
plt.title('Top 20 Most Common Words in Bitcoin News')
plt.gca().invert_yaxis()
plt.savefig('most_common_words.png')
plt.show()

# 生成词云
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(all_text)

plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('Word Cloud of Bitcoin News')
plt.savefig('wordcloud.png')
plt.show()

# 负面情绪高频词分析
negative_text = ' '.join(df[df['Sentiment_Type'] == 'negative']['Short Description'].dropna())
negative_text = re.sub(r'[^\w\s]', '', negative_text).lower()
negative_words = negative_text.split()
negative_words = [word for word in negative_words if word not in stopwords and len(word) > 2]
negative_word_counts = Counter(negative_words)
most_common_negative_words = negative_word_counts.most_common(50)

print("\n负面新闻中最常见的50个词:")
print(most_common_negative_words)

# 绘制负面情绪高频词条形图
most_common_negative_df = pd.DataFrame(most_common_negative_words, columns=['Word', 'Frequency'])
plt.figure(figsize=(12, 15))
plt.barh(most_common_negative_df['Word'], most_common_negative_df['Frequency'])
plt.xlabel('Frequency')
plt.title('Top 50 Most Common Words in Negative Bitcoin News')
plt.gca().invert_yaxis()
plt.savefig('most_common_negative_words.png')
plt.show()

# 加载比特币价格数据
btc_price_file = './BTC_All_graph_coinmarketcap.csv'
btc_df = pd.read_csv(btc_price_file, sep=';')

# 数据预处理
btc_df['timestamp'] = pd.to_datetime(btc_df['timestamp'])
btc_df = btc_df.sort_values(by='timestamp')
btc_df.set_index('timestamp', inplace=True)

# 筛选2021-2024年的数据
btc_df = btc_df.loc['2021':'2024']

# 绘制比特币价格走势图
plt.figure(figsize=(12, 6))
btc_df['price'].plot(title='Bitcoin Price Over Time')
plt.xlabel('Date')
plt.ylabel('Price (USD)')
plt.grid(True)
plt.savefig('bitcoin_price_over_time.png')
plt.show()

delta = 0.2
matplotlib.rcParams['font.sans-serif'] = ['SimHei']
matplotlib.rcParams['axes.unicode_minus'] = False

df['Intensity'] = df['Accurate Sentiments'].abs()
df['IntensityBin'] = pd.cut(df['Intensity'], bins=[0, 0.2, 0.6, np.inf], right=False, labels=['低', '中', '高'])
df['PolarityLabel'] = np.where(df['Accurate Sentiments'] > delta, '正面', np.where(df['Accurate Sentiments'] < -delta, '负面', '中性'))
ct = pd.crosstab(df['IntensityBin'], df['PolarityLabel'])
ct_pct = ct / ct.values.sum() * 100
ct_pct = ct_pct.reindex(columns=['负面', '中性', '正面'])
plt.figure(figsize=(10, 6))
ax = ct_pct.plot(kind='bar', stacked=True, color=['#d62728', '#7f7f7f', '#2ca02c'])
ax.set_title('标题情绪极性与强度分布')
ax.set_xlabel('情绪强度区间')
ax.set_ylabel('占比 (%)')
ax.legend(title='情绪极性', loc='upper right')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig('images/fig_title_polarity_intensity_distribution.png')
plt.show()