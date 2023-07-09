from graphene import Mutation, String
import re

from graphql import StringValueNode


class Email(String):
    @staticmethod
    def serialize(email):
        return email

    @staticmethod
    def parse_value(email):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("Invalid email format")
        return email

    @staticmethod
    def parse_literal(node):
        if not isinstance(node, StringValueNode):
            raise ValueError("Invalid email format")
        email = node.value
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("Invalid email format")
        return email
