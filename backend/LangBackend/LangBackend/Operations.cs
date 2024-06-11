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
                    // "ADD" => lbool + rbool,
                    // "SUB" => lbool - rbool,
                    // "MUL" => lbool * rbool,
                    // "DIV" => lbool / rbool,
                    // "MOD" => lbool % rbool,
                    // "FDIV" => lbool / rbool,
                    // "POW" => Math.Pow(lbool, rbool),
                    "BXOR" => lbool ^ rbool,
                    "BAND" => lbool & rbool,
                    "BOR" => lbool | rbool,
                    // "BRSHIFT" => lbool >> rbool,
                    // "BLSHIFT" => lbool << rbool,
                    // "LTE" => lbool <= rbool,
                    // "GTE" => lbool >= rbool,
                    // "LT" => lbool < rbool,
                    // "GT" => lbool > rbool,
                    "EQ" => lbool == rbool,
                    "NE" => lbool != rbool,
                    "EQ!" => lbool == rbool,
                    "NE!" => lbool != rbool,
                    //"IN" => lbool in rbool,
                    "AND" => lbool && rbool,
                    "OR" => lbool || rbool,
                    "XOR" => lbool ^ rbool,
                    "AND!" => (bool)(lbool & rbool),
                    "OR!" => (bool)(lbool | rbool),
                    // "CAST" => lbool as rbool,
                    //"COALESCE" => lbool ?? rbool,
                    // "IDEMPOTATE" => lbool ,
                    // "NEGATE" => -lbool,
                    // "NOT" => !lbool,
                    // "BINV" => ~lbool,
                    //"ALLOC" => lbool != rbool,
                    //"FREE" => lbool != rbool,
                    //"ADDR" => lbool != rbool,
                    //"VALOF" => lbool != rbool,

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
                    "ADD" => lint8 + rint8,
                    "SUB" => lint8 - rint8,
                    "MUL" => lint8 * rint8,
                    "DIV" => lint8 / rint8,
                    "MOD" => lint8 % rint8,
                    "FDIV" => lint8 / rint8,
                    "POW" => Math.Pow(lint8, rint8),
                    "BXOR" => lint8 ^ rint8,
                    "BAND" => lint8 & rint8,
                    "BOR" => lint8 | rint8,
                    "BRSHIFT" => lint8 >> rint8,
                    "BLSHIFT" => lint8 << rint8,
                    "LTE" => lint8 <= rint8,
                    "GTE" => lint8 >= rint8,
                    "LT" => lint8 < rint8,
                    "GT" => lint8 > rint8,
                    "EQ" => lint8 == rint8,
                    "NE" => lint8 != rint8,
                    "EQ!" => lint8 == rint8,
                    "NE!" => lint8 != rint8,

                    _ => throw new Exception($"Unknown arithmetic operation: {operation}")
                };
            }
            else if (rhs is Int16 rint16)
            {
                return operation switch
                {
                    "ADD" => lint8 + rint16,
                    "SUB" => lint8 - rint16,
                    "MUL" => lint8 * rint16,
                    "DIV" => lint8 / rint16,
                    "MOD" => lint8 % rint16,
                    "FDIV" => lint8 / rint16,
                    "POW" => Math.Pow(lint8, rint16),
                    "BXOR" => lint8 ^ rint16,
                    "BAND" => lint8 & rint16,
                    "BOR" => lint8 | rint16,
                    "BRSHIFT" => lint8 >> rint16,
                    "BLSHIFT" => lint8 << rint16,
                    "LTE" => lint8 <= rint16,
                    "GTE" => lint8 >= rint16,
                    "LT" => lint8 < rint16,
                    "GT" => lint8 > rint16,
                    "EQ" => lint8 == rint16,
                    "NE" => lint8 != rint16,
                    "EQ!" => false,
                    "NE!" => true,
                    
                    _ => throw new Exception($"Unknown arithmetic operation: {operation}")
                };
            }
            else if (rhs is Int32 rint32)
            {
                return operation switch
                {
                    "ADD" => lint8 + rint32,
                    "SUB" => lint8 - rint32,
                    "MUL" => lint8 * rint32,
                    "DIV" => lint8 / rint32,
                    "MOD" => lint8 % rint32,
                    "FDIV" => lint8 / rint32,
                    "POW" => Math.Pow(lint8, rint32),
                    "BXOR" => lint8 ^ rint32,
                    "BAND" => lint8 & rint32,
                    "BOR" => lint8 | rint32,
                    "BRSHIFT" => lint8 >> rint32,
                    "BLSHIFT" => lint8 << rint32,
                    "LTE" => lint8 <= rint32,
                    "GTE" => lint8 >= rint32,
                    "LT" => lint8 < rint32,
                    "GT" => lint8 > rint32,
                    "EQ" => lint8 == rint32,
                    "NE" => lint8 != rint32,
                    "EQ!" => false,
                    "NE!" => true,

                    _ => throw new Exception($"Unknown arithmetic operation: {operation}")
                };
            }
            else if (rhs is Int64 rint64)
            {
                return operation switch
                {
                    "ADD" => lint8 + rint64,
                    "SUB" => lint8 - rint64,
                    "MUL" => lint8 * rint64,
                    "DIV" => lint8 / rint64,
                    "MOD" => lint8 % rint64,
                    "FDIV" => lint8 / rint64,
                    "POW" => Math.Pow(lint8, rint64),
                    "BXOR" => lint8 ^ rint64,
                    "BAND" => lint8 & rint64,
                    "BOR" => lint8 | rint64,
                    // "BRSHIFT" => ((Int64)lint8) >> rint64,
                    // "BLSHIFT" => lint8 << rint64,
                    "LTE" => lint8 <= rint64,
                    "GTE" => lint8 >= rint64,
                    "LT" => lint8 < rint64,
                    "GT" => lint8 > rint64,
                    "EQ" => lint8 == rint64,
                    "NE" => lint8 != rint64,
                    "EQ!" => false,
                    "NE!" => true,

                    _ => throw new Exception($"Unknown arithmetic operation: {operation}")
                };
            }
            else if (rhs is BigInteger rintd)
            {
                return operation switch
                {
                    "ADD" => lint8 + rintd,
                    "SUB" => lint8 - rintd,
                    "MUL" => lint8 * rintd,
                    "DIV" => lint8 / rintd,
                    "MOD" => lint8 % rintd,
                    "FDIV" => lint8 / rintd,
                    // "POW" => Math.Pow(lint8, rintd),
                    "BXOR" => lint8 ^ rintd,
                    "BAND" => lint8 & rintd,
                    "BOR" => lint8 | rintd,
                    // "BRSHIFT" => lint8 >> rintd,
                    // "BLSHIFT" => lint8 << rintd,
                    "LTE" => lint8 <= rintd,
                    "GTE" => lint8 >= rintd,
                    "LT" => lint8 < rintd,
                    "GT" => lint8 > rintd,
                    "EQ" => lint8 == rintd,
                    "NE" => lint8 != rintd,
                    "EQ!" => false,
                    "NE!" => true,

                    _ => throw new Exception($"Unknown arithmetic operation: {operation}")
                };
            }
            else if (rhs is float rfloat32)
            {
                return operation switch
                {
                    "ADD" => lint8 + rfloat32,
                    "SUB" => lint8 - rfloat32,
                    "MUL" => lint8 * rfloat32,
                    "DIV" => lint8 / rfloat32,
                    "MOD" => lint8 % rfloat32,
                    "FDIV" => lint8 / rfloat32,
                    "POW" => Math.Pow(lint8, rfloat32),
                    "LTE" => lint8 <= rfloat32,
                    "GTE" => lint8 >= rfloat32,
                    "LT" => lint8 < rfloat32,
                    "GT" => lint8 > rfloat32,
                    "EQ" => lint8 == rfloat32,
                    "NE" => lint8 != rfloat32,
                    "EQ!" => false,
                    "NE!" => true,

                    _ => throw new Exception($"Unknown arithmetic operation: {operation}")
                };
            }
            else if (rhs is double rfloat64)
            {
                return operation switch
                {
                    "ADD" => lint8 + rfloat64,
                    "SUB" => lint8 - rfloat64,
                    "MUL" => lint8 * rfloat64,
                    "DIV" => lint8 / rfloat64,
                    "MOD" => lint8 % rfloat64,
                    "FDIV" => lint8 / rfloat64,
                    "POW" => Math.Pow(lint8, rfloat64),
                    "LTE" => lint8 <= rfloat64,
                    "GTE" => lint8 >= rfloat64,
                    "LT" => lint8 < rfloat64,
                    "GT" => lint8 > rfloat64,
                    "EQ" => lint8 == rfloat64,
                    "NE" => lint8 != rfloat64,
                    "EQ!" => false,
                    "NE!" => true,

                    _ => throw new Exception($"Unknown arithmetic operation: {operation}")
                };
            }
            else if (rhs is Complex rcomplex128)
            {
                return operation switch
                {
                    "ADD" => lint8 + rcomplex128,
                    "SUB" => lint8 - rcomplex128,
                    "MUL" => lint8 * rcomplex128,
                    "DIV" => lint8 / rcomplex128,
                    // "POW" => Math.Pow(lint8, rcomplex128),
                    "EQ" => lint8 == rcomplex128,
                    "NE" => lint8 != rcomplex128,
                    "EQ!" => false,
                    "NE!" => true,

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
                    "ADD" => lint16 + rint8,
                    "SUB" => lint16 - rint8,
                    "MUL" => lint16 * rint8,
                    "DIV" => lint16 / rint8,
                    "MOD" => lint16 % rint8,
                    "FDIV" => lint16 / rint8,
                    "POW" => Math.Pow(lint16, rint8),
                    "BXOR" => lint16 ^ rint8,
                    "BAND" => lint16 & rint8,
                    "BOR" => lint16 | rint8,
                    "BRSHIFT" => lint16 >> rint8,
                    "BLSHIFT" => lint16 << rint8,
                    "LTE" => lint16 <= rint8,
                    "GTE" => lint16 >= rint8,
                    "LT" => lint16 < rint8,
                    "GT" => lint16 > rint8,
                    "EQ" => lint16 == rint8,
                    "NE" => lint16 != rint8,
                    "EQ!" => false,
                    "NE!" => true,

                    _ => throw new Exception($"Unknown arithmetic operation: {operation}")
                };
            }
            else if (rhs is Int16 rint16)
            {
                return operation switch
                {
                    "ADD" => lint16 + rint16,
                    "SUB" => lint16 - rint16,
                    "MUL" => lint16 * rint16,
                    "DIV" => lint16 / rint16,
                    "MOD" => lint16 % rint16,
                    "FDIV" => lint16 / rint16,
                    "POW" => Math.Pow(lint16, rint16),
                    "BXOR" => lint16 ^ rint16,
                    "BAND" => lint16 & rint16,
                    "BOR" => lint16 | rint16,
                    "BRSHIFT" => lint16 >> rint16,
                    "BLSHIFT" => lint16 << rint16,
                    "LTE" => lint16 <= rint16,
                    "GTE" => lint16 >= rint16,
                    "LT" => lint16 < rint16,
                    "GT" => lint16 > rint16,
                    "EQ" => lint16 == rint16,
                    "NE" => lint16 != rint16,
                    "EQ!" => lint16 == rint16,
                    "NE!" => lint16 != rint16,

                    _ => throw new Exception($"Unknown arithmetic operation: {operation}")
                };
            }
            else if (rhs is Int32 rint32)
            {
                return operation switch
                {
                    "ADD" => lint16 + rint32,
                    "SUB" => lint16 - rint32,
                    "MUL" => lint16 * rint32,
                    "DIV" => lint16 / rint32,
                    "MOD" => lint16 % rint32,
                    "FDIV" => lint16 / rint32,
                    "POW" => Math.Pow(lint16, rint32),
                    "BXOR" => lint16 ^ rint32,
                    "BAND" => lint16 & rint32,
                    "BOR" => lint16 | rint32,
                    "BRSHIFT" => lint16 >> rint32,
                    "BLSHIFT" => lint16 << rint32,
                    "LTE" => lint16 <= rint32,
                    "GTE" => lint16 >= rint32,
                    "LT" => lint16 < rint32,
                    "GT" => lint16 > rint32,
                    "EQ" => lint16 == rint32,
                    "NE" => lint16 != rint32,
                    "EQ!" => false,
                    "NE!" => true,

                    _ => throw new Exception($"Unknown arithmetic operation: {operation}")
                };
            }
            else if (rhs is Int64 rint64)
            {
                return operation switch
                {
                    "ADD" => lint16 + rint64,
                    "SUB" => lint16 - rint64,
                    "MUL" => lint16 * rint64,
                    "DIV" => lint16 / rint64,
                    "MOD" => lint16 % rint64,
                    "FDIV" => lint16 / rint64,
                    "POW" => Math.Pow(lint16, rint64),
                    "BXOR" => lint16 ^ rint64,
                    "BAND" => lint16 & rint64,
                    "BOR" => lint16 | rint64,
                    "LTE" => lint16 <= rint64,
                    "GTE" => lint16 >= rint64,
                    "LT" => lint16 < rint64,
                    "GT" => lint16 > rint64,
                    "EQ" => lint16 == rint64,
                    "NE" => lint16 != rint64,
                    "EQ!" => false,
                    "NE!" => true,

                    _ => throw new Exception($"Unknown arithmetic operation: {operation}")
                };
            }
            else if (rhs is BigInteger rintd)
            {
                return operation switch
                {
                    "ADD" => lint16 + rintd,
                    "SUB" => lint16 - rintd,
                    "MUL" => lint16 * rintd,
                    "DIV" => lint16 / rintd,
                    "MOD" => lint16 % rintd,
                    "FDIV" => lint16 / rintd,
                    "BXOR" => lint16 ^ rintd,
                    "BAND" => lint16 & rintd,
                    "BOR" => lint16 | rintd,
                    "LTE" => lint16 <= rintd,
                    "GTE" => lint16 >= rintd,
                    "LT" => lint16 < rintd,
                    "GT" => lint16 > rintd,
                    "EQ" => lint16 == rintd,
                    "NE" => lint16 != rintd,
                    "EQ!" => false,
                    "NE!" => true,

                    _ => throw new Exception($"Unknown arithmetic operation: {operation}")
                };
            }
            else if (rhs is float rfloat32)
            {
                return operation switch
                {
                    "ADD" => lint16 + rfloat32,
                    "SUB" => lint16 - rfloat32,
                    "MUL" => lint16 * rfloat32,
                    "DIV" => lint16 / rfloat32,
                    "MOD" => lint16 % rfloat32,
                    "FDIV" => lint16 / rfloat32,
                    "POW" => Math.Pow(lint16, rfloat32),
                    "LTE" => lint16 <= rfloat32,
                    "GTE" => lint16 >= rfloat32,
                    "LT" => lint16 < rfloat32,
                    "GT" => lint16 > rfloat32,
                    "EQ" => lint16 == rfloat32,
                    "NE" => lint16 != rfloat32,
                    "EQ!" => false,
                    "NE!" => true,

                    _ => throw new Exception($"Unknown arithmetic operation: {operation}")
                };
            }
            else if (rhs is double rfloat64)
            {
                return operation switch
                {
                    "ADD" => lint16 + rfloat64,
                    "SUB" => lint16 - rfloat64,
                    "MUL" => lint16 * rfloat64,
                    "DIV" => lint16 / rfloat64,
                    "MOD" => lint16 % rfloat64,
                    "FDIV" => lint16 / rfloat64,
                    "POW" => Math.Pow(lint16, rfloat64),
                    "LTE" => lint16 <= rfloat64,
                    "GTE" => lint16 >= rfloat64,
                    "LT" => lint16 < rfloat64,
                    "GT" => lint16 > rfloat64,
                    "EQ" => lint16 == rfloat64,
                    "NE" => lint16 != rfloat64,
                    "EQ!" => false,
                    "NE!" => true,

                    _ => throw new Exception($"Unknown arithmetic operation: {operation}")
                };
            }
            else if (rhs is Complex rcomplex128)
            {
                return operation switch
                {
                    "ADD" => lint16 + rcomplex128,
                    "SUB" => lint16 - rcomplex128,
                    "MUL" => lint16 * rcomplex128,
                    "DIV" => lint16 / rcomplex128,
                    "FDIV" => lint16 / rcomplex128,
                    //"POW" => Math.Pow(lint16, rcomplex128),
                    "EQ" => lint16 == rcomplex128,
                    "NE" => lint16 != rcomplex128,
                    "EQ!" => false,
                    "NE!" => true,

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
                    "ADD" => lint32 + rint8,
                    "SUB" => lint32 - rint8,
                    "MUL" => lint32 * rint8,
                    "DIV" => lint32 / rint8,
                    "MOD" => lint32 % rint8,
                    "FDIV" => lint32 / rint8,
                    "POW" => Math.Pow(lint32, rint8),
                    "BXOR" => lint32 ^ rint8,
                    "BAND" => lint32 & rint8,
                    "BOR" => lint32 | rint8,
                    "BRSHIFT" => lint32 >> rint8,
                    "BLSHIFT" => lint32 << rint8,
                    "LTE" => lint32 <= rint8,
                    "GTE" => lint32 >= rint8,
                    "LT" => lint32 < rint8,
                    "GT" => lint32 > rint8,
                    "EQ" => lint32 == rint8,
                    "NE" => lint32 != rint8,
                    "EQ!" => false,
                    "NE!" => true,

                    _ => throw new Exception($"Unknown arithmetic operation: {operation}")
                };
            }
            else if (rhs is Int16 rint16)
            {
                return operation switch
                {
                    "ADD" => lint32 + rint16,
                    "SUB" => lint32 - rint16,
                    "MUL" => lint32 * rint16,
                    "DIV" => lint32 / rint16,
                    "MOD" => lint32 % rint16,
                    "FDIV" => lint32 / rint16,
                    "POW" => Math.Pow(lint32, rint16),
                    "BXOR" => lint32 ^ rint16,
                    "BAND" => lint32 & rint16,
                    "BOR" => lint32 | rint16,
                    "BRSHIFT" => lint32 >> rint16,
                    "BLSHIFT" => lint32 << rint16,
                    "LTE" => lint32 <= rint16,
                    "GTE" => lint32 >= rint16,
                    "LT" => lint32 < rint16,
                    "GT" => lint32 > rint16,
                    "EQ" => lint32 == rint16,
                    "NE" => lint32 != rint16,
                    "EQ!" => false,
                    "NE!" => true,

                    _ => throw new Exception($"Unknown arithmetic operation: {operation}")
                };
            }
            else if (rhs is Int32 rint32)
            {
                return operation switch
                {
                    "ADD" => lint32 + rint32,
                    "SUB" => lint32 - rint32,
                    "MUL" => lint32 * rint32,
                    "DIV" => lint32 / rint32,
                    "MOD" => lint32 % rint32,
                    "FDIV" => lint32 / rint32,
                    "POW" => Math.Pow(lint32, rint32),
                    "BXOR" => lint32 ^ rint32,
                    "BAND" => lint32 & rint32,
                    "BOR" => lint32 | rint32,
                    "BRSHIFT" => lint32 >> rint32,
                    "BLSHIFT" => lint32 << rint32,
                    "LTE" => lint32 <= rint32,
                    "GTE" => lint32 >= rint32,
                    "LT" => lint32 < rint32,
                    "GT" => lint32 > rint32,
                    "EQ" => lint32 == rint32,
                    "NE" => lint32 != rint32,
                    "EQ!" => lint32 == rint32,
                    "NE!" => lint32 != rint32,

                    _ => throw new Exception($"Unknown arithmetic operation: {operation}")
                };
            }
            else if (rhs is Int64 rint64)
            {
                return operation switch
                {
                    "ADD" => lint32 + rint64,
                    "SUB" => lint32 - rint64,
                    "MUL" => lint32 * rint64,
                    "DIV" => lint32 / rint64,
                    "MOD" => lint32 % rint64,
                    "FDIV" => lint32 / rint64,
                    "POW" => Math.Pow(lint32, rint64),
                    "BXOR" => lint32 ^ rint64,
                    "BAND" => lint32 & rint64,
                    "BOR" => lint32 | rint64,
                    "LTE" => lint32 <= rint64,
                    "GTE" => lint32 >= rint64,
                    "LT" => lint32 < rint64,
                    "GT" => lint32 > rint64,
                    "EQ" => lint32 == rint64,
                    "NE" => lint32 != rint64,
                    "EQ!" => false,
                    "NE!" => true,

                    _ => throw new Exception($"Unknown arithmetic operation: {operation}")
                };
            }
            else if (rhs is BigInteger rintd)
            {
                return operation switch
                {
                    "ADD" => lint32 + rintd,
                    "SUB" => lint32 - rintd,
                    "MUL" => lint32 * rintd,
                    "DIV" => lint32 / rintd,
                    "MOD" => lint32 % rintd,
                    "FDIV" => lint32 / rintd,
                    "BXOR" => lint32 ^ rintd,
                    "BAND" => lint32 & rintd,
                    "BOR" => lint32 | rintd,
                    "LTE" => lint32 <= rintd,
                    "GTE" => lint32 >= rintd,
                    "LT" => lint32 < rintd,
                    "GT" => lint32 > rintd,
                    "EQ" => lint32 == rintd,
                    "NE" => lint32 != rintd,
                    "EQ!" => false,
                    "NE!" => true,

                    _ => throw new Exception($"Unknown arithmetic operation: {operation}")
                };
            }
            else if (rhs is float rfloat32)
            {
                return operation switch
                {
                    "ADD" => lint32 + rfloat32,
                    "SUB" => lint32 - rfloat32,
                    "MUL" => lint32 * rfloat32,
                    "DIV" => lint32 / rfloat32,
                    "MOD" => lint32 % rfloat32,
                    "FDIV" => lint32 / rfloat32,
                    "POW" => Math.Pow(lint32, rfloat32),
                    "LTE" => lint32 <= rfloat32,
                    "GTE" => lint32 >= rfloat32,
                    "LT" => lint32 < rfloat32,
                    "GT" => lint32 > rfloat32,
                    "EQ" => lint32 == rfloat32,
                    "NE" => lint32 != rfloat32,
                    "EQ!" => false,
                    "NE!" => true,

                    _ => throw new Exception($"Unknown arithmetic operation: {operation}")
                };
            }
            else if (rhs is double rfloat64)
            {
                return operation switch
                {
                    "ADD" => lint32 + rfloat64,
                    "SUB" => lint32 - rfloat64,
                    "MUL" => lint32 * rfloat64,
                    "DIV" => lint32 / rfloat64,
                    "MOD" => lint32 % rfloat64,
                    "FDIV" => lint32 / rfloat64,
                    "POW" => Math.Pow(lint32, rfloat64),
                    "LTE" => lint32 <= rfloat64,
                    "GTE" => lint32 >= rfloat64,
                    "LT" => lint32 < rfloat64,
                    "GT" => lint32 > rfloat64,
                    "EQ" => lint32 == rfloat64,
                    "NE" => lint32 != rfloat64,
                    "EQ!" => false,
                    "NE!" => true,

                    _ => throw new Exception($"Unknown arithmetic operation: {operation}")
                };
            }
            else if (rhs is Complex rcomplex128)
            {
                return operation switch
                {
                    "ADD" => lint32 + rcomplex128,
                    "SUB" => lint32 - rcomplex128,
                    "MUL" => lint32 * rcomplex128,
                    "DIV" => lint32 / rcomplex128,
                    "FDIV" => lint32 / rcomplex128,
                    //"POW" => Math.Pow(lint32, rcomplex128),
                    "EQ" => lint32 == rcomplex128,
                    "NE" => lint32 != rcomplex128,
                    "EQ!" => false,
                    "NE!" => true,

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
                    "ADD" => lint64 + rint8,
                    "SUB" => lint64 - rint8,
                    "MUL" => lint64 * rint8,
                    "DIV" => lint64 / rint8,
                    "MOD" => lint64 % rint8,
                    "FDIV" => lint64 / rint8,
                    "POW" => Math.Pow(lint64, rint8),
                    "BXOR" => lint64 ^ rint8,
                    "BAND" => lint64 & rint8,
                    "BOR" => lint64 | rint8,
                    "BRSHIFT" => lint64 >> rint8,
                    "BLSHIFT" => lint64 << rint8,
                    "LTE" => lint64 <= rint8,
                    "GTE" => lint64 >= rint8,
                    "LT" => lint64 < rint8,
                    "GT" => lint64 > rint8,
                    "EQ" => lint64 == rint8,
                    "NE" => lint64 != rint8,
                    "EQ!" => false,
                    "NE!" => true,

                    _ => throw new Exception($"Unknown arithmetic operation: {operation}")
                };
            }
            else if (rhs is Int16 rint16)
            {
                return operation switch
                {
                    "ADD" => lint64 + rint16,
                    "SUB" => lint64 - rint16,
                    "MUL" => lint64 * rint16,
                    "DIV" => lint64 / rint16,
                    "MOD" => lint64 % rint16,
                    "FDIV" => lint64 / rint16,
                    "POW" => Math.Pow(lint64, rint16),
                    "BXOR" => lint64 ^ rint16,
                    "BAND" => lint64 & rint16,
                    "BOR" => lint64 | rint16,
                    "BRSHIFT" => lint64 >> rint16,
                    "BLSHIFT" => lint64 << rint16,
                    "LTE" => lint64 <= rint16,
                    "GTE" => lint64 >= rint16,
                    "LT" => lint64 < rint16,
                    "GT" => lint64 > rint16,
                    "EQ" => lint64 == rint16,
                    "NE" => lint64 != rint16,
                    "EQ!" => false,
                    "NE!" => true,

                    _ => throw new Exception($"Unknown arithmetic operation: {operation}")
                };
            }
            else if (rhs is Int32 rint32)
            {
                return operation switch
                {
                    "ADD" => lint64 + rint32,
                    "SUB" => lint64 - rint32,
                    "MUL" => lint64 * rint32,
                    "DIV" => lint64 / rint32,
                    "MOD" => lint64 % rint32,
                    "FDIV" => lint64 / rint32,
                    "POW" => Math.Pow(lint64, rint32),
                    "BXOR" => lint64 ^ rint32,
                    "BAND" => lint64 & rint32,
                    "BOR" => lint64 | rint32,
                    "BRSHIFT" => lint64 >> rint32,
                    "BLSHIFT" => lint64 << rint32,
                    "LTE" => lint64 <= rint32,
                    "GTE" => lint64 >= rint32,
                    "LT" => lint64 < rint32,
                    "GT" => lint64 > rint32,
                    "EQ" => lint64 == rint32,
                    "NE" => lint64 != rint32,
                    "EQ!" => false,
                    "NE!" => true,

                    _ => throw new Exception($"Unknown arithmetic operation: {operation}")
                };
            }
            else if (rhs is Int64 rint64)
            {
                return operation switch
                {
                    "ADD" => lint64 + rint64,
                    "SUB" => lint64 - rint64,
                    "MUL" => lint64 * rint64,
                    "DIV" => lint64 / rint64,
                    "MOD" => lint64 % rint64,
                    "FDIV" => lint64 / rint64,
                    "POW" => Math.Pow(lint64, rint64),
                    "BXOR" => lint64 ^ rint64,
                    "BAND" => lint64 & rint64,
                    "BOR" => lint64 | rint64,
                    "LTE" => lint64 <= rint64,
                    "GTE" => lint64 >= rint64,
                    "LT" => lint64 < rint64,
                    "GT" => lint64 > rint64,
                    "EQ" => lint64 == rint64,
                    "NE" => lint64 != rint64,
                    "EQ!" => lint64 == rint64,
                    "NE!" => lint64 != rint64,

                    _ => throw new Exception($"Unknown arithmetic operation: {operation}")
                };
            }
            else if (rhs is BigInteger rintd)
            {
                return operation switch
                {
                    "ADD" => lint64 + rintd,
                    "SUB" => lint64 - rintd,
                    "MUL" => lint64 * rintd,
                    "DIV" => lint64 / rintd,
                    "MOD" => lint64 % rintd,
                    "FDIV" => lint64 / rintd,
                    "BXOR" => lint64 ^ rintd,
                    "BAND" => lint64 & rintd,
                    "BOR" => lint64 | rintd,
                    "LTE" => lint64 <= rintd,
                    "GTE" => lint64 >= rintd,
                    "LT" => lint64 < rintd,
                    "GT" => lint64 > rintd,
                    "EQ" => lint64 == rintd,
                    "NE" => lint64 != rintd,
                    "EQ!" => false,
                    "NE!" => true,

                    _ => throw new Exception($"Unknown arithmetic operation: {operation}")
                };
            }
            else if (rhs is float rfloat32)
            {
                return operation switch
                {
                    "ADD" => lint64 + rfloat32,
                    "SUB" => lint64 - rfloat32,
                    "MUL" => lint64 * rfloat32,
                    "DIV" => lint64 / rfloat32,
                    "MOD" => lint64 % rfloat32,
                    "FDIV" => lint64 / rfloat32,
                    "POW" => Math.Pow(lint64, rfloat32),
                    "LTE" => lint64 <= rfloat32,
                    "GTE" => lint64 >= rfloat32,
                    "LT" => lint64 < rfloat32,
                    "GT" => lint64 > rfloat32,
                    "EQ" => lint64 == rfloat32,
                    "NE" => lint64 != rfloat32,
                    "EQ!" => false,
                    "NE!" => true,

                    _ => throw new Exception($"Unknown arithmetic operation: {operation}")
                };
            }
            else if (rhs is double rfloat64)
            {
                return operation switch
                {
                    "ADD" => lint64 + rfloat64,
                    "SUB" => lint64 - rfloat64,
                    "MUL" => lint64 * rfloat64,
                    "DIV" => lint64 / rfloat64,
                    "MOD" => lint64 % rfloat64,
                    "FDIV" => lint64 / rfloat64,
                    "POW" => Math.Pow(lint64, rfloat64),
                    "LTE" => lint64 <= rfloat64,
                    "GTE" => lint64 >= rfloat64,
                    "LT" => lint64 < rfloat64,
                    "GT" => lint64 > rfloat64,
                    "EQ" => lint64 == rfloat64,
                    "NE" => lint64 != rfloat64,
                    "EQ!" => false,
                    "NE!" => true,

                    _ => throw new Exception($"Unknown arithmetic operation: {operation}")
                };
            }
            else if (rhs is Complex rcomplex128)
            {
                return operation switch
                {
                    "ADD" => lint64 + rcomplex128,
                    "SUB" => lint64 - rcomplex128,
                    "MUL" => lint64 * rcomplex128,
                    "DIV" => lint64 / rcomplex128,
                    "FDIV" => lint64 / rcomplex128,
                    //"POW" => Math.Pow(lint64, rcomplex128),
                    "EQ" => lint64 == rcomplex128,
                    "NE" => lint64 != rcomplex128,
                    "EQ!" => false,
                    "NE!" => true,

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
                    "ADD" => lintd + rint8,
                    "SUB" => lintd - rint8,
                    "MUL" => lintd * rint8,
                    "DIV" => lintd / rint8,
                    "MOD" => lintd % rint8,
                    "FDIV" => lintd / rint8,
                    "BXOR" => lintd ^ rint8,
                    "BAND" => lintd & rint8,
                    "BOR" => lintd | rint8,
                    "BRSHIFT" => lintd >> rint8,
                    "BLSHIFT" => lintd << rint8,
                    "LTE" => lintd <= rint8,
                    "GTE" => lintd >= rint8,
                    "LT" => lintd < rint8,
                    "GT" => lintd > rint8,
                    "EQ" => lintd == rint8,
                    "NE" => lintd != rint8,
                    "EQ!" => false,
                    "NE!" => true,

                    _ => throw new Exception($"Unknown arithmetic operation: {operation}")
                };
            }
            else if (rhs is Int16 rint16)
            {
                return operation switch
                {
                    "ADD" => lintd + rint16,
                    "SUB" => lintd - rint16,
                    "MUL" => lintd * rint16,
                    "DIV" => lintd / rint16,
                    "MOD" => lintd % rint16,
                    "FDIV" => lintd / rint16,
                    "BXOR" => lintd ^ rint16,
                    "BAND" => lintd & rint16,
                    "BOR" => lintd | rint16,
                    "BRSHIFT" => lintd >> rint16,
                    "BLSHIFT" => lintd << rint16,
                    "LTE" => lintd <= rint16,
                    "GTE" => lintd >= rint16,
                    "LT" => lintd < rint16,
                    "GT" => lintd > rint16,
                    "EQ" => lintd == rint16,
                    "NE" => lintd != rint16,
                    "EQ!" => false,
                    "NE!" => true,

                    _ => throw new Exception($"Unknown arithmetic operation: {operation}")
                };
            }
            else if (rhs is Int32 rint32)
            {
                return operation switch
                {
                    "ADD" => lintd + rint32,
                    "SUB" => lintd - rint32,
                    "MUL" => lintd * rint32,
                    "DIV" => lintd / rint32,
                    "MOD" => lintd % rint32,
                    "FDIV" => lintd / rint32,
                    "BXOR" => lintd ^ rint32,
                    "BAND" => lintd & rint32,
                    "BOR" => lintd | rint32,
                    "BRSHIFT" => lintd >> rint32,
                    "BLSHIFT" => lintd << rint32,
                    "LTE" => lintd <= rint32,
                    "GTE" => lintd >= rint32,
                    "LT" => lintd < rint32,
                    "GT" => lintd > rint32,
                    "EQ" => lintd == rint32,
                    "NE" => lintd != rint32,
                    "EQ!" => false,
                    "NE!" => true,

                    _ => throw new Exception($"Unknown arithmetic operation: {operation}")
                };
            }
            else if (rhs is Int64 rint64)
            {
                return operation switch
                {
                    "ADD" => lintd + rint64,
                    "SUB" => lintd - rint64,
                    "MUL" => lintd * rint64,
                    "DIV" => lintd / rint64,
                    "MOD" => lintd % rint64,
                    "FDIV" => lintd / rint64,
                    "BXOR" => lintd ^ rint64,
                    "BAND" => lintd & rint64,
                    "BOR" => lintd | rint64,
                    "LTE" => lintd <= rint64,
                    "GTE" => lintd >= rint64,
                    "LT" => lintd < rint64,
                    "GT" => lintd > rint64,
                    "EQ" => lintd == rint64,
                    "NE" => lintd != rint64,
                    "EQ!" => false,
                    "NE!" => true,

                    _ => throw new Exception($"Unknown arithmetic operation: {operation}")
                };
            }
            else if (rhs is BigInteger rintd)
            {
                return operation switch
                {
                    "ADD" => lintd + rintd,
                    "SUB" => lintd - rintd,
                    "MUL" => lintd * rintd,
                    "DIV" => lintd / rintd,
                    "MOD" => lintd % rintd,
                    "FDIV" => lintd / rintd,
                    "BXOR" => lintd ^ rintd,
                    "BAND" => lintd & rintd,
                    "BOR" => lintd | rintd,
                    "LTE" => lintd <= rintd,
                    "GTE" => lintd >= rintd,
                    "LT" => lintd < rintd,
                    "GT" => lintd > rintd,
                    "EQ" => lintd == rintd,
                    "NE" => lintd != rintd,
                    "EQ!" => lintd == rintd,
                    "NE!" => lintd != rintd,

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
                    "ADD" => lfloat32 + rint8,
                    "SUB" => lfloat32 - rint8,
                    "MUL" => lfloat32 * rint8,
                    "DIV" => lfloat32 / rint8,
                    "MOD" => lfloat32 % rint8,
                    "FDIV" => lfloat32 / rint8,
                    "POW" => Math.Pow(lfloat32, rint8),
                    "LTE" => lfloat32 <= rint8,
                    "GTE" => lfloat32 >= rint8,
                    "LT" => lfloat32 < rint8,
                    "GT" => lfloat32 > rint8,
                    "EQ" => lfloat32 == rint8,
                    "NE" => lfloat32 != rint8,
                    "EQ!" => false,
                    "NE!" => true,

                    _ => throw new Exception($"Unknown arithmetic operation: {operation}")
                };
            }
            else if (rhs is Int16 rint16)
            {
                return operation switch
                {
                    "ADD" => lfloat32 + rint16,
                    "SUB" => lfloat32 - rint16,
                    "MUL" => lfloat32 * rint16,
                    "DIV" => lfloat32 / rint16,
                    "MOD" => lfloat32 % rint16,
                    "FDIV" => lfloat32 / rint16,
                    "POW" => Math.Pow(lfloat32, rint16),
                    "LTE" => lfloat32 <= rint16,
                    "GTE" => lfloat32 >= rint16,
                    "LT" => lfloat32 < rint16,
                    "GT" => lfloat32 > rint16,
                    "EQ" => lfloat32 == rint16,
                    "NE" => lfloat32 != rint16,
                    "EQ!" => false,
                    "NE!" => true,

                    _ => throw new Exception($"Unknown arithmetic operation: {operation}")
                };
            }
            else if (rhs is Int32 rint32)
            {
                return operation switch
                {
                    "ADD" => lfloat32 + rint32,
                    "SUB" => lfloat32 - rint32,
                    "MUL" => lfloat32 * rint32,
                    "DIV" => lfloat32 / rint32,
                    "MOD" => lfloat32 % rint32,
                    "FDIV" => lfloat32 / rint32,
                    "POW" => Math.Pow(lfloat32, rint32),
                    "LTE" => lfloat32 <= rint32,
                    "GTE" => lfloat32 >= rint32,
                    "LT" => lfloat32 < rint32,
                    "GT" => lfloat32 > rint32,
                    "EQ" => lfloat32 == rint32,
                    "NE" => lfloat32 != rint32,
                    "EQ!" => false,
                    "NE!" => true,

                    _ => throw new Exception($"Unknown arithmetic operation: {operation}")
                };
            }
            else if (rhs is Int64 rint64)
            {
                return operation switch
                {
                    "ADD" => lfloat32 + rint64,
                    "SUB" => lfloat32 - rint64,
                    "MUL" => lfloat32 * rint64,
                    "DIV" => lfloat32 / rint64,
                    "MOD" => lfloat32 % rint64,
                    "FDIV" => lfloat32 / rint64,
                    "POW" => Math.Pow(lfloat32, rint64),
                    "LTE" => lfloat32 <= rint64,
                    "GTE" => lfloat32 >= rint64,
                    "LT" => lfloat32 < rint64,
                    "GT" => lfloat32 > rint64,
                    "EQ" => lfloat32 == rint64,
                    "NE" => lfloat32 != rint64,
                    "EQ!" => false,
                    "NE!" => true,

                    _ => throw new Exception($"Unknown arithmetic operation: {operation}")
                };
            }
            else if (rhs is float rfloat32)
            {
                return operation switch
                {
                    "ADD" => lfloat32 + rfloat32,
                    "SUB" => lfloat32 - rfloat32,
                    "MUL" => lfloat32 * rfloat32,
                    "DIV" => lfloat32 / rfloat32,
                    "MOD" => lfloat32 % rfloat32,
                    "FDIV" => lfloat32 / rfloat32,
                    "POW" => Math.Pow(lfloat32, rfloat32),
                    "LTE" => lfloat32 <= rfloat32,
                    "GTE" => lfloat32 >= rfloat32,
                    "LT" => lfloat32 < rfloat32,
                    "GT" => lfloat32 > rfloat32,
                    "EQ" => lfloat32 == rfloat32,
                    "NE" => lfloat32 != rfloat32,
                    "EQ!" => lfloat32 == rfloat32,
                    "NE!" => lfloat32 != rfloat32,

                    _ => throw new Exception($"Unknown arithmetic operation: {operation}")
                };
            }
            else if (rhs is double rfloat64)
            {
                return operation switch
                {
                    "ADD" => lfloat32 + rfloat64,
                    "SUB" => lfloat32 - rfloat64,
                    "MUL" => lfloat32 * rfloat64,
                    "DIV" => lfloat32 / rfloat64,
                    "MOD" => lfloat32 % rfloat64,
                    "FDIV" => lfloat32 / rfloat64,
                    "POW" => Math.Pow(lfloat32, rfloat64),
                    "LTE" => lfloat32 <= rfloat64,
                    "GTE" => lfloat32 >= rfloat64,
                    "LT" => lfloat32 < rfloat64,
                    "GT" => lfloat32 > rfloat64,
                    "EQ" => lfloat32 == rfloat64,
                    "NE" => lfloat32 != rfloat64,
                    "EQ!" => false,
                    "NE!" => true,

                    _ => throw new Exception($"Unknown arithmetic operation: {operation}")
                };
            }
            else if (rhs is Complex rcomplex128)
            {
                return operation switch
                {
                    "ADD" => lfloat32 + rcomplex128,
                    "SUB" => lfloat32 - rcomplex128,
                    "MUL" => lfloat32 * rcomplex128,
                    "DIV" => lfloat32 / rcomplex128,
                    "FDIV" => lfloat32 / rcomplex128,
                    //"POW" => Math.Pow(lfloat32, rcomplex128),
                    "EQ" => lfloat32 == rcomplex128,
                    "NE" => lfloat32 != rcomplex128,
                    "EQ!" => false,
                    "NE!" => true,

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
                    "ADD" => lfloat64 + rint8,
                    "SUB" => lfloat64 - rint8,
                    "MUL" => lfloat64 * rint8,
                    "DIV" => lfloat64 / rint8,
                    "MOD" => lfloat64 % rint8,
                    "FDIV" => lfloat64 / rint8,
                    "POW" => Math.Pow(lfloat64, rint8),
                    "LTE" => lfloat64 <= rint8,
                    "GTE" => lfloat64 >= rint8,
                    "LT" => lfloat64 < rint8,
                    "GT" => lfloat64 > rint8,
                    "EQ" => lfloat64 == rint8,
                    "NE" => lfloat64 != rint8,
                    "EQ!" => false,
                    "NE!" => true,

                    _ => throw new Exception($"Unknown arithmetic operation: {operation}")
                };
            }
            else if (rhs is Int16 rint16)
            {
                return operation switch
                {
                    "ADD" => lfloat64 + rint16,
                    "SUB" => lfloat64 - rint16,
                    "MUL" => lfloat64 * rint16,
                    "DIV" => lfloat64 / rint16,
                    "MOD" => lfloat64 % rint16,
                    "FDIV" => lfloat64 / rint16,
                    "POW" => Math.Pow(lfloat64, rint16),
                    "LTE" => lfloat64 <= rint16,
                    "GTE" => lfloat64 >= rint16,
                    "LT" => lfloat64 < rint16,
                    "GT" => lfloat64 > rint16,
                    "EQ" => lfloat64 == rint16,
                    "NE" => lfloat64 != rint16,
                    "EQ!" => false,
                    "NE!" => true,

                    _ => throw new Exception($"Unknown arithmetic operation: {operation}")
                };
            }
            else if (rhs is Int32 rint32)
            {
                return operation switch
                {
                    "ADD" => lfloat64 + rint32,
                    "SUB" => lfloat64 - rint32,
                    "MUL" => lfloat64 * rint32,
                    "DIV" => lfloat64 / rint32,
                    "MOD" => lfloat64 % rint32,
                    "FDIV" => lfloat64 / rint32,
                    "POW" => Math.Pow(lfloat64, rint32),
                    "LTE" => lfloat64 <= rint32,
                    "GTE" => lfloat64 >= rint32,
                    "LT" => lfloat64 < rint32,
                    "GT" => lfloat64 > rint32,
                    "EQ" => lfloat64 == rint32,
                    "NE" => lfloat64 != rint32,
                    "EQ!" => false,
                    "NE!" => true,

                    _ => throw new Exception($"Unknown arithmetic operation: {operation}")
                };
            }
            else if (rhs is Int64 rint64)
            {
                return operation switch
                {
                    "ADD" => lfloat64 + rint64,
                    "SUB" => lfloat64 - rint64,
                    "MUL" => lfloat64 * rint64,
                    "DIV" => lfloat64 / rint64,
                    "MOD" => lfloat64 % rint64,
                    "FDIV" => lfloat64 / rint64,
                    "POW" => Math.Pow(lfloat64, rint64),
                    "LTE" => lfloat64 <= rint64,
                    "GTE" => lfloat64 >= rint64,
                    "LT" => lfloat64 < rint64,
                    "GT" => lfloat64 > rint64,
                    "EQ" => lfloat64 == rint64,
                    "NE" => lfloat64 != rint64,
                    "EQ!" => false,
                    "NE!" => true,

                    _ => throw new Exception($"Unknown arithmetic operation: {operation}")
                };
            }
            else if (rhs is float rfloat32)
            {
                return operation switch
                {
                    "ADD" => lfloat64 + rfloat32,
                    "SUB" => lfloat64 - rfloat32,
                    "MUL" => lfloat64 * rfloat32,
                    "DIV" => lfloat64 / rfloat32,
                    "MOD" => lfloat64 % rfloat32,
                    "FDIV" => lfloat64 / rfloat32,
                    "POW" => Math.Pow(lfloat64, rfloat32),
                    "LTE" => lfloat64 <= rfloat32,
                    "GTE" => lfloat64 >= rfloat32,
                    "LT" => lfloat64 < rfloat32,
                    "GT" => lfloat64 > rfloat32,
                    "EQ" => lfloat64 == rfloat32,
                    "NE" => lfloat64 != rfloat32,
                    "EQ!" => false,
                    "NE!" => true,

                    _ => throw new Exception($"Unknown arithmetic operation: {operation}")
                };
            }
            else if (rhs is double rfloat64)
            {
                return operation switch
                {
                    "ADD" => lfloat64 + rfloat64,
                    "SUB" => lfloat64 - rfloat64,
                    "MUL" => lfloat64 * rfloat64,
                    "DIV" => lfloat64 / rfloat64,
                    "MOD" => lfloat64 % rfloat64,
                    "FDIV" => lfloat64 / rfloat64,
                    "POW" => Math.Pow(lfloat64, rfloat64),
                    "LTE" => lfloat64 <= rfloat64,
                    "GTE" => lfloat64 >= rfloat64,
                    "LT" => lfloat64 < rfloat64,
                    "GT" => lfloat64 > rfloat64,
                    "EQ" => lfloat64 == rfloat64,
                    "NE" => lfloat64 != rfloat64,
                    "EQ!" => lfloat64 == rfloat64,
                    "NE!" => lfloat64 != rfloat64,
                    
                    _ => throw new Exception($"Unknown arithmetic operation: {operation}")
                };
            }
            else if (rhs is Complex rcomplex128)
            {
                return operation switch
                {
                    "ADD" => lfloat64 + rcomplex128,
                    "SUB" => lfloat64 - rcomplex128,
                    "MUL" => lfloat64 * rcomplex128,
                    "DIV" => lfloat64 / rcomplex128,
                    "FDIV" => lfloat64 / rcomplex128,
                    //"POW" => Math.Pow(lfloat64, rcomplex128),
                    "EQ" => lfloat64 == rcomplex128,
                    "NE" => lfloat64 != rcomplex128,
                    "EQ!" => false,
                    "NE!" => true,

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
                    "ADD" => lcomplex128 + rint8,
                    "SUB" => lcomplex128 - rint8,
                    "MUL" => lcomplex128 * rint8,
                    "DIV" => lcomplex128 / rint8,
                    "FDIV" => lcomplex128 / rint8,
                    "EQ" => lcomplex128 == rint8,
                    "NE" => lcomplex128 != rint8,
                    "EQ!" => false,
                    "NE!" => true,

                    _ => throw new Exception($"Unknown arithmetic operation: {operation}")
                };
            }
            else if (rhs is Int16 rint16)
            {
                return operation switch
                {
                    "ADD" => lcomplex128 + rint16,
                    "SUB" => lcomplex128 - rint16,
                    "MUL" => lcomplex128 * rint16,
                    "DIV" => lcomplex128 / rint16,
                    "FDIV" => lcomplex128 / rint16,
                    "EQ" => lcomplex128 == rint16,
                    "NE" => lcomplex128 != rint16,
                    "EQ!" => false,
                    "NE!" => true,

                    _ => throw new Exception($"Unknown arithmetic operation: {operation}")
                };
            }
            else if (rhs is Int32 rint32)
            {
                return operation switch
                {
                    "ADD" => lcomplex128 + rint32,
                    "SUB" => lcomplex128 - rint32,
                    "MUL" => lcomplex128 * rint32,
                    "DIV" => lcomplex128 / rint32,
                    "FDIV" => lcomplex128 / rint32,
                    "EQ" => lcomplex128 == rint32,
                    "NE" => lcomplex128 != rint32,
                    "EQ!" => false,
                    "NE!" => true,

                    _ => throw new Exception($"Unknown arithmetic operation: {operation}")
                };
            }
            else if (rhs is Int64 rint64)
            {
                return operation switch
                {
                    "ADD" => lcomplex128 + rint64,
                    "SUB" => lcomplex128 - rint64,
                    "MUL" => lcomplex128 * rint64,
                    "DIV" => lcomplex128 / rint64,
                    "FDIV" => lcomplex128 / rint64,
                    "EQ" => lcomplex128 == rint64,
                    "NE" => lcomplex128 != rint64,
                    "EQ!" => false,
                    "NE!" => true,

                    _ => throw new Exception($"Unknown arithmetic operation: {operation}")
                };
            }
            else if (rhs is float rfloat32)
            {
                return operation switch
                {
                    "ADD" => lcomplex128 + rfloat32,
                    "SUB" => lcomplex128 - rfloat32,
                    "MUL" => lcomplex128 * rfloat32,
                    "DIV" => lcomplex128 / rfloat32,
                    "FDIV" => lcomplex128 / rfloat32,
                    "EQ" => lcomplex128 == rfloat32,
                    "NE" => lcomplex128 != rfloat32,
                    "EQ!" => false,
                    "NE!" => true,

                    _ => throw new Exception($"Unknown arithmetic operation: {operation}")
                };
            }
            else if (rhs is double rfloat64)
            {
                return operation switch
                {
                    "ADD" => lcomplex128 + rfloat64,
                    "SUB" => lcomplex128 - rfloat64,
                    "MUL" => lcomplex128 * rfloat64,
                    "DIV" => lcomplex128 / rfloat64,
                    "FDIV" => lcomplex128 / rfloat64,
                    "EQ" => lcomplex128 == rfloat64,
                    "NE" => lcomplex128 != rfloat64,
                    "EQ!" => false,
                    "NE!" => true,

                    _ => throw new Exception($"Unknown arithmetic operation: {operation}")
                };
            }
            else if (rhs is Complex rcomplex128)
            {
                return operation switch
                {
                    "ADD" => lcomplex128 + rcomplex128,
                    "SUB" => lcomplex128 - rcomplex128,
                    "MUL" => lcomplex128 * rcomplex128,
                    "DIV" => lcomplex128 / rcomplex128,
                    "FDIV" => lcomplex128 / rcomplex128,
                    //"POW" => Math.Pow(lcomplex128, rcomplex128),
                    "EQ" => lcomplex128 == rcomplex128,
                    "NE" => lcomplex128 != rcomplex128,
                    "EQ!" => lcomplex128 == rcomplex128,
                    "NE!" => lcomplex128 != rcomplex128,
                    
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
                "IDEMPOTATE" => valint8,
                "NEGATE" => -valint8,
                //"NOT" => !valint8,
                "BINV" => ~valint8,
                // "ALLOC" => ,
                // "FREE" => ,
                // "ADDR" => ,
                // "VALOF" => ,

                _ => throw new Exception($"Unknown arithmetic operation: {operation}")
            };
        }
        else if (operand is Int16 valint16)
        {
            return operation switch
            {
                "IDEMPOTATE" => valint16,
                "NEGATE" => -valint16,
                //"NOT" => !valint16,
                "BINV" => ~valint16,

                _ => throw new Exception($"Unknown arithmetic operation: {operation}")
            };
        }
        else if (operand is Int32 valint32)
        {
            return operation switch
            {
                "IDEMPOTATE" => valint32,
                "NEGATE" => -valint32,
                //"NOT" => !valint32,
                "BINV" => ~valint32,

                _ => throw new Exception($"Unknown arithmetic operation: {operation}")
            };
        }
        else if (operand is Int64 valint64)
        {
            return operation switch
            {
                "IDEMPOTATE" => valint64,
                "NEGATE" => -valint64,
                //"NOT" => !valint64,
                "BINV" => ~valint64,

                _ => throw new Exception($"Unknown arithmetic operation: {operation}")
            };
        }
        else if (operand is BigInteger valintd)
        {
            return operation switch
            {
                "IDEMPOTATE" => valintd,
                "NEGATE" => -valintd,
                //"NOT" => !valintd,
                "BINV" => ~valintd,

                _ => throw new Exception($"Unknown arithmetic operation: {operation}")
            };
        }
        else if (operand is float valfloat32)
        {
            return operation switch
            {
                "IDEMPOTATE" => valfloat32,
                "NEGATE" => -valfloat32,
                
                _ => throw new Exception($"Unknown arithmetic operation: {operation}")
            };
        }
        else if (operand is double valfloat64)
        {
            return operation switch
            {
                "IDEMPOTATE" => valfloat64,
                "NEGATE" => -valfloat64,

                _ => throw new Exception($"Unknown arithmetic operation: {operation}")
            };
        }
        else if (operand is Complex valcomplex)
        {
            return operation switch
            {
                "IDEMPOTATE" => valcomplex,
                "NEGATE" => -valcomplex,

                _ => throw new Exception($"Unknown arithmetic operation: {operation}")
            };
        }
        else if (operand is bool valbool)
        {
            return operation switch
            {
                "NOT" => !valbool,

                _ => throw new Exception($"Unknown arithmetic operation: {operation}")
            };
        }
        else
        {
            throw new Exception($"Unknown arithmetic operand: {operand}");
        }
    }
}