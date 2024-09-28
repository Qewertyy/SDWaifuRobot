# Credits for this parser goes to Kirill R. <https://github.com/python273>

from html.parser import HTMLParser
from html.entities import name2codepoint
from .constants import ALLOWED_TAGS, VOID_ELEMENTS, BLOCK_ELEMENTS


class HtmlToNodesParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)

        self.nodes = []

        self.current_nodes = self.nodes
        self.parent_nodes = []

        self.last_text_node = None

        self.tags_path = []

    def add_str_node(self, s):
            self.current_nodes.append(s)

    def handle_starttag(self, tag, attrs_list):
        if tag not in ALLOWED_TAGS:
            raise Exception(f'{tag} tag is not allowed')

        if tag in BLOCK_ELEMENTS:
            self.last_text_node = None

        node = {'tag': tag}
        self.tags_path.append(tag)
        self.current_nodes.append(node)

        if attrs_list:
            attrs = {}
            node['attrs'] = attrs

            for attr, value in attrs_list:
                attrs[attr] = value

        if tag not in VOID_ELEMENTS:
            self.parent_nodes.append(self.current_nodes)
            self.current_nodes = node['children'] = []

    def handle_endtag(self, tag):
        if tag in VOID_ELEMENTS:
            return

        if not len(self.parent_nodes):
            raise Exception(f'{tag} missing start tag')

        self.current_nodes = self.parent_nodes.pop()

        last_node = self.current_nodes[-1]

        if last_node['tag'] != tag:
            raise Exception(f'{tag} tag closed instead of {last_node["tag"]}')

        self.tags_path.pop()

        if not last_node['children']:
            last_node.pop('children')

    def handle_data(self, data):
        self.add_str_node(data)

    def handle_entityref(self, name):
        self.add_str_node(chr(name2codepoint[name]))

    def handle_charref(self, name):
        if name.startswith('x'):
            c = chr(int(name[1:], 16))
        else:
            c = chr(int(name))

        self.add_str_node(c)

    def get_nodes(self):
        if self.parent_nodes:
            not_closed_tag = self.parent_nodes[-1][-1]['tag']
            raise Exception(f'{not_closed_tag} tag is not closed')

        return self.nodes
    
def htmlToNodes(html):
    parser = HtmlToNodesParser()
    parser.feed(html)
    return parser.get_nodes()