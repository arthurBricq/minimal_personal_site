import {parse} from './snarkdown.js';

export class Section {
	constructor(text, id) {
		this.text = text;
		this.id = id;

		const blocks = text.split("---");
		this.header = blocks[1];
		this.markdown = blocks[2];

		this._html = parse(this.markdown);
		this.parse_header();
	}

	// There are two required headers: title and description
	parse_header() {
		this._title = this.header.match(/title: (.*)/)[1]
		this._description = this.header.match(/description: (.*)/)[1]
		// parse the date
		let date_result = this.header.match(/date: (.*)/)
		if (date_result != null) {
			this._date = date_result[1];
		}
		// parse the priority
		let priority_result = this.header.match(/priority: (.*)/)
		if (priority_result != null) {
			this._priority = priority_result[1];
		}
		// parse the github
		let github_result = this.header.match(/github: (.*)/)
		if (github_result != null) {
			this._github = github_result[1];
		}
		// parse the keywords
		let keywords_result = this.header.match(/keywords: (.*)/)
		if (keywords_result != null) {
			this._keywords = keywords_result[1];
		}
		// parse the featuredImage
		let featuredImage_result = this.header.match(/featuredImage: (.*)/)
		if (featuredImage_result != null) {
			this._featuredImage = featuredImage_result[1];
		}

	}

	get parsed_html() {
		return this._html;
	}

	get title() {
		return this._title;
	}

	get date() {
		return this._date;
	}

	get featuredImage() {
		return this._featuredImage;
	}

	get keywords() {
		return this._keywords;
	}

	get github() {
		return this._github;
	}

	get priority() {
		return this._priority;
	}

	get description() {
		return this._description;
	}

}
