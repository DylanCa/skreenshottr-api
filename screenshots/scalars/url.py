from graphene import Mutation, String
import re

from graphql import StringValueNode


class URL(String):
    URL_REGEX = "^https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)$"

    @staticmethod
    def serialize(url):
        return url

    @staticmethod
    def parse_value(url):
        if not re.match(URL.URL_REGEX, url):
            raise ValueError("Invalid url format")
        return url

    @staticmethod
    def parse_literal(node):
        if not isinstance(node, StringValueNode):
            raise ValueError("Invalid url format")
        url = node.value
        if not re.match(URL.URL_REGEX, url):
            raise ValueError("Invalid url format")
        return url
