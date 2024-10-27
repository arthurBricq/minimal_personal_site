"""
A python script that generates your personal website
"""

from distutils.dir_util import copy_tree
import shutil

from page_builder import create_index_page
from page_builder import create_page_with_children


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

if __name__ == "__main__":
    print("Starting to generate site")

    SITE_ROOT = "./outsite"
    SITE_DATA = "./data/"

    # create project page
    create_page_with_children(
        site_root=SITE_ROOT,
        page_name="projects",
        page_template="./templates/projects.html",
        children_template="./templates/children_template.html",
        page_container_id="projects_list",
        children_input_path=SITE_DATA + "projects",
        header_getter=get_header
    )
    print("Projects generated successfully")

    # create writing page
    create_page_with_children(
        site_root=SITE_ROOT,
        page_name="writings",
        page_template="./templates/writing.html",
        children_template="./templates/children_template.html",
        page_container_id="article_list",
        children_input_path=SITE_DATA + "writing",
        header_getter=get_header
    )
    print("Articles generated successfully")

    # create main page
    create_index_page(
        template_path="templates/index.html", 
        content_path=SITE_DATA + "main_page.md",  
        output_path=SITE_ROOT + "/index.html", 
        container_id="markdown_container", 
        header_getter=get_header)
    print("Main page generated successfully")

    # cp images into outsite
    copy_tree(SITE_DATA + "images", SITE_ROOT + "/images")

    # cp header and style
    shutil.copyfile("templates/header.html", SITE_ROOT + "/header.html")
    shutil.copyfile("templates/style.css", SITE_ROOT + "/style.css")
    shutil.copyfile(SITE_DATA + "resume.pdf", SITE_ROOT + "/resume.pdf")

    print("ressources copied successfully")
    print("finished")
