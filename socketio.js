//var socket = require('socket.io-client')('http://192.168.0.85:7001/terminal');
var socket = require('socket.io-client')('http://192.168.0.171:5001');
var exec = require('child_process').exec;

function printer(socket){
	exec('sudo python3 /home/pi/test/python/printerCheck.py',function(err,stdout,stderr){
			if(err){
				console.log(err)
				socket.emit('error',err)
				}
			socket.emit('check',{'printer':parseInt(stdout)})	
			}
		)
}

function scanner(socket){
	exec('sudo python3 /home/pi/test/python/peripherals/scanner.py',function(err,stdout,stderr){
			if(err){
				console.log(err)
				socket.emit('error',err)
				}
			socket.emit('check',{'scanner':parseInt(stdout)})	
			}
		)	
}

function temperature(socket){
	exec('sudo python3 /home/pi/test/python/peripherals/temperature.py',function(err,stdout,stderr){
			if(err){
				console.log(err)
				socket.emit('error',err)
				}
			socket.emit('check',{'temperature':parseFloat(stdout)})	
			}
	)
}
function weight(socket){
	exec('sudo python3 /home/pi/test/python/peripherals/weight.py',function(err,stdout,stderr){
			if(err){
				console.log(err)
				socket.emit('error',err)
				}
			socket.emit('check',{'weight':parseInt(stdout)})	
			}
	)
}
function camera(socket){
	exec('sudo python3 /home/pi/test/python/peripherals/camera.py',function(err,stdout,stderr){
			if(err){
				console.log(err)
				socket.emit('error',err)
				}
			socket.emit('check',{'camera':parseInt(stdout)})	
			}
		)
}
function device(socket){
	exec('sudo cat /proc/device-tree/model',function(err,stdout,stderr){
			if(err){
				console.log(err)
				socket.emit('error',err)
				}
			socket.emit('check',{'device':stdout})	
			}
		)
}
function serial(socket){
	exec('sudo python3 /home/pi/test/python/peripherals/serial.py',function(err,stdout,stderr){
			if(err){
				console.log(err)
				socket.emit('error',err)
				}
			socket.emit('check',{'serial':stdout})	
			}
		)
}
function uptime(socket){
	exec('sudo uptime -p',function(err,stdout,stderr){
			if(err){
				console.log(err)
				socket.emit('error',err)
				}
			socket.emit('check',{'uptime':stdout})	
			}
		)
}
function ipaddr(socket){
	exec(" ifconfig -a |grep inet|grep -v 127.0.0.1|grep -v inet6|awk '{print $2}'",function(err,stdout,stderr){
			if(err){
				console.log(err)
				socket.emit('error',err)
				}
			socket.emit('check',{'ipaddr':stdout})	
			}
		)
}
function ethermac(socket){
	exec(" cat /sys/class/net/eth0/address",function(err,stdout,stderr){
			if(err){
				console.log(err)
				socket.emit('error',err)
				}
			socket.emit('check',{'ether_mac':stdout})	
			}
		)
}
function wlanmac(socket){
	exec(" cat /sys/class/net/wlan0/address",function(err,stdout,stderr){
			if(err){
				console.log(err)
				socket.emit('error',err)
				}
			socket.emit('check',{'wlan_mac':stdout})	
			}
		)
}
function cpu(socket){
	exec("top -bn1 |grep load|awk '{printf \"%.2f%%\", $(NF-2)}'",function(err,stdout,stderr){
			if(err){
				console.log(err)
				socket.emit('error',err)
				}
			socket.emit('check',{'cpu':stdout})	
			}
		)
}
function memory(socket){
	exec("free -m| awk 'NR == 2{printf \"%s/%sMB\",$3,$2}'",function(err,stdout,stderr){
			if(err){
			console.log(err)
			socket.emit('error',err)
			}
		socket.emit('check',{'memory':stdout})	
			}
		)
}
function process(socket){
	exec("ps -ef|grep node",function(err,stdout,stderr){
			if(err){
				console.log(err)
				socket.emit('error',err)
				}
			node = stdout.split("\n")
			exec("ps -ef|grep python",function(err,stdout,stderr){
				if(err){
					console.log(err)
					socket.emit('error',err)
					}
				python = stdout.split("\n")
				var processes = node.concat(python)
				//processes = JSON.stringify(processes)
				socket.emit('check',{'process':processes})	
				}
			)
			}
		)
}
function wifi(socket){
	exec(" iwconfig wlan0|grep ESSID|awk -F: '{print $2}'",function(err,stdout,stderr){
			if(err){
				console.log(err)
				socket.emit('error',err)
				}
			let s = stdout.replace(/[\n]/g,"");
			s = s.replace(/["]/g,"");
			socket.emit('check',{'wifi':s})	
			}
		)
}
socket.on('connect',function(){
	console.log('connected')
	socket.emit('terminal_check','test')
	socket.emit('test','test')
	socket.on(socket.id,function(msg){
		//console.log('p2p success')
		console.log(msg)
		switch(msg.action){
			case 'check':
				switch(msg.info){
					case 'printer':
						printer(socket);
						break;
					case 'scanner':
						scanner(socket);
						break;
					case 'temperature':
						temperature(socket);
						break;
					case 'weight':
						weight(socket);
						break;
					case 'camera':
						camera(socket);
						break;
					case 'device':
						device(socket);
						break;
					case 'serial':
						serial(socket);
						break;
					case 'uptime':
						uptime(socket);	
						break;
					case 'ipaddr':
						ipaddr(socket);	
						break;
					case 'wifi':
						wifi(socket);	
						break;
					case 'ether_mac':
						ethermac(socket);	
						break;
					case 'wlan_mac':
						wlanmac(socket);	
						break;
					case 'cpu':
						cpu(socket);	
						break;
					case 'memory':
						memory(socket);	
						break;
					case 'process':
						process(socket);
						break;
					case 'all':
						printer(socket);
						scanner(socket);
						temperature(socket);
						weight(socket);
						camera(socket);
						device(socket);
						serial(socket);
						uptime(socket);	
						ipaddr(socket);	
						wifi(socket);
						ethermac(socket);
						wlanmac(socket);
						cpu(socket);
						memory(socket);	
						process(socket);
						break;
					}
				break;
		}
		
		
	})
});
	
socket.on('disconnect',function(){
	console.log('disconnected')
	});



socket.on('receive',function(msg){
	console.log('receive')
	})
