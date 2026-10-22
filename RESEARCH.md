# Research — 22 October 2026

Demand is **inferred** from this workflow: Area alone hides disconnected fragments and enclosed holes; row/column order mistakes can silently move a mask.

[Exact stars-desc GitHub query](https://github.com/search?q=RLE%20mask%20sort%3Astars-desc&type=repositories), observed 2026-10-22T06:18:36.315Z. Highest-star relevant comparable found in the inspected pool: `opencv/opencv`. Keywords are narrow; established comparables were supplemented directly. The difference-constraints keyword results were mostly unrelated and do not establish market coverage.

| Comparable | Stars | Last push | GitHub license metadata | Workflow and setup |
| --- | ---: | --- | --- | --- |
| [opencv/opencv](https://github.com/opencv/opencv) | 91282 | 2026-10-22T06:05:48Z | Apache-2.0 | Broad compiled computer-vision library; connected component APIs expose4/8 connectivity and statistics. |
| [cocodataset/cocoapi](https://github.com/cocodataset/cocoapi) | 6388 | 2024-04-17T05:14:06Z | NOASSERTION | COCO dataset APIs and C mask algorithms with Python/Matlab/Lua examples; source-build instructions. |
| [isarandi/rlemasklib](https://github.com/isarandi/rlemasklib) | 26 | 2026-10-16T14:37:39Z | NOASSERTION | Python/Cython operations directly on compressed RLE masks, pip setup and examples. |

## Choice and tradeoffs

Decode uncompressed column-major COCO RLE and report connected components, perimeters, holes and bounding boxes under explicit dual connectivity. No existing portfolio utility computes segmentation-mask topology. The users and numerical contract differ from temporal scheduling, operation histories, audio markers and BER structures.

The established alternatives are broader and may be the right choice for their supported ecosystem. Our small CLI offers one dependency-free runtime and an inspectable JSON report for the stated subset. It sacrifices generality and may reject valid real-world input outside that subset. READMEs/current docs/source and sampled issues were inspected for workflow context; this does not prove competitor feature absence. ATL explicitly supports WAV CUE/LIST, NetworkX explicitly returns negative cycles, and RLEMaskLib performs mask operations without full raster expansion. Our example proves only our behavior.

Installability and first-result instructions are documented above and in upstream READMEs. Competitor clean installs, time to first useful result, reliability, support response and performance were **not measured**. No superiority, adoption or global ranking claim. Stars are research context only. [Exact provenance and sampled issues/PRs](RESEARCH_PROVENANCE.json). Inconclusive GitHub license metadata is not a legal conclusion; NetworkX README states BSD3, Z3 README MIT, and Knossos README EPL. No implementation is reused.

Primary references:
- https://github.com/cocodataset/cocoapi/blob/master/common/maskApi.c
- https://docs.opencv.org/4.x/d3/dc0/group__imgproc__shape.html
