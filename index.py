from googleapiclient.discovery import build
from textblob import TextBlob

# Set up the YouTube Data API
api_key = "AIzaSyChp2YDtdQS0eLVE6lRI7vjrs05ls-rqB0"  # Replace with your API key
youtube = build("youtube", "v3", developerKey=api_key)

# Define the video ID of the YouTube video you want to analyze
video_id = "LSYEnH5fGfk"  # Replace with the actual video ID

# Fetch comments from the video
comments = []
next_page_token = None
while True:
    comment_response = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        pageToken=next_page_token if next_page_token else ""
    ).execute()
    
    for item in comment_response["items"]:
        comments.append(item["snippet"]["topLevelComment"]["snippet"]["textOriginal"])
    
    next_page_token = comment_response.get("nextPageToken")
    
    if not next_page_token:
        break

# Analyze and classify comments
sentiment_counts = {"positive": 0, "negative": 0, "neutral": 0}

for comment in comments:
    analysis = TextBlob(comment)
    sentiment = "neutral"
    if analysis.sentiment.polarity > 0:
        sentiment = "positive"
    elif analysis.sentiment.polarity < 0:
        sentiment = "negative"
    
    sentiment_counts[sentiment] += 1

# Calculate percentages
total_comments = len(comments)
positive_percentage = (sentiment_counts["positive"] / total_comments) * 100
negative_percentage = (sentiment_counts["negative"] / total_comments) * 100
neutral_percentage = (sentiment_counts["neutral"] / total_comments) * 100

print("Overall Sentiment Analysis:")
print(f"Positive Comments: {positive_percentage:.2f}%")
print(f"Negative Comments: {negative_percentage:.2f}%")
print(f"Neutral Comments: {neutral_percentage:.2f}%")