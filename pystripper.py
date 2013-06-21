#!/usr/bin/python

import sys
import urllib2

from BeautifulSoup import BeautifulSoup, NavigableString

def get_url_html(url):
    return urllib2.urlopen(urllib2.Request(url)).read()


if len(sys.argv) > 1:
    html_file = sys.argv[1]
else:
    html_file ="/tmp/thepage.html"


# Define strip_tags
def strip_tags(soup, invalid_tags, 
               remove_tag_completely):

    for tag in soup.findAll(True, attribute=True):
        if tag.name in remove_tag_completely:
            tag.replaceWith("")

        if tag.name in invalid_tags:
            s = ""

            for c in tag.contents:
                if not isinstance(c, NavigableString):
                    c = strip_tags(unicode(c), 
                                   invalid_tags, 
                                   remove_tag_completely)
                s += unicode(c)

            tag.replaceWith(s)

        for attribute in attributes_to_remove:
            del(tag[attribute])

    return soup

def strip_attributes(soup, attributes_to_remove):
    for attribute in attributes_to_remove:
        for tag in soup.findAll(True):
            del(tag[attribute])

    return soup

# Read the HTML file in as ONE BIG STRING
#html = open(html_file).read()
html = get_url_html(sys.argv[1])

# Retrive the TITLE text from the page
title = BeautifulSoup(html).title.string

# Define the list of tags to remove (while keeping the content)
# E.G., <TAG> foo </TAG> --> foo
invalid_tags = ['span']

# Define list of tags to obliterate
# E.G., <TAG> foo </TAG> --> ""
remove_tag_completely = ['script', 'style', 'head']

# Define a list of attributes to remove
attributes_to_remove = ['style', 'class']

# Initialize variables (priming-read-pattern)
start_keeping = False
new_html = ""

# Read the file one line at a time
for line in open(html_file).readlines():
    
    # Change state to "keeping"
    if "contentarea" in line:
        start_keeping = True

    # If we're keeping, append this line onto "new_html" string.
    if start_keeping:
        new_html += line

def html_output():
    # return the output of new_html striped:
    ret = ("<html>\n"
           "<head><title>%s</title></head>" 
           "<body>" % title)
    
    ret += str(strip_attributes(strip_tags(BeautifulSoup(new_html), 
                                      invalid_tags, 
                                      remove_tag_completely),
                           attributes_to_remove))

    return ret

output_file = open(title + ".html", "w")
output_file.write(html_output())
