import re
from typing import Self, Any


class UnknownTokenError(Exception):
    """ This exception is for use to be thrown when an unknown token is
        encountered in the token stream. It hols the line number and the
        offending token.
    """

    def __init__(self, token: str, lineno: int) -> None:
        """
        Initialise a new token error
        @param token: The offending bad token
        @param lineno: The line number that caused the error
        @return: None
        """
        self.token: str = token
        self.lineno: int = lineno

    def __repr__(self) -> str:
        """
        Return a string representation of the UnknownTokenError
        @return: Human-readable representation of the error
        """
        return "Line #%s, Found token: %s" % (self.lineno, self.token)


class _InputScanner(object):
    """ This class manages the scanning of a specific input. An instance of it is
        returned when scan() is called. It is built to be great for iteration. This is
        mainly to be used by the Lexer and ideally not directly.
    """

    def __init__(self, lexer: 'Lexer', inp: str) -> None:
        """
        Put the lexer into this instance so the callbacks can reference it if needed.
        @param lexer: The lexer object used to parse user input
        @param inp: The input string
        @return: None
        """
        self._position: int = 0
        self.lexer: Lexer = lexer
        self.input: str = inp

    def __iter__(self) -> Self:
        """
        All the code for iteration is controlled by the class itself.
        This and __next__() are so syntax like `for token in Lexer(...):` is valid and works.
        @return: self
        """
        return self

    def __next__(self) -> tuple[str | None, Any] | StopIteration:
        """
        Used for iteration. It returns token after token until there are no more tokens.
        @return: scan_next
        @raise: StopIteration
        """
        if not self.done_scanning():
            return self.scan_next()
        raise StopIteration

    def done_scanning(self) -> bool:
        """
        A simple function that returns true if scanning is complete and false if it isn't.
        @return: True if scanning is complete, False otherwise
        """
        return self._position >= len(self.input)

    def scan_next(self) -> tuple[str | None, Any] | None | UnknownTokenError:
        """
        Retrieve the next token from the input.
        If the flag `omit_whitespace` is set to True, then it will skip over the whitespace characters present.
        @return: match lastgroup, value if successful, else None, TokenError on failure
        """
        if self.done_scanning():
            return None

        if self.lexer.omit_whitespace:
            match = self.lexer.ws_regexc.match(self.input, self._position)
            if match:
                self._position = match.end()

        match = self.lexer.regexc.match(self.input, self._position)

        if match is None:
            lineno = self.input[:self._position].count("\n") + 1
            raise UnknownTokenError(self.input[self._position], lineno)

        self._position = match.end()
        value = match.group(match.lastgroup)

        if match.lastgroup in self.lexer.callbacks:
            value = self.lexer.callbacks[match.lastgroup](self, value)

        return match.lastgroup, value


class Lexer(object):
    """ A lexical scanner. It takes in an input and a set of rules based
        on regular expressions. It then scans the input and returns the
        tokens one-by-one. It is meant to be used through iterating.
    """

    def __init__(self, scan_rules: iter, case_sensitive=True, omit_whitespace=True) -> None:
        """
        Set up the lexical scanner. Build and compile the regular expression and prepare the whitespace searcher.
        @param scan_rules: An iterable containing regular expressions for valid inputs
        @param case_sensitive: Whether to use case-sensitive matching
        @param omit_whitespace: Whether to omit whitespace in matching
        @return: None
        @raise: TypeError
        """
        self._callbacks = {}
        self.omit_whitespace = omit_whitespace
        self.case_sensitive = case_sensitive
        parts = []
        if not isinstance(scan_rules, list):
            raise TypeError("'Rules' needs to be an iterable")
        if not isinstance(case_sensitive, bool):
            raise TypeError("Case flag needs to be a bool value due to python interpretation of strings")
        for name, rule in scan_rules:
            if not isinstance(rule, str):
                rule, callback = rule
                self._callbacks[name] = callback
            parts.append("(?P<%s>%s)" % (name, rule))
        if self.case_sensitive:  # This line fires for any 'truthy' values in python, which is not ideal
            flags = re.M
        else:
            flags = re.M | re.I
        self.regexc = re.compile("|".join(parts), flags)
        self.ws_regexc = re.compile(r"\s*", re.MULTILINE)

    def scan(self, inp: str) -> iter:
        """
        Return a scanner built for matching through the `inp` field.
        The scanner that it returns is built well for iterating.
        @param inp: The input string to scan
        @return: The scanner object
        """
        if type(inp) is str:
            return _InputScanner(self, inp)
        else:
            inp = str(inp)
            return _InputScanner(self, inp)

    @property
    def callbacks(self):
        return self._callbacks


# noinspection PyUnusedLocal
def stmnt_callback(scanner, token) -> NotImplementedError:
    """
    An example of running the scanner through a function
    @param scanner: The scanner object
    @param token: The token to be passed to the scanner
    @raise: NotImplementedError
    """
    raise NotImplementedError("No longer implemented")


# Setup match rules
rules = [
    ("SUPPLIMENT", r"^([a-zA-Z]+:)|(:[a-zA-Z]+:)"),
    ("OBJECT", r"[a-zA-Z_]\w*\(([a-zA-Z_0-9]\w*|,|\()*\)"),
    ("IDENTIFIER", r"[a-zA-Z_]\w*"),
    ("OPERATOR", r"\+|\-|\\|\*|\="),
    ("DIGIT", r"[0-9]+(\.[0-9]+)?"),
    ("LITERAL", r"\"\w*\""),
    ("END_STMNT", (";", stmnt_callback)),
]

# in backus naur form
# <digit> ::= 1|2|3|4|5|6|7|8|9|0  
# <upper> ::= A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z
# <lower> ::= a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z
# <number> ::= <digit>|<number>
# <underscore>  ::= _
# <word> ::= <upper>|<lower>|<word>
# <IDENTIFIER> ::= <word>|<underscore>|<IDENTIFIER>
# <DIGIT> ::= <number>.<number>
# <OPERATOR> ::= +|-|=|*|\
######################################################
