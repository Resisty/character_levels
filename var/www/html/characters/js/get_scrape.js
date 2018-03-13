(function( $ ) {
    "use strict";
    function getCharacters(callback) {
	var url = '/scrape_characters/';
	$.getJSON(url, function(data) {
	    callback(data);
	});
    };

    function makeDiv(data) {
	var character_info = data['character_info'];
	console.log(JSON.stringify(character_info));
	var characters = character_info['characters'];
	var maximum = character_info['maximum'];
	var total = character_info['total'];
	var total_max = 'Total levels / Maximum levels: ' + total + ' / ' + maximum;
	var h2 = $("<h2>",
	           {text: total_max});
	h2.appendTo($('#counts'));
	$('#counts')
	$.each(characters, function(index, character) {
	    var uid = character['realm_name'];
	    var name = character['name'];
	    var realm = character['realm'];
	    var level = character['level'];
	    var character_detail = character['character_detail'];
	    var href = character['href'];
	    var title = name + ' - ' + level + ' ' + character_detail;
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
		       id: uid + "-p"});
	    h3.appendTo(panelhead);
	    var a = $("<a>",
		      {text: title});
	    a.attr('href', href);
	    a.appendTo(h3);
	    var ul = $("<ul>",
		       {class: 'thumbnails',
			id: name + "-render"});
	    if (character['render'] != 'No rendered image available.') {
		ul.appendTo(panelhead);
		var li = $("<li>",
			   {class: 'span4'});
		li.appendTo(ul);
		var ahref = $("<a>",
			    {href: href,
			     class: 'thumbnail'});
		ahref.appendTo(li);
		var img = $("<img>",
			    {src: character['render']});
		img.appendTo(ahref);
	    }
	});
    }
    $(document).ready( function() {
	getCharacters(makeDiv);
    });
})( jQuery );
