"""Module for printing output in table-like format in single style"""

from rich.console import Console
from rich.table import Table


def print_as_rich_table(columns: list[dict], rows: list[list]):
    """
    Prints data as a rich table with customizable columns and rows.

    Args:
        columns: A list of dictionaries, where each dictionary defines a column.
                 Each dictionary should contain keys like "name", "min_width",
                 "max_width", "justify", "no_wrap".
                 Example: [{"name": "Name", "min_width": 10}, {"name": "Age", "justify": "center"}]
        rows: A list of lists, where each inner list represents a row of data.
              The order of elements in each inner list should match the order
              of columns defined in the 'columns' parameter.
    """
    console = Console()

    def none_as_empty(field):
        return str(field) if field is not None else ""

    table = Table(show_header=True, header_style="bold green", show_lines=True, highlight=False,
                  row_styles=["dim", ""])

    for col_info in columns:
        table.add_column(
            col_info.get("name", ""),
            min_width=col_info.get("min_width"),
            max_width=col_info.get("max_width"),
            justify=col_info.get("justify", "left"),
            no_wrap=col_info.get("no_wrap", False)
        )

    for row_data in rows:
        processed_row = [none_as_empty(field) for field in row_data]
        table.add_row(*processed_row)

    console.print(table)
