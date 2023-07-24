

# https://www.codewars.com/kata/526c7b931666d07889000a3c/train/python


import random
import re
from typing import TypeVar


Token = TypeVar("Token")


class Token:
    TYPES = {
      "INT": r"[0-9]",  # Push this number onto the stack.
      "ADD": r"\+",  # Addition: Pop a and b, then push a+b.
      "SUB": r"\-",  # Subtraction: Pop a and b, then push b-a.
      "MUL": r"\*",  # Multiplication: Pop a and b, then push a*b.
      "DIV": r"/",  # Integer division: Pop a and b, then push b/a, rounded down. If a is zero, push zero.
      "MOD": r"%",  # Modulo: Pop a and b, then push the b%a. If a is zero, push zero.
      "NOT": r"!",  # Logical NOT: Pop a value. If the value is zero, push 1; otherwise, push zero.
      "GT": r"`",  # Greater than: Pop a and b, then push 1 if b>a, otherwise push zero.
      "RIGHT": r">",  # Start moving right.
      "LEFT": r"<",  # Start moving left.
      "UP": r"\^",  # Start moving up.
      "DOWN": r"v",  # Start moving down.
      "RAND": r"\?",  # Start moving in a random cardinal direction.
      "HPOP": r"_",  # Pop a value; move right if value = 0, left otherwise.
      "VPOP": r"\|",  # Pop a value; move down if value = 0, up otherwise.
      "STRING": r"\"",  # Start string mode: push each character's ASCII value all the way up to the next ".
      "DUP": r":",  # Duplicate value on top of the stack. If there is nothing on top of the stack, push a 0.
      "SWAP": r"\\",  # Swap two values on top of the stack. If there is only one value, pretend there is an extra 0 on bottom of the stack.
      "POP": r"\$",  # Pop value from the stack and discard it.
      "IPOP": r"\.",  # Pop value and output as an integer.
      "APOP": r",",  # Pop value and output the ASCII character represented by the integer code that is stored in the value.
      "SKIP": r"#",  # Trampoline: Skip next cell.
      "PUT": r"p",  # A "put" call (a way to store a value for later use). Pop y, x and v, then change the character at the position (x,y) in the program to the character with ASCII value v.
      "GET": r"g",  # A "get" call (a way to retrieve data in storage). Pop y and x, then push ASCII value of the character at that position in the program.
      "END": r"@",  # End program.
      "NEWLINE": r"\n",  # New line delimiter.
      "NOOP": r" ",  # No-op. Does nothing.
      "UNKNOWN": r"."  # Catchall
    }

    def __init__(self, string: str):
        self._length: int = 0
        self._type: str = ""

        for type_name, type_regex in Token.TYPES.items():
            match = re.match(type_regex, string)
            if(match is not None and self._length < len(match_string := string[:match.end()])):
                self._type = type_name
                self._length = len(match_string)

        if(self._type == ""):
            raise Exception(f"Unknown token '{string}'")

        self._token: str = string[:self._length]


    def __eq__(self, right: Token | str) -> bool:
        if(isinstance(right, Token)):
            right = right._type

        return self._type == right


    def __len__(self) -> int:
        return self._length


    def __repr__(self) -> str:
        return self._token


    def __int__(self) -> str:
        return int(self._token)


    def __str__(self) -> str:
        return self._token


