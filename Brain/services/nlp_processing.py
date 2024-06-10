import spacy
import subprocess
import sys
import os

# Ensure the parent directory is in sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class NLPProcessor:
    def __init__(self):
        try:
            self.nlp = spacy.load('en_core_web_sm')
        except OSError:
            print("Model 'en_core_web_sm' not found. Installing...")
            subprocess.check_call([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
            self.nlp = spacy.load('en_core_web_sm')

    def tokenize(self, text):
        doc = self.nlp(text)
        return [token.text for token in doc]

    def pos_tagging(self, tokens):
        doc = self.nlp(" ".join(tokens))
        return [(token.text, token.tag_) for token in doc]

    def ner(self, text):
        doc = self.nlp(text)
        return [(ent.text, ent.label_) for ent in doc.ents]

    def lemmatize(self, tokens):
        doc = self.nlp(" ".join(tokens))
        return [token.lemma_.lower() for token in doc]




# Example usage
if __name__ == "__main__":
    nlp_processor = NLPProcessor()
    while True:
        text = input("Enter: ")

        tokens = nlp_processor.tokenize(text)
        print("Tokens:", tokens)

        pos_tags = nlp_processor.pos_tagging(tokens)
        print("POS Tags:", pos_tags)

        named_entities = nlp_processor.ner(text)
        print("Named Entities:", named_entities)
