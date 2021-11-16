from interpreter import Interpreter, Parser
import interpreter

if __name__ == "__main__":
    parser = Parser()
    print(parser.parse("2 + 2"))
