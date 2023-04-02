// node.js script to create the .html files for each of the articles.

import fs from "fs";
import {Section} from './script/section.js'

let template_start = `
<!DOCTYPE html>
<link rel="stylesheet" type="text/css" href="../style.css">
<html lang="en">
	<head>
		<meta charset="utf-8">
		<meta name="viewport" content="width=device-width">

		<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>

		<title>Personal Website</title>
		<meta name="description" content="My personal website">
		<meta name="author" content="Arthur Bricq">
	</head>
	<body>
		<div id="header"></div>
		<article>
`;

let template_end = `
		</article>
		<script>
$(function(){
	$.get("../header.html", function(data){
		$("#header").replaceWith(data);
	});
});
		</script>
	</body>
</html>
`;

const articles_path = './data/writing/';
const project_path = './data/projects/';
const output_article_path = './generated_articles/'
const output_project_path = './generated_projects/'

// delete files already there
fs.rmSync(output_article_path, { recursive: true, force: true });
fs.mkdirSync(output_article_path);

// create new files
fs.readdir(articles_path, (_err, files) => {
	files.forEach(file => {
		// Only markdown files are considered
		if ( file.endsWith('.md') ) {
			// Remove the .md in the file name
			let name = file.replace(/.md/, '');

			// read the file
			fs.readFile(articles_path + file, {encoding: 'utf-8'}, (_err, data) => {
				let s = new Section(data);
				let html = s.parsed_html;
				let title = s.title;
				let desc = s.description;
				let file_to_write = output_article_path + name;

				// 1. Save the html file
				fs.writeFile(file_to_write + '.html', template_start + html + template_end, (err) => {
					if (err)
						console.log(err);
				});

				// 2. Save the .json file
				let json = `
{
	"title": "${title}",
	"desc": "${desc}",
	"date": "${s.date}"
}
				`;
				fs.writeFile(file_to_write + '.json', json, (err) => {
					if (err)
						console.log(err);
					else {
						console.log(fs.readFileSync(file_to_write + '.json', "utf8"));
					}
				});

			}
			);

		}

	});
});


// Now, let's take care of projects
fs.rmSync(output_project_path, { recursive: true, force: true });
fs.mkdirSync(output_project_path);

// create new files
fs.readdir(project_path, (_err, files) => {
	files.forEach(file => {
		// Only markdown files are considered
		if ( file.endsWith('.md') ) {
			fs.readFile(project_path + file, {encoding: 'utf-8'}, (_err, data) => {
				// Parse the markdown file
				let s = new Section(data);
				let html = s.meta_html + s.parsed_html;

				// Let's create some meta
				let file_to_write = output_project_path + file.replace(/.md/, '');
				fs.writeFile(file_to_write + '.html', html, (err) => {
					if (err)
						console.log(err);
				});

			});

		}

	});
});


