(function(document) {

var arr = [];

setInterval(function() {

	/*
	var link = document.getElementsByClassName('_52c6');//document.getElementsByTagName("a");

	for(var i=0; i<link.length; i++) {
		var url = link[i].href;
		if(arr[url] != 1) {
			arr.push(url);
			arr[url] = 1;
			console.log(url);
		} else {
			//console.log("link in hash table");
		}
	}
	
	var text = document.getElementsByClassName('_5pbx userContent');

	for(var i=0; i<text.length; i++) {
		var txt = text[i].textContent;
		if(arr[txt] != 1) {
			arr.push(txt);
			arr[txt] = 1;
			console.log(txt);
		} else {
			//console.log("text in hash table");
		}
	}
	*/
    
    /*
	var picComment = document.getElementsByClassName('uiScaledImageContainer _4-ep');

	for(var i=0; i<picComment.length; i++) {
		var picture = picComment[i].getElementsByTagName('img');
		var pc = picture[0].src;
		if(arr[pc] != 1) {
			arr.push(pc);
			arr[pc] = 1;
			console.log(pc);
		} else {
			//console.log("pic in hash table");
		}
	}

	var picPost = document.getElementsByClassName('_46-h _517g');

	for(var i=0; i<picPost.length; i++) {
		var picture2 = picPost[i].getElementsByTagName('img');
		var pc2= picture2[0].src;
		if(arr[pc2] != 1) {
			arr.push(pc2);
			arr[pc2] = 1;
			console.log(pc2);
		} else {
			//console.log("pic in hash table");
		}
	}
	*/

	var test = document.getElementsByClassName('userContentWrapper _5pcr');

	for(var i=0; i<picComment.length; i++) {
		//var picture = picComment[i].getElementsByTagName('img');
		//var pc = picture[0].src;
		if(arr[test] != 1) {
			arr.push(test);
			arr[test] = 1;
			console.log(test);
		} else {
			//console.log("pic in hash table");
		}
	}

}, 1000);
	
})(document);