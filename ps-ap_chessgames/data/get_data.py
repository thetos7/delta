import wget
import re
import os
from tqdm import tqdm
from collections import OrderedDict
import bz2
import csv

DB_URL = (
    "https://database.lichess.org/standard/lichess_db_standard_rated_2013-01.pgn.bz2"
)


def download_db(db_url, dst_path):
    print("Downloading database...")
    wget.download(db_url, out=dst_path)
    print()


def parse_pgn_line(line):
    key_value = re.match(r'\[(\w+) "([^"]*)"]', line)
    if not key_value:
        line = line[:-1]
        return ("Moves", line) if line else None
    return (key_value.group(1), key_value.group(2))


def pgn_bz2_to_csv(bz2_path, csv_path):
    db_file = bz2.open(bz2_path)

    header = [
        "Event",
        "Site",
        "White",
        "Black",
        "Result",
        "UTCDate",
        "UTCTime",
        "WhiteElo",
        "BlackElo",
        "WhiteRatingDiff",
        "BlackRatingDiff",
        "ECO",
        "Opening",
        "TimeControl",
        "Termination",
        "BlackTitle",
        "WhiteTitle",
        "Moves",
    ]
    db_dict = OrderedDict([(key, None) for key in header])
    csv_file = open(csv_path, "w", encoding="UTF8")
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(header)

    progress_bar = tqdm(desc="Parsing database to csv", unit=" lines")
    line = db_file.readline()
    while line:
        key_value = parse_pgn_line(line.decode("utf-8"))
        if key_value:
            db_dict[key_value[0]] = key_value[1]
            if key_value[0] == "Moves":
                csv_writer.writerow(list(db_dict.values()))
                db_dict = OrderedDict([(key, None) for key in header])
                progress_bar.update()
        line = db_file.readline()

    csv_file.close()
    db_file.close()


if __name__ == "__main__":
    dst_directory = os.path.dirname(os.path.abspath(__file__))
    bz2_name = DB_URL[DB_URL.rfind("/") + 1 :]
    bz2_path = os.path.join(dst_directory, bz2_name)
    csv_name = bz2_name.replace(".pgn.bz2", ".csv")
    csv_path = os.path.join(dst_directory, csv_name)

    if os.path.exists(csv_path):
        print('"data/' + csv_name + '"', "already exists. Data extraction canceled.")
    else:
        if not os.path.exists(bz2_path):
            download_db(DB_URL, bz2_path)
        else:
            print(
                '"data/' + bz2_name + '"',
                "already exists. Starting data extraction from this file...",
            )
        pgn_bz2_to_csv(bz2_path, csv_path)
