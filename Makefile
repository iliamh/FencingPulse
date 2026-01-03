PY=python

.PHONY: install train1 train3 run build-proto

install:
	$(PY) -m pip install -r requirements.txt

train1:
	$(PY) scripts/train_phase1.py --csv data/sample/phase1_text_sample.csv --output models/phase1_logreg.joblib

train3:
	$(PY) scripts/train_phase3.py --csv data/sample/phase3_match_sample.csv --output models/phase3_logreg.joblib

run:
	streamlit run app/streamlit_app.py

build-proto:
	$(PY) scripts/build_prototypes.py --input data/sample/sample_video.mp4 --output_dir models/prototypes