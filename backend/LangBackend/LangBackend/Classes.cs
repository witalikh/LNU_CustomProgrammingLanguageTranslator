namespace LangBackend;

public partial class Interpreter
{
    private void ExecuteClassDefinition(List<Token> tokenList, ref int idx)
    {
        // consume CLASS keyword
        idx++;
        
        string className = tokenList[idx++].Value;
        var classDef = new ClassDefinition(className);

        while (tokenList[idx].Value != Syntax.EndClass)
        {
            Token token = tokenList[idx++];
            switch (token.Value)
            {
                case Syntax.Set:
                    string fieldType = tokenList[idx++].Value;
                    string fieldName = tokenList[idx++].Value;
                    classDef.Fields[fieldName] = fieldType;
                    break;
                case Syntax.Method:
                    this.ExecuteMethodDefinition(tokenList, ref idx, classDef);
                    break;
                default:
                    throw new Exception($"Unknown token in class definition: {token.Value}");
            }
        }

        idx++; // Skip "ENDCLASS"
        this._classes[className] = classDef;
    }
    
    private void ExecuteMethodDefinition(List<Token> tokenList, ref int idx, ClassDefinition classDef)
    {
        // "METHOD" keyword is already consumed
        
        string methodName = tokenList[idx++].Value;
        int paramsCount = int.Parse(tokenList[idx++].Value);
        List<string> parameters = new List<string>();

        for (int i = 0; i < paramsCount; i++)
        {
            idx++; // Skip the "PARAM" keyword
            parameters.Add(tokenList[idx++].Value); // Add the parameter name
        }

        List<Token> body = new List<Token>();

        while (tokenList[idx].Value != Syntax.EndMethod)
        {
            body.Add(tokenList[idx++]);
        }

        idx++; // Skip the "ENDMETHOD" keyword
        classDef.Methods[methodName] = new FunctionDefinition(paramsCount, parameters, body);
    }
    
    private void ExecuteAllocate(List<Token> tokenList, ref int idx)
    {
        string className = tokenList[idx++].Value;
        if (!this._classes.ContainsKey(className))
        {
            throw new Exception($"Class not found: {className}");
        }

        this._currentInstance = new Dictionary<string, object>();
        var classDef = this._classes[className];

        foreach (var field in classDef.Fields)
        {
            ((Dictionary<string, object>)this._currentInstance)[field.Key] = field.Value switch
            {
                Syntax.Int32 => 0,
                Syntax.Float64 => 0.0,
                Syntax.Array => new List<object>(),
                _ => throw new Exception($"Unknown type: {field.Value}")
            };
        }
    }

    private object? ExecuteConstruct(List<Token> tokenList, ref int idx)
    {
        string className = tokenList[idx++].Value;
        string constructorName = "$constructor"; // TODO: REPLACE
        int paramsCount = int.Parse(tokenList[idx++].Value);

        List<object> args = new List<object>();
        for (int i = 0; i < paramsCount; i++)
        {
            args.Add(this.ResolveValue(tokenList[idx++].Value));
        }

        var classDef = this._classes[className];
        var methodDef = classDef.Methods[constructorName];

        if (paramsCount != methodDef.ParamsCount)
        {
            throw new Exception($"Constructor {constructorName} expects {methodDef.ParamsCount} arguments, but got {paramsCount}");
        }

        Dictionary<string, object> localVariables = new Dictionary<string, object>();
        for (int i = 0; i < methodDef.ParamsCount; i++)
        {
            localVariables[methodDef.Params[i]] = args[i];
        }

        this._stack.Push(new Frame { Variables = localVariables });
        int subIndex = 0;
        while (subIndex < methodDef.Body.Count)
        {
            this.ExecuteNextToken(methodDef.Body, ref subIndex);
        }

        this._stack.Pop();

        return null;
    }
}