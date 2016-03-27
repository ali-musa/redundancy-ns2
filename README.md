redundancy 
==========
####requires
tdom for tcl<br />
matplotlib and mpltools for plotting<br />

####To spawn batch runs
python runme.py<br />

####For analysis
cd automated_scripts/<br />
python analyze_logs.py "experiment numbers"<br />

####For plotting
cd automated_scripts/<br />
python generate_plots.py "base experiment number" "experiment numbers"<br />

####To change run settings
edit config.xml<br />
edit runme.py<br />
edit automated_scripts/run_batch_loads.sh or automated_scripts/run_batch_loads.py<br />

To change plot settings:<br />
edit automated_scripts/generate_plots.py<br />

config notes
------------
#### tag: options "comment optional"
file_size_distribution: deterministic or pareto<br />
copies: any integer greater than 0<br />
use_different_priorities: 1 or 0<br />
cancellation: 1 or 0<br />
purging: 1 or 0 "setting this to 1 will automatically enable cancellation"<br />
