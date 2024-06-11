namespace LangBackend;

public partial class Interpreter
{
    private string? ParseType(List<Token> tokenList, ref int idx)
    {
        string type = tokenList[idx++].Value;
        switch (type)
        {
            case Syntax.ConstTypeMode:
            case Syntax.NullableTypeMode:
            case Syntax.ReferenceTypeMode:
            case Syntax.Int8:
            case Syntax.Int16:
            case Syntax.Int32:
            case Syntax.Int64:
            case Syntax.IntLarge:
            case Syntax.Float32:
            case Syntax.Float64:
            case Syntax.Complex128:
            case Syntax.Char:
            case Syntax.String:
            case Syntax.ByteString:
            case Syntax.IoStream:
            case Syntax.Array:
            case Syntax.Of:
            case Syntax.ArrayLiteral:
            case Syntax.Keymap:
            case Syntax.From:
            case Syntax.To:
                break;
            default:
                break;
        }

        return null;
    }
}