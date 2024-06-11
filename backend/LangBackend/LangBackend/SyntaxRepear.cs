namespace LangBackend;

public static partial class Syntax
{
    private static HashSet<string> AllKeywords = new ()
    {
        // scopes
        "REGION",
        "FUNCTION",
        "METHOD",
        "CLASS",

        "ENDREGION",
        "ENDFUNCTION",
        "ENDMETHOD",
        "ENDCLASS",

        // regions
        "CLASS_DEFNS",
        "FUNC_DEFNS",

        // functions
        "PARAM",
        "RETURN",
        "NOTHING",
        "THIS",

        // helpers
        "SET",
        "UNSET",

        "VALCOPY",
        "REFCOPY",

        "LABEL",
        "JUMP",

        "COND",

        // identifiers
        "ID",
        "CLASSID",

        // operators
        // call, index
        "CALL",
        "INDEX",

        // oop
        "ACCESS",
        "REFACCESS",
        "CONSTRUCT",

        // additive
        "ADD",
        "SUB",
        "MUL",
        "DIV",
        "MOD",
        "FDIV",
        "POW",

        // comparison
        "LTE",
        "GTE",
        "LT",
        "GT",
        "EQ",
        "NE",
        "EQ!",
        "NE!",
        "IN",


        // bitwise
        "BXOR",
        "BAND",
        "BOR",
        "BLSHIFT",
        "BRSHIFT",


        // boolean only
        "AND",
        "OR",
        "XOR",

        "AND!",
        "OR!",


        "CAST",
        "COALESCE",


        // unary
        "IDEMPOTATE",
        "NEGATE",

        "NOT",
        "BINV",

        "ALLOC",
        "FREE",

        "ADDR",
        "VALOF",


        //types
        "FREEZE",
        "VOID",
        "REF",


        "INT8",
        "INT16",
        "INT32",
        "INT64",
        "INTD",

        "FLOAT32",
        "FLOAT64",
        "COMPLEX128",


        "CHAR",
        "STRING",
        "BYTESTRING",
        "IOSTREAM",


        "ARRAY",
        "OF",
        "ARRAYLITERAL",

        "KEYMAP",
        "FROM",
        "TO",
    };

    public static bool IsKeyword(string x)
    {
        return AllKeywords.Contains(x);
    }
}