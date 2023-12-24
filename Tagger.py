"""

"""

# Import the required modules
import nicegui as ng
from nicegui import ui
import pandas as pd
import threading
import time

# Create a sample Pandas DataFrame
test_data = {
    'Name': ['Alice', 'Bob', 'Charlie', 'David'],
    'Age': [25, 30, 35, 40],
    'City': ['New York', 'Los Angeles', 'Chicago', 'Houston']
}

df = pd.DataFrame(test_data)
# df = pd.DataFrame(data)

class GameData:
    def __init__(self):
        self.gun_list=pd.DataFrame(data=test_data)

# df = pd.DataFrame(data={'col1': [1, 2], 'col2': [3, 4]})
game_data = GameData()
# df = game_data.gun_list
table = ui.table(
    columns=[{'field': col} for col in df.columns],
    rows=df.to_dict('records'),
)
table.update_rows(df.to_dict('records'))


# new_row = {'Name': 'Eve', 'Age': 28, 'City': 'Miami'}

# Append the new row to the DataFrame
age = 103
def add_row():
    global game_data,table,age
    while True:
        new_row = {'Name': 'Eve', 'Age': age, 'City': 'Miami'}
        age += 1
        game_data.gun_list = pd.concat([game_data.gun_list, pd.DataFrame([new_row])], ignore_index=True)
        table.update_rows(game_data.gun_list.to_dict('records'))
        # with ui.card().classes('w-64'):
        #     # table = ui.table({}).classes('max-h-32')
        #     df = game_data.gun_list
        #     table.view.load_pandas_frame(df)
        # # gun_table.view.load
        # grid2.rowdata = df.to_dict(orient='records')
        # grid2.update()  # Update the NiceGUI interface NOT WORKING
        # ui.update()
        time.sleep(5)  # Sleep for 5 seconds before adding another row

# Start the thread
update_thread = threading.Thread(target=add_row)
update_thread.daemon = True
update_thread.start()

# def update():
#     table.options['rowData'][0]['Age'] += 1
#     # grid2.rowdata = df.to_dict(orient='records')
#     table.update()
#
# ui.button('Update', on_click=update)
# v = ui.checkbox('visible', value= True )
# with ui.column().bind_visibility_from(v,'value'):
#     ui.aggrid.from_pandas(game_data.gun_list).bind_value(game_data,'gun_list')


# Display the DataFrame using NiceGUI
ui.run(port=9000)
