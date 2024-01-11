# academic-projects
This repository contains following projects made as univeristy assignments:

## Bachelor's degree

### galacats
Pygame game inspired by Space Invaders - there are several changes to game dynamics, also instead of spaceships there are cats shooting laser bullets.

### LCG
Jupyter notebook containing my implementation of Linear Congruential Generator and detailed description of the steps I'm taking throughout the way (in Polish). My tasks in this projects were: 
<ul>
  <li> implementation of pseudo-random integers generator,</li>
  <li> based on created pseudo-random generator: implementation of the generator of real numbers coming from the continuous uniform distribution, including very large numbers (up to 2<sup>64</sup>),</li>
  <li> making the seed of the generator completely random,</li>
  <li> clear, understandable graphic presentation of my results,</li>
  <li> calculating sample mean and variance (comparison to generator already implemented in Python), running Kolmogorov-Smirnov test on generated sample.</li>
</ul>

### traffic

Traffic simulation made with Pygame. Folder contains: <em>traffic.py</em> file (simulation code), <em>traffic.pdf</em> file (detailed description and analysis of the problem in Polish), <em>stuff</em> directory, containing all needed graphics, and two directories - <em>plots</em> and <em>gif</em> - to which required plots and animations are saved. My task in this project was creating a simulation of car traffic at several intersections, following given rules:
<ul>
  <li> Map is divided into identical sqares. Every car moves square by square, unless the next square is taken or the car comes across an intersection. </li>
  <li> Cars show up on entry roads according to Poisson process with different intensity functions for each entrance. </li>
  <li> Green light turns on clockwise for every intersection. Also, every traffic light has its own parameters describing green, yellow and red light duration. Those parameters are set by user. </li>
  <li> At the intersection, every car waits for the green light. When it turns on, car has to choose its next direction according to given discreet probability distribution (predefined for each intersection). </li>
  <li> After leaving the map, cars disappear and are no longer part of the traffic. </li>
  <li> User should be able to save simulation to animated gif. </li>
</ul>

### q-voter

Q-voter model on the ring. Folder contains: <em>qvoter.jl</em> file (Julia language implementation of the model, results of the simulation are written to .txt files), <em>qplots</em> file, where I create plots from existing .txt files, and <em>results.pdf</em> with created plots and their short analysis (in English).

### arma

Group project (in Polish). Our tasks here included:
<ul>
  <li> finding real data time series with seasonality and linear trend (we chose EUR/PLN exchange rate), </li>
  <li> calculating basic summary statistics for the data, </li>
  <li> data preparation: removing trend and seasonality, </li>
  <li> empirical ACF and PACF analysis, </li>
  <li> ARMA(p, q) model fitting, </li>
  <li> residual analysis. </li>
</ul>

## Master's degree
