# noinspection PyInterpreter
"""
lda_server.py

Listen for HTTP requests and respond with a list of relevant documents in JSON format

"""


import logging
import pickle

from gensim import corpora, utils, models, similarities

from flask import Flask, request, send_from_directory, send_file
from flask_restful import Resource, Api
#from flask_cors import CORS, cross_origin

from text_cleaning import text_cleaning
from Content import Content


# Set up logging for gensim
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

# Database and backups
DATABASE = './data/content.db'
LDA_BACKUP = './data/lda_model'
DICT_BACKUP = './data/dictionary'
CORPUS_BACKUP = './data/corpus'

# Load database and backups of LDA model, dictionary and corpus
content = Content(DATABASE)
page_ids = content.get_page_ids()

lda = models.LdaModel.load(LDA_BACKUP)
with open (DICT_BACKUP, 'rb') as fp:
    dictionary = pickle.load(fp)
fp.close()
with open (CORPUS_BACKUP, 'rb') as fp:
    corpus = pickle.load(fp)
fp.close()

# Set up a basic webserver
PORT_NUMBER = 5000
app = Flask(__name__,static_url_path='')
# CORS(app)
api = Api(app)


# Get similarity between the documents and the query
def get_similarity(lda, q_vec):
    index = similarities.MatrixSimilarity(lda[corpus])
    sims = index[q_vec]
    return sims


# Query the LDA model
def query_lda_model(query):
    bow = dictionary.doc2bow(text_cleaning.get_cleaned_text(query).split())
    words = [word for word in bow]
    for word in words:
        print('{}: {}'.format(word[0], dictionary[word[0]]))
    q_vec = lda[bow]
    print('query_lda_model(): {}'.format(lda.print_topic(max(q_vec, key=lambda item: item[1])[0])))
    sims = get_similarity(lda, q_vec)
    sims = sorted(enumerate(sims), key=lambda item: -item[1])
    idx = 0
    pids = []
    num_results = 10
    results = []
    while num_results > 0:
        pageid = page_ids[sims[idx][0]]
        if pageid not in pids:
            pids.append(pageid)
            results.append((pageid[0], content.get_page_url_by_id(pageid)[0]))
            num_results -= 1
        idx += 1
    return results


class LdaServer(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        result = {}
        if 'query' in json_data:
            result.update(query_lda_model(json_data['query']))
        else:
            result = 'Incorrect json request'
        return result


api.add_resource(LdaServer,'/lda')

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=PORT_NUMBER)