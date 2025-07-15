# 🎵 AI音乐推荐系统

基于LangChain的智能音乐推荐系统，通过分析用户的听歌历史，生成个性化的音乐推荐歌单。

## ✨ 功能特点

- 🎯 **智能推荐**: 基于用户听歌历史分析偏好，生成个性化推荐
- 🧠 **AI驱动**: 使用LangChain和向量嵌入技术进行相似度匹配
- 📊 **偏好分析**: 深度分析用户的流派、情绪、主题偏好
- 🎨 **多界面**: 支持Web界面、命令行界面和API调用
- 📈 **数据可视化**: 提供详细的统计图表和偏好分析
- 💾 **结果导出**: 支持JSON和TXT格式的结果导出

## 🏗️ 系统架构

```
musicList/
├── music_data.py          # 音乐数据管理
├── music_recommender.py   # 核心推荐算法
├── app.py                 # Streamlit Web界面
├── cli.py                 # 命令行界面
├── README.md              # 项目文档
└── requirements.txt       # 依赖包列表
```

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 运行Web界面

```bash
cd musicList
streamlit run app.py
```

### 3. 使用命令行

```bash
cd musicList
python cli.py --history-size 8 --recommendations 10
```

## 📋 使用说明

### Web界面使用

1. 打开浏览器访问 `http://localhost:8501`
2. 在侧边栏调整用户历史数量和推荐数量
3. 点击"生成新的用户历史"创建模拟数据
4. 点击"生成推荐"获取个性化歌单
5. 查看用户偏好分析和推荐结果

### 命令行使用

```bash
# 基本使用
python cli.py

# 自定义参数
python cli.py --history-size 10 --recommendations 15

# 保存结果到文件
python cli.py --save-json --export-txt

# 显示详细信息
python cli.py --verbose
```

### 命令行参数

- `--history-size`: 用户听歌历史数量 (默认: 8)
- `--recommendations`: 推荐歌曲数量 (默认: 10)
- `--save-json`: 保存推荐结果到JSON文件
- `--export-txt`: 导出歌单到文本文件
- `--output-prefix`: 输出文件前缀 (默认: music_recommendations)
- `--verbose`: 显示详细信息

## 🎵 音乐数据库

系统包含丰富的音乐数据，涵盖多种风格：

### 难过抑郁风格歌曲 (20首)
- **Mad World** - Gary Jules (Alternative)
- **Hurt** - Johnny Cash (Country)
- **Creep** - Radiohead (Alternative Rock)
- **Everybody Hurts** - R.E.M. (Alternative Rock)
- **Nothing Compares 2 U** - Sinead O'Connor (Pop)
- **The Sound of Silence** - Disturbed (Rock)
- **Say Something** - A Great Big World & Christina Aguilera (Pop)
- **All of Me** - John Legend (R&B)
- **Someone Like You** - Adele (Pop)
- **Fix You** - Coldplay (Alternative Rock)
- **Skinny Love** - Bon Iver (Indie Folk)
- **The Scientist** - Coldplay (Alternative Rock)
- **How to Save a Life** - The Fray (Alternative Rock)
- **Chasing Cars** - Snow Patrol (Alternative Rock)
- **Bleeding Out** - Imagine Dragons (Alternative Rock)
- **Demons** - Imagine Dragons (Alternative Rock)
- **Let Her Go** - Passenger (Folk)
- **Stay With Me** - Sam Smith (Pop)
- **Hello** - Adele (Pop)
- **When I Was Your Man** - Bruno Mars (Pop)

### 其他风格歌曲
- 快乐风格: Happy, Uptown Funk
- 活力风格: Eye of the Tiger, We Will Rock You

## 🧠 推荐算法

### 1. 用户偏好分析
- **流派偏好**: 统计用户最常听的音乐流派
- **情绪偏好**: 分析用户偏好的音乐情绪
- **节奏偏好**: 识别用户喜欢的音乐节奏
- **主题偏好**: 分析歌词主题偏好
- **年代偏好**: 计算用户偏好的音乐年代
- **流行度偏好**: 分析用户对音乐流行度的偏好

### 2. 相似度匹配
- 使用HuggingFace嵌入模型创建音乐向量表示
- 基于用户画像进行相似度搜索
- 结合用户历史歌曲进行推荐

### 3. 偏好评分
- 流派匹配: +3分
- 情绪匹配: +2分
- 节奏匹配: +2分
- 主题匹配: +2分
- 年代匹配: +1-2分
- 流行度匹配: +1分

## 📊 数据字段

每首歌曲包含以下信息：

```json
{
  "title": "歌曲名",
  "artist": "艺术家",
  "genre": "流派",
  "mood": "情绪",
  "tempo": "节奏",
  "lyrics_theme": "歌词主题",
  "year": "发行年份",
  "popularity": "流行度评分",
  "tags": ["标签1", "标签2", ...]
}
```

## 🔧 技术栈

- **LangChain**: AI框架和向量嵌入
- **HuggingFace**: 句子嵌入模型
- **FAISS**: 向量相似度搜索
- **Streamlit**: Web界面框架
- **Pandas**: 数据处理和可视化
- **NumPy**: 数值计算
- **Tabulate**: 命令行表格显示

## 📈 系统特性

### 智能分析
- 自动分析用户听歌模式
- 识别音乐偏好特征
- 生成个性化推荐

### 多维度推荐
- 基于相似度的推荐
- 基于偏好的推荐
- 混合推荐策略

### 可视化展示
- 用户偏好统计图表
- 音乐数据分布图
- 推荐结果可视化

### 结果导出
- JSON格式的详细数据
- TXT格式的歌单列表
- 支持自定义输出格式

## 🎯 应用场景

- **个人音乐推荐**: 为用户提供个性化歌单
- **音乐发现**: 帮助用户发现新的音乐风格
- **情感匹配**: 根据用户情绪推荐合适的音乐
- **音乐研究**: 分析音乐偏好和趋势
- **教育用途**: 学习音乐推荐算法

## 🔮 未来扩展

- [ ] 集成真实音乐API (Spotify, Apple Music)
- [ ] 添加更多音乐风格和流派
- [ ] 实现实时推荐更新
- [ ] 支持多用户系统
- [ ] 添加音乐情感分析
- [ ] 集成语音识别功能

## 📝 许可证

本项目采用MIT许可证。

## 🤝 贡献

欢迎提交Issue和Pull Request来改进这个项目！

---

**🎵 让AI为您的音乐之旅增添色彩！** 