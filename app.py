import streamlit as st
import json
import random
from typing import List, Dict
import pandas as pd

from music_data import get_all_music_data, generate_user_history
from music_recommender import MusicRecommender

# 页面配置
st.set_page_config(
    page_title="AI音乐推荐系统",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS样式
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .song-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid #1f77b4;
    }
    .recommendation-section {
        background-color: #e8f4fd;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
    }
    .stats-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        border: 1px solid #dee2e6;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # 主标题
    st.markdown('<h1 class="main-header">🎵 AI音乐推荐系统</h1>', unsafe_allow_html=True)
    
    # 侧边栏
    with st.sidebar:
        st.header("🎛️ 系统设置")
        
        # 用户历史设置
        st.subheader("用户听歌历史")
        history_size = st.slider("历史歌曲数量", 3, 15, 8)
        
        # 推荐设置
        st.subheader("推荐设置")
        num_recommendations = st.slider("推荐歌曲数量", 5, 20, 10)
        
        # 生成新的用户历史
        if st.button("🔄 生成新的用户历史"):
            st.session_state.user_history = generate_user_history(history_size)
            st.session_state.recommendations = None
            st.success("已生成新的用户听歌历史！")
        
        # 显示当前用户历史
        if 'user_history' in st.session_state:
            st.subheader("当前用户历史")
            for i, song in enumerate(st.session_state.user_history, 1):
                st.write(f"{i}. {song['title']} - {song['artist']}")
    
    # 主内容区域
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📊 用户偏好分析")
        
        if 'user_history' not in st.session_state:
            st.session_state.user_history = generate_user_history(history_size)
        
        # 初始化推荐器
        recommender = MusicRecommender()
        
        # 分析用户偏好
        preferences = recommender.analyze_user_history(st.session_state.user_history)
        
        # 显示偏好统计
        col1_1, col1_2 = st.columns(2)
        
        with col1_1:
            st.markdown('<div class="stats-card">', unsafe_allow_html=True)
            st.metric("总听歌数", preferences['total_songs'])
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="stats-card">', unsafe_allow_html=True)
            st.metric("平均年代", f"{preferences['average_year']:.0f}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col1_2:
            st.markdown('<div class="stats-card">', unsafe_allow_html=True)
            st.metric("平均流行度", f"{preferences['average_popularity']:.0f}")
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="stats-card">', unsafe_allow_html=True)
            st.metric("年代跨度", preferences['year_range'])
            st.markdown('</div>', unsafe_allow_html=True)
        
        # 显示详细偏好
        st.subheader("🎯 偏好详情")
        
        # 流派偏好
        if preferences['favorite_genres']:
            st.write("**最喜欢的流派:**")
            for genre in preferences['favorite_genres']:
                st.write(f"• {genre}")
        
        # 情绪偏好
        if preferences['favorite_moods']:
            st.write("**最喜欢的情绪:**")
            for mood in preferences['favorite_moods']:
                st.write(f"• {mood}")
        
        # 主题偏好
        if preferences['favorite_themes']:
            st.write("**最喜欢的主题:**")
            for theme in preferences['favorite_themes']:
                st.write(f"• {theme}")
    
    with col2:
        st.header("🎵 推荐歌单")
        
        # 获取推荐
        if st.button("🎯 生成推荐") or 'recommendations' not in st.session_state:
            with st.spinner("正在分析用户偏好并生成推荐..."):
                st.session_state.recommendations = recommender.get_recommendations(
                    st.session_state.user_history, 
                    num_recommendations
                )
        
        # 显示推荐结果
        if 'recommendations' in st.session_state:
            recommendations = st.session_state.recommendations
            
            # 歌单描述
            st.markdown('<div class="recommendation-section">', unsafe_allow_html=True)
            st.write("**🎼 歌单描述:**")
            st.write(recommendations['playlist_description'])
            st.markdown('</div>', unsafe_allow_html=True)
            
            # 推荐歌曲列表
            st.subheader(f"📋 推荐歌曲 ({len(recommendations['recommendations'])})")
            
            for i, song in enumerate(recommendations['recommendations'], 1):
                with st.container():
                    st.markdown(f"""
                    <div class="song-card">
                        <h4>{i}. {song['title']}</h4>
                        <p><strong>艺术家:</strong> {song['artist']}</p>
                        <p><strong>流派:</strong> {song['genre']} | <strong>情绪:</strong> {song['mood']} | <strong>节奏:</strong> {song['tempo']}</p>
                        <p><strong>主题:</strong> {song['lyrics_theme']} | <strong>年份:</strong> {song['year']} | <strong>流行度:</strong> {song['popularity']}</p>
                        <p><strong>标签:</strong> {', '.join(song['tags'])}</p>
                    </div>
                    """, unsafe_allow_html=True)
    
    # 底部统计信息
    st.markdown("---")
    st.header("📈 数据统计")
    
    all_music = get_all_music_data()
    
    col3, col4, col5, col6 = st.columns(4)
    
    with col3:
        st.metric("总歌曲数", len(all_music))
    
    with col4:
        genres = [song['genre'] for song in all_music]
        unique_genres = len(set(genres))
        st.metric("流派数量", unique_genres)
    
    with col5:
        moods = [song['mood'] for song in all_music]
        unique_moods = len(set(moods))
        st.metric("情绪类型", unique_moods)
    
    with col6:
        years = [song['year'] for song in all_music]
        year_range = max(years) - min(years)
        st.metric("年代跨度", f"{year_range}年")
    
    # 显示数据分布
    st.subheader("📊 数据分布")
    
    col7, col8 = st.columns(2)
    
    with col7:
        # 流派分布
        genre_counts = pd.Series(genres).value_counts()
        st.write("**流派分布:**")
        st.bar_chart(genre_counts)
    
    with col8:
        # 情绪分布
        mood_counts = pd.Series(moods).value_counts()
        st.write("**情绪分布:**")
        st.bar_chart(mood_counts)

if __name__ == "__main__":
    main() 