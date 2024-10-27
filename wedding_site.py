
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

<div style="font-size: larger; font-style: italic; color: grey;">
Susanne & Arthur's Wedding
</div>

<nav>
    <a href="{root}/index.html">Home</a>
    <a href="{root}/cv.html">Castelvecchio</a>
</nav>
    """

if __name__ == "__main__":
    print("Starting to generate site")

    SITE_ROOT = "./outsite_wedding"
    SITE_DATA = "./data_wedding/"

    # create main page
    create_index_page(
        template_path="templates_wedding/index.html", 
        content_path=SITE_DATA + "index.md",  
        output_path=SITE_ROOT + "/index.html", 
        container_id="markdown_container", 
        header_getter=get_header)

    create_index_page(
        template_path="templates_wedding/page.html",
        content_path=SITE_DATA + "cv.md",
        output_path=SITE_ROOT + "/cv.html",
        container_id="markdown_container",
        header_getter=get_header)

    # cp images into outsite
    copy_tree(SITE_DATA + "images", SITE_ROOT + "/images")

    # cp header and style
    shutil.copyfile("templates_wedding/header.html", SITE_ROOT + "/header.html")
    shutil.copyfile("templates_wedding/style.css", SITE_ROOT + "/style.css")

    print("ressources copied successfully")
    print("finished")
