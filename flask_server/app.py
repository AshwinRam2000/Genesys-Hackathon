from flask import Flask, request,  Response
import requests
import json
import os
from quest import parse, newline
app = Flask(__name__)

at = 'Enter access code'


@app.route('/test',  methods=['GET'])
def test():
    return 'Hello, World!'


@app.route('/listKBS', methods=['GET'])
def listAllKBS():
    url = "https://api.mypurecloud.com/api/v2/knowledge/knowledgebases"
    payload = {}
    headers = {
        'Authorization': ('Bearer ' + at)
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    resp = response.text.encode('utf8')
    print(headers)
    return resp


@app.route('/deleteKBS/<kbid>', methods=['GET'])
def delKBS(kbid):
    url = "https://api.mypurecloud.com/api/v2/knowledge/knowledgebases/" + kbid

    payload = {}
    headers = {
        'organizationId': 'Enter organization id',
        'Authorization': 'Bearer ' + at
    }

    response = requests.request("DELETE", url, headers=headers, data=payload)
    print(response.text.encode('utf8'))

    return 'Success'


@app.route('/addKBS', methods=['POST'])
def addKBD():
    name = request.args.get('name', default='KBS', type=str)
    desc = request.args.get('desc', default='Genesys Hackathon', type=str)
    url = "https://api.mypurecloud.com/api/v2/knowledge/knowledgebases"

    # payload = '{"name" : "{}","description" : "{}","coreLanguage" : "en-US"}'.format(name, desc)
    payload = json.dumps(
        {'name': name, 'description': desc, 'coreLanguage': 'en-US'})

    print('#########')
    print(payload)
    print('#########')

    headers = {
        'organizationId': 'Enter organization id',
        'Authorization': 'Bearer ' + at,
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    resp = response.text.encode('utf8')

    return resp


@app.route("/new", methods=["POST"])
def new():

    new = request.form.get('ques')
    file = request.files['myfile']
    global verbose
    verbose = False
    filename = (file.filename)
    file.save(os.path.join("./", filename))
    filehandle = open(filename, 'r', encoding="utf8")
    textinput = filehandle.read()
    res = newline(textinput, new)
    print(":::::::::")
    print(res)
    return res


@app.route('/addDocs', methods=['POST'])
def addDocs():
    kbid = 'd1c7ceea-753f-4d48-8192-2cf9beb5c74c'
    data = request.json['docs']
    url = 'https://api.mypurecloud.com/api/v2/knowledge/knowledgebases/%s/languages/en-US/documents' % kbid
    headers = {
        'organizationId': 'Enter organization id',
        'Content-Type': 'application/json',
        'Authorization': 'Bearer %s' % at
    }

    mydata = '['
    for i in range(len(data['ques'])):
        mydata += '''{"type": "Faq","faq": {"question": "%s","answer": "%s"}},''' % (
            data['ques'][i], data['ans'][i])

    mydata = mydata[:-1]
    mydata += ']'
    print(mydata)

    response = requests.request(
        "PATCH", url, headers=headers, data=mydata)

    resp = response.text.encode('utf8')
    print(resp)
    return resp


@app.route('/getQues', methods=['POST'])
def getQues():
    file = request.files['myfile']
    global verbose
    verbose = False
    filename = (file.filename)
    file.save(os.path.join("./", filename))
    filehandle = open(filename, 'r', encoding="utf8")
    textinput = filehandle.read()
    question, answers = parse(textinput)

    print("\n")
    # print(question)

    # ques=question

    data = {"ques": question, "ans": answers}
    js = json.dumps(data)
    print(js)
    res = Response(js, status=200, mimetype="application/json")
    return res


@app.route('/getDocs/<kbid>', methods=['GET'])
def getDocs(kbid):
    url = 'https://api.mypurecloud.com/api/v2/knowledge/knowledgebases/%s/languages/en-US/documents' % kbid

    payload = {}
    headers = {
        'organizationId': 'Enter organization id',
        'Content-Type': 'application/json',
        'Authorization': 'Bearer %s' % at
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    resp = response.text.encode('utf8')
    return resp


if __name__ == "__main__":
    app.run(debug=True)
