#!/usr/bin/env python3
from urllib.request import urlopen
from urllib.parse import urlencode
import csv
import datetime
import os
import os.path
import time
import json
import string

def fetch(sym, begin_date, end_date, *, dividends):
    path = sym.lower() + "-"
    path += "d" if dividends else "p"
    path += ".csv"

    if not os.access(path, os.R_OK) or os.stat(path).st_mtime < time.time() - 12*60*60:
        with open(path, "wb") as outf:
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
            with urlopen("http://ichart.finance.yahoo.com/table.csv?" + urlencode(query)) as inf:
                outf.write(inf.read())

    with open(path) as f:
        result = [row for row in csv.DictReader(f)]

    result.reverse() # return ascending, not descending
    return result

def main():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    os.chdir(script_dir)

    with open("stockfite.html") as inf:
        templ = string.Template(inf.read())

    begin_date = datetime.date(2017, 1, 1)
    end_date = datetime.date(2017, 12, 29)
    repls = {
        "ntdoy_p": json.dumps(fetch("ntdoy", begin_date, end_date, dividends=False)),
        "ntdoy_d": json.dumps(fetch("ntdoy", begin_date, end_date, dividends=True)),
        "fds_p": json.dumps(fetch("fds", begin_date, end_date, dividends=False)),
        "fds_d": json.dumps(fetch("fds", begin_date, end_date, dividends=True))
    }

    with open(os.path.expanduser("~/public_html/stockfite.html"), "w") as outf:
        outf.write(templ.substitute(repls))

if __name__ == "__main__":
    main()

