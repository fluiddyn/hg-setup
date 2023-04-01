from pathlib import Path

from lark import Lark, Token, Transformer

from .ast import (
    Assignment,
    Code,
    Dict,
    DimensionSet,
    Directive,
    FoamInputFile,
    List,
    Value,
    VariableAssignment,
)

here = Path(__file__).absolute().parent

grammar = (here / "grammar.lark").read_text()

lark_parser = Lark(grammar, start="value", lexer="basic")


def parse(text):
    text = "\n".join(line.rstrip() for line in text.split("\n"))
    tree = lark_parser.parse(text)
    return FoamTransformer().transform(tree)


def dump(tree):
    return tree.dump()


def filter_no_newlines(items):
    return [item for item in items if item is not None]


def _convert_to_number(number):
    number = str(number)
    try:
        return int(number)
    except ValueError:
        return float(number)


class FoamTransformer(Transformer):
    def SIGNED_NUMBER(self, token):
        return _convert_to_number(token)

    def CNAME(self, token):
        return token.value

    def NEWLINE(self, nodes):
        return None

    def ESCAPED_STRING(self, token):
        return token.value

    def DOUBLE_NAME(self, token):
        return token.value

    def EQKEY(self, token):
        return token.value

    def MACRO_TERM(self, token):
        return token.value[1:]

    def dimension_set(self, items):
        return DimensionSet(
            [
                item
                for item in items
                if not (isinstance(item, Token) and item.type == "NEWLINE")
            ]
        )

    def macro(self, nodes):
        return "$" + nodes[0]

    def directive(self, nodes):
        if len(nodes) != 1:
            raise RuntimeError
        return str(nodes[0])

    def list(self, items):
        return List(
            [
                item
                for item in items
                if not (isinstance(item, Token) and item.type == "NEWLINE")
                and item is not None
            ]
        )

    def file(self, nodes):
        first_assignment = nodes[0]
        if first_assignment.name == "FoamFile":
            info_dict = first_assignment.value
            nodes = nodes[1:]
        else:
            info_dict = None

        for node in nodes:
            if isinstance(node.value, List):
                node.value.add_name(node.name)

        return FoamInputFile(info_dict, {node.name: node.value for node in nodes})

    def var_assignment(self, nodes):
        nodes = [node for node in nodes if node is not None]
        dimension_set = None
        name_in_value = None
        name = nodes.pop(0)
        if len(nodes) == 1:
            value = nodes[0]
        else:
            try:
                index_dimension = [
                    isinstance(elem, DimensionSet) for elem in nodes
                ].index(True)
            except ValueError:
                if all([isinstance(elem, str) for elem in nodes]):
                    value = " ".join(nodes)
                elif (
                    len(nodes) == 2
                    and isinstance(nodes[0], str)
                    and isinstance(nodes[1], List)
                ):
                    value = nodes[1]
                    value._name = nodes[0]
                else:
                    value = nodes
            else:
                dimension_set = nodes.pop(index_dimension)

                if len(nodes) == 2:
                    name_in_value, value = nodes

                elif len(nodes) == 1:
                    value = nodes[0]
                else:
                    raise NotImplementedError()
                value = Value(value, name=name_in_value, dimension=dimension_set)
        return VariableAssignment(name, value)

    def dict_assignment(self, nodes):
        nodes = filter_no_newlines(nodes)
        directive = None

        if len(nodes) == 1:
            name = nodes.pop(0)
            return Assignment(name, Dict(data={}, name=name))

        if isinstance(nodes[1], str) and nodes[1].startswith("#"):
            # like #codeStream
            directive = nodes.pop(1)

        name = nodes.pop(0)

        for node in nodes:
            if isinstance(node.value, List):
                node.value.add_name(node.name)
        return Assignment(
            name,
            Dict(
                data={node.name: node.value for node in nodes},
                name=name,
                directive=directive,
            ),
        )

    def list_assignment(self, nodes):
        nodes = filter_no_newlines(nodes)
        if len(nodes) == 3:
            name, subname, the_list = nodes
            name_internal = name + " " + subname
        elif len(nodes) == 2:
            name, the_list = nodes
            name_internal = name
        else:
            raise NotImplementedError
        the_list._name = name_internal
        return Assignment(name, the_list)

    def dimension_assignment(self, nodes):
        nodes = [node for node in nodes if node is not None]
        name = nodes.pop(0)

        if len(nodes) == 3:
            return Assignment(name, Value(nodes[-1], nodes[0], nodes[-2]))
        elif len(nodes) == 2:
            return Assignment(name, Value(nodes[-1], dimension=nodes[-2]))
        else:
            raise RuntimeError()

    def macro_assignment(self, nodes):
        nodes = [node for node in nodes if node is not None]
        if len(nodes) != 1:
            raise NotImplementedError
        name = nodes.pop(0)
        return Assignment(name, "")

    def equal_assign(self, nodes):
        if len(nodes) != 2:
            raise RuntimeError
        value = nodes[1]
        if hasattr(value, "dump"):
            value = value.dump()
        return f"{nodes[0]}={value}"

    def directive_assignment(self, nodes):
        nodes = [node for node in nodes if node is not None]
        if len(nodes) == 2:
            directive, content = nodes
        else:
            directive = nodes.pop(0)
            function_name = nodes.pop(0)
            arguments = ", ".join(nodes)
            content = function_name + f"({arguments})"
        key = directive + " " + content
        return Assignment(key, Directive(directive, content))

    def code_assignment(self, nodes):
        nodes = filter_no_newlines(nodes)
        if len(nodes) != 2:
            raise NotImplementedError
        name, code = nodes
        code = str(code)
        code = code.split("\n", 1)[-1]
        code = code.rsplit("\n", 1)[0]
        return Assignment(name, Code(name, code))
