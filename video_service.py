"""
Video Service Module - Finds and curates educational videos
Uses YouTube Data API (free tier: 10,000 requests/day)
"""

import os
import requests
from typing import List, Dict, Any
from urllib.parse import urlencode

class VideoService:
    def __init__(self):
        self.api_key = os.environ.get('YOUTUBE_API_KEY', '')
        self.base_url = "https://www.googleapis.com/youtube/v3"
        
        # Quality channel IDs for STEM content
        self.trusted_channels = {
            'chemistry': [
                'UCEWpbFLzoYGPfuWUMFPSaoA',  # Organic Chemistry Tutor
                'UCX6b17PVsYBQ0ip5gyeme-Q',  # CrashCourse (Chemistry)
                'UCsXVk37bltHxD1rDPwtNM8Q',  # Khan Academy
            ],
            'physics': [
                'UCJ0-OtVpF0wOKEqT2Z1HEtA',  # ElectroBOOM
                'UCiEHVhv0SBMpP75JbzJShqw',  # For the Love of Physics
            ],
            'mathematics': [
                'UCsXVk37bltHxD1rDPwtNM8Q',  # Khan Academy
                'UCYO_jab_esuFRV4b17AJtAw',  # 3Blue1Brown
            ],
            'engineering': [
                'UCEWpbFLzoYGPfuWUMFPSaoA',  # Organic Chemistry Tutor
                'UC5RFxgG9_6--nxyixhAM1Og',  # Practical Engineering
            ]
        }
    
    def find_educational_videos(self, topic: str, course_code: str = "", 
                                max_results: int = 10, difficulty: str = "intermediate") -> List[Dict[str, Any]]:
        """
        Find relevant educational videos for a topic
        
        Args:
            topic: Search topic (e.g., "organic chemistry reactions")
            course_code: Course code for context
            max_results: Maximum number of videos to return
            difficulty: Difficulty level (beginner, intermediate, advanced)
        
        Returns:
            List of video objects with metadata
        """
        
        # If no API key, return curated mock data
        if not self.api_key:
            return self._get_mock_videos(topic, max_results)
        
        # Enhance search query based on difficulty
        search_query = self._build_search_query(topic, course_code, difficulty)
        
        # Search YouTube
        videos = self._search_youtube(search_query, max_results)
        
        # Filter and rank results
        ranked_videos = self._rank_videos(videos, topic, difficulty)
        
        return ranked_videos[:max_results]
    
    def _build_search_query(self, topic: str, course_code: str, difficulty: str) -> str:
        """Build optimized search query"""
        
        query_parts = [topic]
        
        # Add difficulty modifiers
        if difficulty == "beginner":
            query_parts.append("introduction tutorial basics explained")
        elif difficulty == "intermediate":
            query_parts.append("explained lecture")
        elif difficulty == "advanced":
            query_parts.append("advanced detailed analysis")
        
        # Add course context
        if course_code:
            query_parts.append(f"university {course_code}")
        
        return " ".join(query_parts)
    
    def _search_youtube(self, query: str, max_results: int) -> List[Dict]:
        """Search YouTube API"""
        
        params = {
            'part': 'snippet',
            'q': query,
            'type': 'video',
            'maxResults': max_results * 2,  # Get more to filter
            'order': 'relevance',
            'videoDuration': 'medium',  # 4-20 minutes (good for learning)
            'videoDefinition': 'high',
            'key': self.api_key
        }
        
        try:
            url = f"{self.base_url}/search?{urlencode(params)}"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            videos = []
            
            for item in data.get('items', []):
                video_id = item['id']['videoId']
                snippet = item['snippet']
                
                # Get additional video statistics
                stats = self._get_video_stats(video_id)
                
                videos.append({
                    'video_id': video_id,
                    'title': snippet['title'],
                    'description': snippet['description'],
                    'channel': snippet['channelTitle'],
                    'channel_id': snippet['channelId'],
                    'thumbnail': snippet['thumbnails']['high']['url'],
                    'published_at': snippet['publishedAt'],
                    'url': f"https://www.youtube.com/watch?v={video_id}",
                    'stats': stats
                })
            
            return videos
            
        except Exception as e:
            print(f"YouTube API Error: {e}")
            return []
    
    def _get_video_stats(self, video_id: str) -> Dict:
        """Get video statistics (views, likes, duration)"""
        
        params = {
            'part': 'statistics,contentDetails',
            'id': video_id,
            'key': self.api_key
        }
        
        try:
            url = f"{self.base_url}/videos?{urlencode(params)}"
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            
            data = response.json()
            if data.get('items'):
                item = data['items'][0]
                stats = item.get('statistics', {})
                content = item.get('contentDetails', {})
                
                return {
                    'views': int(stats.get('viewCount', 0)),
                    'likes': int(stats.get('likeCount', 0)),
                    'comments': int(stats.get('commentCount', 0)),
                    'duration': content.get('duration', 'PT0S')
                }
        except:
            pass
        
        return {'views': 0, 'likes': 0, 'comments': 0, 'duration': 'PT0S'}
    
    def _rank_videos(self, videos: List[Dict], topic: str, difficulty: str) -> List[Dict]:
        """Rank videos by quality and relevance"""
        
        def calculate_score(video):
            score = 0
            
            # View count (normalized)
            views = video['stats'].get('views', 0)
            if views > 100000:
                score += 3
            elif views > 10000:
                score += 2
            elif views > 1000:
                score += 1
            
            # Like ratio
            likes = video['stats'].get('likes', 0)
            if views > 0:
                like_ratio = likes / views
                if like_ratio > 0.05:  # 5%+ like ratio is excellent
                    score += 2
                elif like_ratio > 0.02:
                    score += 1
            
            # Trusted channel bonus
            channel_id = video.get('channel_id', '')
            for channels in self.trusted_channels.values():
                if channel_id in channels:
                    score += 5
                    break
            
            # Title relevance (simple keyword matching)
            title_lower = video['title'].lower()
            topic_lower = topic.lower()
            if topic_lower in title_lower:
                score += 3
            
            # Difficulty match
            title_words = title_lower.split()
            if difficulty == "beginner" and any(word in title_words for word in ['introduction', 'basics', 'beginner', 'tutorial']):
                score += 2
            elif difficulty == "advanced" and any(word in title_words for word in ['advanced', 'detailed', 'deep']):
                score += 2
            
            return score
        
        # Sort by score
        videos_with_scores = [(video, calculate_score(video)) for video in videos]
        videos_with_scores.sort(key=lambda x: x[1], reverse=True)
        
        return [video for video, score in videos_with_scores]
    
    def curate_learning_playlist(self, course_code: str, topics: List[str]) -> Dict[str, Any]:
        """
        Create a curated learning playlist for multiple topics
        
        Args:
            course_code: Course code
            topics: List of topics to cover
        
        Returns:
            Structured playlist with videos for each topic
        """
        
        playlist = {
            'course_code': course_code,
            'topics': [],
            'total_videos': 0,
            'estimated_duration': '0:00'
        }
        
        for topic in topics:
            videos = self.find_educational_videos(
                topic=topic,
                course_code=course_code,
                max_results=5,
                difficulty='intermediate'
            )
            
            playlist['topics'].append({
                'topic': topic,
                'videos': videos,
                'count': len(videos)
            })
            
            playlist['total_videos'] += len(videos)
        
        return playlist
    
    def _get_mock_videos(self, topic: str, max_results: int) -> List[Dict]:
        """Return mock video data when API key is not available"""
        
        mock_videos = [
            {
                'video_id': 'mock_001',
                'title': f'Introduction to {topic} - Complete Tutorial',
                'description': f'Learn everything about {topic} in this comprehensive tutorial.',
                'channel': 'Khan Academy',
                'channel_id': 'mock_channel_1',
                'thumbnail': 'https://via.placeholder.com/480x360?text=Video+1',
                'published_at': '2024-01-01T00:00:00Z',
                'url': f'https://www.youtube.com/results?search_query={topic.replace(" ", "+")}',
                'stats': {
                    'views': 150000,
                    'likes': 8500,
                    'comments': 450,
                    'duration': 'PT15M30S'
                }
            },
            {
                'video_id': 'mock_002',
                'title': f'{topic} Explained Simply',
                'description': f'A clear explanation of {topic} with examples.',
                'channel': 'Organic Chemistry Tutor',
                'channel_id': 'mock_channel_2',
                'thumbnail': 'https://via.placeholder.com/480x360?text=Video+2',
                'published_at': '2024-01-15T00:00:00Z',
                'url': f'https://www.youtube.com/results?search_query={topic.replace(" ", "+")}',
                'stats': {
                    'views': 89000,
                    'likes': 4200,
                    'comments': 230,
                    'duration': 'PT12M45S'
                }
            },
            {
                'video_id': 'mock_003',
                'title': f'Advanced {topic} Concepts',
                'description': f'Deep dive into {topic} for university students.',
                'channel': 'MIT OpenCourseWare',
                'channel_id': 'mock_channel_3',
                'thumbnail': 'https://via.placeholder.com/480x360?text=Video+3',
                'published_at': '2024-02-01T00:00:00Z',
                'url': f'https://www.youtube.com/results?search_query={topic.replace(" ", "+")}',
                'stats': {
                    'views': 45000,
                    'likes': 2800,
                    'comments': 156,
                    'duration': 'PT25M15S'
                }
            }
        ]
        
        return mock_videos[:max_results]
    
    def get_video_transcript(self, video_id: str) -> str:
        """
        Get video transcript/subtitles (placeholder - would need youtube-transcript-api)
        
        Args:
            video_id: YouTube video ID
        
        Returns:
            Video transcript text
        """
        
        # This would require the youtube-transcript-api package
        # For now, return a placeholder
        return f"[Transcript for video {video_id} - Requires youtube-transcript-api package]"
