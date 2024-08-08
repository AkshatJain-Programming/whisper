import whisper
import os
from flask import Flask, request, redirect, url_for, render_template, jsonify


model = whisper.load_model("base")


app = Flask(__name__)
UPLOAD_FOLDER = 'static'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        # If the user does not select a file, the browser submits an empty file without a filename
        if file.filename == '':
            return 'No selected file'
        if file:
            filename = file.filename
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            result = model.transcribe(filepath)
            print(result)
            return redirect(url_for('results', text=result['text']))
    return render_template('index.html')

@app.route('/results')
def results():
    text = request.args.get('text')
    return render_template('results.html', text=text)
  
if __name__ == '__main__':
    app.run(debug=True)
