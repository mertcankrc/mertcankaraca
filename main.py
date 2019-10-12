# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START gae_python37_render_template]

from flask import Flask, render_template, jsonify, request
import requests
from json2html import *

def get_data(startdate,finishdate):
    URL = "http://staging1.alo-tech.com"
    TOKEN = "ag9zfnRlbGVmb25pLXRlc3RyHwsSElRlbmFudEFwcGxpY2F0aW9ucxiAgICw46OcCQyiARVzdGFnaW5nMS5hbG8tdGVjaC5jb20"
    #start_date = "2017-08-01%2013:00:00"
    start_date = startdate.replace("T","%20") + ":00"
    #finish_date = "2017-08-04%2013:00:00"
    finish_date = finishdate.replace("T","%20") + ":00"
    URL = URL + "/api/?function=reportsCDRLogs&startdate=" + start_date + "&finishdate=" + finish_date + "&app_token=" + TOKEN
    r = requests.get(url = URL)
    data = r.json()
    records =data["CallList"]
    return records

app = Flask(__name__)


@app.route('/')
def root():
    return render_template('index.html')

@app.route('/list', methods = ['GET', 'POST'])
def result():
    keys = ["calldate", "called_num", "callerid", "answered", "duration"]
    if request.method == 'POST':
        startdate = str(request.form['Start_Date'])
        finishdate = str(request.form['Finish_Date'])
        records = get_data(startdate,finishdate)
        final_list = [{k: v for k, v in d.items() if k in keys} for d in records]
        #result = json2html.convert(json=final_list)
        return render_template("result.html",keys=keys,entries=final_list)
	

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [START gae_python37_render_template]
