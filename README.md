redundancy 
==========
requires:<br />
tdom for tcl<br />
matplotlib and mpltools for plotting<br />

To spawn batch runs:<br />
python runme.py<br />

For analysis:<br />
cd automated_scripts/<br />
python analyze_logs.py "experiment numbers"<br />

For plotting:<br />
cd automated_scripts/<br />
python generate_plots.py "base experiment number" "experiment numbers"<br />

To run change settings:<br />
edit config.xml<br />
edit runme.py<br />
edit automated_scripts/run_batch_loads.sh or automated_scripts/run_batch_loads.py<br />

To change plot settings:<br />
edit automated_scripts/generate_plots.py<br />