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
in ASCII table format. Default fields are shown. See the -g and -c options for
all of the available fields.

```
$ ./ksm.py dump all -n '*hornet*' -f table
$ ./ksm.py dump all -n '*hornet*' -f table
+------------+-----+--------------------------------+-------+--------------+---------+------+--------+--------+
|   source   |  id |              name              |  size |    status    |   mass  | beam | height | length |
+------------+-----+--------------------------------+-------+--------------+---------+------+--------+--------+
| hardpoint  |     |           F7A Hornet           | small |              | 73317.0 |      |        |        |
| hardpoint  |     |           F7C Hornet           | small |              | 74132.0 |      |        |        |
| hardpoint  |     |      F7C Hornet Wildfire       | small |              | 74132.0 |      |        |        |
| hardpoint  |     |       F7C-M Super Hornet       | small |              | 78886.0 |      |        |        |
| hardpoint  |     | F7C-M Super Hornet Heartseeker | small |              | 78886.0 |      |        |        |
| hardpoint  |     |      F7C-R Hornet Tracker      | small |              | 74197.0 |      |        |        |
| hardpoint  |     |       F7C-S Hornet Ghost       | small |              | 73724.0 |      |        |        |
|    rsi     |  37 |           F7A Hornet           | small |  In Concept  | 73317.0 | 22.0 |  7.0   |  22.5  |
|    rsi     |  11 |           F7C Hornet           | small | Flight Ready | 73535.0 | 21.5 |  6.5   |  22.5  |
|    rsi     | 122 |      F7C Hornet Wildfire       | small | Flight Ready | 73535.0 | 21.5 |  6.5   |  22.5  |
|    rsi     |  15 |       F7C-M Super Hornet       | small | Flight Ready | 78466.0 | 24.0 |  6.5   |  25.5  |
|    rsi     | 177 | F7C-M Super Hornet Heartseeker | small | Flight Ready | 78466.0 | 24.0 |  6.5   |  25.5  |
|    rsi     |  14 |      F7C-R Hornet Tracker      | small | Flight Ready | 73497.0 | 21.5 |  6.5   |  22.5  |
|    rsi     |  13 |       F7C-S Hornet Ghost       | small | Flight Ready | 73454.0 | 21.5 |  6.5   |  22.5  |
| scunpacked |     |           F7A Hornet           | small |              | 73317.0 |      |        |        |
| scunpacked |     |           F7A Hornet           | small |              | 74132.0 |      |        |        |
| scunpacked |     |           F7C Hornet           | small |              | 74132.0 |      |        |        |
| scunpacked |     |      F7C Hornet Wildfire       | small |              | 74132.0 |      |        |        |
| scunpacked |     |       F7C-M Super Hornet       | small |              | 78886.0 |      |        |        |
| scunpacked |     | F7C-M Super Hornet Heartseeker | small |              | 78670.0 |      |        |        |
| scunpacked |     |      F7C-R Hornet Tracker      | small |              | 74197.0 |      |        |        |
| scunpacked |     |       F7C-S Hornet Ghost       | small |              | 73724.0 |      |        |        |
|    spat    |     |           F7C Hornet           |       |              |         |      |        |        |
|    spat    |     |       F7C-M Super Hornet       |       |              |         |      |        |        |
|    uex     |     |           F7A Hornet           |       |              |         |      |        |        |
|    uex     |     |           F7C Hornet           |       |              |         |      |        |        |
|    uex     |     |      F7C Hornet Wildfire       |       |              |         |      |        |        |
|    uex     |     |       F7C-M Super Hornet       |       |              |         |      |        |        |
|    uex     |     | F7C-M Super Hornet Heartseeker |       |              |         |      |        |        |
|    uex     |     |      F7C-R Hornet Tracker      |       |              |         |      |        |        |
|    uex     |     |       F7C-S Hornet Ghost       |       |              |         |      |        |        |
+------------+-----+--------------------------------+-------+--------------+---------+------+--------+--------+
```

TODO:

- Merge RSI IDs into all data sets
- Data validation and repair tooling
- CSV export format
