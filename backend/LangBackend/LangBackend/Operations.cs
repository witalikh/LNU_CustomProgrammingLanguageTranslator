using System.Numerics;

namespace LangBackend;

public static class Operations
{
    public static object? PerformBinaryOperation(string operation, object? lhs, object? rhs)
    {
        # region implicit-numeric-casts
        // Large boilerplate code piece
        
        if (lhs is bool lbool)
        {
            if (rhs is bool rbool)
            {
                return operation switch
                {
                    // Syntax.Add => lbool + rbool,
                    // Syntax.Subtract => lbool - rbool,
                    // Syntax.Multiply => lbool * rbool,
                    // Syntax.Divide => lbool / rbool,
                    // Syntax.Modulo => lbool % rbool,
                    // Syntax.FloorDivision => lbool / rbool,
                    // Syntax.Power => Math.Pow(lbool, rbool),
                    Syntax.BitwiseXor => lbool ^ rbool,
                    Syntax.BitwiseAnd => lbool & rbool,
                    Syntax.BitwiseOr => lbool | rbool,
                    // Syntax.BitwiseRightShift => lbool >> rbool,
                    // Syntax.BitwiseLeftShift => lbool << rbool,
                    // Syntax.LessThanOrEqual => lbool <= rbool,
                    // Syntax.GreaterThanOrEqual => lbool >= rbool,
                    // Syntax.LessThan => lbool < rbool,
                    // Syntax.GreaterThan => lbool > rbool,
                    Syntax.Equal => lbool == rbool,
                    Syntax.NotEqual => lbool != rbool,
                    Syntax.StrictEqual => lbool == rbool,
                    Syntax.StrictNotEqual => lbool != rbool,
                    //Syntax.IsElementOf => lbool in rbool,
                    Syntax.BooleanAnd => lbool && rbool,
                    Syntax.BooleanOr => lbool || rbool,
                    Syntax.BooleanXor => lbool ^ rbool,
                    Syntax.BooleanFullAnd => (bool)(lbool & rbool),
                    Syntax.BooleanFullOr => (bool)(lbool | rbool),
                    // Syntax.TypeCast => lbool as rbool,
                    //Syntax.NullCoalesce => lbool ?? rbool,
                    // Syntax.UnaryIdempotate => lbool ,
                    // Syntax.UnaryNegate => -lbool,
                    // Syntax.BooleanNot => !lbool,
                    // Syntax.BitwiseInverse => ~lbool,
                    //Syntax.Allocate => lbool != rbool,
                    //Syntax.Free => lbool != rbool,
                    //Syntax.GetReferenceOf => lbool != rbool,
                    //Syntax.GetValueOf => lbool != rbool,

                    _ => throw new Exception($"Unknown arithmetic operation: {operation}")
                };
            }
            else
            {
                throw new Exception($"Unsupported operand type for {lhs}: {rhs}");
            }
        }
        else if (lhs is Byte lint8)
        {
            if (rhs is Byte rint8)
            {
                return operation switch
                {
                    Syntax.Add => lint8 + rint8,
                    Syntax.Subtract => lint8 - rint8,
                    Syntax.Multiply => lint8 * rint8,
                    Syntax.Divide => lint8 / rint8,
                    Syntax.Modulo => lint8 % rint8,
                    Syntax.FloorDivision => lint8 / rint8,
                    Syntax.Power => Math.Pow(lint8, rint8),
                    Syntax.BitwiseXor => lint8 ^ rint8,
                    Syntax.BitwiseAnd => lint8 & rint8,
                    Syntax.BitwiseOr => lint8 | rint8,
                    Syntax.BitwiseRightShift => lint8 >> rint8,
                    Syntax.BitwiseLeftShift => lint8 << rint8,
                    Syntax.LessThanOrEqual => lint8 <= rint8,
                    Syntax.GreaterThanOrEqual => lint8 >= rint8,
                    Syntax.LessThan => lint8 < rint8,
                    Syntax.GreaterThan => lint8 > rint8,
                    Syntax.Equal => lint8 == rint8,
                    Syntax.NotEqual => lint8 != rint8,
                    Syntax.StrictEqual => lint8 == rint8,
                    Syntax.StrictNotEqual => lint8 != rint8,

                    _ => throw new Exception($"Unknown arithmetic operation: {operation}")
                };
            }
            else if (rhs is Int16 rint16)
            {
                return operation switch
                {
                    Syntax.Add => lint8 + rint16,
                    Syntax.Subtract => lint8 - rint16,
                    Syntax.Multiply => lint8 * rint16,
                    Syntax.Divide => lint8 / rint16,
                    Syntax.Modulo => lint8 % rint16,
                    Syntax.FloorDivision => lint8 / rint16,
                    Syntax.Power => Math.Pow(lint8, rint16),
                    Syntax.BitwiseXor => lint8 ^ rint16,
                    Syntax.BitwiseAnd => lint8 & rint16,
                    Syntax.BitwiseOr => lint8 | rint16,
                    Syntax.BitwiseRightShift => lint8 >> rint16,
                    Syntax.BitwiseLeftShift => lint8 << rint16,
                    Syntax.LessThanOrEqual => lint8 <= rint16,
                    Syntax.GreaterThanOrEqual => lint8 >= rint16,
                    Syntax.LessThan => lint8 < rint16,
                    Syntax.GreaterThan => lint8 > rint16,
                    Syntax.Equal => lint8 == rint16,
                    Syntax.NotEqual => lint8 != rint16,
                    Syntax.StrictEqual => false,
                    Syntax.StrictNotEqual => true,
                    
                    _ => throw new Exception($"Unknown arithmetic operation: {operation}")
                };
            }
            else if (rhs is Int32 rint32)
            {
                return operation switch
                {
                    Syntax.Add => lint8 + rint32,
                    Syntax.Subtract => lint8 - rint32,
                    Syntax.Multiply => lint8 * rint32,
                    Syntax.Divide => lint8 / rint32,
                    Syntax.Modulo => lint8 % rint32,
                    Syntax.FloorDivision => lint8 / rint32,
                    Syntax.Power => Math.Pow(lint8, rint32),
                    Syntax.BitwiseXor => lint8 ^ rint32,
                    Syntax.BitwiseAnd => lint8 & rint32,
                    Syntax.BitwiseOr => lint8 | rint32,
                    Syntax.BitwiseRightShift => lint8 >> rint32,
                    Syntax.BitwiseLeftShift => lint8 << rint32,
                    Syntax.LessThanOrEqual => lint8 <= rint32,
                    Syntax.GreaterThanOrEqual => lint8 >= rint32,
                    Syntax.LessThan => lint8 < rint32,
                    Syntax.GreaterThan => lint8 > rint32,
                    Syntax.Equal => lint8 == rint32,
                    Syntax.NotEqual => lint8 != rint32,
                    Syntax.StrictEqual => false,
                    Syntax.StrictNotEqual => true,

                    _ => throw new Exception($"Unknown arithmetic operation: {operation}")
                };
            }
            else if (rhs is Int64 rint64)
            {
                return operation switch
                {
                    Syntax.Add => lint8 + rint64,
                    Syntax.Subtract => lint8 - rint64,
                    Syntax.Multiply => lint8 * rint64,
                    Syntax.Divide => lint8 / rint64,
                    Syntax.Modulo => lint8 % rint64,
                    Syntax.FloorDivision => lint8 / rint64,
                    Syntax.Power => Math.Pow(lint8, rint64),
                    Syntax.BitwiseXor => lint8 ^ rint64,
                    Syntax.BitwiseAnd => lint8 & rint64,
                    Syntax.BitwiseOr => lint8 | rint64,
                    // Syntax.BitwiseRightShift => ((Int64)lint8) >> rint64,
                    // Syntax.BitwiseLeftShift => lint8 << rint64,
                    Syntax.LessThanOrEqual => lint8 <= rint64,
                    Syntax.GreaterThanOrEqual => lint8 >= rint64,
                    Syntax.LessThan => lint8 < rint64,
                    Syntax.GreaterThan => lint8 > rint64,
                    Syntax.Equal => lint8 == rint64,
                    Syntax.NotEqual => lint8 != rint64,
                    Syntax.StrictEqual => false,
                    Syntax.StrictNotEqual => true,

                    _ => throw new Exception($"Unknown arithmetic operation: {operation}")
                };
            }
            else if (rhs is BigInteger rintd)
            {
                return operation switch
                {
                    Syntax.Add => lint8 + rintd,
                    Syntax.Subtract => lint8 - rintd,
                    Syntax.Multiply => lint8 * rintd,
                    Syntax.Divide => lint8 / rintd,
                    Syntax.Modulo => lint8 % rintd,
                    Syntax.FloorDivision => lint8 / rintd,
                    // Syntax.Power => Math.Pow(lint8, rintd),
                    Syntax.BitwiseXor => lint8 ^ rintd,
                    Syntax.BitwiseAnd => lint8 & rintd,
                    Syntax.BitwiseOr => lint8 | rintd,
                    // Syntax.BitwiseRightShift => lint8 >> rintd,
                    // Syntax.BitwiseLeftShift => lint8 << rintd,
                    Syntax.LessThanOrEqual => lint8 <= rintd,
                    Syntax.GreaterThanOrEqual => lint8 >= rintd,
                    Syntax.LessThan => lint8 < rintd,
                    Syntax.GreaterThan => lint8 > rintd,
                    Syntax.Equal => lint8 == rintd,
                    Syntax.NotEqual => lint8 != rintd,
                    Syntax.StrictEqual => false,
                    Syntax.StrictNotEqual => true,

                    _ => throw new Exception($"Unknown arithmetic operation: {operation}")
                };
            }
            else if (rhs is float rfloat32)
            {
                return operation switch
                {
                    Syntax.Add => lint8 + rfloat32,
                    Syntax.Subtract => lint8 - rfloat32,
                    Syntax.Multiply => lint8 * rfloat32,
                    Syntax.Divide => lint8 / rfloat32,
                    Syntax.Modulo => lint8 % rfloat32,
                    Syntax.FloorDivision => lint8 / rfloat32,
                    Syntax.Power => Math.Pow(lint8, rfloat32),
                    Syntax.LessThanOrEqual => lint8 <= rfloat32,
                    Syntax.GreaterThanOrEqual => lint8 >= rfloat32,
                    Syntax.LessThan => lint8 < rfloat32,
                    Syntax.GreaterThan => lint8 > rfloat32,
                    Syntax.Equal => lint8 == rfloat32,
                    Syntax.NotEqual => lint8 != rfloat32,
                    Syntax.StrictEqual => false,
                    Syntax.StrictNotEqual => true,

                    _ => throw new Exception($"Unknown arithmetic operation: {operation}")
                };
            }
            else if (rhs is double rfloat64)
            {
                return operation switch
                {
                    Syntax.Add => lint8 + rfloat64,
                    Syntax.Subtract => lint8 - rfloat64,
                    Syntax.Multiply => lint8 * rfloat64,
                    Syntax.Divide => lint8 / rfloat64,
                    Syntax.Modulo => lint8 % rfloat64,
                    Syntax.FloorDivision => lint8 / rfloat64,
                    Syntax.Power => Math.Pow(lint8, rfloat64),
                    Syntax.LessThanOrEqual => lint8 <= rfloat64,
                    Syntax.GreaterThanOrEqual => lint8 >= rfloat64,
                    Syntax.LessThan => lint8 < rfloat64,
                    Syntax.GreaterThan => lint8 > rfloat64,
                    Syntax.Equal => lint8 == rfloat64,
                    Syntax.NotEqual => lint8 != rfloat64,
                    Syntax.StrictEqual => false,
                    Syntax.StrictNotEqual => true,

                    _ => throw new Exception($"Unknown arithmetic operation: {operation}")
                };
            }
            else if (rhs is Complex rcomplex128)
            {
                return operation switch
                {
                    Syntax.Add => lint8 + rcomplex128,
                    Syntax.Subtract => lint8 - rcomplex128,
                    Syntax.Multiply => lint8 * rcomplex128,
                    Syntax.Divide => lint8 / rcomplex128,
                    // Syntax.Power => Math.Pow(lint8, rcomplex128),
                    Syntax.Equal => lint8 == rcomplex128,
                    Syntax.NotEqual => lint8 != rcomplex128,
                    Syntax.StrictEqual => false,
                    Syntax.StrictNotEqual => true,

                    _ => throw new Exception($"Unknown arithmetic operation: {operation}")
                };
            }
            else
            {
                throw new Exception($"Unsupported operand type for {lhs}: {rhs}");
            }
        }
        else if (lhs is Int16 lint16)
        {
            if (rhs is Byte rint8)
            {
                return operation switch
                {
                    Syntax.Add => lint16 + rint8,
                    Syntax.Subtract => lint16 - rint8,
                    Syntax.Multiply => lint16 * rint8,
                    Syntax.Divide => lint16 / rint8,
                    Syntax.Modulo => lint16 % rint8,
                    Syntax.FloorDivision => lint16 / rint8,
                    Syntax.Power => Math.Pow(lint16, rint8),
                    Syntax.BitwiseXor => lint16 ^ rint8,
                    Syntax.BitwiseAnd => lint16 & rint8,
                    Syntax.BitwiseOr => lint16 | rint8,
                    Syntax.BitwiseRightShift => lint16 >> rint8,
                    Syntax.BitwiseLeftShift => lint16 << rint8,
                    Syntax.LessThanOrEqual => lint16 <= rint8,
                    Syntax.GreaterThanOrEqual => lint16 >= rint8,
                    Syntax.LessThan => lint16 < rint8,
                    Syntax.GreaterThan => lint16 > rint8,
                    Syntax.Equal => lint16 == rint8,
                    Syntax.NotEqual => lint16 != rint8,
                    Syntax.StrictEqual => false,
                    Syntax.StrictNotEqual => true,

                    _ => throw new Exception($"Unknown arithmetic operation: {operation}")
                };
            }
            else if (rhs is Int16 rint16)
            {
                return operation switch
                {
                    Syntax.Add => lint16 + rint16,
                    Syntax.Subtract => lint16 - rint16,
                    Syntax.Multiply => lint16 * rint16,
                    Syntax.Divide => lint16 / rint16,
                    Syntax.Modulo => lint16 % rint16,
                    Syntax.FloorDivision => lint16 / rint16,
                    Syntax.Power => Math.Pow(lint16, rint16),
                    Syntax.BitwiseXor => lint16 ^ rint16,
                    Syntax.BitwiseAnd => lint16 & rint16,
                    Syntax.BitwiseOr => lint16 | rint16,
                    Syntax.BitwiseRightShift => lint16 >> rint16,
                    Syntax.BitwiseLeftShift => lint16 << rint16,
                    Syntax.LessThanOrEqual => lint16 <= rint16,
                    Syntax.GreaterThanOrEqual => lint16 >= rint16,
                    Syntax.LessThan => lint16 < rint16,
                    Syntax.GreaterThan => lint16 > rint16,
                    Syntax.Equal => lint16 == rint16,
                    Syntax.NotEqual => lint16 != rint16,
                    Syntax.StrictEqual => lint16 == rint16,
                    Syntax.StrictNotEqual => lint16 != rint16,

                    _ => throw new Exception($"Unknown arithmetic operation: {operation}")
                };
            }
            else if (rhs is Int32 rint32)
            {
                return operation switch
                {
                    Syntax.Add => lint16 + rint32,
                    Syntax.Subtract => lint16 - rint32,
                    Syntax.Multiply => lint16 * rint32,
                    Syntax.Divide => lint16 / rint32,
                    Syntax.Modulo => lint16 % rint32,
                    Syntax.FloorDivision => lint16 / rint32,
                    Syntax.Power => Math.Pow(lint16, rint32),
                    Syntax.BitwiseXor => lint16 ^ rint32,
                    Syntax.BitwiseAnd => lint16 & rint32,
                    Syntax.BitwiseOr => lint16 | rint32,
                    Syntax.BitwiseRightShift => lint16 >> rint32,
                    Syntax.BitwiseLeftShift => lint16 << rint32,
                    Syntax.LessThanOrEqual => lint16 <= rint32,
                    Syntax.GreaterThanOrEqual => lint16 >= rint32,
                    Syntax.LessThan => lint16 < rint32,
                    Syntax.GreaterThan => lint16 > rint32,
                    Syntax.Equal => lint16 == rint32,
                    Syntax.NotEqual => lint16 != rint32,
                    Syntax.StrictEqual => false,
                    Syntax.StrictNotEqual => true,

                    _ => throw new Exception($"Unknown arithmetic operation: {operation}")
                };
            }
            else if (rhs is Int64 rint64)
            {
                return operation switch
                {
                    Syntax.Add => lint16 + rint64,
                    Syntax.Subtract => lint16 - rint64,
                    Syntax.Multiply => lint16 * rint64,
                    Syntax.Divide => lint16 / rint64,
                    Syntax.Modulo => lint16 % rint64,
                    Syntax.FloorDivision => lint16 / rint64,
                    Syntax.Power => Math.Pow(lint16, rint64),
                    Syntax.BitwiseXor => lint16 ^ rint64,
                    Syntax.BitwiseAnd => lint16 & rint64,
                    Syntax.BitwiseOr => lint16 | rint64,
                    Syntax.LessThanOrEqual => lint16 <= rint64,
                    Syntax.GreaterThanOrEqual => lint16 >= rint64,
                    Syntax.LessThan => lint16 < rint64,
                    Syntax.GreaterThan => lint16 > rint64,
                    Syntax.Equal => lint16 == rint64,
                    Syntax.NotEqual => lint16 != rint64,
                    Syntax.StrictEqual => false,
                    Syntax.StrictNotEqual => true,

                    _ => throw new Exception($"Unknown arithmetic operation: {operation}")
                };
            }
            else if (rhs is BigInteger rintd)
            {
                return operation switch
                {
                    Syntax.Add => lint16 + rintd,
                    Syntax.Subtract => lint16 - rintd,
                    Syntax.Multiply => lint16 * rintd,
                    Syntax.Divide => lint16 / rintd,
                    Syntax.Modulo => lint16 % rintd,
                    Syntax.FloorDivision => lint16 / rintd,
                    Syntax.BitwiseXor => lint16 ^ rintd,
                    Syntax.BitwiseAnd => lint16 & rintd,
                    Syntax.BitwiseOr => lint16 | rintd,
                    Syntax.LessThanOrEqual => lint16 <= rintd,
                    Syntax.GreaterThanOrEqual => lint16 >= rintd,
                    Syntax.LessThan => lint16 < rintd,
                    Syntax.GreaterThan => lint16 > rintd,
                    Syntax.Equal => lint16 == rintd,
                    Syntax.NotEqual => lint16 != rintd,
                    Syntax.StrictEqual => false,
                    Syntax.StrictNotEqual => true,

                    _ => throw new Exception($"Unknown arithmetic operation: {operation}")
                };
            }
            else if (rhs is float rfloat32)
            {
                return operation switch
                {
                    Syntax.Add => lint16 + rfloat32,
                    Syntax.Subtract => lint16 - rfloat32,
                    Syntax.Multiply => lint16 * rfloat32,
                    Syntax.Divide => lint16 / rfloat32,
                    Syntax.Modulo => lint16 % rfloat32,
                    Syntax.FloorDivision => lint16 / rfloat32,
                    Syntax.Power => Math.Pow(lint16, rfloat32),
                    Syntax.LessThanOrEqual => lint16 <= rfloat32,
                    Syntax.GreaterThanOrEqual => lint16 >= rfloat32,
                    Syntax.LessThan => lint16 < rfloat32,
                    Syntax.GreaterThan => lint16 > rfloat32,
                    Syntax.Equal => lint16 == rfloat32,
                    Syntax.NotEqual => lint16 != rfloat32,
                    Syntax.StrictEqual => false,
                    Syntax.StrictNotEqual => true,

                    _ => throw new Exception($"Unknown arithmetic operation: {operation}")
                };
            }
            else if (rhs is double rfloat64)
            {
                return operation switch
                {
                    Syntax.Add => lint16 + rfloat64,
                    Syntax.Subtract => lint16 - rfloat64,
                    Syntax.Multiply => lint16 * rfloat64,
                    Syntax.Divide => lint16 / rfloat64,
                    Syntax.Modulo => lint16 % rfloat64,
                    Syntax.FloorDivision => lint16 / rfloat64,
                    Syntax.Power => Math.Pow(lint16, rfloat64),
                    Syntax.LessThanOrEqual => lint16 <= rfloat64,
                    Syntax.GreaterThanOrEqual => lint16 >= rfloat64,
                    Syntax.LessThan => lint16 < rfloat64,
                    Syntax.GreaterThan => lint16 > rfloat64,
                    Syntax.Equal => lint16 == rfloat64,
                    Syntax.NotEqual => lint16 != rfloat64,
                    Syntax.StrictEqual => false,
                    Syntax.StrictNotEqual => true,

                    _ => throw new Exception($"Unknown arithmetic operation: {operation}")
                };
            }
            else if (rhs is Complex rcomplex128)
            {
                return operation switch
                {
                    Syntax.Add => lint16 + rcomplex128,
                    Syntax.Subtract => lint16 - rcomplex128,
                    Syntax.Multiply => lint16 * rcomplex128,
                    Syntax.Divide => lint16 / rcomplex128,
                    Syntax.FloorDivision => lint16 / rcomplex128,
                    //Syntax.Power => Math.Pow(lint16, rcomplex128),
                    Syntax.Equal => lint16 == rcomplex128,
                    Syntax.NotEqual => lint16 != rcomplex128,
                    Syntax.StrictEqual => false,
                    Syntax.StrictNotEqual => true,

                    _ => throw new Exception($"Unknown arithmetic operation: {operation}")
                };
            }
            else
            {
                throw new Exception($"Unsupported operand type for {lhs}: {rhs}");
            }
        }
        else if (lhs is Int32 lint32)
        {
            if (rhs is Byte rint8)
            {
                return operation switch
                {
                    Syntax.Add => lint32 + rint8,
                    Syntax.Subtract => lint32 - rint8,
                    Syntax.Multiply => lint32 * rint8,
                    Syntax.Divide => lint32 / rint8,
                    Syntax.Modulo => lint32 % rint8,
                    Syntax.FloorDivision => lint32 / rint8,
                    Syntax.Power => Math.Pow(lint32, rint8),
                    Syntax.BitwiseXor => lint32 ^ rint8,
                    Syntax.BitwiseAnd => lint32 & rint8,
                    Syntax.BitwiseOr => lint32 | rint8,
                    Syntax.BitwiseRightShift => lint32 >> rint8,
                    Syntax.BitwiseLeftShift => lint32 << rint8,
                    Syntax.LessThanOrEqual => lint32 <= rint8,
                    Syntax.GreaterThanOrEqual => lint32 >= rint8,
                    Syntax.LessThan => lint32 < rint8,
                    Syntax.GreaterThan => lint32 > rint8,
                    Syntax.Equal => lint32 == rint8,
                    Syntax.NotEqual => lint32 != rint8,
                    Syntax.StrictEqual => false,
                    Syntax.StrictNotEqual => true,

                    _ => throw new Exception($"Unknown arithmetic operation: {operation}")
                };
            }
            else if (rhs is Int16 rint16)
            {
                return operation switch
                {
                    Syntax.Add => lint32 + rint16,
                    Syntax.Subtract => lint32 - rint16,
                    Syntax.Multiply => lint32 * rint16,
                    Syntax.Divide => lint32 / rint16,
                    Syntax.Modulo => lint32 % rint16,
                    Syntax.FloorDivision => lint32 / rint16,
                    Syntax.Power => Math.Pow(lint32, rint16),
                    Syntax.BitwiseXor => lint32 ^ rint16,
                    Syntax.BitwiseAnd => lint32 & rint16,
                    Syntax.BitwiseOr => lint32 | rint16,
                    Syntax.BitwiseRightShift => lint32 >> rint16,
                    Syntax.BitwiseLeftShift => lint32 << rint16,
                    Syntax.LessThanOrEqual => lint32 <= rint16,
                    Syntax.GreaterThanOrEqual => lint32 >= rint16,
                    Syntax.LessThan => lint32 < rint16,
                    Syntax.GreaterThan => lint32 > rint16,
                    Syntax.Equal => lint32 == rint16,
                    Syntax.NotEqual => lint32 != rint16,
                    Syntax.StrictEqual => false,
                    Syntax.StrictNotEqual => true,

                    _ => throw new Exception($"Unknown arithmetic operation: {operation}")
                };
            }
            else if (rhs is Int32 rint32)
            {
                return operation switch
                {
                    Syntax.Add => lint32 + rint32,
                    Syntax.Subtract => lint32 - rint32,
                    Syntax.Multiply => lint32 * rint32,
                    Syntax.Divide => lint32 / rint32,
                    Syntax.Modulo => lint32 % rint32,
                    Syntax.FloorDivision => lint32 / rint32,
                    Syntax.Power => Math.Pow(lint32, rint32),
                    Syntax.BitwiseXor => lint32 ^ rint32,
                    Syntax.BitwiseAnd => lint32 & rint32,
                    Syntax.BitwiseOr => lint32 | rint32,
                    Syntax.BitwiseRightShift => lint32 >> rint32,
                    Syntax.BitwiseLeftShift => lint32 << rint32,
                    Syntax.LessThanOrEqual => lint32 <= rint32,
                    Syntax.GreaterThanOrEqual => lint32 >= rint32,
                    Syntax.LessThan => lint32 < rint32,
                    Syntax.GreaterThan => lint32 > rint32,
                    Syntax.Equal => lint32 == rint32,
                    Syntax.NotEqual => lint32 != rint32,
                    Syntax.StrictEqual => lint32 == rint32,
                    Syntax.StrictNotEqual => lint32 != rint32,

                    _ => throw new Exception($"Unknown arithmetic operation: {operation}")
                };
            }
            else if (rhs is Int64 rint64)
            {
                return operation switch
                {
                    Syntax.Add => lint32 + rint64,
                    Syntax.Subtract => lint32 - rint64,
                    Syntax.Multiply => lint32 * rint64,
                    Syntax.Divide => lint32 / rint64,
                    Syntax.Modulo => lint32 % rint64,
                    Syntax.FloorDivision => lint32 / rint64,
                    Syntax.Power => Math.Pow(lint32, rint64),
                    Syntax.BitwiseXor => lint32 ^ rint64,
                    Syntax.BitwiseAnd => lint32 & rint64,
                    Syntax.BitwiseOr => lint32 | rint64,
                    Syntax.LessThanOrEqual => lint32 <= rint64,
                    Syntax.GreaterThanOrEqual => lint32 >= rint64,
                    Syntax.LessThan => lint32 < rint64,
                    Syntax.GreaterThan => lint32 > rint64,
                    Syntax.Equal => lint32 == rint64,
                    Syntax.NotEqual => lint32 != rint64,
                    Syntax.StrictEqual => false,
                    Syntax.StrictNotEqual => true,

                    _ => throw new Exception($"Unknown arithmetic operation: {operation}")
                };
            }
            else if (rhs is BigInteger rintd)
            {
                return operation switch
                {
                    Syntax.Add => lint32 + rintd,
                    Syntax.Subtract => lint32 - rintd,
                    Syntax.Multiply => lint32 * rintd,
                    Syntax.Divide => lint32 / rintd,
                    Syntax.Modulo => lint32 % rintd,
                    Syntax.FloorDivision => lint32 / rintd,
                    Syntax.BitwiseXor => lint32 ^ rintd,
                    Syntax.BitwiseAnd => lint32 & rintd,
                    Syntax.BitwiseOr => lint32 | rintd,
                    Syntax.LessThanOrEqual => lint32 <= rintd,
                    Syntax.GreaterThanOrEqual => lint32 >= rintd,
                    Syntax.LessThan => lint32 < rintd,
                    Syntax.GreaterThan => lint32 > rintd,
                    Syntax.Equal => lint32 == rintd,
                    Syntax.NotEqual => lint32 != rintd,
                    Syntax.StrictEqual => false,
                    Syntax.StrictNotEqual => true,

                    _ => throw new Exception($"Unknown arithmetic operation: {operation}")
                };
            }
            else if (rhs is float rfloat32)
            {
                return operation switch
                {
                    Syntax.Add => lint32 + rfloat32,
                    Syntax.Subtract => lint32 - rfloat32,
                    Syntax.Multiply => lint32 * rfloat32,
                    Syntax.Divide => lint32 / rfloat32,
                    Syntax.Modulo => lint32 % rfloat32,
                    Syntax.FloorDivision => lint32 / rfloat32,
                    Syntax.Power => Math.Pow(lint32, rfloat32),
                    Syntax.LessThanOrEqual => lint32 <= rfloat32,
                    Syntax.GreaterThanOrEqual => lint32 >= rfloat32,
                    Syntax.LessThan => lint32 < rfloat32,
                    Syntax.GreaterThan => lint32 > rfloat32,
                    Syntax.Equal => lint32 == rfloat32,
                    Syntax.NotEqual => lint32 != rfloat32,
                    Syntax.StrictEqual => false,
                    Syntax.StrictNotEqual => true,

                    _ => throw new Exception($"Unknown arithmetic operation: {operation}")
                };
            }
            else if (rhs is double rfloat64)
            {
                return operation switch
                {
                    Syntax.Add => lint32 + rfloat64,
                    Syntax.Subtract => lint32 - rfloat64,
                    Syntax.Multiply => lint32 * rfloat64,
                    Syntax.Divide => lint32 / rfloat64,
                    Syntax.Modulo => lint32 % rfloat64,
                    Syntax.FloorDivision => lint32 / rfloat64,
                    Syntax.Power => Math.Pow(lint32, rfloat64),
                    Syntax.LessThanOrEqual => lint32 <= rfloat64,
                    Syntax.GreaterThanOrEqual => lint32 >= rfloat64,
                    Syntax.LessThan => lint32 < rfloat64,
                    Syntax.GreaterThan => lint32 > rfloat64,
                    Syntax.Equal => lint32 == rfloat64,
                    Syntax.NotEqual => lint32 != rfloat64,
                    Syntax.StrictEqual => false,
                    Syntax.StrictNotEqual => true,

                    _ => throw new Exception($"Unknown arithmetic operation: {operation}")
                };
            }
            else if (rhs is Complex rcomplex128)
            {
                return operation switch
                {
                    Syntax.Add => lint32 + rcomplex128,
                    Syntax.Subtract => lint32 - rcomplex128,
                    Syntax.Multiply => lint32 * rcomplex128,
                    Syntax.Divide => lint32 / rcomplex128,
                    Syntax.FloorDivision => lint32 / rcomplex128,
                    //Syntax.Power => Math.Pow(lint32, rcomplex128),
                    Syntax.Equal => lint32 == rcomplex128,
                    Syntax.NotEqual => lint32 != rcomplex128,
                    Syntax.StrictEqual => false,
                    Syntax.StrictNotEqual => true,

                    _ => throw new Exception($"Unknown arithmetic operation: {operation}")
                };
            }
            else
            {
                throw new Exception($"Unsupported operand type for {lhs}: {rhs}");
            }
        }
        else if (lhs is Int64 lint64)
        {
            if (rhs is Byte rint8)
            {
                return operation switch
                {
                    Syntax.Add => lint64 + rint8,
                    Syntax.Subtract => lint64 - rint8,
                    Syntax.Multiply => lint64 * rint8,
                    Syntax.Divide => lint64 / rint8,
                    Syntax.Modulo => lint64 % rint8,
                    Syntax.FloorDivision => lint64 / rint8,
                    Syntax.Power => Math.Pow(lint64, rint8),
                    Syntax.BitwiseXor => lint64 ^ rint8,
                    Syntax.BitwiseAnd => lint64 & rint8,
                    Syntax.BitwiseOr => lint64 | rint8,
                    Syntax.BitwiseRightShift => lint64 >> rint8,
                    Syntax.BitwiseLeftShift => lint64 << rint8,
                    Syntax.LessThanOrEqual => lint64 <= rint8,
                    Syntax.GreaterThanOrEqual => lint64 >= rint8,
                    Syntax.LessThan => lint64 < rint8,
                    Syntax.GreaterThan => lint64 > rint8,
                    Syntax.Equal => lint64 == rint8,
                    Syntax.NotEqual => lint64 != rint8,
                    Syntax.StrictEqual => false,
                    Syntax.StrictNotEqual => true,

                    _ => throw new Exception($"Unknown arithmetic operation: {operation}")
                };
            }
            else if (rhs is Int16 rint16)
            {
                return operation switch
                {
                    Syntax.Add => lint64 + rint16,
                    Syntax.Subtract => lint64 - rint16,
                    Syntax.Multiply => lint64 * rint16,
                    Syntax.Divide => lint64 / rint16,
                    Syntax.Modulo => lint64 % rint16,
                    Syntax.FloorDivision => lint64 / rint16,
                    Syntax.Power => Math.Pow(lint64, rint16),
                    Syntax.BitwiseXor => lint64 ^ rint16,
                    Syntax.BitwiseAnd => lint64 & rint16,
                    Syntax.BitwiseOr => lint64 | rint16,
                    Syntax.BitwiseRightShift => lint64 >> rint16,
                    Syntax.BitwiseLeftShift => lint64 << rint16,
                    Syntax.LessThanOrEqual => lint64 <= rint16,
                    Syntax.GreaterThanOrEqual => lint64 >= rint16,
                    Syntax.LessThan => lint64 < rint16,
                    Syntax.GreaterThan => lint64 > rint16,
                    Syntax.Equal => lint64 == rint16,
                    Syntax.NotEqual => lint64 != rint16,
                    Syntax.StrictEqual => false,
                    Syntax.StrictNotEqual => true,

                    _ => throw new Exception($"Unknown arithmetic operation: {operation}")
                };
            }
            else if (rhs is Int32 rint32)
            {
                return operation switch
                {
                    Syntax.Add => lint64 + rint32,
                    Syntax.Subtract => lint64 - rint32,
                    Syntax.Multiply => lint64 * rint32,
                    Syntax.Divide => lint64 / rint32,
                    Syntax.Modulo => lint64 % rint32,
                    Syntax.FloorDivision => lint64 / rint32,
                    Syntax.Power => Math.Pow(lint64, rint32),
                    Syntax.BitwiseXor => lint64 ^ rint32,
                    Syntax.BitwiseAnd => lint64 & rint32,
                    Syntax.BitwiseOr => lint64 | rint32,
                    Syntax.BitwiseRightShift => lint64 >> rint32,
                    Syntax.BitwiseLeftShift => lint64 << rint32,
                    Syntax.LessThanOrEqual => lint64 <= rint32,
                    Syntax.GreaterThanOrEqual => lint64 >= rint32,
                    Syntax.LessThan => lint64 < rint32,
                    Syntax.GreaterThan => lint64 > rint32,
                    Syntax.Equal => lint64 == rint32,
                    Syntax.NotEqual => lint64 != rint32,
                    Syntax.StrictEqual => false,
                    Syntax.StrictNotEqual => true,

                    _ => throw new Exception($"Unknown arithmetic operation: {operation}")
                };
            }
            else if (rhs is Int64 rint64)
            {
                return operation switch
                {
                    Syntax.Add => lint64 + rint64,
                    Syntax.Subtract => lint64 - rint64,
                    Syntax.Multiply => lint64 * rint64,
                    Syntax.Divide => lint64 / rint64,
                    Syntax.Modulo => lint64 % rint64,
                    Syntax.FloorDivision => lint64 / rint64,
                    Syntax.Power => Math.Pow(lint64, rint64),
                    Syntax.BitwiseXor => lint64 ^ rint64,
                    Syntax.BitwiseAnd => lint64 & rint64,
                    Syntax.BitwiseOr => lint64 | rint64,
                    Syntax.LessThanOrEqual => lint64 <= rint64,
                    Syntax.GreaterThanOrEqual => lint64 >= rint64,
                    Syntax.LessThan => lint64 < rint64,
                    Syntax.GreaterThan => lint64 > rint64,
                    Syntax.Equal => lint64 == rint64,
                    Syntax.NotEqual => lint64 != rint64,
                    Syntax.StrictEqual => lint64 == rint64,
                    Syntax.StrictNotEqual => lint64 != rint64,

                    _ => throw new Exception($"Unknown arithmetic operation: {operation}")
                };
            }
            else if (rhs is BigInteger rintd)
            {
                return operation switch
                {
                    Syntax.Add => lint64 + rintd,
                    Syntax.Subtract => lint64 - rintd,
                    Syntax.Multiply => lint64 * rintd,
                    Syntax.Divide => lint64 / rintd,
                    Syntax.Modulo => lint64 % rintd,
                    Syntax.FloorDivision => lint64 / rintd,
                    Syntax.BitwiseXor => lint64 ^ rintd,
                    Syntax.BitwiseAnd => lint64 & rintd,
                    Syntax.BitwiseOr => lint64 | rintd,
                    Syntax.LessThanOrEqual => lint64 <= rintd,
                    Syntax.GreaterThanOrEqual => lint64 >= rintd,
                    Syntax.LessThan => lint64 < rintd,
                    Syntax.GreaterThan => lint64 > rintd,
                    Syntax.Equal => lint64 == rintd,
                    Syntax.NotEqual => lint64 != rintd,
                    Syntax.StrictEqual => false,
                    Syntax.StrictNotEqual => true,

                    _ => throw new Exception($"Unknown arithmetic operation: {operation}")
                };
            }
            else if (rhs is float rfloat32)
            {
                return operation switch
                {
                    Syntax.Add => lint64 + rfloat32,
                    Syntax.Subtract => lint64 - rfloat32,
                    Syntax.Multiply => lint64 * rfloat32,
                    Syntax.Divide => lint64 / rfloat32,
                    Syntax.Modulo => lint64 % rfloat32,
                    Syntax.FloorDivision => lint64 / rfloat32,
                    Syntax.Power => Math.Pow(lint64, rfloat32),
                    Syntax.LessThanOrEqual => lint64 <= rfloat32,
                    Syntax.GreaterThanOrEqual => lint64 >= rfloat32,
                    Syntax.LessThan => lint64 < rfloat32,
                    Syntax.GreaterThan => lint64 > rfloat32,
                    Syntax.Equal => lint64 == rfloat32,
                    Syntax.NotEqual => lint64 != rfloat32,
                    Syntax.StrictEqual => false,
                    Syntax.StrictNotEqual => true,

                    _ => throw new Exception($"Unknown arithmetic operation: {operation}")
                };
            }
            else if (rhs is double rfloat64)
            {
                return operation switch
                {
                    Syntax.Add => lint64 + rfloat64,
                    Syntax.Subtract => lint64 - rfloat64,
                    Syntax.Multiply => lint64 * rfloat64,
                    Syntax.Divide => lint64 / rfloat64,
                    Syntax.Modulo => lint64 % rfloat64,
                    Syntax.FloorDivision => lint64 / rfloat64,
                    Syntax.Power => Math.Pow(lint64, rfloat64),
                    Syntax.LessThanOrEqual => lint64 <= rfloat64,
                    Syntax.GreaterThanOrEqual => lint64 >= rfloat64,
                    Syntax.LessThan => lint64 < rfloat64,
                    Syntax.GreaterThan => lint64 > rfloat64,
                    Syntax.Equal => lint64 == rfloat64,
                    Syntax.NotEqual => lint64 != rfloat64,
                    Syntax.StrictEqual => false,
                    Syntax.StrictNotEqual => true,

                    _ => throw new Exception($"Unknown arithmetic operation: {operation}")
                };
            }
            else if (rhs is Complex rcomplex128)
            {
                return operation switch
                {
                    Syntax.Add => lint64 + rcomplex128,
                    Syntax.Subtract => lint64 - rcomplex128,
                    Syntax.Multiply => lint64 * rcomplex128,
                    Syntax.Divide => lint64 / rcomplex128,
                    Syntax.FloorDivision => lint64 / rcomplex128,
                    //Syntax.Power => Math.Pow(lint64, rcomplex128),
                    Syntax.Equal => lint64 == rcomplex128,
                    Syntax.NotEqual => lint64 != rcomplex128,
                    Syntax.StrictEqual => false,
                    Syntax.StrictNotEqual => true,

                    _ => throw new Exception($"Unknown arithmetic operation: {operation}")
                };
            }
            else
            {
                throw new Exception($"Unsupported operand type for {lhs}: {rhs}");
            }
        }
        else if (lhs is BigInteger lintd)
        {
            if (rhs is Byte rint8)
            {
                return operation switch
                {
                    Syntax.Add => lintd + rint8,
                    Syntax.Subtract => lintd - rint8,
                    Syntax.Multiply => lintd * rint8,
                    Syntax.Divide => lintd / rint8,
                    Syntax.Modulo => lintd % rint8,
                    Syntax.FloorDivision => lintd / rint8,
                    Syntax.BitwiseXor => lintd ^ rint8,
                    Syntax.BitwiseAnd => lintd & rint8,
                    Syntax.BitwiseOr => lintd | rint8,
                    Syntax.BitwiseRightShift => lintd >> rint8,
                    Syntax.BitwiseLeftShift => lintd << rint8,
                    Syntax.LessThanOrEqual => lintd <= rint8,
                    Syntax.GreaterThanOrEqual => lintd >= rint8,
                    Syntax.LessThan => lintd < rint8,
                    Syntax.GreaterThan => lintd > rint8,
                    Syntax.Equal => lintd == rint8,
                    Syntax.NotEqual => lintd != rint8,
                    Syntax.StrictEqual => false,
                    Syntax.StrictNotEqual => true,

                    _ => throw new Exception($"Unknown arithmetic operation: {operation}")
                };
            }
            else if (rhs is Int16 rint16)
            {
                return operation switch
                {
                    Syntax.Add => lintd + rint16,
                    Syntax.Subtract => lintd - rint16,
                    Syntax.Multiply => lintd * rint16,
                    Syntax.Divide => lintd / rint16,
                    Syntax.Modulo => lintd % rint16,
                    Syntax.FloorDivision => lintd / rint16,
                    Syntax.BitwiseXor => lintd ^ rint16,
                    Syntax.BitwiseAnd => lintd & rint16,
                    Syntax.BitwiseOr => lintd | rint16,
                    Syntax.BitwiseRightShift => lintd >> rint16,
                    Syntax.BitwiseLeftShift => lintd << rint16,
                    Syntax.LessThanOrEqual => lintd <= rint16,
                    Syntax.GreaterThanOrEqual => lintd >= rint16,
                    Syntax.LessThan => lintd < rint16,
                    Syntax.GreaterThan => lintd > rint16,
                    Syntax.Equal => lintd == rint16,
                    Syntax.NotEqual => lintd != rint16,
                    Syntax.StrictEqual => false,
                    Syntax.StrictNotEqual => true,

                    _ => throw new Exception($"Unknown arithmetic operation: {operation}")
                };
            }
            else if (rhs is Int32 rint32)
            {
                return operation switch
                {
                    Syntax.Add => lintd + rint32,
                    Syntax.Subtract => lintd - rint32,
                    Syntax.Multiply => lintd * rint32,
                    Syntax.Divide => lintd / rint32,
                    Syntax.Modulo => lintd % rint32,
                    Syntax.FloorDivision => lintd / rint32,
                    Syntax.BitwiseXor => lintd ^ rint32,
                    Syntax.BitwiseAnd => lintd & rint32,
                    Syntax.BitwiseOr => lintd | rint32,
                    Syntax.BitwiseRightShift => lintd >> rint32,
                    Syntax.BitwiseLeftShift => lintd << rint32,
                    Syntax.LessThanOrEqual => lintd <= rint32,
                    Syntax.GreaterThanOrEqual => lintd >= rint32,
                    Syntax.LessThan => lintd < rint32,
                    Syntax.GreaterThan => lintd > rint32,
                    Syntax.Equal => lintd == rint32,
                    Syntax.NotEqual => lintd != rint32,
                    Syntax.StrictEqual => false,
                    Syntax.StrictNotEqual => true,

                    _ => throw new Exception($"Unknown arithmetic operation: {operation}")
                };
            }
            else if (rhs is Int64 rint64)
            {
                return operation switch
                {
                    Syntax.Add => lintd + rint64,
                    Syntax.Subtract => lintd - rint64,
                    Syntax.Multiply => lintd * rint64,
                    Syntax.Divide => lintd / rint64,
                    Syntax.Modulo => lintd % rint64,
                    Syntax.FloorDivision => lintd / rint64,
                    Syntax.BitwiseXor => lintd ^ rint64,
                    Syntax.BitwiseAnd => lintd & rint64,
                    Syntax.BitwiseOr => lintd | rint64,
                    Syntax.LessThanOrEqual => lintd <= rint64,
                    Syntax.GreaterThanOrEqual => lintd >= rint64,
                    Syntax.LessThan => lintd < rint64,
                    Syntax.GreaterThan => lintd > rint64,
                    Syntax.Equal => lintd == rint64,
                    Syntax.NotEqual => lintd != rint64,
                    Syntax.StrictEqual => false,
                    Syntax.StrictNotEqual => true,

                    _ => throw new Exception($"Unknown arithmetic operation: {operation}")
                };
            }
            else if (rhs is BigInteger rintd)
            {
                return operation switch
                {
                    Syntax.Add => lintd + rintd,
                    Syntax.Subtract => lintd - rintd,
                    Syntax.Multiply => lintd * rintd,
                    Syntax.Divide => lintd / rintd,
                    Syntax.Modulo => lintd % rintd,
                    Syntax.FloorDivision => lintd / rintd,
                    Syntax.BitwiseXor => lintd ^ rintd,
                    Syntax.BitwiseAnd => lintd & rintd,
                    Syntax.BitwiseOr => lintd | rintd,
                    Syntax.LessThanOrEqual => lintd <= rintd,
                    Syntax.GreaterThanOrEqual => lintd >= rintd,
                    Syntax.LessThan => lintd < rintd,
                    Syntax.GreaterThan => lintd > rintd,
                    Syntax.Equal => lintd == rintd,
                    Syntax.NotEqual => lintd != rintd,
                    Syntax.StrictEqual => lintd == rintd,
                    Syntax.StrictNotEqual => lintd != rintd,

                    _ => throw new Exception($"Unknown arithmetic operation: {operation}")
                };
            }
            else
            {
                throw new Exception($"Unsupported operand type for {lhs}: {rhs}");
            }
        }
        else if (lhs is float lfloat32)
        {
            if (rhs is Byte rint8)
            {
                return operation switch
                {
                    Syntax.Add => lfloat32 + rint8,
                    Syntax.Subtract => lfloat32 - rint8,
                    Syntax.Multiply => lfloat32 * rint8,
                    Syntax.Divide => lfloat32 / rint8,
                    Syntax.Modulo => lfloat32 % rint8,
                    Syntax.FloorDivision => lfloat32 / rint8,
                    Syntax.Power => Math.Pow(lfloat32, rint8),
                    Syntax.LessThanOrEqual => lfloat32 <= rint8,
                    Syntax.GreaterThanOrEqual => lfloat32 >= rint8,
                    Syntax.LessThan => lfloat32 < rint8,
                    Syntax.GreaterThan => lfloat32 > rint8,
                    Syntax.Equal => lfloat32 == rint8,
                    Syntax.NotEqual => lfloat32 != rint8,
                    Syntax.StrictEqual => false,
                    Syntax.StrictNotEqual => true,

                    _ => throw new Exception($"Unknown arithmetic operation: {operation}")
                };
            }
            else if (rhs is Int16 rint16)
            {
                return operation switch
                {
                    Syntax.Add => lfloat32 + rint16,
                    Syntax.Subtract => lfloat32 - rint16,
                    Syntax.Multiply => lfloat32 * rint16,
                    Syntax.Divide => lfloat32 / rint16,
                    Syntax.Modulo => lfloat32 % rint16,
                    Syntax.FloorDivision => lfloat32 / rint16,
                    Syntax.Power => Math.Pow(lfloat32, rint16),
                    Syntax.LessThanOrEqual => lfloat32 <= rint16,
                    Syntax.GreaterThanOrEqual => lfloat32 >= rint16,
                    Syntax.LessThan => lfloat32 < rint16,
                    Syntax.GreaterThan => lfloat32 > rint16,
                    Syntax.Equal => lfloat32 == rint16,
                    Syntax.NotEqual => lfloat32 != rint16,
                    Syntax.StrictEqual => false,
                    Syntax.StrictNotEqual => true,

                    _ => throw new Exception($"Unknown arithmetic operation: {operation}")
                };
            }
            else if (rhs is Int32 rint32)
            {
                return operation switch
                {
                    Syntax.Add => lfloat32 + rint32,
                    Syntax.Subtract => lfloat32 - rint32,
                    Syntax.Multiply => lfloat32 * rint32,
                    Syntax.Divide => lfloat32 / rint32,
                    Syntax.Modulo => lfloat32 % rint32,
                    Syntax.FloorDivision => lfloat32 / rint32,
                    Syntax.Power => Math.Pow(lfloat32, rint32),
                    Syntax.LessThanOrEqual => lfloat32 <= rint32,
                    Syntax.GreaterThanOrEqual => lfloat32 >= rint32,
                    Syntax.LessThan => lfloat32 < rint32,
                    Syntax.GreaterThan => lfloat32 > rint32,
                    Syntax.Equal => lfloat32 == rint32,
                    Syntax.NotEqual => lfloat32 != rint32,
                    Syntax.StrictEqual => false,
                    Syntax.StrictNotEqual => true,

                    _ => throw new Exception($"Unknown arithmetic operation: {operation}")
                };
            }
            else if (rhs is Int64 rint64)
            {
                return operation switch
                {
                    Syntax.Add => lfloat32 + rint64,
                    Syntax.Subtract => lfloat32 - rint64,
                    Syntax.Multiply => lfloat32 * rint64,
                    Syntax.Divide => lfloat32 / rint64,
                    Syntax.Modulo => lfloat32 % rint64,
                    Syntax.FloorDivision => lfloat32 / rint64,
                    Syntax.Power => Math.Pow(lfloat32, rint64),
                    Syntax.LessThanOrEqual => lfloat32 <= rint64,
                    Syntax.GreaterThanOrEqual => lfloat32 >= rint64,
                    Syntax.LessThan => lfloat32 < rint64,
                    Syntax.GreaterThan => lfloat32 > rint64,
                    Syntax.Equal => lfloat32 == rint64,
                    Syntax.NotEqual => lfloat32 != rint64,
                    Syntax.StrictEqual => false,
                    Syntax.StrictNotEqual => true,

                    _ => throw new Exception($"Unknown arithmetic operation: {operation}")
                };
            }
            else if (rhs is float rfloat32)
            {
                return operation switch
                {
                    Syntax.Add => lfloat32 + rfloat32,
                    Syntax.Subtract => lfloat32 - rfloat32,
                    Syntax.Multiply => lfloat32 * rfloat32,
                    Syntax.Divide => lfloat32 / rfloat32,
                    Syntax.Modulo => lfloat32 % rfloat32,
                    Syntax.FloorDivision => lfloat32 / rfloat32,
                    Syntax.Power => Math.Pow(lfloat32, rfloat32),
                    Syntax.LessThanOrEqual => lfloat32 <= rfloat32,
                    Syntax.GreaterThanOrEqual => lfloat32 >= rfloat32,
                    Syntax.LessThan => lfloat32 < rfloat32,
                    Syntax.GreaterThan => lfloat32 > rfloat32,
                    Syntax.Equal => lfloat32 == rfloat32,
                    Syntax.NotEqual => lfloat32 != rfloat32,
                    Syntax.StrictEqual => lfloat32 == rfloat32,
                    Syntax.StrictNotEqual => lfloat32 != rfloat32,

                    _ => throw new Exception($"Unknown arithmetic operation: {operation}")
                };
            }
            else if (rhs is double rfloat64)
            {
                return operation switch
                {
                    Syntax.Add => lfloat32 + rfloat64,
                    Syntax.Subtract => lfloat32 - rfloat64,
                    Syntax.Multiply => lfloat32 * rfloat64,
                    Syntax.Divide => lfloat32 / rfloat64,
                    Syntax.Modulo => lfloat32 % rfloat64,
                    Syntax.FloorDivision => lfloat32 / rfloat64,
                    Syntax.Power => Math.Pow(lfloat32, rfloat64),
                    Syntax.LessThanOrEqual => lfloat32 <= rfloat64,
                    Syntax.GreaterThanOrEqual => lfloat32 >= rfloat64,
                    Syntax.LessThan => lfloat32 < rfloat64,
                    Syntax.GreaterThan => lfloat32 > rfloat64,
                    Syntax.Equal => lfloat32 == rfloat64,
                    Syntax.NotEqual => lfloat32 != rfloat64,
                    Syntax.StrictEqual => false,
                    Syntax.StrictNotEqual => true,

                    _ => throw new Exception($"Unknown arithmetic operation: {operation}")
                };
            }
            else if (rhs is Complex rcomplex128)
            {
                return operation switch
                {
                    Syntax.Add => lfloat32 + rcomplex128,
                    Syntax.Subtract => lfloat32 - rcomplex128,
                    Syntax.Multiply => lfloat32 * rcomplex128,
                    Syntax.Divide => lfloat32 / rcomplex128,
                    Syntax.FloorDivision => lfloat32 / rcomplex128,
                    //Syntax.Power => Math.Pow(lfloat32, rcomplex128),
                    Syntax.Equal => lfloat32 == rcomplex128,
                    Syntax.NotEqual => lfloat32 != rcomplex128,
                    Syntax.StrictEqual => false,
                    Syntax.StrictNotEqual => true,

                    _ => throw new Exception($"Unknown arithmetic operation: {operation}")
                };
            }
            else
            {
                throw new Exception($"Unsupported operand type for {lhs}: {rhs}");
            }
        }
        else if (lhs is double lfloat64)
        {
            if (rhs is Byte rint8)
            {
                return operation switch
                {
                    Syntax.Add => lfloat64 + rint8,
                    Syntax.Subtract => lfloat64 - rint8,
                    Syntax.Multiply => lfloat64 * rint8,
                    Syntax.Divide => lfloat64 / rint8,
                    Syntax.Modulo => lfloat64 % rint8,
                    Syntax.FloorDivision => lfloat64 / rint8,
                    Syntax.Power => Math.Pow(lfloat64, rint8),
                    Syntax.LessThanOrEqual => lfloat64 <= rint8,
                    Syntax.GreaterThanOrEqual => lfloat64 >= rint8,
                    Syntax.LessThan => lfloat64 < rint8,
                    Syntax.GreaterThan => lfloat64 > rint8,
                    Syntax.Equal => lfloat64 == rint8,
                    Syntax.NotEqual => lfloat64 != rint8,
                    Syntax.StrictEqual => false,
                    Syntax.StrictNotEqual => true,

                    _ => throw new Exception($"Unknown arithmetic operation: {operation}")
                };
            }
            else if (rhs is Int16 rint16)
            {
                return operation switch
                {
                    Syntax.Add => lfloat64 + rint16,
                    Syntax.Subtract => lfloat64 - rint16,
                    Syntax.Multiply => lfloat64 * rint16,
                    Syntax.Divide => lfloat64 / rint16,
                    Syntax.Modulo => lfloat64 % rint16,
                    Syntax.FloorDivision => lfloat64 / rint16,
                    Syntax.Power => Math.Pow(lfloat64, rint16),
                    Syntax.LessThanOrEqual => lfloat64 <= rint16,
                    Syntax.GreaterThanOrEqual => lfloat64 >= rint16,
                    Syntax.LessThan => lfloat64 < rint16,
                    Syntax.GreaterThan => lfloat64 > rint16,
                    Syntax.Equal => lfloat64 == rint16,
                    Syntax.NotEqual => lfloat64 != rint16,
                    Syntax.StrictEqual => false,
                    Syntax.StrictNotEqual => true,

                    _ => throw new Exception($"Unknown arithmetic operation: {operation}")
                };
            }
            else if (rhs is Int32 rint32)
            {
                return operation switch
                {
                    Syntax.Add => lfloat64 + rint32,
                    Syntax.Subtract => lfloat64 - rint32,
                    Syntax.Multiply => lfloat64 * rint32,
                    Syntax.Divide => lfloat64 / rint32,
                    Syntax.Modulo => lfloat64 % rint32,
                    Syntax.FloorDivision => lfloat64 / rint32,
                    Syntax.Power => Math.Pow(lfloat64, rint32),
                    Syntax.LessThanOrEqual => lfloat64 <= rint32,
                    Syntax.GreaterThanOrEqual => lfloat64 >= rint32,
                    Syntax.LessThan => lfloat64 < rint32,
                    Syntax.GreaterThan => lfloat64 > rint32,
                    Syntax.Equal => lfloat64 == rint32,
                    Syntax.NotEqual => lfloat64 != rint32,
                    Syntax.StrictEqual => false,
                    Syntax.StrictNotEqual => true,

                    _ => throw new Exception($"Unknown arithmetic operation: {operation}")
                };
            }
            else if (rhs is Int64 rint64)
            {
                return operation switch
                {
                    Syntax.Add => lfloat64 + rint64,
                    Syntax.Subtract => lfloat64 - rint64,
                    Syntax.Multiply => lfloat64 * rint64,
                    Syntax.Divide => lfloat64 / rint64,
                    Syntax.Modulo => lfloat64 % rint64,
                    Syntax.FloorDivision => lfloat64 / rint64,
                    Syntax.Power => Math.Pow(lfloat64, rint64),
                    Syntax.LessThanOrEqual => lfloat64 <= rint64,
                    Syntax.GreaterThanOrEqual => lfloat64 >= rint64,
                    Syntax.LessThan => lfloat64 < rint64,
                    Syntax.GreaterThan => lfloat64 > rint64,
                    Syntax.Equal => lfloat64 == rint64,
                    Syntax.NotEqual => lfloat64 != rint64,
                    Syntax.StrictEqual => false,
                    Syntax.StrictNotEqual => true,

                    _ => throw new Exception($"Unknown arithmetic operation: {operation}")
                };
            }
            else if (rhs is float rfloat32)
            {
                return operation switch
                {
                    Syntax.Add => lfloat64 + rfloat32,
                    Syntax.Subtract => lfloat64 - rfloat32,
                    Syntax.Multiply => lfloat64 * rfloat32,
                    Syntax.Divide => lfloat64 / rfloat32,
                    Syntax.Modulo => lfloat64 % rfloat32,
                    Syntax.FloorDivision => lfloat64 / rfloat32,
                    Syntax.Power => Math.Pow(lfloat64, rfloat32),
                    Syntax.LessThanOrEqual => lfloat64 <= rfloat32,
                    Syntax.GreaterThanOrEqual => lfloat64 >= rfloat32,
                    Syntax.LessThan => lfloat64 < rfloat32,
                    Syntax.GreaterThan => lfloat64 > rfloat32,
                    Syntax.Equal => lfloat64 == rfloat32,
                    Syntax.NotEqual => lfloat64 != rfloat32,
                    Syntax.StrictEqual => false,
                    Syntax.StrictNotEqual => true,

                    _ => throw new Exception($"Unknown arithmetic operation: {operation}")
                };
            }
            else if (rhs is double rfloat64)
            {
                return operation switch
                {
                    Syntax.Add => lfloat64 + rfloat64,
                    Syntax.Subtract => lfloat64 - rfloat64,
                    Syntax.Multiply => lfloat64 * rfloat64,
                    Syntax.Divide => lfloat64 / rfloat64,
                    Syntax.Modulo => lfloat64 % rfloat64,
                    Syntax.FloorDivision => lfloat64 / rfloat64,
                    Syntax.Power => Math.Pow(lfloat64, rfloat64),
                    Syntax.LessThanOrEqual => lfloat64 <= rfloat64,
                    Syntax.GreaterThanOrEqual => lfloat64 >= rfloat64,
                    Syntax.LessThan => lfloat64 < rfloat64,
                    Syntax.GreaterThan => lfloat64 > rfloat64,
                    Syntax.Equal => lfloat64 == rfloat64,
                    Syntax.NotEqual => lfloat64 != rfloat64,
                    Syntax.StrictEqual => lfloat64 == rfloat64,
                    Syntax.StrictNotEqual => lfloat64 != rfloat64,
                    
                    _ => throw new Exception($"Unknown arithmetic operation: {operation}")
                };
            }
            else if (rhs is Complex rcomplex128)
            {
                return operation switch
                {
                    Syntax.Add => lfloat64 + rcomplex128,
                    Syntax.Subtract => lfloat64 - rcomplex128,
                    Syntax.Multiply => lfloat64 * rcomplex128,
                    Syntax.Divide => lfloat64 / rcomplex128,
                    Syntax.FloorDivision => lfloat64 / rcomplex128,
                    //Syntax.Power => Math.Pow(lfloat64, rcomplex128),
                    Syntax.Equal => lfloat64 == rcomplex128,
                    Syntax.NotEqual => lfloat64 != rcomplex128,
                    Syntax.StrictEqual => false,
                    Syntax.StrictNotEqual => true,

                    _ => throw new Exception($"Unknown arithmetic operation: {operation}")
                };
            }
            else
            {
                throw new Exception($"Unsupported operand type for {lhs}: {rhs}");
            }
        }
        else if (lhs is Complex lcomplex128)
        {
            if (rhs is Byte rint8)
            {
                return operation switch
                {
                    Syntax.Add => lcomplex128 + rint8,
                    Syntax.Subtract => lcomplex128 - rint8,
                    Syntax.Multiply => lcomplex128 * rint8,
                    Syntax.Divide => lcomplex128 / rint8,
                    Syntax.FloorDivision => lcomplex128 / rint8,
                    Syntax.Equal => lcomplex128 == rint8,
                    Syntax.NotEqual => lcomplex128 != rint8,
                    Syntax.StrictEqual => false,
                    Syntax.StrictNotEqual => true,

                    _ => throw new Exception($"Unknown arithmetic operation: {operation}")
                };
            }
            else if (rhs is Int16 rint16)
            {
                return operation switch
                {
                    Syntax.Add => lcomplex128 + rint16,
                    Syntax.Subtract => lcomplex128 - rint16,
                    Syntax.Multiply => lcomplex128 * rint16,
                    Syntax.Divide => lcomplex128 / rint16,
                    Syntax.FloorDivision => lcomplex128 / rint16,
                    Syntax.Equal => lcomplex128 == rint16,
                    Syntax.NotEqual => lcomplex128 != rint16,
                    Syntax.StrictEqual => false,
                    Syntax.StrictNotEqual => true,

                    _ => throw new Exception($"Unknown arithmetic operation: {operation}")
                };
            }
            else if (rhs is Int32 rint32)
            {
                return operation switch
                {
                    Syntax.Add => lcomplex128 + rint32,
                    Syntax.Subtract => lcomplex128 - rint32,
                    Syntax.Multiply => lcomplex128 * rint32,
                    Syntax.Divide => lcomplex128 / rint32,
                    Syntax.FloorDivision => lcomplex128 / rint32,
                    Syntax.Equal => lcomplex128 == rint32,
                    Syntax.NotEqual => lcomplex128 != rint32,
                    Syntax.StrictEqual => false,
                    Syntax.StrictNotEqual => true,

                    _ => throw new Exception($"Unknown arithmetic operation: {operation}")
                };
            }
            else if (rhs is Int64 rint64)
            {
                return operation switch
                {
                    Syntax.Add => lcomplex128 + rint64,
                    Syntax.Subtract => lcomplex128 - rint64,
                    Syntax.Multiply => lcomplex128 * rint64,
                    Syntax.Divide => lcomplex128 / rint64,
                    Syntax.FloorDivision => lcomplex128 / rint64,
                    Syntax.Equal => lcomplex128 == rint64,
                    Syntax.NotEqual => lcomplex128 != rint64,
                    Syntax.StrictEqual => false,
                    Syntax.StrictNotEqual => true,

                    _ => throw new Exception($"Unknown arithmetic operation: {operation}")
                };
            }
            else if (rhs is float rfloat32)
            {
                return operation switch
                {
                    Syntax.Add => lcomplex128 + rfloat32,
                    Syntax.Subtract => lcomplex128 - rfloat32,
                    Syntax.Multiply => lcomplex128 * rfloat32,
                    Syntax.Divide => lcomplex128 / rfloat32,
                    Syntax.FloorDivision => lcomplex128 / rfloat32,
                    Syntax.Equal => lcomplex128 == rfloat32,
                    Syntax.NotEqual => lcomplex128 != rfloat32,
                    Syntax.StrictEqual => false,
                    Syntax.StrictNotEqual => true,

                    _ => throw new Exception($"Unknown arithmetic operation: {operation}")
                };
            }
            else if (rhs is double rfloat64)
            {
                return operation switch
                {
                    Syntax.Add => lcomplex128 + rfloat64,
                    Syntax.Subtract => lcomplex128 - rfloat64,
                    Syntax.Multiply => lcomplex128 * rfloat64,
                    Syntax.Divide => lcomplex128 / rfloat64,
                    Syntax.FloorDivision => lcomplex128 / rfloat64,
                    Syntax.Equal => lcomplex128 == rfloat64,
                    Syntax.NotEqual => lcomplex128 != rfloat64,
                    Syntax.StrictEqual => false,
                    Syntax.StrictNotEqual => true,

                    _ => throw new Exception($"Unknown arithmetic operation: {operation}")
                };
            }
            else if (rhs is Complex rcomplex128)
            {
                return operation switch
                {
                    Syntax.Add => lcomplex128 + rcomplex128,
                    Syntax.Subtract => lcomplex128 - rcomplex128,
                    Syntax.Multiply => lcomplex128 * rcomplex128,
                    Syntax.Divide => lcomplex128 / rcomplex128,
                    Syntax.FloorDivision => lcomplex128 / rcomplex128,
                    //Syntax.Power => Math.Pow(lcomplex128, rcomplex128),
                    Syntax.Equal => lcomplex128 == rcomplex128,
                    Syntax.NotEqual => lcomplex128 != rcomplex128,
                    Syntax.StrictEqual => lcomplex128 == rcomplex128,
                    Syntax.StrictNotEqual => lcomplex128 != rcomplex128,
                    
                    _ => throw new Exception($"Unknown arithmetic operation: {operation}")
                };
            }
            else
            {
                throw new Exception($"Unsupported operand type for {lhs}: {rhs}");
            }
        }
        
