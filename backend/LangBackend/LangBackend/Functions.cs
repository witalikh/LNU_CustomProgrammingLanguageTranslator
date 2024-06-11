namespace LangBackend;

public partial class Interpreter
{
    private void ExecuteFunctionDefinition(List<Token> tokenList, ref int idx)
    {
        // consume FUNCTION keyword
        idx++;
        
        string functionName = tokenList[idx++].Value;
        
        // consume PARAMS_COUNT keyword and count required params for func def
        idx++;
        int paramsCount = int.Parse(tokenList[idx++].Value);
        
        
        // parse required params in type-name tuples
        List<string> parameters = new List<string>();

        for (int i = 0; i < paramsCount; i++)
        {
            idx++; // Skip the "PARAM" keyword
            string? _ = this.ParseType(tokenList, ref idx); // useless because typing performed earlier
            parameters.Add(tokenList[idx++].Value); // Add the parameter name
        }

        List<Token> body = new List<Token>();

        while (tokenList[idx].Value != Syntax.EndFunction)
        {
            body.Add(tokenList[idx++]);
        }
        
        // Skip the "ENDFUNCTION" keyword and name
        idx++;
        idx++;
        
        // Save function definition
        this._functions[functionName] = new FunctionDefinition(paramsCount, parameters, body);
    }
    
    private object? ExecuteCall(List<Token> tokenList, ref int idx)
    {
        idx++;

        int argsCount = int.Parse(tokenList[idx++].Value);

        string functionName = tokenList[idx++].Value;
        if (!this._functions.TryGetValue(functionName, out var function))
        {
            throw new Exception($"Function not found: {functionName}");
        }

        if (argsCount - 1 != function.ParamsCount) 
        {
            throw new Exception($"Function {functionName} expects {function.ParamsCount} arguments, but got {argsCount - 1}");
        }

        Dictionary<string, object?> localVariables = new Dictionary<string, object?>();

        for (int i = 0; i < function.ParamsCount; i++)
        {
            string paramName = function.Params[i];
            object? value = this.ParseOperand(tokenList, ref idx);
            localVariables[paramName] = value;
        }

        this._stack.Push(new Frame { Variables = localVariables });

        int localIndex = 0;
        while (localIndex < function.Body.Count)
        {
            if (function.Body[localIndex].Value == Syntax.Return)
            {
                localIndex++;
                return ParseOperand(function.Body, ref localIndex);
            }
            
            this.ExecuteNextToken(function.Body, ref localIndex);
        }

        this._stack.Pop();

        return null;
    }
}