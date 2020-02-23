import 'dart:convert';
import 'dart:io';

import 'package:admin/list.dart';
import 'package:file_picker/file_picker.dart';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:permission/permission.dart';

void main() {
  runApp(MyApp());
  Permission.requestPermissions([PermissionName.Storage]);
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: HomePage(),
    );
  }
}
class HomePage extends StatefulWidget {
  const HomePage({
    Key key,
  }) : super(key: key);

  @override
  _HomePageState createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  Widget homeWidget;

  Future<Null> uploadTextDoc(BuildContext context) async {
    File _file = await FilePicker.getFile(
      fileExtension: 'txt',
      type: FileType.CUSTOM,
    );
    _upload(_file.path, context);
  }

  Future<Null> _upload(String file, BuildContext context) async {
    Map<String, dynamic> qna;
    print('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^');
    var request = new http.MultipartRequest(
      "POST",
      Uri.http(
        "2912044b.ngrok.io",
        "/getQues",
      ),
    );

    request.files.add(await http.MultipartFile.fromPath('myfile', file));

    setState(() {
      homeWidget = CircularProgressIndicator();
    });

    await request.send().then((response) async {
      if (response.statusCode == 200) {
        print("Uploaded!");
      }

      dynamic resp = (await response.stream.bytesToString());
      print(resp);
      qna = jsonDecode(resp.toString());
      print(qna);
    });

    Navigator.of(context).push(MaterialPageRoute(
      builder: (bc) => MyList(qna),
    ));
  }

  @override
  void initState() {
    homeWidget = Column(
      mainAxisSize: MainAxisSize.min,
      children: <Widget>[
        RaisedButton(
          onPressed: () => uploadTextDoc(context),
          child: Text('Upload .txt file'),
        ),
      ],
    );
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: homeWidget,
      ),
    );
  }
}
