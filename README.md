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

### stefan-problem

Group project for Partial Differential Equations class. 
<ul>
  <li> Stefan problem - model that describes the heat transfer and phase change phenomena occurring at the interface (a boundary moving in time) between a solid and a liquid during melting or solidification process.</li>
  <li> Attached notebook contains more detailed Stefan problem description and its solution with Crank-Nicholson scheme.</li>
  <li> Recommended to open in jupyter notebook, in VScode some LaTeX-related errors appear.</li>
</ul>

### CSoSP1

Group report for Computer Simulations of Stochastic Processes class.
<ul>
  <li> Comparison of methods for alpha stable parameters estimation. </li>
  <li> Analysis of the tails of the alpha stable variable. </li>
</ul>

### CSoSP2

Group report for Computer Simulations of Stochastic Processes class.
<ul>
  <li> Simulation of alpha stable vectors. </li>
  <li> Spectral measure estimation. </li>
</ul>

### CSoSP3

Group report for Computer Simulations of Stochastic Processes class.
<ul>
  <li> Hurst index estimation for Fractional Brownian Motion. </li>
  <li> Comparison of two methods - lag variance and rescaled range. </li>
</ul>

### Threshold_qvoter

Group project for Diffusion Processes on Complex Networks class.
<ul>
  <li> Description and implementation of the threshold q-voter model with our own modification for three types of networks - Random Graph, Barabasi-Albert and Watts-Strogatz. </li>
  <li> Contains .ipynb with implementation and .pdf with project results. </li>
</ul>

### spam

Group project for Data Mining class.
<ul>
  <li> Analysis of  <i>Spambase</i> dataset. </li>
  <li> EDA and classification (spam vs nonspam e-mails) using four classifiers - KNN, Random Forest, LDA, QDA. </li>
</ul>

### neural_net

My implementation of a simple neural network for MNIST handwritten numbers classification (Machine Learning class).

### cnn

Classification of cifar10 dataset images using Cpnvolutional Neural Network built in keras (Machine Learning class).

### rnn

Prediction of Tesla open stock prices using simple RNN, LSTM and GRU models, built in keras (Machine Learning class).

### GoL

My implementation of Conway's Game of Life, done for Agent Based Modelling class.
<ul>
  <li> gol.ipynb - implementation </li>
  <li> grids - initial grids in .txt files </li>
  <li> gifs - resulting gifs </li>
</ul>

### schelling

My implementation of Schelling's separation model, done for Agent Based Modelling class.

### bass

My implementation of Bass diffusion model, done for Agent Based Modelling class.
