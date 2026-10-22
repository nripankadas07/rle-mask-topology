# rle-mask-topology

Decode uncompressed column-major COCO RLE and report connected components, perimeters, holes and bounding boxes under explicit dual connectivity.

For computer-vision dataset curators inspecting a small COCO-style binary mask.

## Quickstart

Python3.10+; no runtime dependencies or external service. The wheel build needs setuptools and wheel from the normal Python registry. Linux shell:

```sh
git clone https://github.com/nripankadas07/rle-mask-topology.git
cd rle-mask-topology
python -m venv .venv
. .venv/bin/activate
python -m pip install .
rle-mask-topology example.json
```

The invented3x3 ring has area8,one component,one hole and unit-edge perimeter16. [Expected report](example-output.json).

## Input and interpretation

Start from [example.json](example.json). Inputs are read only. JSON files are UTF8,<=1MiB; duplicate/unknown keys, booleans in integer fields and nonfinite constants reject.

size=[height,width],each1..512; integer counts list<=262145, starting with background and alternating, zeros allowed, exact sum=height*width. No compressed counts strings,polygons,images,labels or batch masks. Decode fully to bounded raster. Foreground4-connected,background8-connected; holes are background components that do not touch raster edge. Euler=foreground components-holes. Perimeter counts unit foreground/background/outside edges. Bounding box[x,y,width,height],<=4096 foreground components. Not a continuous/polygon topology or diagonal perimeter estimator.

Exit0 means analysis completed, including any infeasibility, NOT_LINEARIZABLE, UNKNOWN or reference finding. Inspect the report fields; exit0 is not a health assertion. Exit2 means malformed/unsupported input or I/O failure, with JSON error on stderr and no partial report. No live-system operations, network requests or credential reads occur. Reports may expose supplied identifiers and bytes; review before sharing.

## Verification

```sh
python -m unittest -v
python -m compileall -q rle_mask_topology.py
python -m pip wheel --no-deps . -w dist
```

50 seeded pixel-set oracles, bounding boxes/ring/diagonal connectivity, column-major decoding, empty/full/zero-run masks and malformed RLE rejection. [Validation record](VALIDATION.md). CI runs Python3.10/3.12/3.14 on Linux and the installed console outside checkout. Windows/macOS, production workloads and competitor performance remain untested.

## Scope and provenance

Alpha utility. Original AI-assisted code and invented fixtures; standard algorithms independently reimplemented. No third-party implementation/prose copied. MIT. [Candidate brief](BRIEF.json), [research](RESEARCH.md), [support](SUPPORT.md), [contributing](CONTRIBUTING.md), [security](SECURITY.md).

No existing portfolio utility computes segmentation-mask topology. The users and numerical contract differ from temporal scheduling, operation histories, audio markers and BER structures.
