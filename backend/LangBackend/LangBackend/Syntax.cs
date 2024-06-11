namespace LangBackend;

public static partial class Syntax
{
    // scopes
    public const string Region = "REGION";
    public const string Function = "FUNCTION";
    public const string Method = "METHOD";
    public const string Class = "CLASS";
    
    public const string EndRegion = "ENDREGION";
    public const string EndFunction = "ENDFUNCTION";
    public const string EndMethod = "ENDMETHOD";
    public const string EndClass = "ENDCLASS";
    
    // regions
    public const string ClassDefinitions = "CLASS_DEFNS";
    public const string FunctionDefinitions = "FUNC_DEFNS";
    
    // functions
    public const string Param = "PARAM";
    public const string Return = "RETURN";
    public const string Nothing = "NOTHING";
    public const string This = "THIS";
        
    // helpers
    
    public const string Set ="SET"; 
    public const string Unset = "UNSET";
        
    public const string ValCopy = "VALCOPY";
    public const string RefCopy = "REFCOPY";
            
    public const string Label = "LABEL";
    public const string Jump = "JUMP";
    
    public const string Condition = "COND";
            
    // identifiers
    public const string Identifier = "ID";
    public const string ClassIdentifier = "CLASSID";
            
    // operators
    // call, index
    public const string Call = "CALL";
    public const string Indexation = "INDEX";
            
    // oop
    public const string MemberAccess = "ACCESS";
    public const string ReferenceMemberAccess = "REFACCESS";
    public const string ConstructorCall = "CONSTRUCT";
            
    // additive
    public const string Add = "ADD";
    public const string Subtract = "SUB";
    public const string Multiply = "MUL";
    public const string Divide = "DIV";
    public const string Modulo = "MOD";
    public const string FloorDivision = "FDIV";
    public const string Power = "POW";
            
    // comparison
    public const string LessThanOrEqual = "LTE";
    public const string GreaterThanOrEqual = "GTE";
    public const string LessThan = "LT";
    public const string GreaterThan = "GT";
    public const string Equal = "EQ";
    public const string NotEqual = "NE";
    public const string StrictEqual = "EQ!";
    public const string StrictNotEqual = "NE!";
    public const string IsElementOf = "IN";
    
            
    // bitwise
    public const string BitwiseXor = "BXOR";
    public const string BitwiseAnd = "BAND";
    public const string BitwiseOr = "BOR";
    public const string BitwiseLeftShift = "BLSHIFT";
    public const string BitwiseRightShift = "BRSHIFT";
    
            
    // boolean only
    public const string BooleanAnd = "AND";
    public const string BooleanOr = "OR";
    public const string BooleanXor = "XOR";
    
    public const string BooleanFullAnd = "AND!";
    public const string BooleanFullOr = "OR!";
    
            
    public const string TypeCast = "CAST";
    public const string NullCoalesce = "COALESCE";
    
            
    // unary
    public const string UnaryIdempotate = "IDEMPOTATE";
    public const string UnaryNegate = "NEGATE";
    
    public const string BooleanNot = "NOT";
    public const string BitwiseInverse = "BINV";
    
    public const string Allocate = "ALLOC";
    public const string Free = "FREE";
    
    public const string GetReferenceOf = "ADDR";
    public const string GetValueOf = "VALOF";
    
        
    //types
    public const string ConstTypeMode = "FREEZE";
    public const string NullableTypeMode = "VOID";
    public const string ReferenceTypeMode = "REF";
    
        
    public const string Int8 = "INT8";
    public const string Int16 = "INT16";
    public const string Int32 = "INT32";
    public const string Int64 = "INT64";
    public const string IntLarge = "INTD";
    
    public const string Float32 = "FLOAT32";
    public const string Float64 = "FLOAT64";
    public const string Complex128 = "COMPLEX128";
    
        
    public const string Char = "CHAR";
    public const string String = "STRING";
    public const string ByteString = "BYTESTRING";
    public const string IoStream = "IOSTREAM";
    
        
    public const string Array = "ARRAY";
    public const string Of = "OF";
    public const string ArrayLiteral = "ARRAYLITERAL";
    
    public const string Keymap = "KEYMAP";
    public const string From = "FROM";
    public const string To = "TO";
    
}