"""Module for printing output in table-like format in single style"""
from __future__ import annotations

from datetime import datetime
from datetime import time

from rich.console import Console
from rich.table import Table

SORTABLE_TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S"
SORTABLE_DATE_FORMAT = "%Y-%m-%d"


def print_as_rich_table(
    columns: list[dict], rows: list[list], sort_by: str = "", reverse_sort: bool = False
):
    """
    Prints data as a rich table with customizable columns and rows.

    Args:
        columns: A list of dictionaries, where each dictionary defines a column.
                 Each dictionary should contain keys like "name", "min_width",
                 "max_width", "justify", "no_wrap".
                 Example: [{"name": "Name", "min_width": 10},
                     {"name": "Age", "justify": "center"}]
        rows: A list of lists, where each inner list represents a row of data.
              The order of elements in each inner list should match the order
              of columns defined in the 'columns' parameter.
        sort_by: optional column name to sort by
        reverse_sort: optional boolean flag to sort in reversed order
    """
    console = Console()

    def none_as_empty(field):
        return str(field) if field is not None else ""

    def date_time_sortable_format(field):
        if isinstance(field, datetime):
            if field.time() == time(0, 0, 0):
                return field.strftime(SORTABLE_DATE_FORMAT)
            else:
                return field.strftime(SORTABLE_TIMESTAMP_FORMAT)
        else:
            return field

    table = Table(
        show_header=True,
        header_style="bold green",
        show_lines=True,
        highlight=False,
        row_styles=["dim", ""],
    )

    for col_info in columns:
        table.add_column(
            col_info.get("name", ""),
            min_width=col_info.get("min_width"),
            max_width=col_info.get("max_width"),
            justify=col_info.get("justify", "left"),
            no_wrap=col_info.get("no_wrap", False),
        )

    if sort_by:
        sort_col_index = [col.get("name").casefold() for col in columns].index(
            sort_by.casefold()
        )
        rows.sort(key=lambda row: str(row[sort_col_index]), reverse=reverse_sort)
        console.print(
            f"[bold yellow]Sorting by '{sort_col_index}' ({'Descending' if reverse_sort else 'Ascending'})[/bold yellow]"
        )

    for row_data in rows:
        processed_row = [
            none_as_empty(date_time_sortable_format(field)) for field in row_data
        ]
        table.add_row(*processed_row)

    console.print(table)
