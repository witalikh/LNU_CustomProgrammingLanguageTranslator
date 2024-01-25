"""
Miscellaneous code, not directly related with translation process
"""
import re


class CustomEnum:
    """
    Custom enumeration class that behaves almost as AttrDict
    """
    @classmethod
    def __const_attrs_dict__(cls):

        if not hasattr(cls, "_inner_dict"):
            new_dct = cls.__dict__.copy()
            for key in cls.__dict__.keys():
                if key.startswith("__") and key.endswith("__"):
                    new_dct.pop(key, None)
            cls._inner_dict = new_dct

        # noinspection PyUnresolvedReferences
        return cls._inner_dict

    @classmethod
    def keys(cls):
        return cls.__const_attrs_dict__().keys()

    @classmethod
    def values(cls):
        return cls.__const_attrs_dict__().values()


def join_bounded_keywords_as_regex(lst: list | tuple) -> str:
    """
    Join a list of words into a regular expression.
    All words are escaped and bounded.
    :param lst: list or tuple of keywords
    :return: regular expression for the keywords
    """
    return "|".join(map(lambda x: bounded(x), lst))


def bounded(s: str) -> str:
    """
    Escape and bound (meaning that regex should consider the word as whole) keyword
    :param s: string for keyword
    :return: bounded string
    """
    return rf'\b{re.escape(s)}\b'
