from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import os
import math

app = Flask(__name__)

# Upload folder
UPLOAD_FOLDER = 'static/files'
app.config['UPLOAD_FOLDER'] =  UPLOAD_FOLDER

@app.route('/') 
def index():
    return render_template('index.html')

@app.route('/vfScorer')
def vf_scorer():
    return render_template('vf_scorer.html')

@app.route("/vfScorer", methods=['POST'])

def uploadFiles():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
        # set the file path
        uploaded_file.save(file_path)
        parseCSV(file_path)
        # save the file
    return redirect(url_for('confirm'))

def calc_score(fil, pat):
    pattern_dict = {
        'OOOOO':0.377,
        'OOOOXO':0.894,
        'OOOOXX':0.028,
        'OOOXOO':0.315,
        'OOOXOX':-0.432,
        'OOOXXO':1.139,
        'OOOXXX':0.5,
        'OOXOOO':-0.154,
        'OOXOOX':-0.861,
        'OOXOXO':0.737,
        'OOXOXX':0.169,
        'OOXXOO':0.372,
        'OOXXOX':-0.169,
        'OOXXXO':1.5,
        'OOXXXX':0.897,
        'OXOOOO':-0.547,
        'OXOOOX':-1.25,
        'OXOOXO':0.372,
        'OXOOXX':-0.169,
        'OXOXOO':0.022,
        'OXOXOX':-0.5,
        'OXOXXO':1.169,
        'OXOXXX':0.611,
        'OXXOOO':-0.296,
        'OXXOOX':-0.831,
        'OXXOXO':0.831,
        'OXXOXX':0.296,
        'OXXXOO':0.5,
        'OXXXOX':-0.043,
        'OXXXXO':1.603,
        'OXXXXX':0.893,
        'XXXXOX':-0.894,
        'XXXXOO':-0.028,
        'XXXOXX':-0.315,
        'XXXOXO':0.432,
        'XXXOOX':-1.139,
        'XXXOOO':-0.5,
        'XXOXXX':0.154,
        'XXOXXO':0.861,
        'XXOXOX':-0.737,
        'XXOXOO':-0.169,
        'XXOOXX':-0.372,
        'XXOOXO':0.169,
        'XXOOOX':-1.5,
        'XXOOOO':-0.897,
        'XOXXXX':0.547,
        'XOXXXO':1.25,
        'XOXXOX':-0.372,
        'XOXXOO':0.169,
        'XOXOXX':-0.022,
        'XOXOXO':0.5,
        'XOXOOX':-1.169,
        'XOXOOO':-0.611,
        'XOOXXX':0.296,
        'XOOXXO':0.831,
        'XOOXOX':-0.831,
        'XOOXOO':-0.296,
        'XOOOXX':-0.5,
        'XOOOXO':0.043,
        'XOOOOX':-1.603,
        'XOOOOO':-0.983,
        'XXXXX':0.555   
    }
    
    fil_dict = {
        1: .008,
        2: .02,
        3: .04,
        4: .07,
        5: .16,
        6: .4,
        7: .6,
        8: 1
    }
    mean_dif = 0.299558573
    
    force = fil_dict[fil] 
    k = pattern_dict[pat]
    
    #log of last filament
    fil_log = math.log(force, 10)
    
    exp = (fil_log + (k*mean_dif))
    score = 10**exp
    return(score)
    # 50% threshold=10^[log(force)+kd]

def parseCSV(filePath):
    # Use Pandas to parse the CSV file
    df = pd.read_csv(filePath)
    df['last_fil'] = df['last_fil'].astype(int)
    
    scores = []
    
    for i, row in df.iterrows():
        score = calc_score(row['last_fil'], row['pattern'])
        scores.append(score)
   
    df['result'] = scores
    output_path = os.path.join(app.config['UPLOAD_FOLDER'], 'output.csv')
    df.to_csv(output_path, index=False)
    
    for i,row in df.iterrows():
        print(i,row['data_item'],row['pattern'],row['last_fil'], row['result'])
   

@app.route('/confirm')
def confirm():
    return render_template('confirm.html')

if __name__ == '__main__':
    app.run(debug=True)