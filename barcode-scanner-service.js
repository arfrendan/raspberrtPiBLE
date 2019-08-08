var util = require('util');
var bleno = require('bleno');

var BlenoPrimaryService = bleno.PrimaryService;
var BluetoothSubscribeCharacteristic = require('./bluetooth-subscribe-characteristic')

// The service of BLE
// Implement a characteristic for the service
function BarcodeScannerService(codeListener) {
  BarcodeScannerService.super_.call(this, {
      uuid: '00000000000000000000000000000000',
      characteristics: [
          new BluetoothSubscribeCharacteristic(codeListener),
      ]
  });
}

util.inherits(BarcodeScannerService, BlenoPrimaryService);

module.exports = BarcodeScannerService;

