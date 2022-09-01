# Bachelor Thesis Process Mining

This repository contains artifacts of my bachelor thesis at the chair for Information Systems and Business Process Management (Prof. Helmut Krcmar).   

I wrote the thesis during the winter semester 2021/2022.  The topic of the thesis was **Simulation of Continuous Business Process Data for Process Mining in Teaching.**

This repository contains the thesis itself, the corresponding presentation, some of the simulation data as well as the source code artifacts.

My task was to develop a tool that continuously simulates process data, which gets written to a database and then is transferred to Celonis, a process mining software solution.  

I implemented the simulation tool in Python and set up an Ubuntu server that runs the tool roughly every 10 minutes. Additionally, I installed MySQL on the very same server and store the simulated data in a database. Eventually I set up a project in Celonis which pulls data from the database regularly and updates the corresponding process analysis.  

The goal of this work was to improve the teaching of process mining by using continuously updated process data instead of static, one-time generated data.  

For a quick overview of my work, read the abstract of the thesis or take a look at the presentation slides.
