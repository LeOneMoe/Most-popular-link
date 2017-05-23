import re
import lxml.html
import requests


def link_graph(extracted_links, link, graph):

    for extracted_link in extracted_links:

        if extracted_link not in graph:
            graph[extracted_link] = [link]

        elif link not in graph[extracted_link]:
            graph[extracted_link].append(link)

    return graph


def extract_all_links(html, filter_hash=True, filter_regexp=r'^[0-9a-zA-Z_]*\.html$'):

    if html == '':
        return []

    html = lxml.html.fromstring(html)
    links = set(html.xpath("(//td)[3]//a/@href"))

    if filter_hash:
        links = [link for link in links if not link.startswith('#')]

    if filter_regexp:
        links = [link for link in links if re.match(filter_regexp, link) is not None]

    return links


def most_popular_link(graph):

    most_popular = ["", 0]

    for link in graph:

        bad_link = "lekcii_po_vysshei_matematike.html"

        if link != bad_link and len(graph[link]) > most_popular[1]:

            most_popular = [link, len(graph[link])]

    return most_popular


def main():

    all_links = open("links.txt", "r")

    graph = {}

    for link in all_links:

        link_graph(extract_all_links(requests.get(link.strip()).text), link, graph)

    all_links.close()

    return " ".join(map(str, most_popular_link(graph)))


print(main())
