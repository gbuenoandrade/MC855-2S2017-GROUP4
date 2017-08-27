from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer
import nltk
import pickle


class Analyzer:
    def __init__(self, project_path, should_train=False):
        self.project_path = project_path
        self.st = PorterStemmer()
        self.stop_words = set(stopwords.words('english'))
        if should_train:
            self._train()
        else:
            self._load()

    def _tokenize(self, text):
        raw_tokens = word_tokenize(text)
        tokens = []
        for token in raw_tokens:
            # removing stop words and simple punctuation
            if token not in self.stop_words and len(token) >= 2:
                tokens.append(self.st.stem(token.lower()))
        return tokens

    def _load(self):
        with open(self.project_path + '/analyzer/classifier.pickle', 'rb') as f:
            self.classifier = pickle.load(f)

        with open(self.project_path + '/analyzer/words.txt', 'r') as f:
            self.words = set([line.rstrip('\n') for line in f])

    def _get_features(self, tokens):
        features = {}
        for word in self.words:
            features[word] = word in tokens
        return features

    def _train(self):
        self.words = set()
        training = []
        with open(self.project_path + '/analyzer/raw_training.txt', 'r') as f:
            raw = []
            lines = f.readlines()
            for line in lines:
                label = 'pos' if line[0] == '1' else 'neg'
                tokens = self._tokenize(line[2:])
                raw.append((label, tokens))
                self.words |= set(tokens)
            for label, tokens in raw:
                entry = (self._get_features(tokens), label)
                training.append(entry)
        self.classifier = nltk.NaiveBayesClassifier.train(training)
        self.classifier.show_most_informative_features()

        with open(self.project_path + '/analyzer/classifier.pickle', 'wb') as f:
            pickle.dump(self.classifier, f)

        with open(self.project_path + '/analyzer/words.txt', 'w') as f:
            for word in self.words:
                f.write(word+'\n')

    def classify(self, text):
        features = self._get_features(self._tokenize(text))
        ans = self.classifier.prob_classify(features)
        pos = ans._prob_dict['pos']
        neg = ans._prob_dict['neg']
        dist = abs(pos-neg)
        # TODO verify this constant
        if dist > 0.25:
            return 1 if pos > neg else -1
        return 0
