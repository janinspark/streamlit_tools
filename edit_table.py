import streamlit as st

@st.dialog("Edit")
def edit_table_data(x):
    st.write(x)

def display_table(table_data, column_formatting=None, edit_function=False, has_header=True, header_color=None, alternating_row_colors=False):
    """
    Displays a table in a Streamlit app with optional row editing functionality. Requires a active color theme in config.toml to work nicely.

    Parameters:
    -----------
    table_data : list of lists
        The data to display in the table. Each sublist represents a row. 
        If `edit_function` is provided, the first column is assumed to be an ID and will be hidden but passed to the edit function.
    
    column_formatting : list or int, optional
        Specifies the number of columns or the specific column layout (e.g., [1, 2, 1]). If not provided, the number of columns will be based on `table_data`.
    
    edit_function : callable, optional
        A function to be called when the "Edit" button is clicked. This function receives the value from the first column (ID), which is hidden when `edit_function` is used.
        If `edit_function` is set, an "Edit" button will be displayed at the end of each row (except the header).
    
    has_header : bool, default=True
        If True, treats the first row as a header and applies bold formatting. The header will not display an "Edit" button.
    
    header_color : str, optional
        The background color for the header row, given in a CSS-compatible format (e.g., 'rgba(151, 166, 195, 0.25)'). If not provided, the default style will be used.
    
    alternating_row_colors : bool, default=False
        If True, applies alternating background colors to the rows for better readability. The secondary background color is pulled from the Streamlit theme settings.

    Behavior:
    ---------
    - Displays the table with optional formatting for the header.
    - If `edit_function` is provided, the first column (assumed to be an ID) will be hidden and passed to the edit function when the user clicks the "Edit" button.
    - Allows for customizable row formatting with alternating row colors.
    - The table layout can be adjusted with custom column widths or equal-sized columns.

    Example Usage:
    --------------
    ```
    data = [['ID', 'Name', 'Age'],
            ['1', 'Alice', '30'],
            ['2', 'Bob', '25']]

    def edit_entry(id_value):
        st.write(f"Editing entry with ID: {id_value}")

    display_table(
        data,
        edit_function=edit_entry,
        header_color='rgba(151, 166, 195, 0.25)',
        alternating_row_colors=True,
    )
    ```
    """
    
    st.html("""<style> .st-key-rnd_table { display: block;} </style>""")
    
    with st.container(key="rnd_table"):
        for j, row in enumerate(table_data):
            # Determine the style for the header or alternating rows
            if j == 0 and header_color:
                style = header_color
            else:
                if alternating_row_colors and ((j+1) % 2 != 0):
                    style = st.get_option("theme.secondaryBackgroundColor")
                else:
                    style = 'transparent'
            with st.container(key=f"row_{j}"):
                columns = st.columns(len(row) if not column_formatting else column_formatting)
                # Skip the first column if edit_function is provided
                for i, col in enumerate(row[1:] if edit_function else row):
                    if j == 0:
                        columns[i].markdown("***"+col+"***")
                    else:
                        columns[i].write(col)
                # If edit_function is provided and not in the header row, display the edit button
                if edit_function and (j != 0 or not has_header):
                    with columns[i+1]:
                        if st.button("Edit", key=f'edit_{j}'):
                            # Pass the first column (hidden ID) to the edit_function
                            edit_function(row[0])
            # Set the background style for the current row
            st.html(f"""<style> .st-key-row_{j} {{ background-color: {style};}} </style>""")

data = [['First', 'Second', 'Third'],
        ['A', 'B', 'C'],
        ['D', 'E', 'F'],
        ['G', 'H', 'I']]
print(st.get_option('theme.primaryColor'))
display_table(
        data,
        edit_function=edit_table_data,
        header_color='rgba(151, 166, 195, 0.25)',
        alternating_row_colors=True,
    )
