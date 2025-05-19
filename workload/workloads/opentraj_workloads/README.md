# OpenTraj - HumanRobotTrajectories
This repository contains a collection of open-source datasets from OpenTraj for human trajectory prediction in shared human-robot environments.


## Overview
As Industry 4.0 advances, shared human-robot environments in manufacturing are becoming more common, with robots, collaborative robots(cobots), autonomous guided vehicles (AGVs), and AI-powered systems. In such dynamic workplaces, Human Trajectory Prediction (HTP) is critical to ensure safety, efficiency, and smooth collaboration.
The workload focuses on processing large-scale human trajectory data from the OpenTraj dataset to develop predictive models for movement classification and trajectory forecasting. We aim to classify individuals as stationary or moving based on features we engineer, such as velocity and acceleration, to predict their movement patterns over time. 

## Datasets
Utilizing publicly available OpenTraj datasets, a benchmark that includes multiple datasets for human trajectories, we can access various data sources suitable for trajectory modeling and prediction in manufacturing environments. The OpenTraj dataset is a collection of data useful for predicting human movement from various environments to understand patterns in human motion, for Human Trajectory Prediction (HTP) task, and provides tools to load, visualize and analyze datasets. Each dataset has its unique structure, including formats such as JSON, XML, and text files. 

Eight OpenTraj datasets were used to simulate diverse human movement patterns:
-  **ETH:** Walking pedestrians scenes from a top-down perspective.
-  **PETS 2009:** Different crowd activity scenarios.
-  **HERMES:** Controlled experiments of Pedestrian Dynamics (Unidirectional and bidirectional flows)
-  **L-CAS:** Multisensor People Dataset Collected by a Pioneer 3-AT robot
-  **Edinburgh:** Human movement data in a university building.
-  **Town Center:** CCTV footage of pedestrians in a busy downtown area.
-  **Wild Track:** Surveillance video dataset of students recorded outside the university building.
-  **ETH-Person:** Multi-person data collected from mobile platforms.


## Purpose
The primary objective of this framework was to classify human movements as either stationary or moving and to predict trajectory patterns over time based on extracted motion features, particularly velocity and acceleration.


## Key insights
Human trajectory prediction framework was developed for  energy-efficient  manufac-turing applications, such as crowd tracking, robot navigation,anomaly detection in human-robot interactions, and predictive analytics for dynamic environments,  to minimize unnecessary robotmovements,  enhance  cobot  efficiency,  and  facilitate  real-timedecision-making, enhances  operational  efficiency and  real-time  energy-efficient  robotic  movement  and  promotes sustainability  on  the  factory  floor, further enhancing worker safety  and  reduces  robotic  power  consumption  by  optimizing movement patterns. Overall, these findings provide a strong foun-dation for trajectory-aware manufacturing systems and supportthe  shift  toward  AI-powered,  data-driven,  and  energy-efficientsmart  manufacturing. 
These eight publicly available OpenTraj datasets were used to simulate diverse human movement patterns for robotics tasks that involve tracking trajectories for smart manufacturing use case. The final combined dataset consists of 36,761,429 rows and has a total of 2.1 GB. These datasets were preprocessed to calculate velocity, acceleration, and movement labels (stationary vs. moving).
A Random Forest Classifier was trained using engineered features such as velocity and acceleration. Hyperparameter optimization was conducted using RandomizedSearchCV, and the model’s performance was evaluated using metrics like precision, recall, F1-score, and accuracy.


## Metrics
-  **Speed and Acceleration:** Analyzing the speed and acceleration of human movements can provide insights into humans movement patterns, helps for real-time robot adjustments.
-  **Trajectory Predictability:** Assessing predictable trajectories to understand humans movement in a given environment, humans interact with robots, which is crucial for robots to anticipate human actions and in 

Performance metrics, including accuracy, recall, and F1-score, are used to assess the model

## Framework
Preprocessed these datasets, which contained raw positional data in the form of (X, Y) coordinates and timestamps. From this, we derived key features such as velocity, acceleration, proximity, and direction angle. These features labeled human movement behavior—0 for stationary and 1 for moving. We then trained two models: (1) a Random Forest Classifier, which performed binary classification of movement states, and (2) an LSTM model, which leveraged sequential dependencies in movement data to predict the likelihood of transitioning between stationary and moving states. Finaly model’s performance was evaluated using metrics like precision, recall, F1-score, and accuracy.
