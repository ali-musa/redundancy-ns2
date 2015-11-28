redundancy
==========
requires:
tdom for tcl
matplotlib and mpltools for plotting


To spawn batch runs:
python runme.py

For analysis:
cd automated_scripts/
python analyze_logs.py "experiment numbers"

For plotting:
cd automated_scripts/
python generate_plots.py "base experiment number" "experiment numbers"


To run change settings:
edit config.xml
edit runme.py
edit automated_scripts/run_batch_loads.sh or automated_scripts/run_batch_loads.py

To change plot settings:
edit automated_scripts/generate_plots.py