# 新闻安全分析期末作业

## 项目简介 

本项目是新闻安全分析课程的期末作业，主要致力于对新闻标题进行情感（Sentiment）和情绪（Emotion）分析。

## 项目结构 

项目文件已整理为以下结构：

- **`data/`**: 存放所有数据文件，包括原始的新闻标题 CSV 数据（如 `reuters_headlines.csv`, `guardian_headlines.csv`）以及模型字典（`.pickle` 文件）。
- **`notebooks/`**: 包含用于数据处理、分析和可视化的 Jupyter Notebooks。
  - 情感分析 (Sentiment Analysis)
  - 情绪分析 (Emotion Analysis)
  - 媒体倾向性分析 (Outlet Bias)
- **`src/`**: 包含核心 Python 脚本。
  - `bitcoin_sentiment_analysis.py`: 比特币情感分析相关代码。
  - `headline_analysis.py`: 标题分析核心逻辑。
  - `outletsBiasRatings.py`: 媒体偏见评分处理。

## 主要功能 (Key Features)

1. **情感与情绪标注**: 使用预训练模型（如 DistilBERT, Roberta）对新闻标题进行情感和情绪标注。
2. **媒体分析**: 分析不同媒体（Outlets）的情感倾向和情绪特征。
3. **加密货币关联**: 探索新闻情感与比特币价格波动之间的潜在联系。

## 使用说明 (Usage)

请在 `notebooks/` 目录下运行相应的 Jupyter Notebook 查看分析过程和结果。
核心逻辑代码位于 `src/` 目录中。
