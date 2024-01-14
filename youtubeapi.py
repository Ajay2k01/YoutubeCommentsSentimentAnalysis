import os
from googleapiclient.discovery import build

# Set your API key here
API_KEY = "AIzaSyBdxgorKD0A_hwm4ou-mWu2XmfcBwITI-c"

# Define the YouTube Data API service
youtube = build('youtube', 'v3', developerKey=API_KEY)

def get_video_comments(video_id):
    comments = []
    results = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        textFormat="plainText",
        maxResults=100  # You can adjust this based on your needs
    ).execute()

    while results:
        for item in results["items"]:
            comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
            likes = item["snippet"]["topLevelComment"]["snippet"]["likeCount"]
            time = item["snippet"]["topLevelComment"]["snippet"]["publishedAt"]
           
            comments.append(comment)

        # Check if there are more pages of results
        if "nextPageToken" in results:
            results = youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                textFormat="plainText",
                maxResults=100,
                pageToken=results["nextPageToken"]
            ).execute()
        else:
            break

    return comments

if __name__ == "__main__":
    video_url = "https://www.youtube.com/watch?v=ksyBX4Ix32s"
    video_id = video_url.split("v=")[1]
    comments = get_video_comments(video_id)
    
    for i, comment in enumerate(comments):
        print(f"Comment {i + 1}: {comment}")
