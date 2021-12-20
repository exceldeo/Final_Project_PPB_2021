import 'dart:io';
import 'dart:typed_data';

import 'package:flutter/material.dart';
// import 'package:image_gallery_saver/image_gallery_saver.dart';
// import 'package:permission_handler/permission_handler.dart';
import 'package:signature_example/utils.dart';
import 'dart:convert';
import 'package:http/http.dart' as http;

class SignaturePreviewPage extends StatelessWidget {
  final Uint8List signature;
  final int number;

  const SignaturePreviewPage({
    Key key,
    @required this.signature,
    @required this.number,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) => Scaffold(
        backgroundColor: Colors.white,
        appBar: AppBar(
          leading: CloseButton(),
          title: Text('Preview Painting'),
          centerTitle: true,
          actions: [
            IconButton(
              icon: Icon(Icons.done),
              onPressed: () => storeSignature(context),
            ),
            const SizedBox(width: 8),
          ],
        ),
        body: Center(
          child: Image.memory(signature, width: double.infinity),
        ),
      );

  Future storeSignature(BuildContext context) async {
    // print("test1");
    // print(signature);
    // print("test2");

    final imageEncoded = base64.encode(signature); // returns base64 string

    // print("test3");
    // print("data:image/jpg;base64," + imageEncoded);
    // print("test4");

    var data = "data:image/jpg;base64," + imageEncoded;

    var url = Uri.parse('http://192.168.18.81:5000/test');
    final response = await http.post(url, body: imageEncoded);

    print(response.body);

    // final status = await Permission.storage.status;
    // if (!status.isGranted) {
    //   await Permission.storage.request();
    // }

    // final time = DateTime.now().toIso8601String().replaceAll('.', ':');
    // final name = 'signature_$time.png';

    // final result = await ImageGallerySaver.saveImage(signature, name: name);
    // final isSuccess = result['isSuccess'];

    // if (isSuccess) {
    Navigator.pop(context);

    if (response.body == number.toString()) {
      Utils.showSnackBar(
        context,
        text: 'Angka yang anda tulis adalah ' + response.body,
        color: Colors.green,
      );
    } else {
      Utils.showSnackBar(
        context,
        text: 'Angka yang anda tuliskan salah',
        color: Colors.red,
      );
    }
  }
}
