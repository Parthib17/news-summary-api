from flask import Flask,request,jsonify

import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest


def summarizer(rawtext):

    stopwords=list(STOP_WORDS)   #stop words
    #print(stopwords)
    nlp = spacy.load('en_core_web_sm')      #small module of spacy
    doc =nlp(rawtext)
    # print(doc)
    tokens = [token.text for token in doc]
    # print(tokens)
    word_freq={}
    for word in doc:
        if word.text.lower() not in stopwords and word.text.lower() not in punctuation:
            if word.text not in word_freq.keys():
                word_freq[word.text]=1
            else:
                word_freq[word.text]+=1
        
    # print(word_freq)

    max_freq= max(word_freq.values())

    for word in word_freq.keys():
        word_freq[word]=word_freq[word]/max_freq

    # print(word_freq)

    sen_tokens=[sent for sent in doc.sents]
    # print(sen_tokens)
    sent_scores={}
    for sent in sen_tokens:
        for word in sent:
            if word.text in word_freq.keys():
                if sent not in sent_scores.keys():
                    sent_scores[sent]=word_freq[word.text]
                else:
                    sent_scores[sent]+=word_freq[word.text]

    # print(sent_scores)
    select_len =int(len(sen_tokens)*0.3)
    summary = nlargest(select_len, sent_scores, key=sent_scores.get)
    final_summary = [word.text for word in summary]
    summary =' '.join(final_summary)
    return summary

app = Flask(__name__)

# @app.route('/')
# def home():
#     return "hello world"

@app.route('/analyze',methods=['GET'])
def analyze():
    if request.method == 'POST':
        rawtext = request.form.get('text')
        # result= {'text':text}
        result = summarizer(rawtext)
    
    return jsonify({'Summary':result})

    
if __name__ == '__main__':
    app.run(debug=True)
    