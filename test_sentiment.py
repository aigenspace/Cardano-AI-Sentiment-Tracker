import requests
import pandas as pd
from datetime import datetime
import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import MaxNLocator


def aggregate_and_save_sentiment_scores(input_csv, output_csv, keyword):
    if os.path.exists(output_csv):
        print(f"{output_csv} already exists. Skipping aggregation.")
        return
    df = pd.read_csv(input_csv)    
    monthly_sentiments = {}

    for _, row in df.iterrows():
        text = row['text']
        date = datetime.strptime(row['date'], '%Y-%m-%d %H:%M:%S')
        month = date.strftime('%Y-%m')

        # Prepare data the POST request
        data = {
            "text": text,
            "keywords": [keyword]
        }

        # Send POST request to the /filter-and-analyze endpoint
        response = requests.post('http://localhost:5000/filter-and-analyze', json=data)
        if response.ok:
            analysis_results = response.json().get('analysis_results', [])

            # Process and store sentiment scores
            for result in analysis_results:
                positive_score = result.get('positive', 0)
                negative_score = result.get('negative', 0)
                if month not in monthly_sentiments:
                    monthly_sentiments[month] = {'positive': [], 'negative': []}
                monthly_sentiments[month]['positive'].append(positive_score)
                monthly_sentiments[month]['negative'].append(negative_score)

    #Save monthly sentiments to a CSV file
    with open(output_csv, 'w') as f:
        f.write('Month,AveragePositive,AverageNegative\n')
        for month, scores in monthly_sentiments.items():
            f.write(f"{month},{sum(scores['positive'])/len(scores['positive']):.2f},{sum(scores['negative'])/len(scores['negative']):.2f}\n")

    print(f"Sentiment scores saved to {output_csv}")

    
def read_and_output_sentiment_scores(output_csv):
    if not os.path.exists(output_csv):
        print(f"{output_csv} does not exist. Please run the aggregation first.")
        return

    df = pd.read_csv(output_csv)
    print(df)


def plot_sentiment_scores(csv_path, keyword, output_image_path):
    df = pd.read_csv(csv_path)

    df['Month'] = pd.to_datetime(df['Month'])
    df.sort_values('Month', inplace=True)
    fig, ax = plt.subplots(figsize=(14, 7))
    ax.plot(df['Month'], df['AveragePositive'], label='Average Positive', marker='o', linestyle='-', linewidth=2, color='blue', markersize=8)
    ax.plot(df['Month'], df['AverageNegative'], label='Average Negative', marker='s', linestyle='-', linewidth=2, color='crimson', markersize=8)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_minor_locator(mdates.WeekdayLocator())
    plt.title('"' + keyword + '"' + ' Monthly Positive and Negative Sentiments in News Headlines', fontsize=18, fontweight='bold', color='navy')
    plt.xlabel('Month', fontsize=16, labelpad=20)
    plt.ylabel('Sentiment Score', fontsize=16, labelpad=20)
    plt.xticks(rotation=45, ha='right', fontsize=14)
    plt.yticks(fontsize=14)
    ax.legend(fontsize=14, loc='upper left', frameon=True, fancybox=True)
    ax.grid(color='grey', linestyle='--', linewidth=0.5, alpha=0.7)
    ax.xaxis.grid(True, 'minor')
    ax.yaxis.grid(True, 'major')
    ax.set_axisbelow(True)
    fig.patch.set_facecolor('whitesmoke')
    ax.set_facecolor('aliceblue')
    ax.xaxis.set_major_locator(MaxNLocator(nbins=6))
    ax.yaxis.set_label_position("right")
    ax.yaxis.tick_right()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(output_image_path, format='png', dpi=300)

    print(f"Plot saved as {output_image_path}") 

if __name__ == "__main__": 
    keyword = "ADA"
    input_csv = 'data/newsdata.csv'
    output_csv = keyword+'_monthly_sentiments.csv'
    aggregate_and_save_sentiment_scores(input_csv, output_csv, keyword)
    read_and_output_sentiment_scores(output_csv)
    
    image_path = keyword+"_sentiment_scores_plot.png"
    plot_sentiment_scores(output_csv, keyword, image_path)

