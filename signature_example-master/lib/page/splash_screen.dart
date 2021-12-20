import 'dart:async';

import 'package:flutter/material.dart';
import 'package:signature_example/page/signature_page.dart';

class SplashScreen extends StatefulWidget {
  @override
  _SplashScreenState createState() => _SplashScreenState();
}

class _SplashScreenState extends State<SplashScreen> {
  @override
  void initState() {
    // TODO: implement initState
    super.initState();
    Timer(
        Duration(seconds: 3),
        () => Navigator.of(context).pushReplacement(MaterialPageRoute(
            builder: (BuildContext context) => SignaturePage())));
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      body: Container(
          child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Text(
            'Permainan Edukasi Belajar',
            style: TextStyle(
              fontSize: 32,
              color: Color.fromRGBO(76, 76, 102, 1),
              fontWeight: FontWeight.bold,
            ),
            textAlign: TextAlign.center,
          ),
          SizedBox(
            width: 20,
          ),
          Text(
            'Menulis Angka untuk Murid Taman Kanak-Kanak',
            style: TextStyle(
              fontSize: 24,
              color: Color.fromRGBO(76, 76, 102, 1),
            ),
            textAlign: TextAlign.center,
          ),
        ],
      )),
    );
  }
}
