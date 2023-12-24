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

gun_info = pd.DataFrame(test_data)

table = ui.table(
    columns=[{'field': col} for col in gun_info.columns],
    rows=gun_info.to_dict('records'),
)

age = 103


def add_row():
    global table, age, gun_info
    while True:
        new_row = {'Name': 'Eve', 'Age': age, 'City': 'Miami'}
        age += 1
        gun_info = pd.concat([gun_info, pd.DataFrame([new_row])], ignore_index=True)
        table.update_rows(gun_info.to_dict('records'))
        time.sleep(0.5)  # Sleep for 5 seconds before adding another row


# Start the thread
update_thread = threading.Thread(target=add_row)
update_thread.daemon = True
update_thread.start()

# Display the DataFrame using NiceGUI
ui.run(port=9000)
