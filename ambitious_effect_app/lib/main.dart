import 'dart:async';
import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:flutter/material.dart';
import 'package:pedometer/pedometer.dart';
import 'package:permission_handler/permission_handler.dart';


void main() {
  runApp(MT());
}

class MT extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(home: MyApp());
  }
}

class MyApp extends StatefulWidget {
  @override
  _MyAppState createState() => _MyAppState();
}

class _MyAppState extends State<MyApp> {
  Stream<StepCount> _stepCountStream;
  Stream<PedestrianStatus> _pedestrianStatusStream;
  String _status = '?';
  int _steps = 0;
  int _sent_steps = 0;
  String _answer_text = '';
  String _username = '';
  String _hostname = '';
  final Map<String, String> _json_headers = {
    'content-type': 'application/json'
  };
  String get _addStepsEndpoint {
    return "http://" + _hostname + "/steps/" + _username;
  }
  String get _chatQuestionEndpoint {
    return "http://" + _hostname + "/chat/question/" + _username;
  }

  @override
  void initState() {
    super.initState();
    initPlatformState();
  }

  void onStepCount(StepCount event) {
    print(event);
    setState(() {
      int newSteps = event.steps;
      _steps = newSteps;

      String body = json.encode({
        "steps": newSteps - _sent_steps
      });
      http.post(_addStepsEndpoint, headers: _json_headers, body: body).
        then((response){
          if(response.statusCode == 201) {
            _sent_steps = newSteps;
          }
      });
    });
  }

  void onPedestrianStatusChanged(PedestrianStatus event) {
    print(event);
    setState(() {
      _status = event.status;
    });
  }

  void onPedestrianStatusError(error) {
    print('onPedestrianStatusError: $error');
    setState(() {
      _status = 'Pedestrian Status not available';
    });
    print(_status);
  }

  void onStepCountError(error) {
    print('onStepCountError: $error');
    setState(() {
      _steps = 0;
    });
  }

  void initPlatformState() {
    _pedestrianStatusStream = Pedometer.pedestrianStatusStream;
    _pedestrianStatusStream
        .listen(onPedestrianStatusChanged)
        .onError(onPedestrianStatusError);

    _stepCountStream = Pedometer.stepCountStream;
    _stepCountStream.listen(onStepCount).onError(onStepCountError);

    if (!mounted) return;
  }

  void updateUsername(String username) {
    _username = username;
  }

  void updateHost(String host) {
    _hostname = host;
  }

  void queryChatbot(String question) {
    String body = json.encode({
      "question": question,
    });
    http.post(_chatQuestionEndpoint, headers: _json_headers, body: body).
    then((response){
      if(response.statusCode == 200) {
        setState(() {
          var answer = json.decode(response.body)['answer'];
          _answer_text = answer;
        });
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        appBar: AppBar(
          title: const Text('AmbitiousEffect'),
          actions: <Widget>[
            IconButton(
              icon: const Icon(Icons.settings),
              onPressed: () async {
                var hasOpened = openAppSettings();
                debugPrint('App Settings opened: ' + hasOpened.toString());
              },
            )
          ],
        ),
        body: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: <Widget>[
              Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: <Widget>[
                  Container(
                    height: 30,
                    width: 200,
                    child: TextField(
                        decoration: InputDecoration(
                          border: OutlineInputBorder(),
                          labelText: 'Username',
                        ),
                        onSubmitted: updateUsername,
                      ),
                  ),
                ],
              ),
              Divider(
                height: 10,
                thickness: 0,
                color: Colors.white,
              ),
              Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: <Widget>[
                  Container(
                    height: 35,
                    width: 200,
                    child: TextButton(
                      child: Text(
                          'Configure host'
                      ),
                      onPressed: () {
                        showDialog(
                          context: context,
                          builder: (context) {
                            return AlertDialog(
                              title: Text('Configure host'),
                              content: TextField(
                                decoration: InputDecoration(
                                  border: OutlineInputBorder(),
                                  labelText: 'Host',
                                ),
                                onSubmitted: updateHost,
                              ),
                            );
                          },
                        );
                      },
                    ),
                  ),
                ]
              ),
              Divider(
                height: 25,
                thickness: 0,
                color: Colors.white,
              ),
              Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: <Widget>[
                  Container(
                    height: 100,
                    width: 300,
                    child: TextField(
                      // maxLines: 3,
                      decoration: InputDecoration(
                        border: OutlineInputBorder(),
                        labelText: 'Question',
                      ),
                      onSubmitted: queryChatbot,
                    ),
                  ),
                ],
              ),
              Divider(
                height: 25,
                thickness: 0,
                color: Colors.white,
              ),
              Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: <Widget>[
                  Container(
                    decoration: BoxDecoration(
                      border: Border.all(
                          width: 3.0
                      ),
                      borderRadius: BorderRadius.all(
                          Radius.circular(5.0) //                 <--- border radius here
                      ),
                    ),
                    height: 100,
                    width: 300,
                    child: Flexible(
                      child: Text(
                        _answer_text,
                      ),
                    ),
                  ),
                ],
              ),
              Divider(
                height: 25,
                thickness: 0,
                color: Colors.white,
              ),
              Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: <Widget>[
                  Text(
                    'Steps taken:',
                    style: TextStyle(fontSize: 10),
                  ),
                  Text(
                    _steps.toString(),
                    style: TextStyle(fontSize: 20),
                  ),
                  VerticalDivider( 
                    width: 25,
                    thickness: 0,
                    color: Colors.white,
                  ),
                  Text(
                    'Pedestrian status:',
                    style: TextStyle(fontSize: 10),
                  ),
                  Icon(
                    _status == 'walking'
                      ? Icons.directions_walk
                      : _status == 'stopped'
                      ? Icons.accessibility_new
                      : Icons.error,
                    size: 25,
                  ),
                  Center(
                    child: Text(
                      _status,
                      style: _status == 'walking' || _status == 'stopped'
                        ? TextStyle(fontSize: 20)
                        : TextStyle(fontSize: 15, color: Colors.red),
                    ),
                  ),
                ],
              ),
            ],
          )
        ),

    );
  }
}
