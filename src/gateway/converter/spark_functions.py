# SPDX-License-Identifier: Apache-2.0
"""Provides the mapping of Spark functions to Substrait."""
import dataclasses

from backends.backend_options import BackendEngine
from gateway.converter.conversion_options import ConversionOptions
from substrait.gen.proto import algebra_pb2, type_pb2


# pylint: disable=E1101
@dataclasses.dataclass
class ExtensionFunction:
    """Represents a Substrait function."""

    uri: str
    name: str
    output_type: type_pb2.Type
    anchor: int
    max_args: int | None
    options: list[algebra_pb2.FunctionOption] | None

    def __init__(self, uri: str, name: str, output_type: type_pb2.Type,
                 max_args: int | None = None,
                 options: list[algebra_pb2.FunctionOption] | None = None):
        """Create the ExtensionFunction structure."""
        self.uri = uri
        self.name = name
        self.output_type = output_type
        self.max_args = max_args
        self.options = options

    def __lt__(self, obj) -> bool:
        """Compare two ExtensionFunction objects."""
        return self.uri < obj.uri and self.name < obj.name


# pylint: disable=E1101
SPARK_SUBSTRAIT_MAPPING = {
    'split': ExtensionFunction(
        '/functions_string.yaml', 'string_split:str_str', type_pb2.Type(
            string=type_pb2.Type.String(
                nullability=type_pb2.Type.Nullability.NULLABILITY_REQUIRED)),
        max_args=2),
    '==': ExtensionFunction(
        '/functions_comparison.yaml', 'equal:str_str', type_pb2.Type(
            bool=type_pb2.Type.Boolean(
                nullability=type_pb2.Type.Nullability.NULLABILITY_REQUIRED))),
    'equal_null': ExtensionFunction(
        '/functions_comparison.yaml', 'is_not_distinct_from:str_str', type_pb2.Type(
            bool=type_pb2.Type.Boolean(
                nullability=type_pb2.Type.Nullability.NULLABILITY_REQUIRED))),
    '<=': ExtensionFunction(
        '/functions_comparison.yaml', 'lte:i64_i64', type_pb2.Type(
            bool=type_pb2.Type.Boolean(
                nullability=type_pb2.Type.Nullability.NULLABILITY_REQUIRED))),
    '>=': ExtensionFunction(
        '/functions_comparison.yaml', 'gte:i64_i64', type_pb2.Type(
            bool=type_pb2.Type.Boolean(
                nullability=type_pb2.Type.Nullability.NULLABILITY_REQUIRED))),
    '<': ExtensionFunction(
        '/functions_comparison.yaml', 'lt:i64_i64', type_pb2.Type(
            bool=type_pb2.Type.Boolean(
                nullability=type_pb2.Type.Nullability.NULLABILITY_REQUIRED))),
    '>': ExtensionFunction(
        '/functions_comparison.yaml', 'gt:i64_i64', type_pb2.Type(
            bool=type_pb2.Type.Boolean(
                nullability=type_pb2.Type.Nullability.NULLABILITY_REQUIRED))),
    '<=>': ExtensionFunction(
        '/functions_comparison.yaml', 'is_not_distinct_from:any_any', type_pb2.Type(
            bool=type_pb2.Type.Boolean(
                nullability=type_pb2.Type.Nullability.NULLABILITY_NULLABLE))),
    'isnull': ExtensionFunction(
        '/functions_comparison.yaml', 'is_null:int', type_pb2.Type(
            bool=type_pb2.Type.Boolean(
                nullability=type_pb2.Type.Nullability.NULLABILITY_REQUIRED))),
    'isnotnull': ExtensionFunction(
        '/functions_comparison.yaml', 'is_not_null:int', type_pb2.Type(
            bool=type_pb2.Type.Boolean(
                nullability=type_pb2.Type.Nullability.NULLABILITY_REQUIRED))),
    'nullif': ExtensionFunction(
        '/functions_comparison.yaml', 'nullif:int_int', type_pb2.Type(
            bool=type_pb2.Type.Boolean(
                nullability=type_pb2.Type.Nullability.NULLABILITY_REQUIRED))),
    '+': ExtensionFunction(
        '/functions_arithmetic.yaml', 'add:i64_i64', type_pb2.Type(
            i64=type_pb2.Type.I64(
                nullability=type_pb2.Type.Nullability.NULLABILITY_REQUIRED))),
    'try_add': ExtensionFunction(
        '/functions_arithmetic.yaml', 'add:i64_i64', type_pb2.Type(
            i64=type_pb2.Type.I64(
                nullability=type_pb2.Type.Nullability.NULLABILITY_REQUIRED)),
        options=[algebra_pb2.FunctionOption(name='on_domain_error', preference=['NULL'])]),
    '-': ExtensionFunction(
        '/functions_arithmetic.yaml', 'subtract:i64_i64', type_pb2.Type(
            i64=type_pb2.Type.I64(
                nullability=type_pb2.Type.Nullability.NULLABILITY_REQUIRED))),
    'try_subtract': ExtensionFunction(
        '/functions_arithmetic.yaml', 'subtract:i64_i64', type_pb2.Type(
            i64=type_pb2.Type.I64(
                nullability=type_pb2.Type.Nullability.NULLABILITY_REQUIRED)),
        options=[algebra_pb2.FunctionOption(name='on_domain_error', preference=['NULL'])]),
    '*': ExtensionFunction(
        '/functions_arithmetic.yaml', 'multiply:i64_i64', type_pb2.Type(
            i64=type_pb2.Type.I64(
                nullability=type_pb2.Type.Nullability.NULLABILITY_REQUIRED))),
    'try_multiply': ExtensionFunction(
        '/functions_arithmetic.yaml', 'multiply:i64_i64', type_pb2.Type(
            i64=type_pb2.Type.I64(
                nullability=type_pb2.Type.Nullability.NULLABILITY_REQUIRED)),
        options=[algebra_pb2.FunctionOption(name='on_domain_error', preference=['NULL'])]),
    '/': ExtensionFunction(
        '/functions_arithmetic.yaml', 'divide:i64_i64', type_pb2.Type(
            i64=type_pb2.Type.I64(
                nullability=type_pb2.Type.Nullability.NULLABILITY_REQUIRED))),
    'try_divide': ExtensionFunction(
        '/functions_arithmetic.yaml', 'divide:i64_i64', type_pb2.Type(
            i64=type_pb2.Type.I64(
                nullability=type_pb2.Type.Nullability.NULLABILITY_REQUIRED)),
        options=[algebra_pb2.FunctionOption(name='on_domain_error', preference=['NULL'])]),
    '&': ExtensionFunction(
        '/functions_arithmetic.yaml', 'bitwise_and:i64_i64', type_pb2.Type(
            i64=type_pb2.Type.I64(
                nullability=type_pb2.Type.Nullability.NULLABILITY_REQUIRED))),
    '|': ExtensionFunction(
        '/functions_arithmetic.yaml', 'bitwise_or:i64_i64', type_pb2.Type(
            i64=type_pb2.Type.I64(
                nullability=type_pb2.Type.Nullability.NULLABILITY_REQUIRED))),
    '^': ExtensionFunction(
        '/functions_arithmetic.yaml', 'bitwise_xor:i64_i64', type_pb2.Type(
            i64=type_pb2.Type.I64(
                nullability=type_pb2.Type.Nullability.NULLABILITY_REQUIRED))),
    'array_contains': ExtensionFunction(
        '/functions_set.yaml', 'index_in:str_list<str>', type_pb2.Type(
            bool=type_pb2.Type.Boolean(
                nullability=type_pb2.Type.Nullability.NULLABILITY_REQUIRED))),
    'sum': ExtensionFunction(
        '/functions_arithmetic.yaml', 'sum:int', type_pb2.Type(
            i32=type_pb2.Type.I32(
                nullability=type_pb2.Type.Nullability.NULLABILITY_REQUIRED))),
    'try_sum': ExtensionFunction(
        '/functions_arithmetic.yaml', 'sum:int', type_pb2.Type(
            i32=type_pb2.Type.I32(
                nullability=type_pb2.Type.Nullability.NULLABILITY_REQUIRED)),
        options=[algebra_pb2.FunctionOption(name='overflow', preference=['SILENT'])]),
    'avg': ExtensionFunction(
        '/functions_arithmetic.yaml', 'avg:int', type_pb2.Type(
            i32=type_pb2.Type.I32(
                nullability=type_pb2.Type.Nullability.NULLABILITY_REQUIRED))),
    'try_avg': ExtensionFunction(
        '/functions_arithmetic.yaml', 'avg:int', type_pb2.Type(
            i32=type_pb2.Type.I32(
                nullability=type_pb2.Type.Nullability.NULLABILITY_REQUIRED)),
        options=[algebra_pb2.FunctionOption(name='overflow', preference=['SILENT'])]),
    'sqrt': ExtensionFunction(
        '/functions_arithmetic.yaml', 'sqrt:fp64', type_pb2.Type(
            fp64=type_pb2.Type.FP64(
                nullability=type_pb2.Type.Nullability.NULLABILITY_REQUIRED)),
        options=[algebra_pb2.FunctionOption(name='on_domain_error', preference=['NAN'])]),
    'abs': ExtensionFunction(
        '/functions_arithmetic.yaml', 'abs:fp64', type_pb2.Type(
            fp64=type_pb2.Type.FP64(
                nullability=type_pb2.Type.Nullability.NULLABILITY_REQUIRED))),
    'toradians': ExtensionFunction(
        '/functions_arithmetic.yaml', 'radians:fp64', type_pb2.Type(
            fp64=type_pb2.Type.FP64(
                nullability=type_pb2.Type.Nullability.NULLABILITY_REQUIRED))),
    'radians': ExtensionFunction(
        '/functions_arithmetic.yaml', 'radians:fp64', type_pb2.Type(
            fp64=type_pb2.Type.FP64(
                nullability=type_pb2.Type.Nullability.NULLABILITY_REQUIRED))),
    'sign': ExtensionFunction(
        '/functions_arithmetic.yaml', 'sign:fp64', type_pb2.Type(
            fp64=type_pb2.Type.FP64(
                nullability=type_pb2.Type.Nullability.NULLABILITY_REQUIRED))),
    'signum': ExtensionFunction(
        '/functions_arithmetic.yaml', 'sign:fp64', type_pb2.Type(
            fp64=type_pb2.Type.FP64(
                nullability=type_pb2.Type.Nullability.NULLABILITY_REQUIRED))),
    'acos': ExtensionFunction(
        '/functions_arithmetic.yaml', 'acos:fp64', type_pb2.Type(
            fp64=type_pb2.Type.FP64(
                nullability=type_pb2.Type.Nullability.NULLABILITY_REQUIRED))),
    'acosh': ExtensionFunction(
        '/functions_arithmetic.yaml', 'acosh:fp64', type_pb2.Type(
            fp64=type_pb2.Type.FP64(
                nullability=type_pb2.Type.Nullability.NULLABILITY_REQUIRED))),
    'asin': ExtensionFunction(
        '/functions_arithmetic.yaml', 'asin:fp64', type_pb2.Type(
            fp64=type_pb2.Type.FP64(
                nullability=type_pb2.Type.Nullability.NULLABILITY_REQUIRED))),
    'asinh': ExtensionFunction(
        '/functions_arithmetic.yaml', 'asinh:fp64', type_pb2.Type(
            fp64=type_pb2.Type.FP64(
                nullability=type_pb2.Type.Nullability.NULLABILITY_REQUIRED))),
    'atan': ExtensionFunction(
        '/functions_arithmetic.yaml', 'atan:fp64', type_pb2.Type(
            fp64=type_pb2.Type.FP64(
                nullability=type_pb2.Type.Nullability.NULLABILITY_REQUIRED))),
    'atanh': ExtensionFunction(
        '/functions_arithmetic.yaml', 'atanh:fp64', type_pb2.Type(
            fp64=type_pb2.Type.FP64(
                nullability=type_pb2.Type.Nullability.NULLABILITY_REQUIRED))),
    'atan2': ExtensionFunction(
        '/functions_arithmetic.yaml', 'atan2:fp64_fp64', type_pb2.Type(
            fp64=type_pb2.Type.FP64(
                nullability=type_pb2.Type.Nullability.NULLABILITY_REQUIRED))),
    'cos': ExtensionFunction(
        '/functions_arithmetic.yaml', 'cos:fp64', type_pb2.Type(
            fp64=type_pb2.Type.FP64(
                nullability=type_pb2.Type.Nullability.NULLABILITY_REQUIRED))),
    'cosh': ExtensionFunction(
        '/functions_arithmetic.yaml', 'cosh:fp64', type_pb2.Type(
            fp64=type_pb2.Type.FP64(
                nullability=type_pb2.Type.Nullability.NULLABILITY_REQUIRED))),
    'sin': ExtensionFunction(
        '/functions_arithmetic.yaml', 'sin:fp64', type_pb2.Type(
            fp64=type_pb2.Type.FP64(
                nullability=type_pb2.Type.Nullability.NULLABILITY_REQUIRED))),
    'sinh': ExtensionFunction(
        '/functions_arithmetic.yaml', 'sinh:fp64', type_pb2.Type(
            fp64=type_pb2.Type.FP64(
                nullability=type_pb2.Type.Nullability.NULLABILITY_REQUIRED))),
    'tan': ExtensionFunction(
        '/functions_arithmetic.yaml', 'tan:fp64', type_pb2.Type(
            fp64=type_pb2.Type.FP64(
                nullability=type_pb2.Type.Nullability.NULLABILITY_REQUIRED))),
    'tanh': ExtensionFunction(
        '/functions_arithmetic.yaml', 'tanh:fp64', type_pb2.Type(
            fp64=type_pb2.Type.FP64(
                nullability=type_pb2.Type.Nullability.NULLABILITY_REQUIRED))),
    'exp': ExtensionFunction(
        '/functions_arithmetic.yaml', 'exp:fp64', type_pb2.Type(
            fp64=type_pb2.Type.FP64(
                nullability=type_pb2.Type.Nullability.NULLABILITY_REQUIRED))),
    'pow': ExtensionFunction(
        '/functions_arithmetic.yaml', 'power:fp64_fp64', type_pb2.Type(
            fp64=type_pb2.Type.FP64(
                nullability=type_pb2.Type.Nullability.NULLABILITY_REQUIRED))),
    'power': ExtensionFunction(
        '/functions_arithmetic.yaml', 'power:fp64_fp64', type_pb2.Type(
            fp64=type_pb2.Type.FP64(
                nullability=type_pb2.Type.Nullability.NULLABILITY_REQUIRED))),
    'ceil': ExtensionFunction(
        '/functions_rounding.yaml', 'ceil:fp64', type_pb2.Type(
            fp64=type_pb2.Type.FP64(
                nullability=type_pb2.Type.Nullability.NULLABILITY_REQUIRED))),
    'ceiling': ExtensionFunction(
        '/functions_rounding.yaml', 'ceil:fp64', type_pb2.Type(
            fp64=type_pb2.Type.FP64(
                nullability=type_pb2.Type.Nullability.NULLABILITY_REQUIRED))),
    'floor': ExtensionFunction(
        '/functions_rounding.yaml', 'floor:fp64', type_pb2.Type(
            fp64=type_pb2.Type.FP64(
                nullability=type_pb2.Type.Nullability.NULLABILITY_REQUIRED))),
    'rint': ExtensionFunction(
        '/functions_rounding.yaml', 'round:fp64', type_pb2.Type(
            i64=type_pb2.Type.I64(
                nullability=type_pb2.Type.Nullability.NULLABILITY_REQUIRED))),
    'round': ExtensionFunction(
        '/functions_rounding.yaml', 'round:fp64', type_pb2.Type(
            fp64=type_pb2.Type.FP64(
                nullability=type_pb2.Type.Nullability.NULLABILITY_REQUIRED))),
    'bround': ExtensionFunction(
        '/functions_rounding.yaml', 'round:fp64', type_pb2.Type(
            fp64=type_pb2.Type.FP64(
                nullability=type_pb2.Type.Nullability.NULLABILITY_REQUIRED)),
        options=[algebra_pb2.FunctionOption(name='rounding', preference=['TIE_TO_EVEN'])]),
    'regexp_extract_all': ExtensionFunction(
        '/functions_string.yaml', 'regexp_match:str_binary_str', type_pb2.Type(
            list=type_pb2.Type.List(type=type_pb2.Type(string=type_pb2.Type.String(
                nullability=type_pb2.Type.Nullability.NULLABILITY_REQUIRED))))),
    'regexp_substring': ExtensionFunction(
        '/functions_string.yaml', 'regexp_substring:str_str_i64_i64', type_pb2.Type(
            i64=type_pb2.Type.I64(nullability=type_pb2.Type.Nullability.NULLABILITY_REQUIRED))),
    'DUCKDB_regexp_matches': ExtensionFunction(
        '/functions_string.yaml', 'regexp_matches:str_str', type_pb2.Type(
            bool=type_pb2.Type.Boolean(
                nullability=type_pb2.Type.Nullability.NULLABILITY_REQUIRED))),
    'substr': ExtensionFunction(
        '/functions_string.yaml', 'substring:str_int_int', type_pb2.Type(
            string=type_pb2.Type.String(
                nullability=type_pb2.Type.Nullability.NULLABILITY_REQUIRED))),
    'substring': ExtensionFunction(
        '/functions_string.yaml', 'substring:str_int_int', type_pb2.Type(
            string=type_pb2.Type.String(
                nullability=type_pb2.Type.Nullability.NULLABILITY_REQUIRED))),
    'instr': ExtensionFunction(
        '/functions_string.yaml', 'strpos:str_str', type_pb2.Type(
            i64=type_pb2.Type.I64(
                nullability=type_pb2.Type.Nullability.NULLABILITY_REQUIRED))),
    'startswith': ExtensionFunction(
        '/functions_string.yaml', 'starts_with:str_str', type_pb2.Type(
            bool=type_pb2.Type.Boolean(
                nullability=type_pb2.Type.Nullability.NULLABILITY_REQUIRED))),
    'endswith': ExtensionFunction(
        '/functions_string.yaml', 'ends_with:str_str', type_pb2.Type(
            bool=type_pb2.Type.Boolean(
                nullability=type_pb2.Type.Nullability.NULLABILITY_REQUIRED))),
    'contains': ExtensionFunction(
        '/functions_string.yaml', 'contains:str_str', type_pb2.Type(
            bool=type_pb2.Type.Boolean(
                nullability=type_pb2.Type.Nullability.NULLABILITY_REQUIRED))),
    'length': ExtensionFunction(
        '/functions_string.yaml', 'char_length:str', type_pb2.Type(
            i64=type_pb2.Type.I64(
                nullability=type_pb2.Type.Nullability.NULLABILITY_REQUIRED))),
    'max': ExtensionFunction(
        '/unknown.yaml', 'max:i64', type_pb2.Type(
            i64=type_pb2.Type.I64(
                nullability=type_pb2.Type.Nullability.NULLABILITY_REQUIRED))),
    'min': ExtensionFunction(
        '/unknown.yaml', 'min:i64', type_pb2.Type(
            i64=type_pb2.Type.I64(
                nullability=type_pb2.Type.Nullability.NULLABILITY_REQUIRED))),
    'string_agg': ExtensionFunction(
        '/functions_string.yaml', 'string_agg:str', type_pb2.Type(
            string=type_pb2.Type.String(
                nullability=type_pb2.Type.Nullability.NULLABILITY_REQUIRED))),
    'btrim': ExtensionFunction(
        '/functions_string.yaml', 'trim:str', type_pb2.Type(
            string=type_pb2.Type.String(
                nullability=type_pb2.Type.Nullability.NULLABILITY_REQUIRED))),
    'ltrim': ExtensionFunction(
        '/functions_string.yaml', 'ltrim:str', type_pb2.Type(
            string=type_pb2.Type.String(
                nullability=type_pb2.Type.Nullability.NULLABILITY_REQUIRED))),
    'rtrim': ExtensionFunction(
        '/functions_string.yaml', 'rtrim:str', type_pb2.Type(
            string=type_pb2.Type.String(
                nullability=type_pb2.Type.Nullability.NULLABILITY_REQUIRED))),
    'trim': ExtensionFunction(
        '/functions_string.yaml', 'trim:str', type_pb2.Type(
            string=type_pb2.Type.String(
                nullability=type_pb2.Type.Nullability.NULLABILITY_REQUIRED))),
    'lcase': ExtensionFunction(
        '/functions_string.yaml', 'lower:str', type_pb2.Type(
            string=type_pb2.Type.String(
                nullability=type_pb2.Type.Nullability.NULLABILITY_REQUIRED))),
    'lower': ExtensionFunction(
        '/functions_string.yaml', 'lower:str', type_pb2.Type(
            string=type_pb2.Type.String(
                nullability=type_pb2.Type.Nullability.NULLABILITY_REQUIRED))),
    'ucase': ExtensionFunction(
        '/functions_string.yaml', 'upper:str', type_pb2.Type(
            string=type_pb2.Type.String(
                nullability=type_pb2.Type.Nullability.NULLABILITY_REQUIRED))),
    'upper': ExtensionFunction(
        '/functions_string.yaml', 'upper:str', type_pb2.Type(
            string=type_pb2.Type.String(
                nullability=type_pb2.Type.Nullability.NULLABILITY_REQUIRED))),
    'left': ExtensionFunction(
        '/functions_string.yaml', 'left:int_str', type_pb2.Type(
            string=type_pb2.Type.String(
                nullability=type_pb2.Type.Nullability.NULLABILITY_REQUIRED))),
    'right': ExtensionFunction(
        '/functions_string.yaml', 'right:int_str', type_pb2.Type(
            string=type_pb2.Type.String(
                nullability=type_pb2.Type.Nullability.NULLABILITY_REQUIRED))),
    'least': ExtensionFunction(
        '/functions_comparison.yaml', 'least:i64', type_pb2.Type(
            i64=type_pb2.Type.I64(
                nullability=type_pb2.Type.Nullability.NULLABILITY_REQUIRED))),
    'greatest': ExtensionFunction(
        '/functions_comparison.yaml', 'greatest:i64', type_pb2.Type(
            i64=type_pb2.Type.I64(
                nullability=type_pb2.Type.Nullability.NULLABILITY_REQUIRED))),
    'coalesce': ExtensionFunction(
        '/functions_comparison.yaml', 'coalesce:any', type_pb2.Type(
            string=type_pb2.Type.String(
                nullability=type_pb2.Type.Nullability.NULLABILITY_NULLABLE))),
    'isnan': ExtensionFunction(
        '/functions_comparison.yaml', 'is_nan:fp64', type_pb2.Type(
            bool=type_pb2.Type.Boolean(
                nullability=type_pb2.Type.Nullability.NULLABILITY_REQUIRED))),
    'concat': ExtensionFunction(
        '/functions_string.yaml', 'concat:str_str', type_pb2.Type(
            string=type_pb2.Type.String(
                nullability=type_pb2.Type.Nullability.NULLABILITY_REQUIRED))),
    'concat_ws': ExtensionFunction(
        '/functions_string.yaml', 'concat_ws:str_str', type_pb2.Type(
            string=type_pb2.Type.String(
                nullability=type_pb2.Type.Nullability.NULLABILITY_REQUIRED))),
    'repeat': ExtensionFunction(
        '/functions_string.yaml', 'repeat:str_i64', type_pb2.Type(
            string=type_pb2.Type.String(
                nullability=type_pb2.Type.Nullability.NULLABILITY_REQUIRED))),
    'replace': ExtensionFunction(
        '/functions_string.yaml', 'replace:str_str_str', type_pb2.Type(
            string=type_pb2.Type.String(
                nullability=type_pb2.Type.Nullability.NULLABILITY_REQUIRED))),
    'lpad': ExtensionFunction(
        '/functions_string.yaml', 'lpad:str_i64_str', type_pb2.Type(
            string=type_pb2.Type.String(
                nullability=type_pb2.Type.Nullability.NULLABILITY_REQUIRED))),
    'rpad': ExtensionFunction(
        '/functions_string.yaml', 'rpad:str_i64_str', type_pb2.Type(
            string=type_pb2.Type.String(
                nullability=type_pb2.Type.Nullability.NULLABILITY_REQUIRED))),
    'regexp_strpos': ExtensionFunction(
        '/functions_string.yaml', 'regexp_strpos:str_str_i64_i64', type_pb2.Type(
            i64=type_pb2.Type.I64(
                nullability=type_pb2.Type.Nullability.NULLABILITY_REQUIRED))),
    'rlike': ExtensionFunction(
        '/functions_string.yaml', 'regexp_like:str_str', type_pb2.Type(
            bool=type_pb2.Type.Boolean(
                nullability=type_pb2.Type.Nullability.NULLABILITY_REQUIRED))),
    'regexp': ExtensionFunction(
        '/functions_string.yaml', 'regexp_like:str_str', type_pb2.Type(
            bool=type_pb2.Type.Boolean(
                nullability=type_pb2.Type.Nullability.NULLABILITY_REQUIRED))),
    'regexp_like': ExtensionFunction(
        '/functions_string.yaml', 'regexp_like:str_str', type_pb2.Type(
            bool=type_pb2.Type.Boolean(
                nullability=type_pb2.Type.Nullability.NULLABILITY_REQUIRED))),
    'bit_length': ExtensionFunction(
        '/functions_string.yaml', 'bit_length:str', type_pb2.Type(
            i64=type_pb2.Type.I64(
                nullability=type_pb2.Type.Nullability.NULLABILITY_REQUIRED))),
    'character_length': ExtensionFunction(
        '/functions_string.yaml', 'char_length:str', type_pb2.Type(
            i64=type_pb2.Type.I64(
                nullability=type_pb2.Type.Nullability.NULLABILITY_REQUIRED))),
    'char_length': ExtensionFunction(
        '/functions_string.yaml', 'char_length:str', type_pb2.Type(
            i64=type_pb2.Type.I64(
                nullability=type_pb2.Type.Nullability.NULLABILITY_REQUIRED))),
    'octet_length': ExtensionFunction(
        '/functions_string.yaml', 'octet_length:str', type_pb2.Type(
            i64=type_pb2.Type.I64(
                nullability=type_pb2.Type.Nullability.NULLABILITY_REQUIRED))),
    'count': ExtensionFunction(
        '/functions_aggregate_generic.yaml', 'count:any', type_pb2.Type(
            i64=type_pb2.Type.I64(
                nullability=type_pb2.Type.Nullability.NULLABILITY_REQUIRED))),
    'approx_count_distinct': ExtensionFunction(
        '/functions_aggregate_approx.yaml', 'approx_count_distinct:any',
        type_pb2.Type(i64=type_pb2.Type.I64(
            nullability=type_pb2.Type.Nullability.NULLABILITY_REQUIRED))),
    'any_value': ExtensionFunction(
        '/functions_aggregate_generic.yaml', 'any_value:any', type_pb2.Type(
            i64=type_pb2.Type.I64(
                nullability=type_pb2.Type.Nullability.NULLABILITY_REQUIRED))),
    'first_value': ExtensionFunction(
        '/functions_aggregate_generic.yaml', 'first_value:any', type_pb2.Type(
            i64=type_pb2.Type.I64(
                nullability=type_pb2.Type.Nullability.NULLABILITY_REQUIRED))),
    'and': ExtensionFunction(
        '/functions_boolean.yaml', 'and:bool_bool', type_pb2.Type(
            bool=type_pb2.Type.Boolean(
                nullability=type_pb2.Type.Nullability.NULLABILITY_REQUIRED))),
    'or': ExtensionFunction(
        '/functions_boolean.yaml', 'or:bool_bool', type_pb2.Type(
            bool=type_pb2.Type.Boolean(
                nullability=type_pb2.Type.Nullability.NULLABILITY_REQUIRED))),
    'not': ExtensionFunction(
        '/functions_boolean.yaml', 'not:bool', type_pb2.Type(
            bool=type_pb2.Type.Boolean(
                nullability=type_pb2.Type.Nullability.NULLABILITY_REQUIRED))),
    'struct_extract': ExtensionFunction(
        '/functions_structs.yaml', 'struct_extract:any_str', type_pb2.Type(
            i64=type_pb2.Type.I64(
                nullability=type_pb2.Type.Nullability.NULLABILITY_REQUIRED))),
}
SPARK_SUBSTRAIT_MAPPING_FOR_DUCKDB = {
    'struct': ExtensionFunction(
        '/functions_structs.yaml', 'struct_pack:any_str', type_pb2.Type(
            i64=type_pb2.Type.I64(
                nullability=type_pb2.Type.Nullability.NULLABILITY_REQUIRED))),
    **SPARK_SUBSTRAIT_MAPPING
}


def _find_mapping(options:ConversionOptions) -> dict[str, ExtensionFunction]:
    match options.backend.backend:
        case BackendEngine.DUCKDB:
            return SPARK_SUBSTRAIT_MAPPING_FOR_DUCKDB
        case _:
            return SPARK_SUBSTRAIT_MAPPING


def lookup_spark_function(name: str, options: ConversionOptions) -> ExtensionFunction:
    """Return a Substrait function given a spark function name."""
    mapping = _find_mapping(options)
    definition = mapping.get(name)
    if definition is None:
        raise ValueError(f'Function {name} not found in the Spark to Substrait mapping table.')
    if not options.return_names_with_types:
        definition.name = definition.name.split(':', 1)[0]
    return definition
