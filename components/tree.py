def vertical_lines(last_node_flags):
    vertical_lines = []
    vertical_line = '\u2502'
    for last_node_flag in last_node_flags[0:-1]:
        if not last_node_flag:
            vertical_lines.append(vertical_line + ' ' * 3)
        else:
            vertical_lines.append(' ' * 4)
    return ''.join(vertical_lines)

def horizontal_line(last_node_flags):
    horizontal_line = '\u251c\u2500\u2500 '
    horizontal_line_end = '\u2514\u2500\u2500 '
    return horizontal_line_end if last_node_flags[-1] else horizontal_line

class Tree:
    def __init__(self):
        self.nodes = {}
        self.root = None

    def is_expandable(self, node):
        if node.terminal:
            return False
        return len(node.untried_actions) > 0

    def iter(self, identifier, depth, last_node_flags):
        node = self.root if identifier is None else self.nodes[identifier]

        if depth == 0:
            yield "", node
        else:
            yield vertical_lines(last_node_flags) + horizontal_line(last_node_flags), node

        children = [self.nodes[identifier] for identifier in node.children_identifiers]
        last_index = len(children) - 1

        depth += 1
        for index, child in enumerate(children):
            last_node_flags.append(index == last_index)
            for edge, node in self.iter(child.identifier, depth, last_node_flags):
                yield edge, node
            last_node_flags.pop()

    def add_node(self, node, parent=None):
        self.nodes.update({node.identifier: node})

        if parent is None:
            self.root = node
            self.nodes[node.identifier].parent = None
        else:
            self.nodes[parent.identifier].children_identifiers.append(node.identifier)
            self.nodes[node.identifier].parent_identifier = parent.identifier

    def children(self, node):
        return [self.nodes[identifier] for identifier in self.nodes[node.identifier].children_identifiers]

    def parent(self, node):
        parent_identifier = self.nodes[node.identifier].parent_identifier
        return None if parent_identifier is None else self.nodes[parent_identifier]

    def show(self):
        lines = ""
        for edge, node in self.iter(identifier=None, depth=0, last_node_flags=[]):
            lines += "{}{}\n".format(edge, node)
        return lines
    
    def get_visit_count(self, state, action=None):
        count = 0
        for node in self.nodes.values():
            if node.state == state:
                if action is None:
                    count += node.num_visits
                elif node.action == action:
                    count += node.num_visits
        return count

