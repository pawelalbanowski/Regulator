import json

def check_H(file):
    read_json_file = open(file, 'r')
    json_data = json.load(read_json_file)
    read_json_file.close()
    return json_data


def save_H(file, data):
    write_json = json.dumps(data, indent=4)
    write_file = open(file, 'w')
    write_file.write(write_json)
    write_file.close()
    return
