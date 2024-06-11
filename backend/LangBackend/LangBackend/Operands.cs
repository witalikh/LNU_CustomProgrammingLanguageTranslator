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
        object? value = null;
        
        switch (token.Type)
        {
            case TokenType.Number:
                value = ParseNumber(token.Value);
                break;
            case TokenType.String:
                value = token.Value;
                break;
            case TokenType.Identifier:
                throw new Exception("Invalid place to meet identifier, yet");
            case TokenType.Symbol:
                break;
            default:
                switch (token.Value)
                {
                    case Syntax.Add:
                    case Syntax.Subtract:
                    case Syntax.Multiply:
                    case Syntax.Divide:
                    case Syntax.Modulo:
                    case Syntax.FloorDivision:
                    case Syntax.Power:
                    case Syntax.BitwiseXor:
                    case Syntax.BitwiseAnd:
                    case Syntax.BitwiseOr:
                    case Syntax.BitwiseLeftShift:
                    case Syntax.BitwiseRightShift:
                        value = this.EvaluateBinaryArithmetic(tokenList, ref idx);
                        break;
                    case Syntax.LessThanOrEqual:
                    case Syntax.GreaterThanOrEqual:
                    case Syntax.LessThan:
                    case Syntax.GreaterThan:
                    case Syntax.Equal:
                    case Syntax.NotEqual:
                    case Syntax.StrictEqual:
                    case Syntax.StrictNotEqual:
                    case Syntax.MemberAccess:
                        value = this.EvaluateBinaryComparison(tokenList, ref idx);
                        break;
                    case Syntax.BooleanAnd:
                    case Syntax.BooleanOr:
                    case Syntax.BooleanXor:
                    case Syntax.BooleanFullAnd:
                    case Syntax.BooleanFullOr:
                        value = this.EvaluateBoolean(tokenList, ref idx);
                        break;
                    case Syntax.TypeCast:
                    case Syntax.NullCoalesce:
                        value = this.EvaluateTypeConversion(tokenList, ref idx);
                        break;
                    case Syntax.UnaryIdempotate:
                    case Syntax.UnaryNegate:
                    case Syntax.BooleanNot:
                    case Syntax.BitwiseInverse:
                        return this.EvaluateUnaryArithmetic(tokenList, ref idx);
                    case Syntax.Free:
                        value = this.EvaluateMemoryManagement(tokenList, ref idx);
                        break;
                    case Syntax.GetReferenceOf:
                    case Syntax.GetValueOf:
                        value = this.ExecuteReference(tokenList, ref idx);
                        break;
                    case Syntax.Identifier:
                        value = this.EvaluateIdentifier(tokenList, ref idx);
                        break;
                    case Syntax.Call:
                        value = this.ExecuteCall(tokenList, ref idx);
                        break;
                    case Syntax.Indexation:
                        value = this.ExecuteIndex(tokenList, ref idx);
                        break;
                    case Syntax.Allocate:
                        ExecuteAllocate(tokenList, ref idx);
                        break;
                    case Syntax.ConstructorCall:
                        this.ExecuteConstruct(tokenList, ref idx);
                        break;
                    default:
                        throw new Exception($"Unknown or unsupported token: {token.Value}");
                }

                break;
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
            Syntax.TypeCast => Convert.ChangeType(value, Type.GetType(tokenList[idx++].Value)),
            Syntax.NullCoalesce => value ?? this.ResolveValue(tokenList[idx++].Value),
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
        if (operation == Syntax.Allocate)
        {
            return this.ExecuteConstruct(tokenList, ref idx);
        }
        if (operation == Syntax.Free)
        {
            var target = this.EvaluateIdentifier(tokenList, ref idx);
            // TODO: FREE
            //this._variables.Remove(target);
            return null;
        }
        throw new Exception($"Unknown memory management operation: {operation}");
    }

    private object? ExecuteReference(List<Token> tokenList, ref int idx)
    {
        string operation = tokenList[idx++].Value;
        object? value = this.ParseOperand(tokenList, ref idx, false);

        object result = operation switch
        {
            Syntax.GetReferenceOf => value,
            Syntax.GetValueOf => this._variables[(string)value],
            _ => throw new Exception($"Unknown reference operation: {operation}")
        };

        return result;
    }
    
    private object? ExecuteIndex(List<Token> tokenList, ref int idx)
    {
        // consume INDEX keyword
        
        idx++;
        
        int operands = int.Parse(tokenList[idx++].Value);
        object? arrayName = this.EvaluateIdentifier(tokenList, ref idx);
        
        int index = (int)this.ResolveValue(tokenList[idx++].Value);

        return null;
    }
}