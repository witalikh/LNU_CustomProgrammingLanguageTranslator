import argparse
import sys


def main():

    from frontend.lexer import Lexer
    from frontend.syntax import RULES
    from frontend.parser import Parser
    from frontend.type_checking.entrypoint import type_check_program

    parser = argparse.ArgumentParser(
        description='Compile multiple input ItchyLang source code files '
                    'and write its intermediate to an output file or print to the console.'
    )

    # Add input file arguments with a detailed help message
    parser.add_argument(
        '-i', '--input',
        action='append',
        # required=True,
        help='Specify input file(s) for ItchyLang source code.'
             'This option can be used multiple times to add more files (as importing mechanism isn\'t implemented yet).'
             'Example: -i file1 -i file2'
    )

    # Add positional argument for input files without a flag
    parser.add_argument(
        'positional_input',
        nargs='*',
        help='Specify ItchyLang source code input file(s) without using -i. Example: file1 file2'
    )

    # Add output file argument with a detailed help message
    parser.add_argument(
        '-o', '--output',
        help='Specify the output file to write the ItchyLang\'s intermediate code. '
             'If not specified, the intermediate code will be printed to the console.'
    )

    # Add print-tree argument with a detailed help message
    parser.add_argument(
        '--print-tree',
        action='store_true',
        help='Print the content of each input file in a tree structure with separators.'
    )

    # Add no-output argument with a detailed help message
    parser.add_argument(
        '--no-output',
        action='store_true',
        help='Explicitly indicate that no output file should be created and print the content to the console.'
    )

    # Parse the command line arguments
    args = parser.parse_args()

    # Combine both input sources: positional_input and input
    input_files = args.positional_input
    if args.input:
        input_files.extend(args.input)

    # TODO: optimize (later, coz premature)
    # List to hold the content from all input files
    all_content = []

    # Read each input file and store its content
    for input_file in input_files:
        with open(input_file, 'r') as f:
            all_content.append(f.read())

    lexer = Lexer(RULES)
    lexemes_iter = lexer.scan(''.join(all_content))

    parser = Parser(lexemes_iter)
    x = parser.parse()

    print(type_check_program(x))
    print("Entire program valid:", x.is_valid())

    # desugar_ast_tree(x)

    # Check if print-tree option is specified
    if args.print_tree:
        print("AST of the code:")
        print(x)

    if args.no_output or not args.output:

        print('\n\n CODE: \n')
        x.translate(sys.stdout)
    else:
        with open(args.output, 'w') as f:
            x.translate(f)


if __name__ == '__main__':
    main()
