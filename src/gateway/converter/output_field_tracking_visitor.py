# SPDX-License-Identifier: Apache-2.0
"""A library to search Substrait plan for local files."""
from typing import Any, Optional

from substrait.gen.proto import algebra_pb2, plan_pb2

from gateway.converter.label_relations import get_common_section
from gateway.converter.substrait_plan_visitor import SubstraitPlanVisitor
from gateway.converter.symbol_table import SymbolTable


# pylint: disable=E1101
def get_plan_id_from_common(common: algebra_pb2.RelCommon) -> int:
    """Gets the plan ID from the common section."""
    ref_rel = algebra_pb2.ReferenceRel()
    common.advanced_extension.optimization.Unpack(ref_rel)
    return ref_rel.subtree_ordinal


# pylint: disable=E1101
def get_plan_id(rel: algebra_pb2.Rel) -> int:
    """Gets the plan ID from the relation."""
    common = get_common_section(rel)
    return get_plan_id_from_common(common)


# pylint: disable=no-member,fixme
class OutputFieldTrackingVisitor(SubstraitPlanVisitor):
    """Replaces all cast expressions with projects of casts instead."""

    def __init__(self):
        super().__init__()
        self._current_plan_id: Optional[int] = None  # The relation currently being processed.
        self._symbol_table = SymbolTable()

    def update_field_references(self, plan_id: int) -> None:
        """Uses the field references using the specified portion of the plan."""
        source_symbol = self._symbol_table.get_symbol(plan_id)
        current_symbol = self._symbol_table.get_symbol(self._current_plan_id)
        current_symbol.input_fields.extend(source_symbol.output_fields)
        current_symbol.output_fields.extend(current_symbol.input_fields)
        current_symbol.output_fields.extend(current_symbol.generated_fields)

    def visit_read_relation(self, rel: algebra_pb2.ReadRel) -> Any:
        """Uses the field references from the read relation."""
        super().visit_read_relation(rel)
        symbol = self._symbol_table.get_symbol(self._current_plan_id)
        # TODO -- Validate this logic where complicated data structures are used.
        for field in rel.base_schema.names:
            symbol.output_fields.append(field)

    def visit_filter_relation(self, rel: algebra_pb2.FilterRel) -> Any:
        super().visit_filter_relation(rel)
        self.update_field_references(get_plan_id(rel.input))

    def visit_fetch_relation(self, rel: algebra_pb2.FetchRel) -> Any:
        super().visit_fetch_relation(rel)
        self.update_field_references(get_plan_id(rel.input))

    def visit_aggregate_relation(self, rel: algebra_pb2.AggregateRel) -> Any:
        super().visit_aggregate_relation(rel)
        symbol = self._symbol_table.get_symbol(self._current_plan_id)
        for _ in rel.groupings:
            symbol.generated_fields.append('grouping')
        for _ in rel.measures:
            symbol.generated_fields.append('measure')
        self.update_field_references(get_plan_id(rel.input))

    def visit_sort_relation(self, rel: algebra_pb2.SortRel) -> Any:
        super().visit_sort_relation(rel)
        self.update_field_references(get_plan_id(rel.input))

    def visit_project_relation(self, rel: algebra_pb2.ProjectRel) -> Any:
        super().visit_project_relation(rel)
        symbol = self._symbol_table.get_symbol(self._current_plan_id)
        for _ in rel.expressions:
            symbol.generated_fields.append('intermediate')
        self.update_field_references(get_plan_id(rel.input))

    def visit_extension_single_relation(self, rel: algebra_pb2.ExtensionSingleRel) -> Any:
        super().visit_extension_single_relation(rel)
        self.update_field_references(get_plan_id(rel.input))

    # TODO -- Add the other relation types.

    def visit_relation(self, rel: algebra_pb2.Rel) -> Any:
        """Visits a relation node."""
        new_plan_id = get_plan_id(rel)
        self._symbol_table.add_symbol(new_plan_id,
                                      parent=self._current_plan_id,
                                      symbol_type=rel.WhichOneof('rel_type'))
        old_plan_id = self._current_plan_id
        self._current_plan_id = new_plan_id

        super().visit_relation(rel)

        self._current_plan_id = old_plan_id

    def visit_plan(self, plan: plan_pb2 .Plan) -> Any:
        """Visits a plan node."""
        super().visit_plan(plan)
        return self._symbol_table
