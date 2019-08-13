
var util = require('util')
var bleno = require('bleno');
var exec = require('child_process').exec;
var os = require('os')
var BarcodeScannerService = require('./barcode-scanner-service')
var event = require('events')

var http_listener = require('./http_listener')
var codeListener = new http_listener.CodeListener()
var primaryService = new BarcodeScannerService(codeListener);

var express = require('express')
var bodyParse = require('body-parser')


//setting the name of the device
process.env['BLENO_DEVICE_NAME'] = os.hostname()
console.log(os.hostname())
     
      
//creating an http server to listen the barcode scanner
var server = express()
server.use(bodyParse.json())
server.use(bodyParse.urlencoded({extended:false}))
server.listen(3000)
server.post('/',function(request,response){
		var code = request.body
		codeListener.emit("code",code)  //when the server get the code, emit it to the codeListener 
		response.send('get')
})



// init the BLE service
bleno.on('stateChange', function(state) {
  console.log('on -> stateChange: ' + state);
  if (state === 'poweredOn') {
    bleno.startAdvertising('raspberrypi', [primaryService.uuid]);
    console.log(primaryService.uuid)
  } else {
    bleno.stopAdvertising();
  }
});


// logging when a new device is connected to the raspi
bleno.on('accept', function(clientAddress) {
  console.log('on -> accept, client: ' + clientAddress)
  bleno.updateRssi()
})


// logging when the connected device is disconencted
bleno.on('disconnect', function(clientAddress) {
  console.log('advertising stop')
  console.log('on -> disconnect, client: ' + clientAddress)
})


// rssiUpdate, called once when the connnection is established
bleno.on('rssiUpdate', function(rssi) {
  console.log('on -> rssiUpdate: ' + rssi)
})


// mtu change
bleno.on('mtuChange', function(mtu) {
  console.log('on -> mtuChange: ' + mtu)
})

// start to advertising
// set the service of the BLE
// meanwhile executing the python script to get the code
bleno.on('advertisingStart', function(error) {
  console.log('on -> advertisingStart: ' + (error ? 'error ' + error : 'success'));

  if (!error) {
    bleno.setServices([primaryService], function(error){
      console.log('setServices: '  + (error ? 'error ' + error : 'success'));
      //execute a python port request program to get the barcode
      var proc = require('child_process').exec('python3 python/httpRequest.py',function(err,stdout,stderr){
              console.log('[python]executing')
              if(err){
                  console.log(err) 
              }
      })
    });
  }
})

// when stop the advertising
bleno.on('advertisingStop', function() {
  console.log('on -> advertisingStop')
})

// when the service is set
bleno.on('servicesSet', function(error) {
  console.log('on -> servicesSet: ' + (error ? 'error ' + error : 'success'))
});

