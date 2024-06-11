"""
For testing and debugging purposes, coz for now I'm lazy for unit tests
"""
from frontend.lexer import Lexer
from frontend.syntax import RULES
from frontend.parser import Parser
from frontend.type_checking.entrypoint import type_check_program
# from frontend.desugaring.main import desugar_ast_tree


def scenario_1() -> None:
    code_example = (r"""
function[double] circleArea(double radius){
    # Handle specific user inputs as zeros for sake of simplicity
    double PI := 3.1415;
    if (radius <= 0) { return 0; }
    return PI * radius ** 2;
}

string x;
input(ref x);
print("The circle area is: \n");
print(circleArea(integerFromString(x)));
    
    """)

    lexer = Lexer(RULES)
    lexemes_iter = lexer.scan(code_example)
    # lexemes = lexer.scan(code_example)
    # for lexeme in lexemes:
    #     print(f'\033[95m<\033[0m\033[93m{lexeme.type}\033[0m   \033[94m{lexeme.value}\033[0m \033[95m>\033[0m')
    parser = Parser(lexemes_iter)
    x = parser.parse()
    type_check_program(x)
    # print(x)

    with open('example.out', 'w') as f:
        x.translate(f)


def scenario_2() -> None:
    # -3**5 - (2 + 2) * 2 / (3 -4) + 3*5**2
    # -3 * -5 ** 2 + func(1, 2, 3, "Lol", `\xA0\xF3`, "(]}{}\r", true, false, null, undefined) [111, 0]
    # (func(a+b*c, b) + 3 << 5 | 4) <= 19 + 5

    code_example = (r"""
    function[float] ff() {
        return 3.141592653589793;
    }

    function[integer] some_func(custom_class[integer, 4] f := 1, integer x) {
        const reference custom_class[integer, 1, my_array[array[integer, 3], 5]] z = new Custom_Class();
        integer y := 123 + 5 % 7 ** 5;
        return 2 * x ** 2 % 3;
    }

    integer i := 0;
    while (4 < i <= 5) {
        print(some_func(3 * i + 1));
        i := i + 1;
    };
    """)

    lexer = Lexer(RULES)
    lexemes_iter = lexer.scan(code_example)
    # print(*lexemes, sep="\n")

    parser = Parser(lexemes_iter)
    x = parser.parse()
    # print(x)
    type_check_program(x)


def scenario_3() -> None:
    code_example = (r"""
    function bubble_sort(reference array[float, ?] arr)
{
    # culprit is here
    integer array_length := arr->length();

    integer i := 0;
    while (i < array_length)
    {
        integer j := 0;
        float buffer;
        boolean swapped := false;

        while (j < array_length - 1 - i) {
            if (arr[j] > arr[j+1]) {
                buffer := arr[j];
                arr[j] := arr[j+1];
                arr[j+1] := buffer;
                swapped := true;
            }
            j := j + 1;
        }
        if (swapped) {
            break;
        }
        i := i + 1;
    }
}

function[float] sum_of_elements(const reference array[float, ?] arr)
{
    integer length := arr->length();
    float _sum := 0;
    integer i := 0;
    while (i < length) {
        _sum := _sum + arr[i];
        i := i + 1;
    }
    return _sum;
}

function Main()
{
    array[float, 7] x := [-3, -1.3, 4, 5, 3.2, 0, 4];
    print(sum_of_elements(reference x));
    bubble_sort(reference x);
    print(x);
}

Main();
    """)

    lexer = Lexer(RULES)
    lexemes_iter = lexer.scan(code_example)

    parser = Parser(lexemes_iter)
    x = parser.parse()
    print(x)


def scenario_4():
    code_example = (r"""
class my_class{
    public integer x;
    public constructor(integer x){
        this.x := x;
    }

    public static function[my_class] operator + (my_class x, integer y){
        return new my_class(x.x + y);
    }
}
integer x := 11;
my_class xr := new my_class(x);
xr := xr + 1;

array[integer] yyyx := [1, 2, 3, 4] + [5, 6, 7, 8];
integer z := 7738;
    """)

    lexer = Lexer(RULES)
    lexemes_iter = lexer.scan(code_example)

    parser = Parser(lexemes_iter)
    x = parser.parse()
    print(type_check_program(x))
    print("Entire program valid:", x.is_valid())

    # desugar_ast_tree(x)

    # print(x)
    with open("example2.out", "w") as f:
        x.translate(f)


def scenario_5():
    with open("code_example.itchy", "rt", encoding='utf-8') as f:
        code_example = f.read()

    lexer = Lexer(RULES)
    lexemes_iter = lexer.scan(code_example)

    parser = Parser(lexemes_iter)
    x = parser.parse()
    print(type_check_program(x))
    print("Entire program valid:", x.is_valid())

    # desugar_ast_tree(x)

    # print(x)
    with open("example5.out", "w", encoding='utf-8') as f:
        x.translate(f)


if __name__ == '__main__':
    scenario_5()

