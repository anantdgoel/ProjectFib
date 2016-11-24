/**
 * @file myScript.js
 * Script to analyze Facebook feed and make connection with the server
 *
 * @author Mark Craft, Qinglin Chen
 * @date Fall 2016
 */
(function(document) {

var feeds = new Set();

/**
 * Http request to fbserve.herokuapp.com.
 *
 * @param url to send to the server.
 * @param the type of information sent
 * @param the location to put the button
 */
function httpGet(input, type, data) {

	var server = "https://fbserve.herokuapp.com/";
	var contents = "?content=";
	var page = (type=="url")? decode(input) : input;
	var theUrl = server + contents + page;
	theUrl = theUrl.replace("&", "^");
	
	//console.log("Type: " + type + " : " + page);

	fetch(theUrl)
		.then(function(res) { 
			return res.text();
		}).then(function(text) {
			var btn = document.createElement('div'),
				button = Ladda.create(btn);
			btn.style = "front-weight:bold; padding: 3px; position:absolute; top: 4px; right: 30px;background: #3b5998; font-size: 15px;";
			if(text=="verified") {
				btn.innerHTML = "verified";
				btn.style.color = "#D5F5E3";
			} else {
				btn.innerHTML = "not verified";
				btn.style.color = "#E74C3C";
			}
			data.appendChild(btn);
		});
	
}

/**
 * Create a button on the screen
 *
 * @param location of the button
 * @param the text to display on the button
 * @param whether the server is down or not
 */
function createButton(btn, loc) {
	btn = document.createElement('div'),
		button = Ladda.create(btn);
	//btn.addEventListener("mouseover", hoverTooltip(text), false);

	btn.innerHTML = "server down";
	btn.style = "front-weight:bold; padding: 3px; position:absolute; top: 4px; right: 30px;background: #3b5998; font-size: 15px; color: #FFFFFF;";

	loc.appendChild(btn);
}

/**
 * Display tooltip with more accurate information
 *
 * @param the information to display
 */
function hoverTooltip(info) {
	//console.log("hovering: " + info);
}

/*
 * Parse through Facebook's encoded url for the actual url
 *
 */
function decode(code) {

	var res = "" + code;
	res = res
		.replace("http://l.facebook.com/l.php?u=", "")
		.replace(/%3A/gi, ":")
		.replace(/%F/gi, "/")
		.replace(/%2F/gi, "/");

	var end = res.substr(res.indexOf("^h"), res.length);
	res = res.replace(end, "");
	var end2 = res.substr(res.indexOf("&"), res.length);
	res = res.replace(end2, "");

	return res;
}  

/**
 * Receive each Facebook post and analyze texts, urls, pics for validity.
 * Refreshes every second.
 *
 */
setInterval(function() {
	
	var test = document.getElementsByClassName('_4-u2 mbm _5v3q _4-u8');

	for(var i=0; i<test.length; i++) {

		var data = test[i];

		// Check if feed needs to be modified

		if(!feeds.has(data)) {
			feeds.add(data);

			// Send server requests

			var statement = "";

			var processed = false;

			var linked = test[i].querySelector('._6ks');
			if(!processed && linked != null && linked.querySelector('a')!=undefined) {
				processed = true;
				httpGet(linked.querySelector('a').href, "url", data);
			}

	
			var link = test[i].querySelector('._5pbx.userContent');
			if(!processed && link != null && link.querySelector('a') != null && link.querySelector('a').href!=undefined) {
				processed = true;
				httpGet(link.href, "url", data);
			}
            

			var picComment = test[i].querySelector('.uiScaledImageContainer._4-ep');
			if(!processed && picComment != null && picComment.querySelector('img') != undefined && picComment.querySelector('img').src!=undefined) {
				processed = true;
				httpGet(picComment.querySelector('img').src, "image", data);
			}

			var picPost = test[i].querySelector('._46-h._517g');
			if(!processed && picPost != null  &&  picPost.querySelector('img') != undefined && picPost.querySelector('img').src!=undefined) {
				processed = true;
				httpGet(picPost.querySelector('img').src, "image", data);
			}
			
			var picTagged = test[i].querySelector('._4-eo._2t9n');
			if(!processed && picTagged != null && picTagged.querySelector('._46-h._4-ep') != undefined && picTagged.querySelector('._46-h._4-ep').querySelector('img') != undefined) {
				processed = true;
				httpGet(picTagged.querySelector('._46-h._4-ep').querySelector('img').src, "image", data);
			}

			/*
			var picAlbum = test[i].querySelector('._2a2q');
			if(!processed && picAlbum != null && picAlbum.querySelectorAll('._5dec._xcx')!=undefined) {
				processed = true;
				var pics = picAlbum.querySelectorAll('a._5dec._xcx');
				for(int i=0; i<pics.length; i++) 
			}
			*/

			var text = test[i].querySelector('._5pbx.userContent');
			if(!processed && text != null && text.textContent!=undefined) {
				processed = true;
				httpGet(text.textContent, "text", data);
			}
	
		}
	}

}, 1000);
	
})(document);