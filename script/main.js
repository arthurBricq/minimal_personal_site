import {parse} from './snarkdown.js';

// Loads the header
$(function(){
	$.get("header.html", function(data){
		$("#header").replaceWith(data);
	});
});


// Inject markdown in the front page
const container = document.getElementById("markdown_container");
let path = 'data/text.md'
fetch(path).then(response => response.text()).then(text => {
	let html = parse(text);
	container.innerHTML = html;
})

