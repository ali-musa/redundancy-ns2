redundancy 
==========
####requires
tdom for tcl<br />
matplotlib and mpltools for plotting<br />
python

####setting up
copy the ns2.35_mods patch to the relevant directories<br />
make and install ns

####For a single run
ns llvr.tcl "%load" "seed value -- optional"<br />

####To spawn batch runs
first edit runme.py and set cluster=0, then use the following command:<br />
python runme.py<br />

####For analysis
cd automated_scripts/<br />
python analyze_logs.py "experiment number(s) {coma seperated}"<br />
* expects a directory structure: /logs/expX/
* where X is the experiment number specified
* expX/ should contain:
 * config.xml with paramaters of the experiment
 * all the ends and starts files generated by running the experiment
* it will create a directory analysis/ inside of expX/
 * analysis/ will contain the analysis for individual seeds
 * and an averages/ directory with average analysis over all the seeds

####For plotting
cd automated_scripts/<br />
python generate_plots.py "base experiment number" "experiment number(s) {coma seperated}"<br />
* expects a directory structure: /logs/expX/analysis/averages/
* where X is the experiment number specified
* averages/ should contain afct.csv and other analysis files generated by analysis of the experiment.

####To change run settings
edit config.xml<br />
edit automated_scripts/run_batch_loads.sh or automated_scripts/run_batch_loads.py {only if needed}<br />
edit runme.py<br />
* overwrites most of the config.xml parameters
* need not edit this for single run
* expects experiment number to be an integer, increments it by 1 before runnnig

####To change plot settings:<br />
edit automated_scripts/generate_plots.py<br />

config notes
------------
#### main_config.xml
edit this to point to the logs and plots directories.

#### config.xml
**tag: options "comment optional"**<br />
* file_size_distribution: deterministic or pareto<br />
* copies: any integer greater than 0<br />
* use_different_priorities: 1 or 0<br />
* cancellation: 1 or 0<br />
* purging: 1 or 0 "setting this to 1 will automatically enable cancellation"<br />

ns code contributions
------------
all ns2.35 code contributions are marked with comment "musa"
