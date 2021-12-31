from plugins.c2c_pb2 import NFCData
from plugins.c2s_pb2 import ServerData
from datetime import datetime
import os

curr_file = ""


def hex_dump(a):
    # return " ".join([f"0x{str(hex(c))[2:].zfill(2)}" for c in a])
    return " ".join([f"{str(hex(c))[2:].zfill(2)}" for c in a])

def format_data(data):
    if len(data) == 0:
        return ""

    nfc_data = NFCData()
    nfc_data.ParseFromString(data)

    letter = "Tag" if nfc_data.data_source == NFCData.CARD else "Rdr"
    initial = "(initial) " if nfc_data.data_type == NFCData.INITIAL else ""
    string_to_return = f"{datetime.fromtimestamp(nfc_data.timestamp/1000)} | {letter} | {hex_dump(nfc_data.data)} {'| ' + initial if initial else ''}\n"
    
    if initial:
        curr_file = f"TransactionLog-{datetime.fromtimestamp(int(nfc_data.timestamp/1000)).strftime('%Y-%m-%d-%H-%M-%S')}.log"
        curr_file = os.path.join(".", "log", curr_file)
        
    with open(curr_file, "a") as f:
        f.write(string_to_return)
    
    #print(nfc_data.data, type(nfc_data.data))
    


def handle_data(log, data):
    server_message = ServerData()
    server_message.ParseFromString(data)

    log(ServerData.Opcode.Name(server_message.opcode), format_data(server_message.data))
    return data
