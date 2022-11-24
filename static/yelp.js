function initialize () {
   limit = 10
}

function findRestaurants () {
   var xhr = new XMLHttpRequest();
   var query1 = (document.getElementById("search").value).split(" ").join("+");
   var query2 = (document.getElementById("city").value).split(" ").join("+");
   xhr.open("GET", "proxy.php?term="+ query1+"&location="+query2+"&limit="+limit);
   xhr.setRequestHeader("Accept","application/json");
   xhr.onreadystatechange = function () {
       if (this.readyState == 4) {
          var json = JSON.parse(this.responseText);
          if(json.hasOwnProperty("error")) document.getElementById("output").innerHTML = json.error.code+"</br>"+json.error.description;
			 else{
				if(json["businesses"].length==0) document.getElementById("output").innerHTML = "No restaurants found";
				else{
					restaurantList(json)
				}
			}
       }
   };
   xhr.send(null);
}

function restaurantList(json){
	output = "<ol>"
	for(var i=0;i<json["businesses"].length;i++){
		output += "<li>"
		output += "<img src=\"" + json["businesses"][i]["image_url"] + "\" style=\"height:120px;width:120px;\">" +"&nbsp"+"&nbsp"+"&nbsp"+"&nbsp"
		output += "<a href=\"" + json["businesses"][i]["url"] + "\">" + json["businesses"][i]["name"] + "</a>"+"&nbsp"+"&nbsp"+"&nbsp"+"&nbsp"
		for(var j=0;j<json["businesses"][i]["categories"].length;j++){
		output += json["businesses"][i]["categories"][j]["title"] + "&nbsp"+"&nbsp"+"&nbsp"+"&nbsp"
		console.log(json["businesses"][i]["categories"][j]["title"])
		}
		output += json["businesses"][i]["price"] + "&nbsp"+"&nbsp"+"&nbsp"+"&nbsp"
		output += json["businesses"][i]["rating"] + "&nbsp"+"&nbsp"+"&nbsp"+"&nbsp"
		output += json["businesses"][i]["location"]["display_address"] + "&nbsp"+"&nbsp"+"&nbsp"+"&nbsp"
		output += json["businesses"][i]["phone"] + "&nbsp"+"&nbsp"+"&nbsp"+"&nbsp"
		output +="</li>"
	}
	output += "</ol>"
	document.getElementById("output").innerHTML = output;
}