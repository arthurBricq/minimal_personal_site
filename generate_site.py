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
        print(f"Folder {path} was successfully deleted")
    except OSError as e:
        print(f"Could not delete folder {path}: {e}")
    # creation
    os.makedirs(path)

def get_header(root = ".") -> str:
    return f"""
<header>
    Arthur Bricq
</header>

<nav>
    <a href="{root}/resume.pdf">My resume</a>
    <a href="{root}/writings.html">Writing</a>
    <a href="{root}/projects.html">Projects</a>
    <a href="{root}/index.html">About</a>
</nav>
    """


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
        self._root = site_root
        self._name = page_name
        self._editor = html_editor
        self._template_path = template
        clear_folder(site_root + page_name)

    def add_children(self, _meta, _soup):
        """
        Add a project to the page's content
        * meta contains information about the project
        * soup contains the parsed
        """
        # create html div with a link to the project's page.
        tag = self.create_html_link(_meta)

        # Modify the project page
        self._editor.append(tag)

        # Create a new page with the project's description
        self._create_project_page(_meta, _soup)

    def _create_project_page(self, _meta, _soup):
        # Load the template for children pages
        with Path(self._template_path).open() as data:
            html_text = data.read()
        if html_text is None:
            print("ERROR opening project's page html template")

        # Find where to add information
        template = bs4.BeautifulSoup(html_text, "html.parser")
        box = template.find(id="content")
        if box is None: return

        # Fill the template with the provided html
        box.append(_soup)

        # Fill the header
        header_container = template.find(id = "header_container")
        if header_container is None: return
        parsed = bs4.BeautifulSoup(get_header(root = ".."), "html.parser")
        header_container.append(parsed)

        # Save the file
        title = _meta["title"]
        with open(self._root + self._name + f"/{title}.html", "w") as file:
            file.write(str(template))

    def create_html_link(self, _meta):
        title = _meta["title"]
        html_list = ""
        html_list += (
            '<li class="project_item"><a href="./{}/{}.html">{}</a> </li>'.format(
                self._name, title, title
            )
        )
        if "keywords" in _meta:
            html_list += '<p class="keyword">{}</p>'.format(_meta["keywords"])
        if "github" in _meta:
            html_list += (
                '<p class="description">Link to <a href="{}">Github</a></p>'.format(
                    _meta["github"]
                )
            )

        # Add the description
        html_list += '<p class="description">{}</p>'.format(_meta["description"])
        # Add the image
        if "featuredImage" in _meta:
            html_list += '<img src="{}" class="thumbnail">'.format(_meta["featuredImage"])

        tag = bs4.BeautifulSoup(html_list, "html.parser")
        return tag



def create_index_page(
    template_path, content_path, output_path, container_id="markdown_container"
):
    """
    Creates the index.html page by filling the template path from the content found in .md file
    """
    # read the template
    with Path(template_path).open() as data:
        html_text = data.read()
    if html_text is None:
        print("ERROR opening project html")

    # create container with the html elements
    soup = bs4.BeautifulSoup(html_text, "html.parser")
    text_container = soup.find(id=container_id)
    if text_container is None: return

    # read the content
    with Path(content_path).open() as data:
        content = data.read()
    if content is None:
        print("ERROR opening project html")

    # parse and add the markdown
    html = markdown2.markdown(content)
    parsed = bs4.BeautifulSoup(html, "html.parser")
    text_container.append(parsed)

    # fill the header
    header_container = soup.find(id = "header_container")
    if header_container is None: return
    parsed = bs4.BeautifulSoup(get_header(), "html.parser")
    header_container.append(parsed)

    # save the output
    with open(output_path, "w") as file:
        file.write(str(soup))


def create_page_with_children(
    site_root,
    page_name,
    page_template,
    children_template,
    page_container_id,
    children_input_path,
):
    """
    Creates a page with associated children pages, listed under this page.
    """
    # read the project
    with Path(page_template).open() as data:
        html_text = data.read()
    if html_text is None:
        print("ERROR opening project html")

    # create container with the html elements
    soup = bs4.BeautifulSoup(html_text, "html.parser")
    project_page = PageBuilder(
        site_root, page_name, soup.find(id=page_container_id), children_template
    )

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

        # parse the .md and format it as html
        html = markdown2.markdown(md, extras=["metadata"])
        meta = html.metadata
        projects.append({"html": html, "meta": meta})

    # sort the list of projects and add them to the parent page
    projects = sorted(projects, key=lambda element: element["meta"]["priority"])
    for p in projects:
        parsed = bs4.BeautifulSoup(p["html"], "html.parser")
        project_page.add_children(p["meta"], parsed)

    # fill the header
    header_container = soup.find(id = "header_container")
    if header_container is None: return
    parsed = bs4.BeautifulSoup(get_header(), "html.parser")
    header_container.append(parsed)

    # Finally, save the project page
    with open(site_root + page_name + ".html", "w") as file:
        file.write(str(soup))


if __name__ == "__main__":
    print("Starting to generate site")

    # create project
    create_page_with_children(
        site_root="outsite/",
        page_name="projects",
        page_template="./src/projects.html",
        children_template="./src/children_template.html",
        page_container_id="projects_list",
        children_input_path="./src/data/projects",
    )

    print("Projects generated successfully")

    # create writing page
    create_page_with_children(
        site_root="outsite/",
        page_name="writings",
        page_template="./src/writing.html",
        children_template="./src/children_template.html",
        page_container_id="article_list",
        children_input_path="./src/data/writing",
    )

    print("Articles generated successfully")

    # create main page
    create_index_page("src/index.html", "src/data/main_page.md", "outsite/index.html")

    print("Main page generated successfully")

    # cp images into outsite
    copy_tree("src/images", "outsite/images")

    # cp header and style
    shutil.copyfile("src/header.html", "outsite/header.html")
    shutil.copyfile("src/style.css", "outsite/style.css")
    shutil.copyfile("src/resume.pdf", "outsite/resume.pdf")

    print("ressources copied successfully")
    print("finished")
