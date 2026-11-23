# OSM source decision matrix

| Use case | Good first option | Avoid as default | Key questions |
| --- | --- | --- | --- |
| Monthly national building inventory | Regional PBF + local processing | Public Overpass | Geometry completeness, update cadence |
| Interactive commercial POI explorer | Local PostGIS/GeoParquet or provisioned service | Per-user public Overpass | Query volume, freshness, SLA |
| One-time low-volume POI exploration | Bounded Overpass (subject to policy) | Planet-wide scan | Bounding box, feature count |
| Road-network routing experiments | OSMnx with local PBF for repeated work | Re-downloading each execution | Graph profile, simplification |
| Basemap for a website | Appropriate hosted tiles or own tiles | Overpass | Map-style license, tile policy, attribution |
| Latest tag changes | Replication/update pipeline | Full daily overpass dump | Operational burden, diff handling |

Explain the tradeoffs for the *actual* problem. Data openness does not imply free unrestricted compute on community servers. Do not claim any specific absolute Overpass rate is guaranteed safe. Review operators' current policies before any live use.
