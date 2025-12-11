import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

# 设置支持中文的字体
matplotlib.rcParams['font.sans-serif'] = ['SimHei']
matplotlib.rcParams['axes.unicode_minus'] = False

# 加载情绪数据
sentiments_df = pd.read_csv('bitcoin_sentiments_21_24.csv')

# 加载比特币价格数据
btc_price_df = pd.read_csv('BTC_All_graph_coinmarketcap.csv', sep=';')
btc_price_df = btc_price_df.rename(columns={'timestamp': 'Date', 'price': 'Price', 'volume': 'Volume'})

# 转换日期列为 datetime 对象
sentiments_df['Date'] = pd.to_datetime(sentiments_df['Date'])
btc_price_df['Date'] = pd.to_datetime(btc_price_df['Date']).dt.normalize() # 标准化为午夜

# 将情绪数据按周二重采样以匹配价格数据
sentiments_weekly = sentiments_df.set_index('Date').resample('W-Tue').agg({
    'Accurate Sentiments': 'mean'
}).rename(columns={'Accurate Sentiments': 'Sentiment'})

# 合并情绪和价格数据
df = pd.merge(btc_price_df, sentiments_weekly, on='Date', how='inner')

# 计算对数回报率
df['Return'] = np.log(df['Price']) - np.log(df['Price'].shift(1))

# 计算波动率（绝对回报率）
df['Volatility'] = df['Return'].abs()

# 将情绪强度定义为情绪得分的绝对值
df['Intensity'] = df['Sentiment'].abs()

# 删除会影响分析的 NaN 值
df.dropna(subset=['Volatility', 'Intensity'], inplace=True)

# 按强度四分位数分组
df['Intensity_Quantile'] = pd.qcut(df['Intensity'], 4, labels=['Q1', 'Q2', 'Q3', 'Q4'], duplicates='drop')

# 计算每个分位数的平均波动率
volatility_by_quantile = df.groupby('Intensity_Quantile')['Volatility'].mean()

# --- 可视化 ---
plt.figure(figsize=(10, 6))
volatility_by_quantile.plot(kind='bar', color=['skyblue', 'lightgreen', 'gold', 'salmon'])

# 按要求设置中文标题和标签
plt.title('按情绪强度四分位分组的比特币波动率比较', fontsize=16)
plt.xlabel('情绪强度四分位', fontsize=12)
plt.ylabel('平均波动率 (|收益率|)', fontsize=12)
plt.xticks(rotation=0, fontsize=10)
plt.yticks(fontsize=10)
plt.grid(axis='y', linestyle='--', alpha=0.7)

# 保存图表
plt.savefig('images/sentiment_volatility_analysis.png', bbox_inches='tight')

# 显示图表
plt.show()

print("分析完成。图表已保存至 images/sentiment_volatility_analysis.png")
print(volatility_by_quantile)