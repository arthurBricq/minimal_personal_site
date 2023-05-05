"""
A python script that generates your personal website
"""
import bs4
import markdown2
from pathlib import Path
from distutils.dir_util import copy_tree
import shutil
import os

def clear_folder(path):
    """
    Deletes a folder, then create it again.
    """
    # deletetion
    try: 
        shutil.rmtree(path)
        print(f"Folder {path} was succesfully deleted")
    except OSError as e:
        print(f"Could not delete folder {path}: {e}")
    # creation
    os.makedirs(path)


class PageBuilder:
    """
    A class to build an html page and all its related children pages.
    """

    def __init__(self, site_root, page_name, html_editor, template):
        """
        Inputs
        ------
        * html_editor: where to put the list of description and links towards the children page
        * template: template for the children page
        * children_output_path: where to write the generated pages
        """
        self._editor = html_editor
        self._template_path = template
        self._root = site_root
        self._name = page_name
        clear_folder(site_root + page_name)

    def add_children(self, _meta, _soup):
        """
        Add a project to the page's content
        """
        # create html div with a link to the project's page.
        tag = self.create_html_link(_meta, _soup)

        # Modify the project page
        self._editor.append(tag)

        # Create a new page with the project's description
        self._create_project_page(_meta, _soup)

    def _create_project_page(self, _meta, _soup):
        # Load the template
        with Path(self._template_path).open() as data:
            html_text = data.read()
        if html_text is None:
            print("ERROR opening project's page html template")
        # Fill the template
        template = bs4.BeautifulSoup(html_text, 'html.parser')
        box = template.find(id="content")
        box.append(_soup)

        # Save the file
        title = _meta['title']
        with open(self._root + self._name + f"/{title}.html", "w") as outf:
            outf.write(str(template))

    # Functions to be overriden
    def create_html_link(self, _meta, _soup):
        title = _meta['title']
        html_list = ''
        html_list += '<li class="project_item"><a href="/{}/{}.html">{}</a> </li>'.format(self._name, title, title);
        if ('github' in _meta):
            html_list += '<p class="description">Link to <a href="{}">Github</a></p>'.format(_meta['github']);
        if ('keywords' in _meta):
            html_list += '<p class="keyword">keywords: {}</p>'.format(_meta['keywords']);
        html_list += '<p class="description">{}</p>'.format(_meta['description']);
        tag = bs4.BeautifulSoup(html_list, 'html.parser')
        return tag;

def create_index_page(template_path, content_path, output_path, container_id = "markdown_container"):
    """
    Creates the index.html page b y filling the template path from the content found in .md file
    """
    # read the template 
    with Path(template_path).open() as data:
        html_text = data.read()
    if html_text is None:
        print("ERROR opening project html")

    # create container with the html elements
    soup = bs4.BeautifulSoup(html_text, 'html.parser')
    container = soup.find(id=container_id)

    # read the content
    with Path(content_path).open() as data:
        content = data.read()
    if content is None:
        print("ERROR opening project html")

    # parse and add the markdown
    html = markdown2.markdown(content)
    parsed = bs4.BeautifulSoup(html, 'html.parser')
    container.append(parsed)

    # save the output
    with open(output_path, "w") as outf:
        outf.write(str(soup))

def create_project_page(site_root, page_name, page_template, children_template, 
                        page_container_id, children_container_id,
                        children_input_path 
                        ):
    """
    Create the project page.

    Inputs
    ------
    * TODO

    """
    # read the project 
    with Path(page_template).open() as data:
        html_text = data.read()
    if html_text is None:
        print("ERROR opening project html")

    # create container with the html elements
    soup = bs4.BeautifulSoup(html_text, 'html.parser')
    project_page = PageBuilder(site_root, page_name, soup.find(id=page_container_id), children_template)

    # for all projects with a markdown description, add the project to the page's content.
    project_folder = Path(children_input_path).glob("**/*.md")
    projects_file = [f for f in project_folder if f.is_file()]
    projects = []
    for p in projects_file:
        # read file
        with p.open() as data:
            md = data.read()
        if md is None:
            print("ERROR opening one of the project: ", p)

        # create html content
        html = markdown2.markdown(md, extras=['metadata'])
        meta = html.metadata
        projects.append({"html": html, "meta": meta})

    # sort the list of projects
    projects = sorted(projects, key= lambda element: element['meta']['priority'])
    for p in projects:
        parsed = bs4.BeautifulSoup(p['html'], 'html.parser')
        project_page.add_children(p['meta'], parsed)

    # Finally, save the project page
    with open(site_root + page_name + '.html', "w") as outf:
        outf.write(str(soup))

if __name__ == "__main__":
    # create project
    create_project_page(site_root = 'outsite/', page_name = 'projects',
                        page_template = './src/projects.html', children_template = './src/children_template.html', 
                        page_container_id = 'projects_list', children_container_id = 'content', 
                        children_input_path = './src/data/projects')

    # create writing page
    create_project_page(site_root = 'outsite/', page_name = 'writings',
                        page_template = './src/writing.html', children_template = './src/children_template.html', 
                        page_container_id = 'article_list', children_container_id = 'content', 
                        children_input_path = './src/data/writing')

    # create main page
    create_index_page("src/index.html", "src/data/text.md", "outsite/index.html")

    # cp images into outsite
    copy_tree("src/images", "outsite/images")

    # cp header and style
    shutil.copyfile("src/header.html", "outsite/header.html")
    shutil.copyfile("src/style.css", "outsite/style.css")
