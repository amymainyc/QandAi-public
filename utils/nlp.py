import spacy
import scispacy

class NLP:

    def __init__(self):
        self.nlp = spacy.load("en_core_sci_sm")



    def getKeywords(self, question):
        keywords = self.nlp(question).ents
        keywordArr = []
        for k in keywords:
            keywordArr.append(str(k))
        return keywordArr



    def getKeywordSimilarity(self, keywords, message):
        match = 0
        for keyword in keywords:
            if str(keyword).lower() in message.lower():
                match += 1
        if len(keywords) > 0:
            return match / len(keywords)
        else:
            return 0



    def getOverallSimilarity(self, question, message):
        question = self.nlp(question)
        message = self.nlp(message)
        return message.similarity(question)