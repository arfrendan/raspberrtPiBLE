var events = require('events')
var util = require('util')
var express = require('express')
var bodyParse = require('body-parser')

//create a server to get the post from the scanner
var working_mode = {
	OFF: 0,
	CONSUMER: 1,
	RECORD: 2
	}

function CodeListener(){
		events.EventEmitter.call(this);
		this.mode = working_mode.CONSUMER
}

util.inherits(CodeListener,events.EventEmitter);

	
module.exports.CodeListener = CodeListener
module.exports.working_mode = working_mode

