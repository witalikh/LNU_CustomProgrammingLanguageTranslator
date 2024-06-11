namespace LangBackend;

public enum TokenType { Keyword, Identifier, Number, String, Symbol }

public class Token
{
    public TokenType Type { get; }
    public string Value { get; }
    public Token(TokenType type, string value)
    {
        this.Type = type;
        this.Value = value;
    }
    public override string ToString() => $"{this.Type}: {this.Value}";
}

public class Lexer
{
    private string _code;
    private int _index;

    public Lexer(string code)
    {
        this._code = code;
        this._index = 0;
    }

    public List<Token> Tokenize()
    {
        var tokens = new List<Token>();
        while (this._index < this._code.Length)
        {
            char current = this._code[this._index];
            if (char.IsWhiteSpace(current))
            {
                this._index++;
                continue;
            }

            if (char.IsLetter(current))
            {
                tokens.Add(this.ReadWord());
            }
            else if (char.IsDigit(current) || current == '.')
            {
                tokens.Add(this.ReadNumber());
            }
            else if (current == '"' || current == '\'')
            {
                tokens.Add(this.ReadString());
            }
            else
            {
                tokens.Add(this.ReadSymbol());
            }
        }
        return tokens;
    }

    private Token ReadWord()
    {
        int start = this._index;
        while (this._index < this._code.Length && (char.IsLetterOrDigit(this._code[this._index]) || this._code[this._index] == '_'))
        {
            this._index++;
        }
        string word = this._code.Substring(start, this._index - start);
        var type = Syntax.IsKeyword(word) ? TokenType.Keyword : TokenType.Identifier;
        return new Token(type, word);
    }

    private Token ReadNumber()
    {
        int start = this._index;
        bool hasDot = false;
        while (this._index < this._code.Length && (char.IsDigit(this._code[this._index]) || this._code[this._index] == '.'))
        {
            if (this._code[this._index] == '.')
            {
                if (hasDot) throw new Exception("Invalid number format");
                hasDot = true;
            }

            this._index++;
        }
        return new Token(TokenType.Number, this._code.Substring(start, this._index - start));
    }

    private Token ReadString()
    {
        char quote = this._code[this._index];
        this._index++;
        int start = this._index;
        while (this._index < this._code.Length && this._code[this._index] != quote)
        {
            this._index++;
        }
        if (this._index >= this._code.Length) throw new Exception("Unterminated string");
        string str = this._code.Substring(start, this._index - start);
        this._index++;
        return new Token(TokenType.String, str);
    }

    private Token ReadSymbol()
    {
        return new Token(TokenType.Symbol, this._code[this._index++].ToString());
    }
}
    
public class VTable
{
    public Dictionary<string, Action<object, List<object>>> Methods { get; private set; }

    public VTable()
    {
        this.Methods = new Dictionary<string, Action<object, List<object>>>();
    }

    public void AddMethod(string methodName, Action<object, List<object>> method)
    {
        this.Methods[methodName] = method;
    }

    public Action<object, List<object>> GetMethod(string methodName)
    {
        return this.Methods.ContainsKey(methodName) ? this.Methods[methodName] : null;
    }
}

class Program
{
    static void Main(string[] args)
    {
        string code = @"
                SET integer a
                SET integer b
                VALCOPY a 5
                VALCOPY b 10
                ADD a a b
                RETURN a
            ";

        var lexer = new Lexer(code);
        var tokens = lexer.Tokenize();

        var interpreter = new Interpreter(tokens);
        interpreter.Execute();

        Console.WriteLine("Execution finished.");
    }
}