class KeywordFiltering:
    def __init__(self, keywords: list = None):
        if keywords is None:
            keywords = []
        self.keywords = [keyword.lower() for keyword in keywords]

    def filter_text(self, text: str) -> list:
        # Split text into sentences
        sentences = text.split('.') 
        # Filter sentences that contain any of the keywords
        filtered_sentences = [sentence.strip() for sentence in sentences if any(keyword in sentence.lower() for keyword in self.keywords)]
        return filtered_sentences