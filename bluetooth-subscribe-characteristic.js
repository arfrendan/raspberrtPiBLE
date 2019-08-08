var util =require('util');
var os =require('os');
var exec = require('child_process').exec;
var execS = require('child_process').execSync;

var fs = require('fs');
var UUID = require('./UUID')
var bleno = require('bleno');
var Descriptor = bleno.Descriptor;
var Characteristic = bleno.Characteristic;
var event = require('events')

var base64arraybuffer = require('./base64-arraybuffer')
var gb2312ToBase64 = require('./gb2312ToBase64')
var http_listener = require('./http_listener')

var express = require('express')
var bodyParse = require('body-parser')

let uuid = UUID.BLUETOOTH_SUBSCRIBE_CHARACTERISTIC_ID ;

// The characteristic of BLE
// Implement a characteristic 
var BluetoothSubscribeCharacteristic = function(codeListener){
	BluetoothSubscribeCharacteristic.super_.call(this,{
		uuid: uuid ,
		properties:['notify','write','read'],
		descriptors:[
			new Descriptor({
				uuid: '2901',
				value: 'subscribe on device'
			})
		]			
	});
	this.http_listener = codeListener;
} ;
util.inherits(BluetoothSubscribeCharacteristic,Characteristic);


/*
 * executing while the characteristic is on subscribe
 * the listener is receiving the code from the scanner (by the python service on subprocess)
 * it exists 3 functional modes for the device:
 * 	0.the off mode
 * 	1.the perchasing mode 
 * 	  when the scanner get the code, notify the code on the miniprogram	
 * 	2.the recording mode
 * 	  when the scanner get the code, the device will start to register the infos of the merchandise
 * 	  the program will spawn a subprocess for a python script to execute
 * 	  which takes 15 seconds, the subrocess is synchronous
 * 
 * TODO: other modes for the devices
 *  
 */
BluetoothSubscribeCharacteristic.prototype.onSubscribe = function(maxValueSize, updateValueCallback){
    console.log("[action]Device subscribed");
    updateValueCallback(new Buffer("ready for barcode scanning!"));
    this.http_listener.mode = 1

    //listener the event
    this.http_listener.on('code',function(result){
      let mode  =  this.mode
      console.log(mode)
      if(mode != 0){
	switch(mode){
	  case 1:
	    console.log('[consumer]the code of this merchandise:'+result.code)
	    exec('mplayer /home/pi/voice/scanned.mp3',function(err,stdout,stderr){
				   if(err){
					   console.log(err) 
				   }
	    })
	    updateValueCallback(new Buffer(result.code));
	    break;
	  case 2:
	    exec('mplayer /home/pi/voice/recording.mp3',function(err,stdout,stderr){
				   if(err){
					   console.log(err) 
				   }
	    })
	    execS('python3 /home/pi/merchandise.py '+result.code,timeout = 15000);
	    updateValueCallback(new Buffer('[recording]logging...'));
	    break;
	  default:
	    console.log('no action')
	    break;
	  }
      }
    })
    
    //notifying the user by the box
    exec('mplayer /home/pi/subscribe.mp3',function(err,stdout,stderr){
		 if(err){
			 console.log(err) 
		 }
	 })
}


// executing when the characteristic is on unsubscribe
// switch the mode of the listener to off mode
BluetoothSubscribeCharacteristic.prototype.onUnsubscribe = function() {
          console.log("[action]Device unsubscribed ");
          exec('mplayer /home/pi/exit.mp3',function(err,stdout,stderr){
			if(err){
			 console.log(err) 
			 console.log(stderr)
			}
			})
	  console.log('[mode]switch to off mode')
	  this.http_listener.mode = 0
	  this.http_listener.removeAllListeners(['code'])
          clearInterval(this.intervalId);
          if(this.changeInterval){
			  clearInterval(this.changeInterval)
			  this.changeInterval = null
	  }
}

/*
 * executing when there is a write request to the characteristic
 * serveral cases for the write data:
 * 	"clear": cleaning the local file 
 * 	"change": switch the working mode of the device (consumer or recording)
 * 	default: operate the printer
 * 
 * the format for the printer check in the python file
 *  
 */
BluetoothSubscribeCharacteristic.prototype.onWriteRequest = function(data, offset, withoutResponse, callback) {
	    var self = this; 
            var base = base64arraybuffer.encode(data);
            var info = gb2312ToBase64.decode64(base);
            
            console.log('[writeinfo]gb:'+info)
            switch(info){
		case 'clear':
		    fs.unlink('input.txt',function(err){
			    if(err){
				    console.log(err)
			      }
                    })
                    fs.writeFile('input.txt','',function(err){
			    if(err){
				    console.log(err)
				  }
		    })
                    break;
                                
		case 'change':
		    console.log('[mode]changing...')
		    switch(this.http_listener.mode){
		      case 1: 
			  console.log('[mode]switch to recording mode')
			  exec('mplayer /home/pi/voice/mode2.mp3',function(err,stdout,stderr){
				   if(err){
					   console.log(err) 
				   }
			   })
			  this.http_listener.mode = 2
			  break;
			  
		      case 2:
			  console.log('[mode]switch to consumer mode')
			  exec('mplayer /home/pi/voice/mode1.mp3',function(err,stdout,stderr){
				   if(err){
					   console.log(err) 
				   }
			   })
			  this.http_listener.mode = 1
			  break;
		      }
                    break;                                                                            
                default:
		      fs.appendFile('/home/pi/test/input.txt', info+"\n",function(err){
			  if(err){
			      console.err(err)
			    }
		      })
		      exec('python3 /home/pi/printer2.py "'+info+'"',function(err,stdout,stderr){
			  exec('mplayer /home/pi/voice/printing.mp3',function(err,stdout,stderr){
			      if(err){
				  console.log(err) 
				 }
			  })
			  if(err){
				console.info(err)
			    }
		      })
                    break;
				}    
                callback(this.RESULT_SUCCESS);
}

// executing when the characteristic get a read request
// read the local file and send to the miniprogram
BluetoothSubscribeCharacteristic.prototype.onReadRequest = async function(offset,callback){
	console.log("[action]Read request received");
	exec('mplayer /home/pi/read.mp3',function(err,stdout,stderr){
		 
		 if(err){
			 console.log(err) 
			 console.log(stderr)
		 }
	 })
        exec('cat ./list.txt',function(err,stdout,stderr){
		var data = stdout.toString();
		callback(this.RESULT_SUCCESS, new Buffer("Echo: " + data));
		}) 
}

// generating a random UUID 
function guid4(){
		return 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'.replace(/[xy]/g,function(c){
			let r = Math.random()*16|0,v=c=='x'?r:(r&0x3|0x8)
			return v.toString(16);
			})
}

module.exports = BluetoothSubscribeCharacteristic;
