"""
For testing and debugging purposes, coz for now I'm lazy for unit tests
"""
from lexer import Lexer
from syntax import RULES
from parser import Parser


def scenario_1():
    code_example = ("""
    const integer number := 3.1415;
    array[string] my_str := ["Hello", "World"];
    
    if (number == 3.13){
        print(number);
        print(my_str[-1]);
    }
    """)

    lexer = Lexer(RULES)
    lexemes = lexer.scan(code_example)
    for lexeme in lexemes:
        print(lexeme)


def scenario_2():
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
    print(x)


def scenario_3():
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
    
    class my_class[T] from x[integer]{
        public integer x;
        
        public static function[my_class] operator + (my_class x, T y){
            this.x := y;
        }
    }
     
    const reference my_class[integers[x, const integer]] x = new my_class[integers[x]]("Hello");
    x[5] := 4;
    array[integer, 6] x = [1, 2, 3, 4];
    integer z := 7738;
    # x(4);
    
    x[y[5]];
    """)

    lexer = Lexer(RULES)
    lexemes_iter = lexer.scan(code_example)
    # print(*lexemes, sep="\n")

    parser = Parser(lexemes_iter)
    x = parser.parse()
    print(x)


if __name__ == '__main__':
    scenario_4()


# Program
# ├──class_definitions:
# ├──function_definitions:
# │   ├──FunctionDeclaration
# │   │   ├──return_type: None
# │   │   ├──function_name: bubble_sort
# │   │   ├──parameters:
# │   │   │   └──FunctionParameter
# │   │   │       ├──type_node: CompoundType
# │   │   │       │   ├──type_name: array
# │   │   │       │   ├──args:
# │   │   │       │   │   ├──SimpleType(float)
# │   │   │       │   │   └──Deduction
# │   │   │       │   └──modifiers: reference
# │   │   │       ├──parameter_name: arr
# │   │   │       ├──operator_type: None
# │   │   │       └──default_value: None
# │   │   └──function_body: Scope
# │   │       ├──statements:
# │   │       │   ├──VariableDeclaration
# │   │       │   │   ├──type: SimpleType(integer)
# │   │       │   │   ├──name: array_length
# │   │       │   │   ├──operator: :=
# │   │       │   │   └──value: MemberOperator
# │   │       │   │       ├──left: Identifier(arr)
# │   │       │   │       ├──operator: ->
# │   │       │   │       └──right: FunctionCall
# │   │       │   │           ├──identifier: Identifier(length)
# │   │       │   │           └──arguments:
# │   │       │   ├──VariableDeclaration
# │   │       │   │   ├──type: SimpleType(integer)
# │   │       │   │   ├──name: i
# │   │       │   │   ├──operator: :=
# │   │       │   │   └──value: Integer(0)
# │   │       │   └──While
# │   │       │       ├──condition: Comparison
# │   │       │       │   ├──left: Identifier(i)
# │   │       │       │   ├──operator: <
# │   │       │       │   └──right: Identifier(array_length)
# │   │       │       └──while_scope: Scope
# │   │       │           ├──statements:
# │   │       │           │   ├──VariableDeclaration
# │   │       │           │   │   ├──type: SimpleType(integer)
# │   │       │           │   │   ├──name: j
# │   │       │           │   │   ├──operator: :=
# │   │       │           │   │   └──value: Integer(0)
# │   │       │           │   ├──VariableDeclaration
# │   │       │           │   │   ├──type: SimpleType(float)
# │   │       │           │   │   ├──name: buffer
# │   │       │           │   │   ├──operator: None
# │   │       │           │   │   └──value: UNDEFINED_LITERAL
# │   │       │           │   ├──VariableDeclaration
# │   │       │           │   │   ├──type: SimpleType(boolean)
# │   │       │           │   │   ├──name: swapped
# │   │       │           │   │   ├──operator: :=
# │   │       │           │   │   └──value: Boolean(false)
# │   │       │           │   ├──While
# │   │       │           │   │   ├──condition: Comparison
# │   │       │           │   │   │   ├──left: Identifier(j)
# │   │       │           │   │   │   ├──operator: <
# │   │       │           │   │   │   └──right: ArithmeticOperator
# │   │       │           │   │   │       ├──left: ArithmeticOperator
# │   │       │           │   │   │       │   ├──left: Identifier(array_length)
# │   │       │           │   │   │       │   ├──operator: -
# │   │       │           │   │   │       │   └──right: Integer(1)
# │   │       │           │   │   │       ├──operator: -
# │   │       │           │   │   │       └──right: Identifier(i)
# │   │       │           │   │   └──while_scope: Scope
# │   │       │           │   │       ├──statements:
# │   │       │           │   │       │   ├──IfElse
# │   │       │           │   │       │   │   ├──condition: Comparison
# │   │       │           │   │       │   │   │   ├──left: Index
# │   │       │           │   │       │   │   │   │   ├──variable: Identifier(arr)
# │   │       │           │   │       │   │   │   │   └──arguments:
# │   │       │           │   │       │   │   │   │       └──Identifier(j)
# │   │       │           │   │       │   │   │   ├──operator: >
# │   │       │           │   │       │   │   │   └──right: Index
# │   │       │           │   │       │   │   │       ├──variable: Identifier(arr)
# │   │       │           │   │       │   │   │       └──arguments:
# │   │       │           │   │       │   │   │           └──ArithmeticOperator
# │   │       │           │   │       │   │   │               ├──left: Identifier(j)
# │   │       │           │   │       │   │   │               ├──operator: +
# │   │       │           │   │       │   │   │               └──right: Integer(1)
# │   │       │           │   │       │   │   ├──if_scope: Scope
# │   │       │           │   │       │   │   │   ├──statements:
# │   │       │           │   │       │   │   │   │   ├──Assignment
# │   │       │           │   │       │   │   │   │   │   ├──left: Identifier(buffer)
# │   │       │           │   │       │   │   │   │   │   ├──operator: :=
# │   │       │           │   │       │   │   │   │   │   └──right: Index
# │   │       │           │   │       │   │   │   │   │       ├──variable: Identifier(arr)
# │   │       │           │   │       │   │   │   │   │       └──arguments:
# │   │       │           │   │       │   │   │   │   │           └──Identifier(j)
# │   │       │           │   │       │   │   │   │   ├──Assignment
# │   │       │           │   │       │   │   │   │   │   ├──left: Index
# │   │       │           │   │       │   │   │   │   │   │   ├──variable: TemporaryIdentifier
# │   │       │           │   │       │   │   │   │   │   │   │   ├──name: arr
# │   │       │           │   │       │   │   │   │   │   │   │   ├──type: None
# │   │       │           │   │       │   │   │   │   │   │   │   └──modifiers: 0
# │   │       │           │   │       │   │   │   │   │   │   └──arguments:
# │   │       │           │   │       │   │   │   │   │   │       └──Identifier(j)
# │   │       │           │   │       │   │   │   │   │   ├──operator: :=
# │   │       │           │   │       │   │   │   │   │   └──right: Index
# │   │       │           │   │       │   │   │   │   │       ├──variable: TemporaryIdentifier
# │   │       │           │   │       │   │   │   │   │       │   ├──name: arr
# │   │       │           │   │       │   │   │   │   │       │   ├──type: None
# │   │       │           │   │       │   │   │   │   │       │   └──modifiers: 0
# │   │       │           │   │       │   │   │   │   │       └──arguments:
# │   │       │           │   │       │   │   │   │   │           └──ArithmeticOperator
# │   │       │           │   │       │   │   │   │   │               ├──left: Identifier(j)
# │   │       │           │   │       │   │   │   │   │               ├──operator: +
# │   │       │           │   │       │   │   │   │   │               └──right: Integer(1)
# │   │       │           │   │       │   │   │   │   ├──Assignment
# │   │       │           │   │       │   │   │   │   │   ├──left: Index
# │   │       │           │   │       │   │   │   │   │   │   ├──variable: TemporaryIdentifier
# │   │       │           │   │       │   │   │   │   │   │   │   ├──name: arr
# │   │       │           │   │       │   │   │   │   │   │   │   ├──type: None
# │   │       │           │   │       │   │   │   │   │   │   │   └──modifiers: 0
# │   │       │           │   │       │   │   │   │   │   │   └──arguments:
# │   │       │           │   │       │   │   │   │   │   │       └──ArithmeticOperator
# │   │       │           │   │       │   │   │   │   │   │           ├──left: Identifier(j)
# │   │       │           │   │       │   │   │   │   │   │           ├──operator: +
# │   │       │           │   │       │   │   │   │   │   │           └──right: Integer(1)
# │   │       │           │   │       │   │   │   │   │   ├──operator: :=
# │   │       │           │   │       │   │   │   │   │   └──right: TemporaryIdentifier
# │   │       │           │   │       │   │   │   │   │       ├──name: buffer
# │   │       │           │   │       │   │   │   │   │       ├──type: None
# │   │       │           │   │       │   │   │   │   │       └──modifiers: 0
# │   │       │           │   │       │   │   │   │   └──Assignment
# │   │       │           │   │       │   │   │   │       ├──left: Identifier(swapped)
# │   │       │           │   │       │   │   │   │       ├──operator: :=
# │   │       │           │   │       │   │   │   │       └──right: Boolean(true)
# │   │       │           │   │       │   │   │   └──local_variables:
# │   │       │           │   │       │   │   └──else_scope: None
# │   │       │           │   │       │   └──Assignment
# │   │       │           │   │       │       ├──left: Identifier(j)
# │   │       │           │   │       │       ├──operator: :=
# │   │       │           │   │       │       └──right: ArithmeticOperator
# │   │       │           │   │       │           ├──left: Identifier(j)
# │   │       │           │   │       │           ├──operator: +
# │   │       │           │   │       │           └──right: Integer(1)
# │   │       │           │   │       └──local_variables:
# │   │       │           │   ├──IfElse
# │   │       │           │   │   ├──condition: Identifier(swapped)
# │   │       │           │   │   ├──if_scope: Scope
# │   │       │           │   │   │   ├──statements:
# │   │       │           │   │   │   │   └──Break
# │   │       │           │   │   │   └──local_variables:
# │   │       │           │   │   └──else_scope: None
# │   │       │           │   └──Assignment
# │   │       │           │       ├──left: Identifier(i)
# │   │       │           │       ├──operator: :=
# │   │       │           │       └──right: ArithmeticOperator
# │   │       │           │           ├──left: Identifier(i)
# │   │       │           │           ├──operator: +
# │   │       │           │           └──right: Integer(1)
# │   │       │           └──local_variables:
# │   │       │               ├──VariableDeclaration
# │   │       │               │   ├──type: SimpleType(integer)
# │   │       │               │   ├──name: j
# │   │       │               │   ├──operator: :=
# │   │       │               │   └──value: Integer(0)
# │   │       │               ├──VariableDeclaration
# │   │       │               │   ├──type: SimpleType(float)
# │   │       │               │   ├──name: buffer
# │   │       │               │   ├──operator: None
# │   │       │               │   └──value: UNDEFINED_LITERAL
# │   │       │               └──VariableDeclaration
# │   │       │                   ├──type: SimpleType(boolean)
# │   │       │                   ├──name: swapped
# │   │       │                   ├──operator: :=
# │   │       │                   └──value: Boolean(false)
# │   │       └──local_variables:
# │   │           ├──VariableDeclaration
# │   │           │   ├──type: SimpleType(integer)
# │   │           │   ├──name: array_length
# │   │           │   ├──operator: :=
# │   │           │   └──value: MemberOperator
# │   │           │       ├──left: Identifier(arr)
# │   │           │       ├──operator: ->
# │   │           │       └──right: FunctionCall
# │   │           │           ├──identifier: Identifier(length)
# │   │           │           └──arguments:
# │   │           └──VariableDeclaration
# │   │               ├──type: SimpleType(integer)
# │   │               ├──name: i
# │   │               ├──operator: :=
# │   │               └──value: Integer(0)
# │   ├──FunctionDeclaration
# │   │   ├──return_type: SimpleType(float)
# │   │   ├──function_name: sum_of_elements
# │   │   ├──parameters:
# │   │   │   └──FunctionParameter
# │   │   │       ├──type_node: CompoundType
# │   │   │       │   ├──type_name: array
# │   │   │       │   ├──args:
# │   │   │       │   │   ├──SimpleType(float)
# │   │   │       │   │   └──Deduction
# │   │   │       │   └──modifiers: const reference
# │   │   │       ├──parameter_name: arr
# │   │   │       ├──operator_type: None
# │   │   │       └──default_value: None
# │   │   └──function_body: Scope
# │   │       ├──statements:
# │   │       │   ├──VariableDeclaration
# │   │       │   │   ├──type: SimpleType(integer)
# │   │       │   │   ├──name: length
# │   │       │   │   ├──operator: :=
# │   │       │   │   └──value: MemberOperator
# │   │       │   │       ├──left: Identifier(arr)
# │   │       │   │       ├──operator: ->
# │   │       │   │       └──right: FunctionCall
# │   │       │   │           ├──identifier: Identifier(length)
# │   │       │   │           └──arguments:
# │   │       │   ├──VariableDeclaration
# │   │       │   │   ├──type: SimpleType(float)
# │   │       │   │   ├──name: _sum
# │   │       │   │   ├──operator: :=
# │   │       │   │   └──value: Integer(0)
# │   │       │   ├──VariableDeclaration
# │   │       │   │   ├──type: SimpleType(integer)
# │   │       │   │   ├──name: i
# │   │       │   │   ├──operator: :=
# │   │       │   │   └──value: Integer(0)
# │   │       │   ├──While
# │   │       │   │   ├──condition: Comparison
# │   │       │   │   │   ├──left: Identifier(i)
# │   │       │   │   │   ├──operator: <
# │   │       │   │   │   └──right: Identifier(length)
# │   │       │   │   └──while_scope: Scope
# │   │       │   │       ├──statements:
# │   │       │   │       │   ├──Assignment
# │   │       │   │       │   │   ├──left: Identifier(_sum)
# │   │       │   │       │   │   ├──operator: :=
# │   │       │   │       │   │   └──right: ArithmeticOperator
# │   │       │   │       │   │       ├──left: Identifier(_sum)
# │   │       │   │       │   │       ├──operator: +
# │   │       │   │       │   │       └──right: Index
# │   │       │   │       │   │           ├──variable: Identifier(arr)
# │   │       │   │       │   │           └──arguments:
# │   │       │   │       │   │               └──Identifier(i)
# │   │       │   │       │   └──Assignment
# │   │       │   │       │       ├──left: Identifier(i)
# │   │       │   │       │       ├──operator: :=
# │   │       │   │       │       └──right: ArithmeticOperator
# │   │       │   │       │           ├──left: Identifier(i)
# │   │       │   │       │           ├──operator: +
# │   │       │   │       │           └──right: Integer(1)
# │   │       │   │       └──local_variables:
# │   │       │   └──Return
# │   │       │       └──value: Identifier(_sum)
# │   │       └──local_variables:
# │   │           ├──VariableDeclaration
# │   │           │   ├──type: SimpleType(integer)
# │   │           │   ├──name: length
# │   │           │   ├──operator: :=
# │   │           │   └──value: MemberOperator
# │   │           │       ├──left: Identifier(arr)
# │   │           │       ├──operator: ->
# │   │           │       └──right: FunctionCall
# │   │           │           ├──identifier: Identifier(length)
# │   │           │           └──arguments:
# │   │           ├──VariableDeclaration
# │   │           │   ├──type: SimpleType(float)
# │   │           │   ├──name: _sum
# │   │           │   ├──operator: :=
# │   │           │   └──value: Integer(0)
# │   │           └──VariableDeclaration
# │   │               ├──type: SimpleType(integer)
# │   │               ├──name: i
# │   │               ├──operator: :=
# │   │               └──value: Integer(0)
# │   └──FunctionDeclaration
# │       ├──return_type: None
# │       ├──function_name: Main
# │       ├──parameters:
# │       └──function_body: Scope
# │           ├──statements:
# │           │   ├──VariableDeclaration
# │           │   │   ├──type: CompoundType
# │           │   │   │   ├──type_name: array
# │           │   │   │   ├──args:
# │           │   │   │   │   ├──SimpleType(float)
# │           │   │   │   │   └──Integer(7)
# │           │   │   │   └──modifiers:
# │           │   │   ├──name: x
# │           │   │   ├──operator: :=
# │           │   │   └──value: ListLiteral
# │           │   │       └──elements:
# │           │   │           ├──UnaryOperator
# │           │   │           │   ├──operator: -
# │           │   │           │   └──expression: Integer(3)
# │           │   │           ├──UnaryOperator
# │           │   │           │   ├──operator: -
# │           │   │           │   └──expression: Float(1.3)
# │           │   │           ├──Integer(4)
# │           │   │           ├──Integer(5)
# │           │   │           ├──Float(3.2)
# │           │   │           ├──Integer(0)
# │           │   │           └──Integer(4)
# │           │   ├──FunctionCall
# │           │   │   ├──identifier: TemporaryIdentifier
# │           │   │   │   ├──name: print
# │           │   │   │   ├──type: None
# │           │   │   │   └──modifiers: 0
# │           │   │   └──arguments:
# │           │   │       └──FunctionCall
# │           │   │           ├──identifier: Identifier(sum_of_elements)
# │           │   │           └──arguments:
# │           │   │               └──Class / struct identifier(x)
# │           │   ├──FunctionCall
# │           │   │   ├──identifier: TemporaryIdentifier
# │           │   │   │   ├──name: bubble_sort
# │           │   │   │   ├──type: None
# │           │   │   │   └──modifiers: 0
# │           │   │   └──arguments:
# │           │   │       └──Class / struct identifier(x)
# │           │   └──FunctionCall
# │           │       ├──identifier: TemporaryIdentifier
# │           │       │   ├──name: print
# │           │       │   ├──type: None
# │           │       │   └──modifiers: 0
# │           │       └──arguments:
# │           │           └──Identifier(x)
# │           └──local_variables:
# │               └──VariableDeclaration
# │                   ├──type: CompoundType
# │                   │   ├──type_name: array
# │                   │   ├──args:
# │                   │   │   ├──SimpleType(float)
# │                   │   │   └──Integer(7)
# │                   │   └──modifiers:
# │                   ├──name: x
# │                   ├──operator: :=
# │                   └──value: ListLiteral
# │                       └──elements:
# │                           ├──UnaryOperator
# │                           │   ├──operator: -
# │                           │   └──expression: Integer(3)
# │                           ├──UnaryOperator
# │                           │   ├──operator: -
# │                           │   └──expression: Float(1.3)
# │                           ├──Integer(4)
# │                           ├──Integer(5)
# │                           ├──Float(3.2)
# │                           ├──Integer(0)
# │                           └──Integer(4)
# └──statements:
#     └──FunctionCall
#         ├──identifier: TemporaryIdentifier
#         │   ├──name: Main
#         │   ├──type: None
#         │   └──modifiers: 0
#         └──arguments:
