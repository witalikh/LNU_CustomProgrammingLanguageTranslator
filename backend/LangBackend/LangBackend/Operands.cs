using System.Numerics;

namespace LangBackend;

public partial class Interpreter
{
    private static object? ParseNumber(string number)
    {
        if (Byte.TryParse(number, out Byte resint8))
        {
            return resint8;
        }
        if (Int16.TryParse(number, out Int16 resint16))
        {
            return resint16;
        }
        if (Int32.TryParse(number, out Int32 resint32))
        {
            return resint32;
        }
        if (Int64.TryParse(number, out Int64 resint64))
        {
            return resint64;
        }
        if (BigInteger.TryParse(number, out var resintd))
        {
            return resintd;
        }
        if (float.TryParse(number, out float resfloat32))
        {
            return resfloat32;
        }
        if (double.TryParse(number, out double resfloat64))
        {
            return resfloat64;
        }
        if (Complex.TryParse(number, null, out var rescomplex))
        {
            return rescomplex;
        }

        throw new Exception($"Invalid number to parse: {number}");
    }

    
    private object? ParseOperand(List<Token> tokenList, ref int idx, bool shift = true)
    {
        var token = tokenList[idx];
        object? value;
        
        if (token.Type == TokenType.Number)
        {
            
            value = ParseNumber(token.Value);
            idx++;
            return value;
        }

        if (token.Type == TokenType.String)
        {
            value = token.Value;
            idx++;
            return value;
        }

        if (token.Type == TokenType.Identifier)
        {
            throw new Exception("Invalid place to meet identifier, yet");
            
        }

        if (token.Type == TokenType.Symbol)
        {
            
        }

        switch (token.Value)
        {
            case "ADD":
            case "SUB":
            case "MUL":
            case "DIV":
            case "MOD":
            case "FDIV":
            case "POW":
            case "BXOR":
            case "BAND":
            case "BOR":
            case "BRSHIFT":
            case "BLSHIFT":
                value = this.EvaluateBinaryArithmetic(tokenList, ref idx);
                break;
            case "LTE":
            case "GTE":
            case "LT":
            case "GT":
            case "EQ":
            case "NE":
            case "EQ!":
            case "NE!":
            case "IN":
                value = this.EvaluateBinaryComparison(tokenList, ref idx);
                break;
            case "AND":
            case "OR":
            case "XOR":
            case "AND!":
            case "OR!":
                value = this.EvaluateBoolean(tokenList, ref idx);
                break;
            case "CAST":
            case "COALESCE":
                value = this.EvaluateTypeConversion(tokenList, ref idx);
                break;
            case "IDEMPOTATE":
            case "NEGATE":
            case "NOT":
            case "BINV":
                return this.EvaluateUnaryArithmetic(tokenList, ref idx);
            case "ALLOC":
            case "FREE":
                value = this.EvaluateMemoryManagement(tokenList, ref idx);
                break;
            case "ADDR":
            case "VALOF":
                value = this.ExecuteReference(tokenList, ref idx);
                break;
            case "ID":
                value = this.EvaluateIdentifier(tokenList, ref idx);
                break;
            case "CALL":
                value = this.ExecuteCall(tokenList, ref idx);
                break;
            case "INDEX":
                value = this.ExecuteIndex(tokenList, ref idx);
                break;
            default:
                throw new Exception($"Unknown or unsupported token: {token.Value}");
        }
        if (shift) idx++;
        return value;
    }
    
        private object? EvaluateBinaryArithmetic(List<Token> tokenList, ref int idx)
    {
        // consume operation
        string operation = tokenList[idx++].Value;
        
        object? lhs = this.ParseOperand(tokenList, ref idx);
        object? rhs = this.ParseOperand(tokenList, ref idx, false);
        
        return Operations.PerformBinaryOperation(operation, lhs, rhs);
    }

    private bool EvaluateBinaryComparison(List<Token> tokenList, ref int idx)
    {
        // consume operation
        string operation = tokenList[idx++].Value;
        
        object? lhs = this.ParseOperand(tokenList, ref idx);
        object? rhs = this.ParseOperand(tokenList, ref idx, false);
        
        return Operations.PerformBinaryOperation(operation, lhs, rhs) as bool? ?? false;
    }

    private bool EvaluateBoolean(List<Token> tokenList, ref int idx)
    {
        // consume operation
        string operation = tokenList[idx++].Value;
        
        bool? lhs = this.ParseOperand(tokenList, ref idx) as bool?;
        bool? rhs = this.ParseOperand(tokenList, ref idx, false) as bool?;
        
        return Operations.PerformBinaryOperation(operation, lhs, rhs) as bool? ?? false;
    }

    private object? EvaluateTypeConversion(List<Token> tokenList, ref int idx)
    {
        // consume REGION keyword
        string operation = tokenList[idx++].Value;
        
        object? value = this.ParseOperand(tokenList, ref idx, false);

        // TODO: type conversion
        return operation switch
        {
            "CAST" => Convert.ChangeType(value, Type.GetType(tokenList[idx++].Value)),
            "COALESCE" => value ?? this.ResolveValue(tokenList[idx++].Value),
            _ => throw new Exception($"Unknown type conversion operation: {operation}")
        };
    }

    private object? EvaluateUnaryArithmetic(List<Token> tokenList, ref int idx)
    {
        string operation = tokenList[idx++].Value;
        object? value = this.ParseOperand(tokenList, ref idx, false);
        
        return Operations.PerformUnaryOperation(operation, value);
    }

    private object? EvaluateMemoryManagement(List<Token> tokenList, ref int idx)
    {
        string operation = tokenList[idx++].Value;
        if (operation == "ALLOC")
        {
            return this.ExecuteConstruct(tokenList, ref idx);
        }
        if (operation == "FREE")
        {
            var target = this.EvaluateIdentifier(tokenList, ref idx);
            // TODO: FREE
            //this._variables.Remove(target);
        }
        else
        {
            throw new Exception($"Unknown memory management operation: {operation}");
        }
    }

    private object? ExecuteReference(List<Token> tokenList, ref int idx)
    {
        string operation = tokenList[idx++].Value;
        object? value = this.ParseOperand(tokenList, ref idx, false);

        object result = operation switch
        {
            "ADDR" => value,
            "VALOF" => this._variables[(string)value],
            _ => throw new Exception($"Unknown reference operation: {operation}")
        };

        this._variables[target] = result;
    }
    
    private object? ExecuteIndex(List<Token> tokenList, ref int idx)
    {
        // consume INDEX keyword
        
        idx++;
        
        int operands = int.Parse(tokenList[idx++].Value);
        object? arrayName = this.EvaluateIdentifier(tokenList, ref idx);
        
        int index = (int)this.ResolveValue(tokenList[idx++].Value);
        
    }
}