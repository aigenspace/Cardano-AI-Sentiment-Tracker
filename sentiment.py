from transformers import pipeline

class SentimentAnalysis:
    def __init__(self, model_name: str = 'distilbert-base-uncased-finetuned-sst-2-english'):
        # Initialize the SentimentAnalysis class with a specified model.
        self.model_name = model_name
        self.analyzer = pipeline('sentiment-analysis', model=self.model_name)

    def analyze_sentiment(self, text: str) -> dict:
        # Analyze the sentiment of the provided text and return sentiment scores.
        sentiment_scores = {'positive': 0, 'negative': 0, 'neutral': 0}
        result = self.analyzer(text)[0]
        sentiment = result['label'].lower()
        score = result['score']
        sentiment_scores[sentiment] += score
        return sentiment_scores
    