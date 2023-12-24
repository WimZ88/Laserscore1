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


# df = pd.DataFrame(data)

class GameData:
    def __init__(self):
        self.gun_list=pd.DataFrame(data=test_data)

# df = pd.DataFrame(data={'col1': [1, 2], 'col2': [3, 4]})
game_data = GameData()

gun_table = ui.aggrid.from_pandas(game_data.gun_list).classes('max-h-40')

new_row = {'Name': 'Eve', 'Age': 28, 'City': 'Miami'}

# Append the new row to the DataFrame

def add_row():
    global game_data
    while True:
        new_row = {'Name': 'Eve', 'Age': 28, 'City': 'Miami'}
        game_data.gun_list = pd.concat([game_data.gun_list, pd.DataFrame([new_row])], ignore_index=True)
        # grid2.rowdata = df.to_dict(orient='records')
        # grid2.update()  # Update the NiceGUI interface NOT WORKING
        # ui.update()
        time.sleep(5)  # Sleep for 5 seconds before adding another row

# Start the thread
update_thread = threading.Thread(target=add_row)
update_thread.daemon = True
update_thread.start()

def update():
    gun_table.options['rowData'][0]['Age'] += 1
    # grid2.rowdata = df.to_dict(orient='records')
    gun_table.update()

ui.button('Update', on_click=update)
v = ui.checkbox('visible', value= True )
with ui.column().bind_visibility_from(v,'value'):
    ui.aggrid.from_pandas(game_data.gun_list).bind_value(game_data,'gun_list')


# Display the DataFrame using NiceGUI
ui.run(port=9000)
