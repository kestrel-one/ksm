WIP.

You'll need to setup the virtual environment first:

```bash
$ make environment && . activate
```

To download the latest versions of sources use the update command. Updated
sources will modify data files so don't forget to commit those.

```
./ksm.py update all  # Update all sources
./ksm.py update spat # Update SPAT only
```

You can list out the normalized data using the dump command. See the command
help for options. Below is an example usage of the command along with the
output.

It's querying for all ships containing "hornet" in the name. Display output is
in ASCII table format and the columns to include are basic and weapons.

```
$ ./ksm.py dump all -n '*hornet*' -f table -g basic -g weapons
+------------+--------------------+-------------+----------+-------------+--------------+--------------------+---------+--------------+
|   source   |        name        | num_weapons | num_guns | num_turrets | num_missiles |        guns        | turrets |   missiles   |
+------------+--------------------+-------------+----------+-------------+--------------+--------------------+---------+--------------+
| hardpoint  | F7C-M Super Hornet |      0      |    0     |      0      |      0       |         []         |    []   |      []      |
|    rsi     | F7C-M Super Hornet |      8      |    2     |      2      |      4       |       [3, 3]       |  [2, 3] | [2, 2, 3, 3] |
| scunpacked | F7C-M Super Hornet |      8      |    6     |      0      |      2       | [3, 1, 1, 3, 2, 2] |    []   |    [3, 3]    |
|    spat    | F7C-M Super Hornet |             |          |             |              |                    |         |              |
|    uex     | F7C-M Super Hornet |             |          |             |              |                    |         |              |
+------------+--------------------+-------------+----------+-------------+--------------+--------------------+---------+--------------+
```

TODO:

- Figure out how to express weapon sizes
- Merge RSI IDs into all data sets
- Data validation and repair tooling
- CSV export format
