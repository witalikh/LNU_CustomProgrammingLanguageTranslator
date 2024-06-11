namespace LangBackend;


public partial class Interpreter
{
    
    private List<Token> _tokens;
    private int _index;

    private Dictionary<string, ClassDefinition> _classes = new Dictionary<string, ClassDefinition>();
    private object? _currentInstance = null;

    private Dictionary<string, FunctionDefinition> _functions = new Dictionary<string, FunctionDefinition>();
    private Dictionary<string, object?> _variables;
    private Dictionary<string, int> _labels;
    private Stack<Frame> _stack;
    private string _currentRegion;
    private bool _isRunning;

    public Interpreter(List<Token> tokens)
    {
        this._tokens = tokens;
        this._index = 0;
        this._variables = new Dictionary<string, object?>();
        this._labels = new Dictionary<string, int>();
        this._stack = new Stack<Frame>();

        this._isRunning = true;

        // Preprocess labels
        this.PreprocessLabels();
    }

    private void PreprocessLabels()
    {
        for (int i = 0; i < this._tokens.Count; i++)
        {
            if (this._tokens[i].Value == Syntax.Label)
            {
                string labelName = this._tokens[i + 1].Value;
                this._labels[labelName] = i + 2;
                i += 2;
            }
        }
    }

    public void Execute()
    {
        this._index = 0;
        while (this._isRunning && this._index < this._tokens.Count)
        {
            this.ExecuteNextToken(this._tokens, ref this._index);
        }
    }

    private void ExecuteNextToken(List<Token> tokenList, ref int idx)
    {
        idx++;
        
        var token = tokenList[idx];
        switch (token.Value)
        {
            case Syntax.Region:
                this.ExecuteRegion(tokenList, ref idx);
                break;
            case Syntax.EndRegion:
                this.ExecuteEndRegion(tokenList, ref idx);
                break;
            case Syntax.Class:
                ExecuteClassDefinition(tokenList, ref idx);
                break;
            case Syntax.EndClass:
                // ENDCLASS is handled within ExecuteClassDefinition
                break;
            case Syntax.Method:
                // METHOD is handled within ExecuteClassDefinition
                break;
            case Syntax.EndMethod:
                // ENDMETHOD is handled within ExecuteClassDefinition
                break;
            case Syntax.Function:
                this.ExecuteFunctionDefinition(tokenList, ref idx);
                break;
            case Syntax.EndFunction:
                // ENDFUNCTION is handled within ExecuteFunctionDefinition
                break;
            case Syntax.Return:
            case Syntax.Nothing:
            case Syntax.This:
                // Skip these for now
                break;
            case Syntax.Set:
                this.ExecuteSet(tokenList, ref idx);
                break;
            case Syntax.Unset:
                this.ExecuteUnset(tokenList, ref idx);
                break;
            case Syntax.ValCopy:
                this.ExecuteValCopy(tokenList, ref idx);
                break;
            case Syntax.RefCopy:
                this.ExecuteRefCopy(tokenList, ref idx);
                break;
            case Syntax.Label:
                // Skip label
                idx += 2;
                break;
            case Syntax.Jump:
                this.ExecuteJump(tokenList, ref idx);
                break;
            case Syntax.MemberAccess:
            case Syntax.ReferenceMemberAccess:
                this.ExecuteAccess(tokenList, ref idx);
                break;
            default:
                this.ParseOperand(tokenList, ref idx, true);
                break;
            
        }
    }


    

    private object? EvaluateIdentifier(List<Token> tokenList, ref int idx)
    {
        // consume ID and variable name
        idx++;
        string variable = tokenList[idx++].Value;

        if (this._stack.Count > 0 && this._stack.Peek().Variables.TryGetValue(variable, out var localValue))
        {
            return localValue;
        }
        
        if (this._variables.TryGetValue(variable, out var globalValue))
        {
            return globalValue;
        }

        throw new Exception($"Variable {variable} doesn't exist in this context!");
    }

    private void ExecuteRegion(List<Token> tokenList, ref int idx)
    {
        // consume REGION keyword
        idx++;
        
        string regionType = tokenList[idx++].Value;
        if (regionType != Syntax.ClassDefinitions && regionType != Syntax.FunctionDefinitions)
        {
            throw new Exception($"Unknown region type: {regionType}");
        }

        this._currentRegion = regionType;
    }

    private void ExecuteEndRegion(List<Token> tokenList, ref int idx)
    {
        // consume ENDREGION keyword
        idx++;
        
        string regionType = tokenList[idx++].Value;
        if (this._currentRegion == null || this._currentRegion != regionType)
        {
            throw new Exception($"Mismatched ENDREGION: expected {this._currentRegion}, got {regionType}");
        }

        this._currentRegion = null;
    }
    
    
    
    private void ExecuteSet(List<Token> tokenList, ref int idx)
    {
        // consume SET keyword
        idx++;
        
        string type = tokenList[idx++].Value;
        string variableName = tokenList[idx++].Value;
        
        // TODO: type default
        this._variables[variableName] = type switch{
            Syntax.Int32 => 0,
            Syntax.Array => new List<object>(),
            Syntax.ClassIdentifier => null,
            _ => throw new Exception($"Unknown type: {type}")
        };
    }



    private void ExecuteUnset(List<Token> tokenList, ref int idx)
    {
        // consume UNSET keyword
        idx++;
        
        string variableName = tokenList[idx++].Value;
        this._variables.Remove(variableName);
    }

    private void ExecuteValCopy(List<Token> tokenList, ref int idx)
    {
        string target = tokenList[idx++].Value;
        object value = this.ResolveValue(tokenList[idx++].Value);
        this._variables[target] = value;
    }

    private void ExecuteRefCopy(List<Token> tokenList, ref int idx)
    {
        string target = tokenList[idx++].Value;
        string source = tokenList[idx++].Value;
        this._variables[target] = this._variables[source];
    }



    private void ExecuteJump(List<Token> tokenList, ref int idx)
    {
        // consume JUMP instruction
        idx++;
        string label = tokenList[idx].Value;
        idx = this._labels[label];
    }

    private void ExecuteAccess(List<Token> tokenList, ref int idx)
    {
        string target = tokenList[idx++].Value;
        string objectName = tokenList[idx++].Value;
        string fieldName = tokenList[idx++].Value;
        this._variables[target] = ((Dictionary<string, object>)this._variables[objectName])[fieldName];
    }

    private object ResolveValue(string value)
    {
        if (int.TryParse(value, out int intValue))
        {
            return intValue;
        }

        if (this._stack.Count > 0 && this._stack.Peek().Variables.TryGetValue(value, out var localValue))
        {
            return localValue;
        }

        return this._variables.TryGetValue(value, out var globalValue) ? globalValue : null;
    }

    private class Frame
    {
        public Dictionary<string, object?> Variables { get; set; } = new Dictionary<string, object>();
    }
}
