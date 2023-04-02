// Loads the header
$(function(){
	$.get("header.html", function(data){
		$("#header").replaceWith(data);
	});
});

// Read the files
const projects_list = document.getElementById("article_list");
const root_path = './generated_articles/';

// Find all projects using JQuery
$.getJSON(root_path, files => {

	var fetches = [];
	var results = [];

	for (var f of files) {
		if (f.endsWith('.json')) {
			let page = root_path + f.replace(/.json/, '.html');

			// fetch all of the articles
			fetches.push(
				fetch(root_path + f)
				.then(response => response.text())
				.then(text => {
					// This is the json
					console.log(text);
					const json = JSON.parse(text);

					// Create the link
					let html = `<h3><a href="${page}">${json.title}</a></h3>`; 
					html += `<p class="date_box">${json.date}</p>`;
					html += `<p class="description">${json.desc}</p>`;

					results.push({
						"content": html,
						"date": Date.parse(json.date)
					}); 

				})
			)

		}

	}

	// Wait for all fetches to be done and append them sorted with the date
	Promise.all(fetches).then(function() {
		results.sort((a,b) => {
			return a.date < b.date;
		})

		var html_list = '';
		for (const result of results) {
			html_list += result.content;
		}
		projects_list.innerHTML = html_list; 
	});
});
