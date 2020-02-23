import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

class MyList extends StatefulWidget {
  Map<String, dynamic> data;
  MyList(this.data);

  @override
  _MyListState createState() => _MyListState(data);
}

class _MyListState extends State<MyList> {
  Map<String, dynamic> mydata;
  _MyListState(this.mydata);

  String tempQues, tempAns;
  Map<String, String> options = {
    'organizationId': 'Enter organizationId',
    'Authorization':
        'Authorization Id'
  };

  List<String> data = [];

  void printWrapped(String text) {
    final pattern = RegExp('.{1,800}'); // 800 is the size of each chunk
    pattern.allMatches(text).forEach((match) => print(match.group(0)));
  }

  @override
  Widget build(BuildContext context) {
    int l = mydata['ques'].length;

    for (var i = 0; i < l; i++) {
      data.add('''{
        "type": "Faq",
        "faq": {
          "question": "${widget.data['ques'][i]}",
          "answer": "${widget.data['ans'][i]}",
        },
      }''');
    }

    printWrapped(data.toString());

    return Scaffold(
      floatingActionButton: FloatingActionButton(
          child: Icon(Icons.check),
          onPressed: () async {
            var req = new http.MultipartRequest(
                "POST", Uri.parse("http://2912044b.ngrok.io/addDocs"));
            print(">>>>>>>>>>>>>>>");
            print(data);
            print("&&&&&&&&&");

            req.fields["docs"] = data.toString();
            print("##########");
            print(req.send());
            showDialog(
                context: context,
                builder: (bc) {
                  return AlertDialog(
                    content: Text('Knowledgebase uploaded successfully'),
                    title: Text('Sucess'),
                    actions: <Widget>[
                      IconButton(
                          icon: Text('Ok'),
                          onPressed: () {
                            Navigator.pop(context);
                          })
                    ],
                  );
                });
          }),
      body: ListView.builder(
        itemCount: l + 2,
        itemBuilder: (bc, i) => i == l
            ? SizedBox(height: 64)
            : Container(
                padding: EdgeInsets.symmetric(vertical: 8, horizontal: 16),
                child: GestureDetector(
                  onTap: () {
                    setState(() {
                      tempQues = widget.data['ques'][i];
                      tempAns = widget.data['ans'][i];
                    });
                    showDialog(
                      context: context,
                      child: AlertDialog(
                        title: Text('Edit Item'),
                        content: Column(
                          mainAxisSize: MainAxisSize.min,
                          children: <Widget>[
                            TextFormField(
                              initialValue: tempQues,
                              decoration: InputDecoration(
                                border: OutlineInputBorder(),
                                hintText: 'Question',
                                labelText: 'Question',
                              ),
                              onChanged: (val) =>
                                  setState(() => tempQues = val),
                            ),
                            SizedBox(height: 16),
                            TextFormField(
                              initialValue: tempAns,
                              decoration: InputDecoration(
                                border: OutlineInputBorder(),
                                hintText: 'Answer',
                                labelText: 'Answer',
                              ),
                              onChanged: (val) => setState(() => tempAns = val),
                            ),
                          ],
                        ),
                        actions: <Widget>[
                          FlatButton(
                              onPressed: () {
                                Navigator.of(context).pop();
                              },
                              child: Text('Cancel')),
                          RaisedButton(
                            color: Colors.blue,
                            child: Text('Ok'),
                            onPressed: () {
                              setState(() {
                                widget.data['question'][i] = tempQues;
                                widget.data['similarity'][i] = tempAns;
                              });
                              Navigator.of(context).pop();
                            },
                          )
                        ],
                      ),
                    );
                  },
                  child: Card(
                    child: Padding(
                      padding: const EdgeInsets.all(8.0),
                      child: Column(
                        children: <Widget>[
                          Text(
                            widget.data['ques'][i],
                            style: TextStyle(
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                          SizedBox(height: 16),
                          Text(widget.data['ans'][i]),
                        ],
                      ),
                    ),
                  ),
                ),
              ),
      ),
    );
  }
}
