import {Section} from './section.js'

// Loads the header
$(function(){
	$.get("header.html", function(data){
		$("#header").replaceWith(data);
	});
});

// Loads all of the projects
const projects_list = document.getElementById("projects_list");
const projects_sections = document.getElementById("projects_sections");
const root_projects_path = './data/projects/';


// Find all projects using JQuery
$.getJSON(root_projects_path, files => {

	// To deal with the asynchronous files reading, we use an array of fetches.
	// https://stackoverflow.com/a/51012898/13219173
	var fetches = [];
	var results = [];

	var tmp = 0;
	for (var f of files) {

		let path = root_projects_path + f
		fetches.push(
			fetch(path)
			.then(response => response.text())
			.then(text => {
				// Create the section
				let s = new Section(text);
				let title = s.title;
				let desc = s.description;

				// Happen the section in the HTML for all projects
				var html = '';
				html += `<div id=${tmp} class="new_project"></div>`;
				html += s.parsed_html;

				// Append in the list of projects
				var html_list = ''
				html_list += `<li class="project_item"><a href="#${tmp}">${title}</a> </li>`;
				if (s.github != null) {
					html_list += `<p class="description">Link to <a href="${s.github}">Github</a></p>`;
				}
				html_list += `<p class="keyword">keywords: ${s.keywords}</p>`;
				html_list += `<p class="description">${desc}</p>`;


				// Increase the counter
				tmp += 1;

				results.push({
					"priority": s.priority,
					"title": s.title,
					"html": html,
					"html_list": html_list,
				})
			})
		)
	}

	// Wait for all fetches to be done
	Promise.all(fetches).then(function() {
		console.log(results);

		results.sort((a,b) => {
			if (a.priority != b.priority) {
				return a.priority > b.priority;
			} else {
				return a.title < b.title;
			}
		})

		var html_projects_list = '<h2>List of projects</h2>';
		html_projects_list += '<ul>'
		var html_sections = '';

		for (const result of results) {
			html_projects_list += result.html_list;
			html_sections += result.html;
		}


		html_projects_list += '</ul>';

		// Fill the project list
		projects_list.innerHTML = html_projects_list;

		// Fill the sections
		projects_sections.innerHTML = html_sections; 
		console.log(html_sections); 

	});
});

// This will change the title of the header
//const myHeading = document.querySelector("h1");
//myHeading.textContent = "Hello world by Arthur (modified by js)!";
