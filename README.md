# retirement-planner
Simulate and visualize many retirement scenarios accounting for many factors.

Key points:
* interactive.py is the plotly/dash app
* simulate.py and brute_force_sweep_sim.py are intended to sweep a range of values and find some optima
* constants.py includes (mostly) average numbers but some are random/extreme
* money.py is a nice set of mathematical functions focused on compound growth


Want to help?
* Double check my math and assumptions
* Suggest improvements to the graph (I'm learning plotly though, so I'd prefer to implement it myself)
* Rewrite or improve the simulators
* Incorporate this multi-parameter sweep into a visualization
* Get some more realistic defaults
* Add mortgage calculation
* It might be early for this but any way to incorporate details like tax savings or changes, enabling/disabling house
purchases, car purchases, or social security would be useful
* Allow users to plot multiple scenarios
* Help with searching for optima. This is actually really hard. For example, say each value in constants.py has a range
except some things like age. What combination(s) of settings will provide the earliest retirement, latest survivability,
biggest house, etc. Bear in mind that not only is the search space quite large but some factors have to be ignored at 
times. In the simulator, you can see that retiring later has the most impact on how long you'll be able to support 
yourself. This is a little uninteresting so perhaps some more interesting metrics could be found. 



**DISCLAIMER: Nothing in this repo constitutes reliable financial advice.**

This project is in its infancy and is a complete mess. I'm still learning plotly/dash, figuring out what I want this to 
do exactly and how best to achieve it. Suggestions welcome!

Values in constants.py are not and should not be representative of any individual and have been pulled by the 
"first thing that popped up in Google" approach.
