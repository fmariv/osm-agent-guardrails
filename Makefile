.PHONY: test validate demo

test:
	PYTHONPATH=src python -m unittest discover -s tests -v
	PYTHONPATH=src python -m osm_guard validate-skills skills
	python tools/validate_skills.py
	python -m compileall -q src tools examples/python examples/offline-poi-app
	PYTHONPATH=src python tools/evaluate_offline.py

validate:
	PYTHONPATH=src python -m osm_guard validate-skills skills
	python tools/validate_skills.py

demo:
	PYTHONPATH=src python -m osm_guard recommend --workflow scheduled --area-km2 800 --daily-runs 10
	python examples/python/local_xml_pois_to_geojson.py
