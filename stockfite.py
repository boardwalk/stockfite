#!/usr/bin/env python3
from urllib.request import urlopen
from urllib.parse import urlencode
import csv
import datetime
import io
import json
import os
import os.path
import string
import time

def fetch(sym, begin_date, end_date, *, dividends):
    query = {
        "s": sym.upper(),
        "a": begin_date.month - 1,
        "b": begin_date.day,
        "c": begin_date.year,
        "d": end_date.month - 1,
        "e": end_date.day,
        "f": end_date.year,
    }

    if dividends:
        query["g"] = "v"

    with urlopen("http://ichart.finance.yahoo.com/table.csv?" + urlencode(query)) as f:
        result = [row for row in csv.DictReader(io.TextIOWrapper(f))]

    result.reverse() # return ascending, not descending
    return result

def main():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    os.chdir(script_dir)

    with open("stockfite.html") as inf:
        templ = string.Template(inf.read())

    begin_date = datetime.date(2017, 1, 17)
    end_date = datetime.date(2017, 12, 29)
    repls = {
        "ntdoy_p": fetch("ntdoy", begin_date, end_date, dividends=False),
        "ntdoy_d": fetch("ntdoy", begin_date, end_date, dividends=True),
        "fds_p": fetch("fds", begin_date, end_date, dividends=False),
        "fds_d": fetch("fds", begin_date, end_date, dividends=True)
    }
    repls = {k: json.dumps(v) for k, v in repls.items()}

    with open(os.path.expanduser("~/public_html/stockfite.html"), "w") as outf:
        outf.write(templ.substitute(repls))

if __name__ == "__main__":
    main()

