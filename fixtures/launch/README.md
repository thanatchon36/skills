# csvdiff

You exported the same table twice and need to know which rows changed. csvdiff compares two CSV
files by a key column and prints added, removed, and changed rows.

```sh
git clone https://github.com/example-dev/csvdiff && cd csvdiff
python3 csvdiff.py examples/old.csv examples/new.csv
```

Requires Python 3.9+. No dependencies.

## Example

```text
+ id=4
- id=2
~ id=1  price: '1.20' -> '1.25'
1 added, 1 removed, 1 changed
```

Exit code 1 when there are differences, so it works as a CI check.

## Limitations

- Loads both files into memory; not for multi-gigabyte files.
- One key column only.

## License

[MIT](LICENSE)
