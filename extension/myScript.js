
/**
 * @file myScript.js
 * Script to analyze Facebook feed;
 *
 * @author Mark Craft, Qinglin Chen
 * @date Fall 2016
 */

var feeds = new Set();

(function(document) {

/**
 * Http request to fbserve.herokuapp.com.
 *
 * @param the text or url to send to the server.
 */
function httpGet(input, type, data) {

	var server = "https://trustfb.herokuapp.com/";
	var contents = "?content=";
	
	var theUrl = server+contents+input;
	theUrl = theUrl.replace("&", "^");

	fetch(theUrl)
		.then(function(res)
		{ return res.text(); })
		.then(function(text)
		{
			/*
			console.log(text);
			if(input=="https://scontent-lga3-1.xx.fbcdn.net/v/t1.0-0/s480x480/15036323_654895641357441_1273137689777177127_n.jpg?oh=62dc1ed1a5bd65bfb984083bf1b61822&oe=58CFE7E7") console.log("ping");
			var div = document.createElement('div'),
					button = Ladda.create(div);
				data.appendChild(div);
				div.innerHTML = "not verified";
				div.style = "front-weight:bold; padding: 3px; position:absolute; top: 4px; right: 30px;background: #3b5998; font-size: 15px; color: #D5F5E3;"
			*/
			/*
			if(input=="https://scontent-lga3-1.xx.fbcdn.net/v/t1.0-0/s480x480/15036323_654895641357441_1273137689777177127_n.jpg?oh=62dc1ed1a5bd65bfb984083bf1b61822&oe=58CFE7E7") {
				console.log("ping");
				var div = document.createElement('div'),
					button = Ladda.create(div);
				data.appendChild(div);
				div.innerHTML = "not verified";
				div.style = "front-weight:bold; padding: 3px; position:absolute; top: 4px; right: 30px;background: #3b5998; font-size: 15px; color: #E74C3C;";
			} else {*/
				console.log(input + "__::__" + text);
				var div = document.createElement('div'),
					button = Ladda.create(div);
				data.appendChild(div);
				div.innerHTML = text;
				if(text=="verified") div.style = "front-weight:bold; padding: 3px; position:absolute; top: 4px; right: 30px;background: #3b5998; font-size: 15px; color: #D5F5E3;";
				else div.style = "front-weight:bold; padding: 3px; position:absolute; top: 4px; right: 30px;background: #3b5998; font-size: 15px; color: #E74C3C;";
			//}
		});
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

			var shared = test[i].querySelector('._52c6');
			if(!processed && shared != null && shared.href!=undefined) {
				httpGet(shared.href, "url", data);
				processed = false;
			}

			var picComment = test[i].querySelector('.uiScaledImageContainer._4-ep');
			if(picComment != null && picComment.src!=undefined) {
				httpGet(picComment.src, "image", data);
				processed = false;
			}

			var picPost = test[i].querySelector('._46-h._517g');
			if(!processed && picPost != null && picPost.src!=undefined) {
				httpGet(picPost.src, "image", data);
				proccessed = false;
			}

			var text = test[i].querySelector('._5pbx.userContent');
			if(!processed && text != null && text.textContent!=undefined) {
				httpGet(text.textContent, "text", data);
				processed = false;
			}

		} else {
			//console.log("have feed");
		}
	}

}, 1000);
	
})(document);