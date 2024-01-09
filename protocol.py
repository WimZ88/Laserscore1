import struct
import pandas as pd

# Define the data
ping_template_data = {
    "message_id": 1,
    "tagger_id": 2,
    "batterylevel": 3,
}

scoring_template_data = {
    "player_id": 1,
    "team_id": 2,
    "rounds_fired": 3,
    "total_hits": 4,
    "game_time_minutes": 5,
    "game_time_seconds": 6,
    "respawns": 7,
    "tagged_out_counter": 8,
    "flag_counter": 9,
    "checksum": 0xff,
}

configuration_template_data = {
    "team_id": 1,
    "sound_set": 2,
    "damage_per_shot": 3,
    "fire_selector": 4,
    "cyclic_rpm": 5,
    "ir_power": 6,
    "ir_range": 7,
    "tagger_settings": 8,
    "respawn_health": 9,
    "game_on_off_settings1": 10,
    "game_on_off_settings2": 11,
    "hit_delay": 12,
    "checksum": 0xff,
}

# Create a Pandas Series
game_score = pd.Series(scoring_template_data)


def pack_scoring_data(score):
    # Pack the score. All 1 byte except rounds_fired and total_hits, which are 2 bytes big-endian.
    packed_data = struct.pack(
        '<BBHHHHBBBB',  # Format string for packing
        score["player_id"],
        score["team_id"],
        score["rounds_fired"],
        score["total_hits"],
        score["game_time_minutes"],
        score["game_time_seconds"],
        score["respawns"],
        score["tagged_out_counter"],
        score["flag_counter"],
        score["checksum"]
    )
    return packed_data


def unpack_ping_data(raw):
    # Unpack the raw data. All 1 byte except rounds_fired and total_hits, which are 2 bytes little-endian.
    unpacked_data = struct.unpack(
        '>BBH',  # Format string for unpacking
        raw
    )

    # Convert the unpacked data to a Pandas Series
    series = pd.Series({
        "message_id": unpacked_data[0],
        "tagger_id": unpacked_data[1],
        "batterylevel": unpacked_data[2],
    })

    return series


def unpack_scoring_data(raw):
    # Unpack the raw data. All 1 byte except rounds_fired and total_hits, which are 2 bytes little-endian.
    unpacked_data = struct.unpack(
        '<BBHHHHBBBB',  # Format string for unpacking
        raw
    )

    # Convert the unpacked data to a Pandas Series
    series = pd.Series({
        "player_id": unpacked_data[0],
        "team_id": unpacked_data[1],
        "rounds_fired": unpacked_data[2],
        "total_hits": unpacked_data[3],
        "game_time_minutes": unpacked_data[4],
        "game_time_seconds": unpacked_data[5],
        "respawns": unpacked_data[6],
        "tagged_out_counter": unpacked_data[7],
        "flag_counter": unpacked_data[8],
        "checksum": unpacked_data[9],
    })

    return series


# packed_score = pack_scoring_data(game_score)
#
# # Convert to hex string
# hex_string = ''.join(f'{byte:02x}' for byte in packed_score)
# print("packed:")
# print(game_score)
# print("into hex", hex_string)
# print()
#
# packed_score = bytearray(packed_score)  # grr
# packed_score[3] = 25  # change
# packed_score = bytes(packed_score)
#
# decoded = unpack_scoring_data(packed_score)
# print("decoded:")
# print(decoded)
#
# # add header
# packed_score = b"abc" + packed_score
# print("\nadded header", ''.join(f'{byte:02x}' for byte in packed_score))
