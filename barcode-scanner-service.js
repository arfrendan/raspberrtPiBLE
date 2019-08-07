var util = require('util');
var bleno = require('bleno');
var UUID = require('./UUID')

var BlenoPrimaryService = bleno.PrimaryService;
var uuid = guid4();

var BluetoothSubscribeCharacteristic = require('./bluetooth-subscribe-characteristic')


var uuidr = guid4()
function BarcodeScannerService(codeListener) {
  BarcodeScannerService.super_.call(this, {
      uuid: '00000000000000000000000000000000',
      characteristics: [
          new BluetoothSubscribeCharacteristic(codeListener),
      ]
  });
}

util.inherits(BarcodeScannerService, BlenoPrimaryService);

function guid4(){
		return 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'.replace(/[xy]/g,function(c){
			let r = Math.random()*16|0,v=c=='x'?r:(r&0x3|0x8)
			return v.toString(16);
			})
}
module.exports = BarcodeScannerService;

