from sentiment import SentimentAnalysisDistilBERT, SentimentAnalysisCryptoBERT
from keywords import KeywordFiltering
from flask import Flask, request, jsonify

class SentimentEndpoint:
    def __init__(self, app: Flask):
        # Initialize the SentimentEndpoint class
        self.app = app
        self.sa = SentimentAnalysisDistilBERT()
        self.kf = KeywordFiltering()

    def display_analysis(self, analysis: dict):
        # Convert the analysis result to a JSON response.
        return jsonify(analysis)

    def customize_analysis(self, keywords: list):
        # Update the keyword filtering based on the provided keywords.
        self.kf = KeywordFiltering(keywords)

    def setup_routes(self):
        # Setup routes for sentiment analysis and keyword filtering.

        @self.app.route('/analyze', methods=['POST'])
        def analyze():
            # Endpoint for performing sentiment analysis on provided text.
            text = request.json.get('text', '')
            sentiment_scores = self.sa.analyze_sentiment(text)
            return self.display_analysis(sentiment_scores)

        @self.app.route('/filter', methods=['POST'])
        def filter():
            # Endpoint for filtering text based on specified keywords.
            text = request.json.get('text', '')
            keywords = request.json.get('keywords', [])
            self.customize_analysis(keywords)
            filtered_text = self.kf.filter_text(text)
            return jsonify({'filtered_text': filtered_text})
        
        @self.app.route('/filter-and-analyze', methods=['POST'])
        def filter_and_analyze():
            # Endpoint for filtering sentences based on specified keywords and then analyzing their sentiment.
            text = request.json.get('text', '')
            keywords = request.json.get('keywords', [])
            self.customize_analysis(keywords)

            # Filter sentences containing the keywords
            filtered_sentences = self.kf.filter_text(text)

            # Analyze sentiment of each filtered sentence
            analysis_results = [self.sa.analyze_sentiment(sentence) for sentence in filtered_sentences]

            return jsonify({'analysis_results': analysis_results})