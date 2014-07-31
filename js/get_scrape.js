"use strict";
var total_levels = 0;
var characters = {'cenarius': ["Alaali",
	                       "Raedal",
			       "Bediviere",
			       "Yowai",
			       "Saelar",
			       "Ouyangbuheng",
			       "Mcfurrington",
			       "Resisty",
			       "Resistard",
			       "Resistyna",
			       "Resistyana"],
		   'aerie-peak': ["Resistyana",
		   		  "Resistylock",
				  "Resistard",
				  "Resisty",
				  "Resistyfu",
				  "Resistyrunes",
				  "Resistotems",
				  "Resistab",
				  "Resistadin",
				  "Pathaleon"]};

function get_scrape(character, realm, callback) {
    var params = "character=" + character + "&realm=" + realm;
    var url = "http://localhost:5000/character_scrape";
    console.log(url + " " + params);
    var http = new XMLHttpRequest();
    http.open("POST", url, true);
    http.onload = function() {
        callback(http);
    };
    http.send(params);
}
		    
function makediv(jsonreq) {
    console.log(jsonreq.responseText);
    var parsedjson = JSON.parse(jsonreq.responseText);
    parsedjson = parsedjson.results;
    var elements = ['level', 'race', 'spec tip', 'class'];
    var docele = document.getElementById('characters');
    var next_char = document.createElement('div');
    var desc = "Level " + parsedjson['level'];
    desc = desc + " " + parsedjson['race'];
    desc = desc + " " + parsedjson['spec tip'];
    desc = desc + " " + parsedjson['class'];
    next_char.innerHTML = desc;
    docele.appendChild(next_char);
    total_levels = total_levels + parseInt(parsedjson['level']);
}

function scrape_characters() {
    Object.keys(characters).forEach(function(realm) {
	for(var i = 0; i < characters[realm].length; i++){
	    console.log("Character: " + characters[realm][i] + ", realm: " + realm);
	    get_scrape(characters[realm][i], realm, makediv);
	}
    })
}

scrape_characters();
