### Introduction

A series of experiments done to split a polygon into two parts, based on a parameter p(0 < p < 1>), such that the common area or the cavity a polygons form are split in the ratio `p:1-p`.

This problem often comes up when two nearby station boundaries in a supply chain are to be drawn/merged/edited, without a lot of manual efforts.

### Illustration

These two polygons say A(red) and B(yellow) have intersections and cavity between them. The goal is to split these parts into two parts with area ratio `p`. 

![prior polygons](https://i.imgur.com/Rn4CstQ.png)

With ratio 0.5, (to split the areas into equal halves), this should be the result.

![resultant polygons](https://i.imgur.com/a65Klmt.png)

### Approach

- Since this problem can be made more generic in a way that the area in between two polygons can be split very smartly if someone considers parameters associated with each grain(points with finite areas within a polygon), like say affluence index of that grain, dividing the polygon into grids is the way to go. This problem can be modelled best as Voronoi Diagrams.
- As seen in the earlier commits, the intersecting and cavity areas were identified using common geometric operations like union,intersection,hulls. The area was [divided into grids manually](https://github.com/plant99/merge-polygons/blob/c67b5d0993d75cdcb35a7ce986d063192f2e5f09/merge_polygon.py#L94) and nearest distance from this point was calculated from exclusive polygons (A - A∩B, B- A∩B), say d1 and d2. If `d1 > p * d2`, the grain would be merged to A, else it'd be merged with B.
- Since it was later understood that, there was a lot of manual effort spent on 'gridding' the area, [h3](https://github.com/uber/h3) was used. This also meant, we can integrate other features like controlling size of the fine grains with different resolutions. [reference](https://github.com/plant99/merge-polygons/blob/060c0222bfd3d8616888298ae7b4e5de3428efe5/merge_polygons_h3.ipynb)
- There were further optimizations made for edge cases, for instance splitting an area into grids with h3 results in protruding shapes which have to be trimmed from A∪B. [reference](https://github.com/plant99/merge-polygons/blob/060c0222bfd3d8616888298ae7b4e5de3428efe5/merge_polygons_h3_trapped.ipynb)