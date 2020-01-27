from shapely.geometry import Polygon, Point
from shapely.ops import cascaded_union
from pygeos import Geometry, points, measurement, set_operations
import folium
p1 = Polygon([
      (
        -72.2779369,
        42.9272056
      ),
      (
        -72.2778833,
        42.9253673
      ),
      (
        -72.2757268,
        42.9254302
      ),
      (
        -72.2758663,
        42.9272685
      ),
      (
        -72.2779369,
        42.9272056
      )
    ])
p2 = Polygon([
      (
        -72.2751045,
        42.9279991
      ),
      (
        -72.2768211,
        42.9270328
      ),
      (
        -72.2763169,
        42.9265772
      ),
      (
        -72.2766709,
        42.9261844
      ),
      (
        -72.2758234,
        42.9255087
      ),
      (
        -72.2748256,
        42.9267971
      ),
      (
        -72.2751045,
        42.9279991
      )])

def merge(p1, p2, intersection_with_former=True):
    if intersection_with_former:
        p2new = p2.difference(p1)
        p1new = p1
    else:
        p1new = p1.difference(p2)
        p2new = p2
    return p1new, p2new

p1new, p2new = (p1.difference(p2), p2.difference(p1))

pyg_p1new = Geometry(p1new.wkt)
pyg_p2new = Geometry(p2new.wkt)

x = p1.intersection(p2)


# converting to list of lists
coordinates = x.exterior.coords
minlat, minlon, maxlat, maxlon = (coordinates[0][0], coordinates[0][1], coordinates[0][0], coordinates[0][1])
print(coordinates[0])
for i, coord in enumerate(coordinates):
    minlat = min(minlat, coord[0])
    minlon = min(minlon, coord[1])
    maxlat = max(maxlat, coord[0])
    maxlon = max(maxlon, coord[1])


delta = 0.00001
lat = minlat

count1 = 0
count2 = 0
p1new_buffer = []
p2new_buffer = []
while lat < maxlat:
    
    lon = minlon
    while lon < maxlon:
        point = points(lat+(delta/2), lon+(delta/2))
        poly = Polygon([
            (lat, lon),
            (lat + delta, lon),
            (lat + delta, lon + delta),
            (lat, lon + delta)
        ])
        pyg_poly = Geometry(poly.wkt)
        d1 = measurement.distance(pyg_p1new, point)
        d2 = measurement.distance(pyg_p2new, point)
        if d1 > d2:
            count1 += 1
            p2new_buffer.append(pyg_poly)
        else:
            count2 += 1
            p1new_buffer.append(pyg_poly)
        lon += delta
    lat += delta


print(count1, count2)
p1new_buffer.append(pyg_p1new)
pyg_p1new = set_operations.union_all(p1new_buffer)

p2new_buffer.append(pyg_p2new)
pyg_p2new = set_operations.union_all(p2new_buffer)
print(pyg_p1new, pyg_p2new)
