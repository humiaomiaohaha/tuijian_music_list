import json
import random
from typing import List, Dict, Optional
from collections import Counter
import numpy as np
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.llms.base import LLM
from langchain.schema import BaseOutputParser
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter

from music_data import get_all_music_data, generate_user_history

class MusicRecommender:
    """基于LangChain的音乐推荐系统"""
    
    def __init__(self, music_data: List[Dict] = None):
        self.music_data = music_data or get_all_music_data()
        self.user_history = []
        self.user_preferences = {}
        
    def analyze_user_history(self, user_history: List[Dict]) -> Dict:
        """分析用户听歌历史，提取偏好特征"""
        self.user_history = user_history
        
        # 统计特征
        genres = [song['genre'] for song in user_history]
        moods = [song['mood'] for song in user_history]
        tempos = [song['tempo'] for song in user_history]
        themes = [song['lyrics_theme'] for song in user_history]
        years = [song['year'] for song in user_history]
        
        # 计算偏好
        genre_pref = Counter(genres).most_common(3)
        mood_pref = Counter(moods).most_common(2)
        tempo_pref = Counter(tempos).most_common(2)
        theme_pref = Counter(themes).most_common(3)
        
        # 年代偏好
        avg_year = np.mean(years)
        year_range = max(years) - min(years)
        
        # 流行度偏好
        avg_popularity = np.mean([song['popularity'] for song in user_history])
        
        self.user_preferences = {
            'favorite_genres': [g[0] for g in genre_pref],
            'favorite_moods': [m[0] for m in mood_pref],
            'favorite_tempos': [t[0] for t in tempo_pref],
            'favorite_themes': [th[0] for th in theme_pref],
            'average_year': avg_year,
            'year_range': year_range,
            'average_popularity': avg_popularity,
            'total_songs': len(user_history)
        }
        
        return self.user_preferences
    
    def create_music_embeddings(self) -> FAISS:
        """为音乐数据创建向量嵌入"""
        # 为每首歌创建文本描述
        music_descriptions = []
        for song in self.music_data:
            description = f"{song['title']} by {song['artist']} - {song['genre']} - {song['mood']} - {song['tempo']} - {song['lyrics_theme']} - {' '.join(song['tags'])}"
            music_descriptions.append(description)
        
        # 使用文本分割器
        text_splitter = CharacterTextSplitter(
            separator="\n",
            chunk_size=1000,
            chunk_overlap=200
        )
        
        # 创建嵌入
        embeddings = HuggingFaceEmbeddings(
            model_name="D:\Embedding\Embedding",
            model_kwargs={'device': 'cpu'}
        )
        
        # 创建向量存储
        vectorstore = FAISS.from_texts(music_descriptions, embeddings)
        
        return vectorstore
    
    def recommend_by_similarity(self, num_recommendations: int = 10) -> List[Dict]:
        """基于相似度推荐"""
        if not self.user_history:
            return random.sample(self.music_data, num_recommendations)
        
        # 创建向量存储
        vectorstore = self.create_music_embeddings()
        
        # 基于用户历史创建查询
        user_profile = self._create_user_profile()
        
        # 搜索相似歌曲
        similar_docs = vectorstore.similarity_search(user_profile, k=num_recommendations * 2)
        
        # 提取歌曲信息
        recommended_songs = []
        seen_titles = set()
        
        for doc in similar_docs:
            # 从文档内容中提取歌曲信息
            for song in self.music_data:
                if song['title'] in doc.page_content and song['title'] not in seen_titles:
                    recommended_songs.append(song)
                    seen_titles.add(song['title'])
                    if len(recommended_songs) >= num_recommendations:
                        break
            if len(recommended_songs) >= num_recommendations:
                break
        
        return recommended_songs
    
    def recommend_by_preferences(self, num_recommendations: int = 10) -> List[Dict]:
        """基于用户偏好推荐"""
        if not self.user_preferences:
            return random.sample(self.music_data, num_recommendations)
        
        # 计算每首歌的匹配分数
        song_scores = []
        
        for song in self.music_data:
            score = 0
            
            # 流派匹配
            if song['genre'] in self.user_preferences['favorite_genres']:
                score += 3
            
            # 情绪匹配
            if song['mood'] in self.user_preferences['favorite_moods']:
                score += 2
            
            # 节奏匹配
            if song['tempo'] in self.user_preferences['favorite_tempos']:
                score += 2
            
            # 主题匹配
            if song['lyrics_theme'] in self.user_preferences['favorite_themes']:
                score += 2
            
            # 年代匹配（越接近用户偏好的年代分数越高）
            year_diff = abs(song['year'] - self.user_preferences['average_year'])
            if year_diff <= 5:
                score += 2
            elif year_diff <= 10:
                score += 1
            
            # 流行度匹配
            pop_diff = abs(song['popularity'] - self.user_preferences['average_popularity'])
            if pop_diff <= 10:
                score += 1
            
            # 避免推荐用户已经听过的歌
            if song not in self.user_history:
                song_scores.append((song, score))
        
        # 按分数排序并返回推荐
        song_scores.sort(key=lambda x: x[1], reverse=True)
        return [song for song, score in song_scores[:num_recommendations]]
    
    def _create_user_profile(self) -> str:
        """创建用户画像文本"""
        if not self.user_preferences:
            return ""
        
        profile_parts = []
        
        if self.user_preferences['favorite_genres']:
            profile_parts.append(f"Genres: {', '.join(self.user_preferences['favorite_genres'])}")
        
        if self.user_preferences['favorite_moods']:
            profile_parts.append(f"Moods: {', '.join(self.user_preferences['favorite_moods'])}")
        
        if self.user_preferences['favorite_themes']:
            profile_parts.append(f"Themes: {', '.join(self.user_preferences['favorite_themes'])}")
        
        # 添加一些用户听过的歌曲作为参考
        recent_songs = self.user_history[-3:]  # 最近3首歌
        if recent_songs:
            song_names = [f"{song['title']} by {song['artist']}" for song in recent_songs]
            profile_parts.append(f"Recent songs: {', '.join(song_names)}")
        
        return " | ".join(profile_parts)
    
    def generate_playlist_description(self, recommended_songs: List[Dict]) -> str:
        """生成歌单描述"""
        if not recommended_songs:
            return "无法生成推荐歌单"
        
        # 分析推荐歌单的特征
        genres = [song['genre'] for song in recommended_songs]
        moods = [song['mood'] for song in recommended_songs]
        themes = [song['lyrics_theme'] for song in recommended_songs]
        
        genre_counts = Counter(genres)
        mood_counts = Counter(moods)
        theme_counts = Counter(themes)
        
        # 生成描述
        description_parts = []
        
        if mood_counts:
            dominant_mood = mood_counts.most_common(1)[0][0]
            description_parts.append(f"这是一个{dominant_mood}风格的音乐集合")
        
        if genre_counts:
            top_genres = [g[0] for g in genre_counts.most_common(2)]
            description_parts.append(f"主要包含{', '.join(top_genres)}等流派")
        
        if theme_counts:
            top_themes = [t[0] for t in theme_counts.most_common(2)]
            description_parts.append(f"主题围绕{', '.join(top_themes)}展开")
        
        description_parts.append(f"共包含{len(recommended_songs)}首精心挑选的歌曲")
        
        return "，".join(description_parts) + "。"
    
    def get_recommendations(self, user_history: List[Dict], num_recommendations: int = 10) -> Dict:
        """获取音乐推荐"""
        # 分析用户历史
        preferences = self.analyze_user_history(user_history)
        
        # 获取推荐
        similarity_recommendations = self.recommend_by_similarity(num_recommendations)
        preference_recommendations = self.recommend_by_preferences(num_recommendations)
        
        # 合并推荐结果（去重）
        all_recommendations = similarity_recommendations + preference_recommendations
        unique_recommendations = []
        seen_titles = set()
        
        for song in all_recommendations:
            if song['title'] not in seen_titles:
                unique_recommendations.append(song)
                seen_titles.add(song['title'])
                if len(unique_recommendations) >= num_recommendations:
                    break
        
        # 生成歌单描述
        playlist_description = self.generate_playlist_description(unique_recommendations)
        
        return {
            'user_preferences': preferences,
            'recommendations': unique_recommendations,
            'playlist_description': playlist_description,
            'total_recommendations': len(unique_recommendations)
        }

def create_sample_user_history() -> List[Dict]:
    """创建示例用户听歌历史"""
    return generate_user_history(8)

if __name__ == "__main__":
    # 测试推荐系统
    recommender = MusicRecommender()
    
    # 创建示例用户历史
    user_history = create_sample_user_history()
    print("用户听歌历史:")
    for i, song in enumerate(user_history, 1):
        print(f"{i}. {song['title']} - {song['artist']} ({song['genre']})")
    
    print("\n" + "="*50)
    
    # 获取推荐
    recommendations = recommender.get_recommendations(user_history, 10)
    
    print("用户偏好分析:")
    for key, value in recommendations['user_preferences'].items():
        print(f"  {key}: {value}")
    
    print(f"\n推荐歌单描述: {recommendations['playlist_description']}")
    
    print("\n推荐歌曲:")
    for i, song in enumerate(recommendations['recommendations'], 1):
        print(f"{i}. {song['title']} - {song['artist']} ({song['genre']}) - {song['mood']}") 