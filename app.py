from flask import Flask,request, redirect, url_for,render_template
from youtubeapi import get_video_comments
from sentiment_analysis import analyze_sentiment_batch,preprocess 
import matplotlib
matplotlib.use('Agg')  # Use the 'Agg' backend
import matplotlib.pyplot as plt
import pandas as pd
from io import BytesIO
import base64

app=Flask(__name__)

app.config['TEMPLATES_AUTO_RELOAD'] = True


@app.route('/collect_comments', methods=['GET', 'POST'])
def collect_comments():
    if request.method == 'POST':
        youtube_url = request.form['youtube_url']
        # Call your comments collection script with youtube_url
        video_id = youtube_url.split("v=")[1]
        comments = get_video_comments(video_id) # Replace with your script
        predicted_sentiments = analyze_sentiment_batch(comments[0:100])

        positive_comments= round(((predicted_sentiments.count("POSITIVE") / len(predicted_sentiments))*100) , 2)
        neutral_comments= round(((predicted_sentiments.count("NEUTRAL") / len(predicted_sentiments))*100) , 2)
        negative_comments= round(((predicted_sentiments.count("NEGATIVE") / len(predicted_sentiments))*100) , 2)

        sentiments=[positive_comments, neutral_comments, negative_comments]
        label=["positive_comments", "neutral_comments", "negative_comments"]

        plt.pie(sentiments,labels=label)
        image_stream = BytesIO()
        plt.savefig(image_stream, format='png')
        image_stream.seek(0)
        plt.close()

        image_base64 = base64.b64encode(image_stream.read()).decode('utf-8')
        
        print(sentiments)
        return render_template('comments.html', comments=comments, reaction=predicted_sentiments,
                               sentiments=sentiments,img=image_base64)
    return render_template('collect_comments.html')

if __name__=="__main__":
    app.run()
    
