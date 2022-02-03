Kestrel's Ship Matrix (KSM)
===========================

Current Release: 2.1.9

Star Citizen Version: 3.16.0

KSM is a script that outputs a list of all ships in Star Citizen. It can be used
to seed your own database of Star Citizen ships, imported into a spreadsheet for
analytics uses, or just get an idea of what ships are available in Star Citizen.

Features
--------

- Includes concept and in production ships
- Combines data from multiple sources (scunpacked, SPAT, etc)
- Supports JSON, ASCII table, and CSV output formats
- Supports basic display options (filtering, sorting)
- Easy to add more sources as they become available

Requirements
------------

- [Python 3](https://www.python.org/downloads/)
- [virtualenv](https://virtualenv.pypa.io/en/latest/)

Setup
-----

Create a virtual enviornment:

```bash
$ make environment
$ . activate
```

Test that the command is working:

```
$ ./ksm.py --version
ksm.py, version 2.1.0
```

Use the --help flag for more info:

```
$ ./ksm --help
```

Displaying Ships
----------------

Display a list of all Hornets as an ASCII table with basic fields:

```
$ ./ksm.py export -n '*hornet*' -g basic -f table
+----+----------------------+-------+
| id |         name         |  size |
+----+----------------------+-------+
| 11 |      F7C Hornet      | Small |
| 15 |  F7C-M Super Hornet  | Small |
| 14 | F7C-R Hornet Tracker | Small |
| 13 |  F7C-S Hornet Ghost  | Small |
| 37 |      F7A Hornet      | Small |
+----+----------------------+-------+
```

Display the same thing but in JSON format and with all fields:

```
$ ./ksm.py export -n '*hornet*' -g all -f json
[
  ... snip ...
  {
    "id": 13,
    "name": "F7C-S Hornet Ghost",
    "size": "small",
    "manufacturer_name": "Anvil Aerospace",
    "manufacturer_code": "ANVL",
    "url": "https://robertsspaceindustries.com/pledge/ships/anvil-hornet/F7C-S-Hornet-Ghost",
    "status": "Flight Ready",
    "loaners": [],
    "mass": 73724,
    "beam": 21.5,
    "height": 6.5,
    "length": 22.5,
    "scm_speed": 192,
    "max_speed": 1229,
    "cargo": 0,
    "max_crew": 1,
    "min_crew": 1,
    "buy_auec": 1654100,
    "buy_usd": 125,
    "rent_auec": null,
    "ins_std_claim_time": "00:06:45",
    "ins_exp_claim_time": "00:02:15",
    "ins_exp_cost": 3375,
    "has_quantum_drive": false,
    "has_gravlev": false
  }
  ... snip ...
]
```

Updating Data
-------------

KSM knows how to download the latest information for its data sources. You
can use the `update` subcommand to do it. Updated sources will modify data
files so don't forget to commit those.

Update all sources:

```
$ ./ksm.py update all  
```

Update SPAT only:

```
$ ./ksm.py update spat
```

Other Commands
--------------

The `dump` subcommand can be used to display raw data from all data sources
before it's merged into one. This is a good way to find the source of erroneous
values.

The `validate` subcommand runs some simple validate checks on the exported data.
It's a good idea to run the validator after running the update subcommand.

Found a problem?
----------------

If you find bad data please open a Github issue. There might be a bug in KSM,
bad data from a data source, or some normalization needs to be done.

Thanks
------

KSM only aggregates, normalizes, and acts as a CLI to the data. A big thanks
for the hard work by [scunpacked](https://scunpacked.com/),
[SPAT](https://docs.google.com/spreadsheets/d/11nI-wLlRjDpsshkY8VLZkHh2jd2mCmWJTIE2VzqZ7ss),
and [UEX](https://uexcorp.space/) to gather, tweak, and test Star Citizen data.

Just want the data?
-------------------

This repository includes full ship data dumps in all supported formats. Look for
the `ships.csv`, `ships.json`, and `ships.txt` files in the `dist` directory.

KSM has also been imported to Google Sheets here:
https://docs.google.com/spreadsheets/d/1CyizYbgT6JlR1ggATBemxM8prWAR05YYImSJI7gyA8w/edit?usp=sharing
