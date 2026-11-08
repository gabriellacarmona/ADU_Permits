# Download assessor parcel polygons for the 3 focus CPAs (paged geojson queries)
import json, urllib.request, urllib.parse, time, sys

BASE = "https://services.arcgis.com/RmCCgQtiZLDCtblq/ArcGIS/rest/services/ASSR_PARCELS_25_View/FeatureServer/0/query"
FOCUS = ["Arleta - Pacoima", "Northeast Los Angeles", "West Adams - Baldwin Hills - Leimert"]

cpas = json.load(open("cpa_boundaries.geojson"))
# geojson polygon -> esri rings
def to_esri(geom):
    if geom["type"] == "Polygon":
        rings = geom["coordinates"]
    else:  # MultiPolygon
        rings = [r for poly in geom["coordinates"] for r in poly]
    return {"rings": rings, "spatialReference": {"wkid": 4326}}

def post(params):
    data = urllib.parse.urlencode(params).encode()
    for attempt in range(4):
        try:
            with urllib.request.urlopen(urllib.request.Request(BASE, data=data), timeout=120) as r:
                return json.load(r)
        except Exception as e:
            print("  retry", attempt, e, file=sys.stderr); time.sleep(3)
    raise RuntimeError("query failed")

out = {"type": "FeatureCollection", "features": []}
for name in FOCUS:
    feat = next(f for f in cpas["features"] if f["properties"]["NAME_ALF"] == name)
    geom = json.dumps(to_esri(feat["geometry"]))
    offset, n = 0, 0
    while True:
        j = post({
            "where": "1=1", "geometry": geom, "geometryType": "esriGeometryPolygon",
            "inSR": "4326", "spatialRel": "esriSpatialRelIntersects",
            "outFields": "AIN,APN,UseCode", "outSR": "4326",
            "geometryPrecision": "6", "maxAllowableOffset": "0.000005",
            "resultOffset": str(offset), "resultRecordCount": "2000", "f": "geojson"})
        feats = j.get("features", [])
        for f in feats:
            f["properties"]["cpa"] = name
        out["features"].extend(feats)
        n += len(feats); offset += len(feats)
        more = j.get("properties", {}).get("exceededTransferLimit", False) or len(feats) == 2000
        print(f"{name}: +{len(feats)} (total {n})", flush=True)
        if not more or not feats: break
print("TOTAL", len(out["features"]))
json.dump(out, open("parcels_focus.geojson", "w"))
