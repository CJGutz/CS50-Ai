import nltk
import sys
import os
import numpy as np
import string

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))
    print(query)

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """

    file_dict = dict()

    path = os.path.join(".", directory)
    files = os.listdir(path)

    for file in files:
        path = os.path.join(".", directory, file)

        f = open(path, "r")
        file_dict[file] = f.read()
        f.close()
    
    return file_dict


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """

    words = list()

    tokens = nltk.tokenize.word_tokenize(document)
    for token in tokens:
        if token not in set(list(string.punctuation)) and token not in set(nltk.corpus.stopwords.words("english")):
            words.append(token.lower())

    return words

def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """

    frequency = dict()
    idf = dict()


    for document in documents.values():
        document_set = set(document)
        for word in document_set:
            try: 
                frequency[word] += 1
            except KeyError:
                frequency[word] = 1
            idf[word] = np.log(len(documents)/frequency[word])

    return idf

def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """

    files_ranked = dict()

    for filename in files:
        files_ranked[filename] = 0
        for query_word in query:
            word_count = 0
            for word in files[filename]:
                word_count += 1 if word == query_word else 0

            try:
                files_ranked[filename] += word_count * idfs[query_word]
            except KeyError:
                pass

    files_ranked = dict(sorted(files_ranked.items(), key=lambda tf_idf: tf_idf[1], reverse=True))
    files_ranked = list(files_ranked)[:n]

    return files_ranked

def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """

    sentences_ranked = dict()

    for query_word in query:
        for sentence in sentences.items():
            frequency = 0
            query_word_sum = 0
            for word in sentence[1]:
                if query_word == word:
                    query_word_sum += idfs[query_word]
                    frequency += 1
            sentences_ranked[sentence[0]] = query_word_sum + frequency/len(sentence[1])/100000

    sentences_ranked = dict(sorted(sentences_ranked.items(), key=lambda tf_idf: tf_idf[1], reverse=True))
    sentences_ranked = list(sentences_ranked)[:n]


    return sentences_ranked

if __name__ == "__main__":
    main()
