from .tokens import TokenType, Token


class InterpreterExceptiont(Exception):
    pass


class Interpreter:

    def __init__(self):
        self._pos: int = 0
        self._current_token: Token = None
        self._text: str = ""
        self._current_char: str = None

    def _next_token(self) -> Token:
        while self._current_char != None:

            if self._current_char == " ":
                self.skip()
                continue
            if self._current_char.isdigit():
                return Token(TokenType.NUMBER, self._number())
            if self._current_char == "+":
                char = self._current_char
                self._forward()
                return Token(TokenType.PLUS, char)
            if self._current_char == "-":
                char = self._current_char
                self._forward()
                return Token(TokenType.MINUS, char)
            raise InterpreterExceptiont(f"bad token{self._current_char}")
        return Token(TokenType.EOS, None)

    def _forward(self):
        self._pos += 1
        if self._pos >= len(self._text):
            self._current_char = None
        else:
            self._current_char = self._text[self._pos]

    def skip(self):
        while self._current_char and self._current_char == " ":
            self._forward()

    def _number(self):
        result: list = []
        while self._current_char and self._current_char.isdigit():
            result.append(self._current_char)
            self._forward()
            if self._current_char == '.' and self._current_char != result[0]:
                result.append(self._current_char)
                self._forward()
        return "".join(result)


    def _check_token_type(self, type_: TokenType):
        if self._current_token.type_ == type_:
            self._current_token = self._next_token()
        else:
            raise InterpreterExceptiont("invalid token order")

    def _expr(self) -> int or InterpreterExceptiont:
        self._current_token = self._next_token()
        left = self._current_token
        self._check_token_type(TokenType.NUMBER)
        op = self._current_token  # Оператор читаем
        if op.type_ == TokenType.PLUS:
            self._check_token_type(TokenType.PLUS)
        else:
            self._check_token_type(TokenType.MINUS)
        right = self._current_token
        self._check_token_type(TokenType.NUMBER)
        if op.type_ == TokenType.PLUS:
            return float(left.value) + float(right.value)
        elif op.type_ == TokenType.MINUS:
            return float(left.value) - float(right.value)
        return InterpreterExceptiont("bad operand")

    def __call__(self, text: str):
        return self.interpret(text)

    def interpret(self, text: str) -> float:
        self._text = text
        self._pos = -1
        self._forward()
        return self._expr()
