#!/usr/bin/env python3
"""
AI音乐推荐系统 - 命令行界面
"""

import argparse
import json
import sys
from typing import List, Dict
from tabulate import tabulate

from music_data import get_all_music_data, generate_user_history
from music_recommender import MusicRecommender

def print_banner():
    """打印系统横幅"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                    🎵 AI音乐推荐系统 🎵                      ║
    ║                                                              ║
    ║  基于LangChain的智能音乐推荐，分析用户偏好，生成个性化歌单    ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def display_user_history(user_history: List[Dict]):
    """显示用户听歌历史"""
    print("\n📋 用户听歌历史:")
    print("=" * 60)
    
    table_data = []
    for i, song in enumerate(user_history, 1):
        table_data.append([
            i,
            song['title'],
            song['artist'],
            song['genre'],
            song['mood'],
            song['year']
        ])
    
    headers = ["#", "歌曲名", "艺术家", "流派", "情绪", "年份"]
    print(tabulate(table_data, headers=headers, tablefmt="grid"))

def display_preferences(preferences: Dict):
    """显示用户偏好分析"""
    print("\n🎯 用户偏好分析:")
    print("=" * 60)
    
    print(f"📊 统计信息:")
    print(f"  总听歌数: {preferences['total_songs']}")
    print(f"  平均年代: {preferences['average_year']:.0f}")
    print(f"  年代跨度: {preferences['year_range']}年")
    print(f"  平均流行度: {preferences['average_popularity']:.0f}")
    
    print(f"\n🎵 偏好详情:")
    if preferences['favorite_genres']:
        print(f"  最喜欢的流派: {', '.join(preferences['favorite_genres'])}")
    if preferences['favorite_moods']:
        print(f"  最喜欢的情绪: {', '.join(preferences['favorite_moods'])}")
    if preferences['favorite_tempos']:
        print(f"  最喜欢的节奏: {', '.join(preferences['favorite_tempos'])}")
    if preferences['favorite_themes']:
        print(f"  最喜欢的主题: {', '.join(preferences['favorite_themes'])}")

def display_recommendations(recommendations: Dict):
    """显示推荐结果"""
    print("\n🎵 推荐歌单:")
    print("=" * 60)
    
    print(f"📝 歌单描述: {recommendations['playlist_description']}")
    print(f"📊 推荐数量: {recommendations['total_recommendations']}")
    
    print(f"\n📋 推荐歌曲:")
    table_data = []
    for i, song in enumerate(recommendations['recommendations'], 1):
        table_data.append([
            i,
            song['title'],
            song['artist'],
            song['genre'],
            song['mood'],
            song['tempo'],
            song['year'],
            song['popularity']
        ])
    
    headers = ["#", "歌曲名", "艺术家", "流派", "情绪", "节奏", "年份", "流行度"]
    print(tabulate(table_data, headers=headers, tablefmt="grid"))

def save_recommendations_to_file(recommendations: Dict, filename: str):
    """保存推荐结果到文件"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(recommendations, f, ensure_ascii=False, indent=2)
        print(f"\n💾 推荐结果已保存到: {filename}")
    except Exception as e:
        print(f"\n❌ 保存文件失败: {e}")

def export_playlist_to_txt(recommendations: Dict, filename: str):
    """导出歌单到文本文件"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("🎵 AI推荐歌单\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"歌单描述: {recommendations['playlist_description']}\n\n")
            f.write("推荐歌曲:\n")
            f.write("-" * 30 + "\n")
            
            for i, song in enumerate(recommendations['recommendations'], 1):
                f.write(f"{i:2d}. {song['title']} - {song['artist']}\n")
                f.write(f"    流派: {song['genre']} | 情绪: {song['mood']} | 年份: {song['year']}\n")
                f.write(f"    主题: {song['lyrics_theme']} | 标签: {', '.join(song['tags'])}\n\n")
        
        print(f"\n📄 歌单已导出到: {filename}")
    except Exception as e:
        print(f"\n❌ 导出歌单失败: {e}")

def main():
    parser = argparse.ArgumentParser(
        description="AI音乐推荐系统 - 基于用户听歌历史生成个性化推荐",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  python cli.py --history-size 8 --recommendations 10
  python cli.py --history-size 5 --recommendations 15 --save-json
  python cli.py --history-size 10 --recommendations 20 --export-txt
        """
    )
    
    parser.add_argument(
        '--history-size', 
        type=int, 
        default=8,
        help='用户听歌历史数量 (默认: 8)'
    )
    
    parser.add_argument(
        '--recommendations', 
        type=int, 
        default=10,
        help='推荐歌曲数量 (默认: 10)'
    )
    
    parser.add_argument(
        '--save-json',
        action='store_true',
        help='保存推荐结果到JSON文件'
    )
    
    parser.add_argument(
        '--export-txt',
        action='store_true',
        help='导出歌单到文本文件'
    )
    
    parser.add_argument(
        '--output-prefix',
        type=str,
        default='music_recommendations',
        help='输出文件前缀 (默认: music_recommendations)'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='显示详细信息'
    )
    
    args = parser.parse_args()
    
    # 打印横幅
    print_banner()
    
    try:
        # 初始化推荐器
        print("🚀 初始化音乐推荐系统...")
        recommender = MusicRecommender()
        
        # 生成用户历史
        print(f"📝 生成用户听歌历史 ({args.history_size}首歌曲)...")
        user_history = generate_user_history(args.history_size)
        
        # 显示用户历史
        display_user_history(user_history)
        
        # 获取推荐
        print(f"\n🎯 分析用户偏好并生成推荐 ({args.recommendations}首歌曲)...")
        recommendations = recommender.get_recommendations(user_history, args.recommendations)
        
        # 显示偏好分析
        display_preferences(recommendations['user_preferences'])
        
        # 显示推荐结果
        display_recommendations(recommendations)
        
        # 保存结果
        if args.save_json:
            json_filename = f"{args.output_prefix}.json"
            save_recommendations_to_file(recommendations, json_filename)
        
        if args.export_txt:
            txt_filename = f"{args.output_prefix}.txt"
            export_playlist_to_txt(recommendations, txt_filename)
        
        # 显示详细信息
        if args.verbose:
            print("\n🔍 详细信息:")
            print("=" * 60)
            print(f"音乐数据库大小: {len(recommender.music_data)}首歌曲")
            print(f"用户历史歌曲: {len(user_history)}首")
            print(f"推荐算法: 相似度匹配 + 偏好分析")
            print(f"推荐结果: {len(recommendations['recommendations'])}首歌曲")
        
        print("\n✅ 推荐完成！")
        
    except KeyboardInterrupt:
        print("\n\n⏹️  用户中断操作")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ 发生错误: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main() 