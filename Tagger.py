"""

"""

# https://github.com/zauberzeug/nicegui/discussions/1713

# Import the required modules
from nicegui import ui
from UDP_tools import rx_udp, rx_queue
import pandas as pd
import threading
import subprocess
import time

from protocol import unpack_ping_data

overview_data = pd.DataFrame(data={'Tagger ID': [1, 2], 'Batterystate': [1, 1], 'Last seen': [1, 1]})
# overview_table = ui.table.from_pandas(overview_data).classes('max-h-max')


def get_git_revision_short_hash() -> str:
    return subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).decode('ascii').strip()


def process_udp_data():
    # global age, gun_info
    print("Start processing data")
    while True:
        while not rx_queue.empty():
            try:
                item = rx_queue.get()
                if item[0] == 0x01:  # ping message.
                    ping_decoded = unpack_ping_data(item)
                    grid.options['rowData'][ping_decoded.tagger_id]['Batterystate'] = ping_decoded.batterylevel
                    grid.update()
                    # overview_data.loc[overview_data[
                    #                       'Tagger ID'] == ping_decoded.tagger_id, 'Batterystate'] = ping_decoded.batterylevel
                    # overview_table.update_rows(overview_data.to_dict('records'))
                elif item[0] == 0x02:  # config message.
                    print(unpack_ping_data(item))
                elif item[0] == 0x03:  # score message.
                    print(unpack_ping_data(item))
            except Exception as e:
                pass  # just try again to do stuff
        time.sleep(0.1)  # Sleep for 100ms


async def output_selected_rows():
    rows = await grid.get_selected_rows()
    if rows:
        for row in rows:
            ui.notify(f"{row['name']}, {row['age']}")
    else:
        ui.notify('No rows selected.')


async def output_selected_row():
    row = await grid.get_selected_row()
    if row:
        ui.notify(f"{row['name']}, {row['age']}")
    else:
        ui.notify('No row selected!')


# Start the threads
UDP_RX = threading.Thread(target=rx_udp)
UDP_RX.daemon = True
UDP_RX.start()

packet_proces = threading.Thread(target=process_udp_data)
packet_proces.daemon = True
packet_proces.start()

# configure GUI
with (ui.tabs().classes('w-full') as tabs):
    one = ui.tab('Overview')
    two = ui.tab('Configuration template')
    three = ui.tab('Scores')
with ui.tab_panels(tabs, value=one).classes('w-full'):
    with ui.tab_panel(one):
        ui.label('Overview')
        # overview_table.add_slot('body-cell-age', '''
        #     <q-td key="age" :props="props">
        #         <q-badge :color="props.value < 21 ? 'red' : 'green'">
        #             {{ props.value }}
        #         </q-badge>
        #     </q-td>
        # ''')
        grid = ui.aggrid.from_pandas(overview_data).classes('max-h-max')
        ui.button('Output selected rows', on_click=output_selected_rows)
        ui.button('Output selected row', on_click=output_selected_row)
    with ui.tab_panel(two):
        ui.label('Configuration template')
        radio1 = ui.radio([1, 2, 3], value=1).props('inline')
        radio2 = ui.radio({1: 'A', 2: 'B', 3: 'C'}).props('inline').bind_value(radio1, 'value')
    with ui.tab_panel(three):
        ui.label('Scores')

with ui.footer().style('background-color: white'):
    ui.label(get_git_revision_short_hash()).style('color: #000000; font-size: 100%; font-weight: 300')
# run GUI

ui.run(port=9000, reload=False)
