# IOP-VRP benchmark instances

Synthetic instance inputs for integrated order picking and vehicle routing in a conveyor-fed parts-to-picker fulfillment system. This repository contains 900 baseline instances selected by the instance filenames in the experimental results workbook. The JSON files are preserved byte for byte; instances have not been regenerated for this repository.

## Instance groups

| Group | Instances | Orders per instance | SKU pool | Picking stations | Open-order capacity |
| --- | ---: | --- | ---: | --- | --- |
| small | 180 | 8, 12, 16, 20 | 20 | 3 | 3 |
| benchmark | 180 | 30, 60, 90, 120 | 30 | 3 | 5 |
| large | 540 | 50, 100, 200 | 50 | 3 or 5 | 3 or 5 |

Across the complete dataset, 450 instances have clustered customer locations (`C`) and 450 have random locations (`R`). Due-date settings are `tight`, `medium`, and `wide`; delivery-area side lengths are 50, 100, and 200 km (`s`, `m`, and `l`). `benchmark` is an internal group name; these are newly generated synthetic instances, not the original Solomon benchmark files. File names retain the identifiers used in the experimental workbook.

## Files

- `instances/small/`, `instances/benchmark/`, `instances/large/`: the 900 JSON inputs.
- `instances_index.csv`: filtered index, workbook row mapping, parameters and SHA-256 checksums.
- `SHA256SUMS`: checksums of the raw JSON files.
- `metadata.json`: snapshot and selection provenance.
- `tools/validate_dataset.py`: standard-library integrity checks.

## Data dictionary

Each JSON file contains `instance_id`, `scale`, `seed`, `params`, `skus_all`, and `orders`.

Important `params` fields:

| Field | Meaning |
| --- | --- |
| `n_stations`, `station_capacity` | Number of picking stations and maximum open orders at a station |
| `delta` | SKU service-slot duration in minutes; 1 in these baseline inputs |
| `n_timeslots` | Picking planning horizon measured in slots |
| `n_vehicles`, `vehicle_capacity` | Available vehicles and capacity per vehicle |
| `depot` | Distribution-center coordinates; node 0 |
| `theta`, `delta_cost` | Tardiness and vehicle-travel cost coefficients |
| `random_stream_seeds` | Component seeds retained in the original inputs |

Important per-order fields:

| Field | Meaning |
| --- | --- |
| `order_id`, `skus`, `num_skus` | Order identifier and required distinct SKUs |
| `x`, `y` | Synthetic customer coordinates |
| `weight` | Vehicle capacity consumed by the order |
| `loading_time`, `service_time` | Order loading duration and customer service duration, in minutes |
| `tw_early` | Earliest permitted customer service time; zero in all 900 baseline inputs |
| `tw_late` | Soft delivery due date, in minutes |
| `earliest_arrival` | Lower-bound estimate used in due-date generation; not the hard service lower bound |
| `due_quantile` | Random quantile used to generate the due date |

Travel time between nodes is the Euclidean distance rounded up to an integer, at the configured speed of 1 km/min. It is computed directly from coordinates. Picking completion times are service-slot indices multiplied by `delta`. Customer service, loading and delivery due dates use minutes.

These baseline inputs assume sufficient single-SKU bin supply and use a station-level picking representation. They do not include conveyor routing, robot trajectories, or transport schedules. This snapshot contains the baseline inputs only; additional sensitivity variants and solver output files are not included.

## Verify the files

Using Python 3 (no third-party packages required):

```sh
python tools/validate_dataset.py
```

To read an instance:

```python
import json
from pathlib import Path

path = next(Path("instances/small").glob("*.json"))
instance = json.loads(path.read_text(encoding="utf-8"))
print(instance["params"])
print(instance["orders"][0])
```

The manifest identifies the current input snapshot. It does not independently certify optimality, solution feasibility, or the historical solver environment.
