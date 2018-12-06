// arrange.js
// copyright 2018 George Hunt

// debug

var action = "right";
var defUrl = "/menus-service/";
// following are the highlighted lines on left(present) 
//    and right(available) columns
var available_element = {};
var present_element = {};
var langSelect = [];

if(typeof debug == 'undefined') {
	debug = true;
}

$( document ).ready(function() {
    get_languages();
    get_available('all');
    get_visible();
});


function get_languages() {
var resp = $.ajax({
		type: 'GET',
		async: true,
		url: defUrl + 'langsavail',
		dataType: 'json'
	})
.done(function( data ) {
      //alert('my data' + data);
      $('#lang').append($('<option>',{value:0,text:"All Items"}));
      $('#lang').append($('<option>',{value:1,text:"Downloaded"}));
      langSelect.push('all');
      langSelect.push('downloaded');
      var selectIndex = 2;
      $.each( data, function( key, val ) {
         $('#lang').append($('<option>', {
            value: selectIndex,
            text: val['name']  + '-' + val['num']
          }));
        // save the lookup index 
        langSelect.push(val['lang']);
        selectIndex++;
      })
      //alert('langSelect = ' + langSelect);
	})
.fail(jsonErrhandler);
}

function available_clicked(element) {
   $( available_element ).css('background','#fff');
   available_element = element;
   $( element ).css('background','#0f0');
}

function visible_clicked(element) {
   $( present_element ).css('background','#fff');
   present_element = element;
   $( element ).css('background','#0f0');
}

function onlanguage (element) {
   // use the langSelect to cross ref drop down index to language
   //var search = langSelect[element.value];
   //alert("in onlanguage " + search);
   get_available(langSelect[element.value]);
}
function get_available(lang="all") {
if ( lang === "all") {
   dburl = defUrl + "all";
} else {
   dburl = defUrl + 'available?lang=' + lang;
}
var resp = $.ajax({
		type: 'GET',
		async: true,
		url: dburl,
		dataType: 'json'
	})
.done(function( data ) {
      var html = '';
      $.each( data, function( key, val ) {
         html += "<p onclick=\"available_clicked(this)\"" +
         " data-id=\"" + val['id'] + 
         "\" data-name=\"" + val['name'] + 
         "\" value=\"" + val['name'] + "\">" +
         val['title'] + " -- " + val['name'] + "--" + val['id'] + "</p>";
      });
      $("#available").html(html);    
	})
.fail(jsonErrhandler);
}

function get_visible() {
var resp = $.ajax({
		type: 'GET',
		async: true,
		url: defUrl + 'visible',
		dataType: 'json'
	})
.done(function( data ) {
      var html = '';
      var line = 0;
      $.each( data, function( key, val ) {
         html += "<p onclick=\"visible_clicked(this)\"" +
         " id=\"" + line + "-visible\"" +
         " data-id=\"" + val['id'] + 
         "\" data-name=\"" + val['name'] + 
         "\" value=\"" + val['name'] + "\">" +
         val['title'] + " -- " + val['name'] + "--" + val['id'] + "</p>";
         line++;
      });
      $("#present").html(html);    
	})
.fail(jsonErrhandler);
}
function choose(id) {
var resp = $.ajax({
		type: 'GET',
		async: true,
		url: defUrl + 'choose?id=' + id,
		dataType: 'json'
	})
.done(function( data ) {
      //alert(data);
      return data['status'];
	})
.fail(jsonErrhandler);
}

function unchoose(id) {
var resp = $.ajax({
		type: 'GET',
		async: true,
		url: defUrl + 'unchoose?id=' + id,
		dataType: 'json'
	})
.done(function( data ) {
      //alert(data);
      return data['status'];
	})
.fail(jsonErrhandler);
}

function upchosen(id) {
var resp = $.ajax({
		type: 'GET',
		async: true,
		url: defUrl + 'upchosen?id=' + id,
		dataType: 'json'
	})
.done(function( data ) {
      //alert(data);
      return data['status'];
	})
.fail(jsonErrhandler);
}

function downchosen(id) {
var resp = $.ajax({
		type: 'GET',
		async: true,
		url: defUrl + 'downchosen?id=' + id,
		dataType: 'json'
	})
.done(function( data ) {
      //alert(data);
      return data['status'];
	})
.fail(jsonErrhandler);
}

function leftclick () {
   //alert('in leftclick');
   choose($( available_element ).data('id'));
   get_visible();
   location.reload();
}

function rightclick () {
   unchoose($( present_element ).data('id'));
   get_visible();
   location.reload();
}

function upclick () {
   upchosen($( present_element ).data('id'));
   get_visible();
   location.reload();
}
function downclick () {
   downchosen($( present_element ).data('id'));
   get_visible();
   location.reload();
}

function consoleLog (msg)
{
	if (debug == true)
	console.log(msg); // for IE there can be no console messages unless in tools mode
}

function jsonErrhandler (jqXHR, textStatus, errorThrown)
{
	// only handle json parse errors here, others in ajaxErrHandler
	//  if (textStatus == "parserror") {
	//    //alert ("Json Errhandler: " + textStatus + ", " + errorThrown);
	//    displayServerCommandStatus("Json Errhandler: " + textStatus + ", " + errorThrown);
	//  }
	consoleLog("In Error Handler logging jqXHR");
	consoleLog(textStatus);
	consoleLog(errorThrown);
	consoleLog(jqXHR);

	return false;
}