class Program:
    def __init__(self, raw_code: str, debug: bool=False):
        self._current_position = [0, 0]
        self._current_direction = [0, 1]
        self._debug: bool = debug
        self._raw_code: str = raw_code
        self._stdout: str = ""
        self._stack = []
        self._tokens = []

        for line in raw_code.split("\n"):
            line_tokens = []
            while(line):
                line_tokens.append(token := Token(line))
                line = line[len(token):]

            self._tokens.append(line_tokens)

        if(self._debug):
            self.print_program_code()


    def __call__(self) -> Token:
        """
        Get the token for the current position
        """
        return self._tokens[self._current_position[0]][self._current_position[1]]


    # ———————————————————————————————————————————————————— STACK  ———————————————————————————————————————————————————— #

    def __str__(self) -> str:
        """
        Return the output string (buffer)
        """
        return self._stdout


    def print_program_code(self):
        lines = self._raw_code.split("\n")
        digit_count = 2
        max_length = max(len(line) for line in lines)
        print()
        print("—" * (max_length * (digit_count + 1) + 10))
        print(f"""|     {f"".join(f"{x:<{digit_count+1}}" for x in range(max_length))}   |""")
        for x, line in enumerate(lines):
            line = "  ".join(list(line))
            print(f"""| {x}   {line:<{max_length * (digit_count + 1)}}   |""")
        print("—" * (max_length * (digit_count + 1) + 10))


    # —————————————————————————————————————————————————— ITERATION  —————————————————————————————————————————————————— #

    def __iter__(self):
        return self


    def __next__(self):
        if(self._debug):
            print(f"[{self._current_position[0]:2}, {self._current_position[1]:2}] ", end="")
        token = self()
        if(self._debug):
            print(f"{str(token)} ({token._type}) {str(self._stack)}", end=" -> ")
        getattr(self, token._type)()
        if(self._debug):
            print(str(self._stack))
        self._current_position = [self._current_position[x] + self._current_direction[x] for x in [0, 1]]


    # ———————————————————————————————————————————————————— STACK  ———————————————————————————————————————————————————— #

    def __add__(self, value: int) -> None:
        """
        Add a value to the stack
        """
        self._stack.append(value)


    def __iadd__(self, value: int) -> None:
        """
        Add a value to the stack
        """
        self._stack.append(value)
        return self


    def __neg__(self) -> int:
        """
        Pop a value from the stack and return it
        """
        return self._stack.pop()


    # —————————————————————————————————————————————————— OPERATIONS —————————————————————————————————————————————————— #

    def INT(self):
        """
        Push this number onto the stack.
        """
        token = self()
        self += int(token)


    def ADD(self):
        """
        Addition: Pop a and b, then push a+b.
        """
        left, right = -self, -self
        self += (left + right)


    def SUB(self):
        """
        Subtraction: Pop a and b, then push b-a.
        """
        right, left = -self, -self
        self += (left - right)


    def MUL(self):
        """
        Multiplication: Pop a and b, then push a*b.
        """
        left, right = -self, -self
        self += (left * right)


    def DIV(self):
        """
        Integer division: Pop a and b, then push b/a, rounded down. If a is zero, push zero.
        """
        left, right = -self, -self
        self += (left // right)


    def MOD(self):
        """
        Modulo: Pop a and b, then push the b%a. If a is zero, push zero.
        """
        left, right = -self, -self
        self += (left % right)


    def NOT(self):
        """
        Logical NOT: Pop a value. If the value is zero, push 1; otherwise, push zero.
        """
        self += int(-self == 0)


    def GT(self):
        """
        Greater than: Pop a and b, then push 1 if b>a, otherwise push zero.
        """
        left, right = -self, -self
        self += int(left < right)


    def RIGHT(self):
        """
        Start moving right.
        """
        self._current_direction = [0, 1]


    def LEFT(self):
        """
        Start moving left.
        """
        self._current_direction = [0, -1]


    def UP(self):
        """
        Start moving up.
        """
        self._current_direction = [-1, 0]


    def DOWN(self):
        """
        Start moving down.
        """
        self._current_direction = [1, 0]


    def RAND(self):
        """
        Start moving in a random cardinal direction.
        """
        self._current_direction = [0, 0]
        self._current_direction[random.randint(0,1)] = {0: -1, 1: 1}[random.randint(0, 1)]


    def HPOP(self):
        """
        Pop a value; move right if value = 0, left otherwise.
        """
        value = -self
        self._current_direction = {True: [0, 1], False: [0, -1]}[value == 0]


    def VPOP(self):
        """
        Pop a value; move down if value = 0, up otherwise.
        """
        value = -self
        self._current_direction = {True: [1, 0], False: [-1, 0]}[value == 0]


    def STRING(self):
        """
        Start string mode: push each character's ASCII value all the way up to the next ".
        """
        string = "\""
        self._current_position = [self._current_position[x] + self._current_direction[x] for x in [0, 1]]

        direction = next(x for x, direction in enumerate(self._current_direction) if(direction != 0))
        max_string_span = len(self._tokens) if(direction == 0) else len(self._tokens[self._current_position[0]])
        for _ in range(max_string_span):
            if((token := self()) == "STRING"):
                break

            self += ord(str(self()))
            self._current_position = [self._current_position[x] + self._current_direction[x] for x in [0, 1]]


    def DUP(self):
        """
        Duplicate value on top of the stack. If there is nothing on top of the stack, push a 0.
        """
        if(len(self._stack) == 0):
            self += 0
        else:
            self += self._stack[-1]


    def SWAP(self):
        """
        Swap two values on top of the stack. If there is only one value, pretend there is an extra 0 on bottom of the
        stack.
        """
        left, right = -self, -self
        self += left
        self += right


    def POP(self):
        """
        Pop value from the stack and discard it.
        """
        -self


    def IPOP(self):
        """
        Pop value and output as an integer.
        """
        self._stdout += str(-self)


    def APOP(self):
        """
        Pop value and output the ASCII character represented by the integer code that is stored in the value.
        """
        # token = int(-self)
        # print(token)
        self._stdout += chr(int(-self))


    def SKIP(self):
        """
        Trampoline: Skip next cell.
        """
        self._current_position = [self._current_position[x] + self._current_direction[x] for x in [0, 1]]


    def PUT(self):
        """
        A "put" call (a way to store a value for later use). Pop y, x and v, then change the character at the position
        (x,y) in the program to the character with ASCII value v.
        """
        x, y, v = -self, -self, -self
        self._tokens[x][y] = Token(chr(v))


    def GET(self):
        """
        A "get" call (a way to retrieve data in storage). Pop y and x, then push ASCII value of the character at that
        position in the program.
        """
        x, y = -self, -self
        self += ord(str(self._tokens[x][y]))


    def END(self):
        """
        End program.
        """
        raise StopIteration


    def NOOP(self):
        """
        No-op. Does nothing.
        """
        return


    def UNKNOWN(self):
        """
        No-op. Does nothing.
        """
        raise Exception(f"No known operation for '{str(self())}'")

def interpret(code):
    program = Program(code)
    [_ for _ in program]

    return str(program)


print(interpret('>987v>.v\nv456<  :\n>321 ^ _@') == '123456789')
print(interpret('>25*"!dlroW olleH":v\n                v:,_@\n                >  ^') == 'Hello World!\n')
print(interpret('08>:1-:v v *_$.@ \n  ^    _$>\\:^') == '40320')
print(interpret('01->1# +# :# 0# g# ,# :# 5# 8# *# 4# +# -# _@') == '01->1# +# :# 0# g# ,# :# 5# 8# *# 4# +# -# _@')
print(interpret('2>:3g" "-!v\\  g30          <\n |!`"&":+1_:.:03p>03g+:"&"`|\n @               ^  p3\\" ":<\n2 2345678901234567890123456789012345678') == '23571113171923293137')