        #endregion
        else if (lhs is string lstring)
        {
            
        }
        else
        {
            throw new Exception($"Unsupported operand type: {lhs}");
        }

        return null;
    }

    public static object? PerformUnaryOperation(string operation, object? operand)
    {
        if (operand is Byte valint8)
        {
            return operation switch
            {
                Syntax.UnaryIdempotate => valint8,
                Syntax.UnaryNegate => -valint8,
                //Syntax.BooleanNot => !valint8,
                Syntax.BitwiseInverse => ~valint8,
                // Syntax.Allocate => ,
                // Syntax.Free => ,
                // Syntax.GetReferenceOf => ,
                // Syntax.GetValueOf => ,

                _ => throw new Exception($"Unknown arithmetic operation: {operation}")
            };
        }
        else if (operand is Int16 valint16)
        {
            return operation switch
            {
                Syntax.UnaryIdempotate => valint16,
                Syntax.UnaryNegate => -valint16,
                //Syntax.BooleanNot => !valint16,
                Syntax.BitwiseInverse => ~valint16,

                _ => throw new Exception($"Unknown arithmetic operation: {operation}")
            };
        }
        else if (operand is Int32 valint32)
        {
            return operation switch
            {
                Syntax.UnaryIdempotate => valint32,
                Syntax.UnaryNegate => -valint32,
                //Syntax.BooleanNot => !valint32,
                Syntax.BitwiseInverse => ~valint32,

                _ => throw new Exception($"Unknown arithmetic operation: {operation}")
            };
        }
        else if (operand is Int64 valint64)
        {
            return operation switch
            {
                Syntax.UnaryIdempotate => valint64,
                Syntax.UnaryNegate => -valint64,
                //Syntax.BooleanNot => !valint64,
                Syntax.BitwiseInverse => ~valint64,

                _ => throw new Exception($"Unknown arithmetic operation: {operation}")
            };
        }
        else if (operand is BigInteger valintd)
        {
            return operation switch
            {
                Syntax.UnaryIdempotate => valintd,
                Syntax.UnaryNegate => -valintd,
                //Syntax.BooleanNot => !valintd,
                Syntax.BitwiseInverse => ~valintd,

                _ => throw new Exception($"Unknown arithmetic operation: {operation}")
            };
        }
        else if (operand is float valfloat32)
        {
            return operation switch
            {
                Syntax.UnaryIdempotate => valfloat32,
                Syntax.UnaryNegate => -valfloat32,
                
                _ => throw new Exception($"Unknown arithmetic operation: {operation}")
            };
        }
        else if (operand is double valfloat64)
        {
            return operation switch
            {
                Syntax.UnaryIdempotate => valfloat64,
                Syntax.UnaryNegate => -valfloat64,

                _ => throw new Exception($"Unknown arithmetic operation: {operation}")
            };
        }
        else if (operand is Complex valcomplex)
        {
            return operation switch
            {
                Syntax.UnaryIdempotate => valcomplex,
                Syntax.UnaryNegate => -valcomplex,

                _ => throw new Exception($"Unknown arithmetic operation: {operation}")
            };
        }
        else if (operand is bool valbool)
        {
            return operation switch
            {
                Syntax.BooleanNot => !valbool,

                _ => throw new Exception($"Unknown arithmetic operation: {operation}")
            };
        }
        else
        {
            throw new Exception($"Unknown arithmetic operand: {operand}");
        }
    }
}