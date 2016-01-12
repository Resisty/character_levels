(function( $ ) {
    "use strict";
    function getCharacters(callback) {
	var url = '/scrape_characters/';
	$.getJSON(url, function(data) {
	    callback(data);
	});
    };

    function makeDiv(data) {
	var characters = data['characters'];
	$.each(characters, function(index, character) {
	    var uid = character['realm_name'];
	    var name = character['name'];
	    var realm = character['realm'];
	    var level = character['level'];
	    var race = character['race'];
	    var spec_tip = character['spec_tip'];
	    var charclass = character['charclass'];
	    var title = name + ' - ' + level + ' ' + spec_tip + ' ' + charclass + ' on ' + realm;
	    var panel = $("<div>",
		          {class: 'panel panel-default',
			   id: uid + '-panel'});
	    panel.appendTo('#characters');
	    var panelhead = $("<div>",
		        {class: "panel-heading " + realm,
			 id: uid + "-row"});
	    panelhead.appendTo(panel);
	    var h3 = $("<h3>",
		      {class: 'panel-heading',
		       text: title,
		       id: uid + "-p"});
	    h3.appendTo(panelhead);
	    var ul = $("<ul>",
		       {class: 'list-group',
			id: name + "-list"});
	    ul.appendTo(panelhead);
	    $.each(character['professions'], function(key, value) {
		var li = $("<li>",
			   {class: 'list-group-item ' + realm});
		li.appendTo(ul);
		var row = $("<div>",
		            {class: 'row'});
		row.appendTo(li);
		var namecol = $("<div>",
		                {class: 'col-sm-3'});
		namecol.appendTo(row);
		var p = $("<p>",
		          {text: key});
		p.appendTo(namecol);
		var numcol = $("<div>",
		           {class: 'col-sm-9'});
		numcol.appendTo(row);
		var percent = value['ratio']
		var progress = $("<div>",
		    {class: 'progress-bar progress-bar-success',
		     role: 'progressbar',
		     'aria-valuenow': percent,
		     'aria-valuemin': 0,
		     'aria-valuemax': 100,
		     style: 'min-width: 7em; width: ' + percent + '%;',
		     text: value['string']});
	    	progress.appendTo(numcol);
	    });
	    if ( jQuery.isEmptyObject(character['professions']) ) {
		var li = $("<li>",
			   {class: 'list-group-item ' + realm,
			   text: 'No professions'});
		li.appendTo(ul);
	    } else {
		console.log(uid + ' professions: ' + JSON.stringify(character['professions']));
	    }
	});
    }
    $(document).ready( function() {
	getCharacters(makeDiv);
    });
})( jQuery );
