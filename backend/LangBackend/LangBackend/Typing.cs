namespace LangBackend;

public partial class Interpreter
{
    private string? ParseType(List<Token> tokenList, ref int idx)
    {
        string type = tokenList[idx++].Value;
        switch (type)
        {
            case "FREEZE":
            case "VOID":
            case "REF":
            case "INT8":
            case "INT16":
            case "INT32":
            case "INT64":
            case "INTD":
            case "FLOAT32":
            case "FLOAT64":
            case "COMPLEX128":
            case "CHAR":
            case "STRING":
            case "BYTESTRING":
            case "IOSTREAM":
            case "ARRAY":
            case "OF":
            case "ARRAYLITERAL":
            case "KEYMAP":
            case "FROM":
            case "TO":
                break;
            default:
                break;
        }

        return null;
    }
}