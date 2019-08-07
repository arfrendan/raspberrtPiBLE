
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



process.env['BLENO_DEVICE_NAME'] = 'raspberrypi'
console.log(os.hostname())
      
      
var server = express()
server.use(bodyParse.json())
server.use(bodyParse.urlencoded({extended:false}))
server.listen(3000)
console.log('port 3000')
server.post('/',function(request,response){
		var code = request.body
		codeListener.emit("code",code)
		response.send('get')
})

bleno.on('stateChange', function(state) {
  console.log('on -> stateChange: ' + state);

  if (state === 'poweredOn') {
    bleno.startAdvertising('raspberrypi', [primaryService.uuid]);
    console.log(primaryService.uuid)
  } else {
    bleno.stopAdvertising();
  }
});

bleno.on('accept', function(clientAddress) {
  console.log('on -> accept, client: ' + clientAddress)
  bleno.updateRssi()
})

bleno.on('disconnect', function(clientAddress) {
  console.log('advertising stop')
  console.log('on -> disconnect, client: ' + clientAddress)
})


bleno.on('rssiUpdate', function(rssi) {
  console.log('on -> rssiUpdate: ' + rssi)
})

bleno.on('mtuChange', function(mtu) {
  console.log('on -> mtuChange: ' + mtu)
})


bleno.on('advertisingStart', function(error) {
  console.log('on -> advertisingStart: ' + (error ? 'error ' + error : 'success'));

  if (!error) {
    bleno.setServices([primaryService], function(error){
      console.log('setServices: '  + (error ? 'error ' + error : 'success'));
      //execute a python port request program to get the barcode
      var proc = require('child_process').exec('python3 /home/pi/httpRequest.py',function(err,stdout,stderr){
              console.log('[python]executing')
              if(err){
                  console.log(err) 
              }
              
      })
      
      
    });
  }
})


bleno.on('advertisingStop', function() {
  console.log('on -> advertisingStop')
})

bleno.on('servicesSet', function(error) {
  console.log('on -> servicesSet: ' + (error ? 'error ' + error : 'success'))
});

