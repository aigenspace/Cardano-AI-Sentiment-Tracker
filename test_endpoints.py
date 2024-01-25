import requests
import json
import utils

# Testing the /analyze endpoint of the Flask application
def test_analyze_endpoint():
    # URL of the /analyze endpoint
    url = "http://localhost:5000/analyze"

    # Data to be sent in the request
    data = {"text": "Cardano is the best!"}
    # Sending a POST request to the /analyze endpoint
    response = requests.post(url, json=data)

    # Printing the JSON response received from the server
    print("Response from /analyze endpoint:")
    print(response.json())


def test_analyze_endpoint_tweets(keyword, data):
    # URL of the /analyze endpoint
    url = "http://localhost:5000/analyze"
    # Sending a POST request to the /analyze endpoint
    scores = {}
    for tweet in data['Tweets']:
        input = {"text": tweet["Content"]}
        response = requests.post(url, json=input)
        print("date: ", tweet["Timestamp"])
        print("score: ", response.json())
        for score in response.json():
            label = score['label']
            if label not in scores:
                scores[label] = []
            scores[label].append(score['score'])
    json.dump(scores, open(f'{keyword}_sentiment_scores.json', 'w'))


def test_analyze_endpoint_date_tweets(keyword, data):
    # URL of the /analyze endpoint
    url = "http://localhost:5000/analyze"
    # Sending a POST request to the /analyze endpoint
    scores = {}
    for tweet in data['Tweets']:
        day = str(utils.get_date_from_timestamp(tweet['Timestamp']))
        if scores.get(day) is None:
            scores[day] = {}
        input = {"text": tweet['Content']}
        response = requests.post(url, json=input)
        for score in response.json():
            print(score)
            label = score['label']
            if label not in scores[day]:
                scores[day][label] = []
            scores[day][label].append(score['score'])
    print(scores)
    json.dump(scores, open(f'{keyword}_date_sentiment_scores.json', 'w'))


# Testing the /filter endpoint of the Flask application
def test_filter_endpoint():
    # URL of the /filter endpoint
    url = "http://localhost:5000/filter"

    # Data to be sent in the request, including the text to be filtered
    # and the list of keywords to filter the text with
    data = {
        "text": "Cardano is making great progress in the cryptocurrency market",
        "keywords": ["Cardano", "cryptocurrency"]
    }

    # Sending a POST request to the /filter endpoint
    response = requests.post(url, json=data)

    # Printing the JSON response received from the server
    print("Response from /filter endpoint:")
    print(response.json())
    
# Testing the /filter-and-analyz endpoint of the Flask application
def test_filter_and_analyze_endpoint():  
    url = "http://localhost:5000/filter-and-analyze"
    data = {
        "text": "Cardano is making great progress. The cryptocurrency market is volatile. Many investors are interested in Cardano.",
        "keywords": ["Cardano"]
    }
    response = requests.post(url, json=data)
    print(response.json())

# Running the test functions
if __name__ == "__main__":
    test_analyze_endpoint()
    test_filter_endpoint()
    test_filter_and_analyze_endpoint()
