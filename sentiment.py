from transformers import TextClassificationPipeline, AutoModelForSequenceClassification, AutoTokenizer, pipeline


class SentimentAnalysisDistilBERT:
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


class SentimentAnalysisCryptoBERT:
    def __init__(self, model_name: str = "ElKulako/cryptobert"):
        # Initialize the SentimentAnalysis class with a specified model.
        tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=True)
        model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels = 3)
        self.pipe = TextClassificationPipeline(model=model, tokenizer=tokenizer, max_length=64, truncation=True, padding='max_length')

    def analyze_sentiment(self, text: str) -> dict:
        # Analyze the sentiment of the provided text and return sentiment scores.
        return self.pipe(text)
