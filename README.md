# FencingPulse

step-1
```
cd <path>
```

step-2
```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

step-3
```
PYTHONPATH=. python scripts/train_phase1.py --csv data/sample/phase1_text_sample.csv --output models/phase1_logreg.joblib
PYTHONPATH=. python scripts/train_phase3.py --csv data/sample/phase3_match_sample.csv --output models/phase3_logreg.joblib
```

step-4
```
PYTHONPATH=. streamlit run app/streamlit_app.py
```
