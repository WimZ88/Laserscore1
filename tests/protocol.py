import struct
import pandas as pd
from dataclasses import dataclass

# Define the data
from dataclasses import dataclass
import pandas as pd
import struct

@dataclass
class ScoreData:
    player_id: int = 1
    team_id: int = 2
    rounds_fired: int = 3
    total_hits: int = 4
    game_time_minutes: int = 5
    game_time_seconds: int = 6
    respawns: int = 7
    tagged_out_counter: int = 8
    flag_counter: int = 9
    checksum: int = 0xff

    def pack(self):
        # Pack the score. All 1 byte except rounds_fired and total_hits, which are 2 bytes big-endian.
        packed_data = struct.pack(
            '<BBHHHHBBBB',  # Format string for packing
            self.player_id,
            self.team_id,
            self.rounds_fired,
            self.total_hits,
            self.game_time_minutes,
            self.game_time_seconds,
            self.respawns,
            self.tagged_out_counter,
            self.flag_counter,
            self.checksum
        )
        return packed_data

    def to_series(self):
        # Return a Pandas Series containing the member values
        return pd.Series({
            "player_id": self.player_id,
            "team_id": self.team_id,
            "rounds_fired": self.rounds_fired,
            "total_hits": self.total_hits,
            "game_time_minutes": self.game_time_minutes,
            "game_time_seconds": self.game_time_seconds,
            "respawns": self.respawns,
            "tagged_out_counter": self.tagged_out_counter,
            "flag_counter": self.flag_counter,
            "checksum": self.checksum,
        })

    @classmethod
    def unpack(cls, raw):  # raw data from network
        # Unpack the raw data. All 1 byte except rounds_fired and total_hits, which are 2 bytes little-endian.
        unpacked_data = struct.unpack(
            '<BBHHHHBBBB',  # Format string for unpacking
            raw
        )

        # Create an instance of ScoreData using the unpacked data
        return cls(*unpacked_data)

playscores = []
for i in range(10):
    playscores.append(ScoreData(player_id=i+100))

playscores[3].flag_counter=50
playscores[0].team_id=25

players = pd.DataFrame([score.to_series() for score in playscores])
print(players)
print(playscores[0] == playscores[0])
print(playscores[0] == playscores[1])

print([p.pack() for p in playscores])
# print(player_1.to_series())
# print(player_2.to_series())


# print(player_1 == player_2)


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
