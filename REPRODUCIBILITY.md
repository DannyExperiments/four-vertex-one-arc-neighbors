# Reproduce the checks

Use Python 3.10 or later for the optional bit-mask census. Run from the repository root.

```sh
python3 -I verification/src/replay.py
python3 -I verification/src/class_census.py
python3 -I scripts/verify_repository.py
```

The first replay tests all 24 queried pairs and conditions for the displayed graphs and each one-arc edit from the fixed input. The second enumerates labelled graphs, rejects cycles, and computes d-separation signatures by ancestral moralization. It compares the globally nearest distinct signature to the best edit over all starting representatives. It verifies 29,281 DAGs and 8,782 signatures at size five, in addition to sizes two through four. [Core replay output](verification/logs/replay.txt) · [Census output](verification/logs/class_census.txt) · [Build the manuscript](paper/BUILD.md)
