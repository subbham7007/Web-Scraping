from flask import Flask, request, jsonify
from googleapiclient.discovery import build
from langdetect import detect, LangDetectException

app = Flask(__name__)

# Set up the YouTube API client
api_key = 'YOUR_API_KEY'
youtube = build('youtube', 'v3', developerKey=api_key)

def get_comments(video_id):
    comments = []
    request = youtube.commentThreads().list(
        part='snippet',
        videoId=video_id,
        textFormat='plainText'
    )
    response = request.execute()
    
    for item in response['items']:
        comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
        comments.append(comment)
    
    return comments

def detect_language(text):
    try:
        return detect(text)
    except LangDetectException:
        return 'unknown'

def filter_comments_by_language(comments, target_language):
    filtered_comments = [comment for comment in comments if detect_language(comment) == target_language]
    return filtered_comments

@app.route('/')
def home():
    return "Welcome to the YouTube Comment Language Filter!"

@app.route('/comments', methods=['GET'])
def comments():
    video_id = request.args.get('video_id')
    target_language = request.args.get('language')
    
    comments = get_comments(video_id)
    filtered_comments = filter_comments_by_language(comments, target_language)
    
    return jsonify(filtered_comments)

if __name__ == '__main__':
    app.run(debug=True)
