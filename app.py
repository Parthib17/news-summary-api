from flask import Flask,request,jsonify
from text_summary_model import summarizer

app = Flask(__name__)

@app.route('/')
def home():
    return "hello world"

@app.route('/analyze',methods=['GET','POST'])
def analyze():
    if request.method == 'POST':
        rawtext = request.form.get('text')
        # result= {'text':text}
        result = summarizer(rawtext)
    
    return jsonify({'Summary':result})

    
if __name__ == '__main__':
    app.run(debug=True)
    