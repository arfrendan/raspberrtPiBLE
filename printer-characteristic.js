var util =require('util');
var exec = require('child_process').exec;

var readline = require('readline');
var fs = require('fs');
var iconvLite = require('iconv-lite')
var bleno = require('bleno');
var Descriptor = bleno.Descriptor;
var Characteristic = bleno.Characteristic;

var UUID = require('./UUID')
let uuid = guid4();

var PrinterCharacteristic = function(){
	PrinterCharacteristic.super_.call(this,{
		uuid: UUID.PRINTER_CHARACTERISTIC_ID,
		properties:['notify','read','write'],
		descriptors:[
			new Descriptor({
				uuid: '2901',
				value: 'printer controller'
			})
		]			
	});
} ;

util.inherits(PrinterCharacteristic,Characteristic);

PrinterCharacteristic.prototype.onWriteRequest = function(data, offset, withoutResponse, callback) {
							//var encodeData = iconvLite.decode(data,'gbk');
                            var request = data.toString("utf-8")
                            console.log('Write request: ' + request);
                            switch(request){
                                case 'test':
                                    exec('sudo python3 /home/pi/printerTest.py --line "test line"',function(err,stdout,stderr){
                                            if(stdout.length>1){console.log(stdout)}
                                            if(err){console.info(stderr)}
                                    })
                                    break;
                                
                                
                                case 'feed':
                                    exec('sudo python3 /home/pi/printerTest.py --command "feed"',function(err,stdout,stderr){
                                            if(stdout.length>1){console.log(stdout)}
                                            if(err){console.info(stderr)}
                                    })
                                    break;
                                
                                case 'play':
                                    exec('python3 /home/pi/voiceGenerator.py',function(err,stdout,stderr){
                                            if(stdout.length>1){console.log(stdout)}
                                            if(err){console.info(stderr)}
                                    })
                                    break;
                                    
                                case 'print':
									exec('python3 /home/pi/printerTest.py  --command "print"',function(err,stdout,stderr){
                                            if(stdout.length>1){console.log(stdout)}
                                            if(err){console.info(stderr)}
                                    })
                                    break;
                                    
                                case 'clear':
									fs.unlink('/home/pi/test/input.txt',function(err){
										if(err) throw err;
										fs.writeFile('/home/pi/test/input.txt','','utf8',function(err){
											if(err) throw err;
											console.log('file cleared')
											})
										})
                                    break;
                                    
                                default:
                                /*
                                    exec('sudo python3 /home/pi/printerTest.py --line '+request ,function(err,stdout,stderr){
                                            if(stdout.length>1){console.log(stdout)}
                                            if(err){console.info(stderr)}
                                    })
                                    */
                                    fs.appendFile('/home/pi/test/input.txt', request+"\n",function(err){
                                        if(err){
                                            console.err(err)
                                        }
                                    })
                                    break;
                                    
                            }                                                       
                            callback(this.RESULT_SUCCESS);
 }

function guid4(){
		return 'xxxx'.replace(/[xy]/g,function(c){
			let r = Math.random()*16|0,v=c=='x'?r:(r&0x3|0x8)
			return v.toString(16);
			})
}
module.exports = PrinterCharacteristic;
