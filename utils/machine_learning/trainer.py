import nltk
from nltk.stem.lancaster import LancasterStemmer

class Trainer(object):
    def __init__(self, training_data):
        self.training_data = training_data
        self.categories = self.__get_categories()
        self.cat_words = None

    def __get_categories(self):
        return self.training_data.get_categories()

    def create_category_words(self):
        category_words = {}
        for cat in self.categories:
            category_words[cat] = []
        return category_words

    def categorize(self):
        self.cat_words = self.create_category_words()
        stemmer = LancasterStemmer()
        corpus_words = {}
        for data in self.training_data.get_training_data():
            # tokenize each sentence into words
            for word in nltk.word_tokenize(data['name']):
                # ignore a some things
                if word not in ["?", "'s"]:
                    # stem and lowercase each word
                    stemmed_word = stemmer.stem(word.lower())
                    # have we not seen this word already?
                    if stemmed_word not in corpus_words:
                        corpus_words[stemmed_word] = 1
                    else:
                        corpus_words[stemmed_word] += 1

                    # add the word to our words in class list
                        self.cat_words[data['cat']].extend([stemmed_word])

        print(corpus_words)
        print(self.cat_words)

    def calculate_class_score(self, sentence, class_name, show_details=True):
        stemmer = LancasterStemmer()
        score = 0
        # tokenize each word in our new sentence
        for word in nltk.word_tokenize(sentence):
            # check to see if the stem of the word is in any of our classes
            if stemmer.stem(word.lower()) in self.cat_words[class_name]:
                # treat each word with same weight
                score += 1

                if show_details:
                    print("   match: %s" % stemmer.stem(word.lower()))
        return score