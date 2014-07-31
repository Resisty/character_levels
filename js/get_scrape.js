"use strict";
var total_levels = 0;
var total_characters = 0;
var characters_counted = 0;
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
				  "Resistystab",
				  "Resistadin",
				  "Pathaleon",
				  "Resistyngton"]};
Object.keys(characters).forEach(function(realm) {
    for(var i = 0; i < characters[realm].length; i++){
	total_characters = total_characters + 1;
    }
})
var max_levels = characters_counted * 90;

function get_scrape(character, realm, callback) {
    var params = {"character": character, "realm": realm};
    var url = "http://brianauron.info:5000/character_scrape";
    console.log(url + " " + params);
    var http = new XMLHttpRequest();
    http.open("POST", url, true);
    http.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    http.onload = function() {
        callback(http);
    };
    http.send(JSON.stringify(params));
}
		    
function makediv(jsonreq) {
    console.log(jsonreq.responseText);
    var parsedjson = JSON.parse(jsonreq.responseText);
    parsedjson = parsedjson.results;
    var elements = ['level', 'race', 'spec tip', 'class'];
    var docele = document.getElementById('characters');
    var next_char = document.createElement('div');
    var desc = parsedjson['character'];
    desc = desc + " " + parsedjson['realm'] + ": ";
    desc = desc + "Level " + parsedjson['level'];
    desc = desc + " " + parsedjson['race'];
    desc = desc + " " + parsedjson['spec tip'];
    desc = desc + " " + parsedjson['class'];
    next_char.innerHTML = desc;
    docele.appendChild(next_char);
    total_levels = total_levels + parseInt(parsedjson['level']);
    characters_counted = characters_counted + 1;
    update_counts();

}

function update_counts() {
    var counts = document.getElementById('counts');
    var characters = document.getElementById('characters');
    var wait = document.getElementById('please-wait');
    var wait_msg = "Please wait, loading characters...";
    if(wait === null){
	    wait = document.createElement('div');
	    wait.setAttribute("id", "please-wait");
	    wait.innerHTML = wait_msg;
	    characters.appendChild(wait);
    }
    if(characters_counted == total_characters){
	    characters.removeChild(wait);
    }

    var total = document.getElementById('total');
    if(total === null){
	total = document.createElement('div');
	total.setAttribute("id", "total");
    }
    var total_desc = "Total levels: " + total_levels;
    total.innerHTML = total_desc;
    counts.appendChild(total);

    max_levels = characters_counted * 90;
    var max = document.getElementById('max');
    if(max === null){
	max = document.createElement('div');
	max.setAttribute("id", "max");
    }
    var max_desc = "Max levels: " + max_levels;
    max.innerHTML = max_desc;
    counts.appendChild(max);

    var diff = document.getElementById('diff');
    if(diff === null){
	diff = document.createElement('div');
	diff.setAttribute("id", "diff");
    }
    var remain = max_levels - total_levels;
    var diff_desc = "Remaining levels: " + remain;
    diff.innerHTML = diff_desc;
    counts.appendChild(diff);

}

function scrape_characters() {
    Object.keys(characters).forEach(function(realm) {
	for(var i = 0; i < characters[realm].length; i++){
	    get_scrape(characters[realm][i], realm, makediv);
	}
    })
}

update_counts();
scrape_characters();
