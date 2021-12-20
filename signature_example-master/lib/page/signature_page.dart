import 'dart:typed_data';

import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:signature/signature.dart';
import 'package:signature_example/page/signature_preview_page.dart';
import 'dart:math';

class SignaturePage extends StatefulWidget {
  @override
  _SignaturePageState createState() => _SignaturePageState();
}

class _SignaturePageState extends State<SignaturePage> {
  SignatureController controller;
  Random random = new Random();
  int randomNumber = 0;

  @override
  void initState() {
    super.initState();

    controller = SignatureController(
      penStrokeWidth: 10,
      penColor: Colors.white,
    );
    randomNumber = random.nextInt(10);
  }

  @override
  void dispose() {
    controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) => Scaffold(
        body: SafeArea(
          child: Column(
            children: <Widget>[
              Container(
                child: Center(
                  child: Text(
                    randomNumber.toString(),
                    style: TextStyle(fontSize: 42),
                  ),
                ),
                height: MediaQuery.of(context).size.height * 0.1,
              ),
              Signature(
                controller: controller,
                backgroundColor: Colors.black,
              ),
              buildButtons(context),
              // buildSwapOrientation(),
            ],
          ),
        ),
      );

  Widget buildSwapOrientation() {
    final isPortrait =
        MediaQuery.of(context).orientation == Orientation.portrait;

    return GestureDetector(
      behavior: HitTestBehavior.opaque,
      onTap: () {
        final newOrientation =
            isPortrait ? Orientation.landscape : Orientation.portrait;

        controller.clear();
        setOrientation(newOrientation);
      },
      child: Container(
        padding: EdgeInsets.symmetric(vertical: 8),
        child: Row(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(
              isPortrait
                  ? Icons.screen_lock_portrait
                  : Icons.screen_lock_landscape,
              size: 40,
            ),
            const SizedBox(width: 12),
            Text(
              'Tap to change painting orientation',
              style: TextStyle(fontWeight: FontWeight.bold),
            ),
          ],
        ),
      ),
    );
  }

  Widget buildButtons(BuildContext context) => Container(
        color: Colors.black,
        child: Row(
          mainAxisAlignment: MainAxisAlignment.spaceEvenly,
          children: <Widget>[
            buildCheck(context),
            buildRandom(),
            buildClear(),
          ],
        ),
      );

  Widget buildCheck(BuildContext context) => IconButton(
        iconSize: 36,
        icon: Icon(Icons.check, color: Colors.green),
        onPressed: () async {
          if (controller.isNotEmpty) {
            final signature = await exportSignature();

            await Navigator.of(context).push(MaterialPageRoute(
              builder: (context) => SignaturePreviewPage(
                  signature: signature, number: randomNumber),
            ));

            controller.clear();
          }
        },
      );

  Widget buildRandom() => TextButton(
        child: Text('Random Number'),
        // iconSize: 36,
        // icon: Icon(Icons.disc_full, color: Colors.green),
        onPressed: () {
          setState(() {
            randomNumber = random.nextInt(10);
          });
        },
      );

  Widget buildClear() => IconButton(
        iconSize: 36,
        icon: Icon(Icons.clear, color: Colors.red),
        onPressed: () => controller.clear(),
      );

  Future<Uint8List> exportSignature() async {
    final exportController = SignatureController(
      penStrokeWidth: 50,
      penColor: Colors.white,
      exportBackgroundColor: Colors.black,
      points: controller.points,
    );

    final signature = await exportController.toPngBytes();
    exportController.dispose();

    return signature;
  }

  void setOrientation(Orientation orientation) {
    if (orientation == Orientation.landscape) {
      SystemChrome.setPreferredOrientations([
        DeviceOrientation.landscapeRight,
        DeviceOrientation.landscapeLeft,
      ]);
    } else {
      SystemChrome.setPreferredOrientations([
        DeviceOrientation.portraitUp,
        DeviceOrientation.portraitDown,
      ]);
    }
  }
}
