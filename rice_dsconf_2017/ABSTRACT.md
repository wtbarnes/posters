---
documentclass: scrartcl
geometry:
 - margin=1in
title: "Timelag Analysis of Global Hydrodynamic Simulations of Active Regions in the Solar Corona"
subtitle: Rice Data Science Conference, 9-10 October 2017, Houston, TX, USA
author:
 - W. T. Barnes
 - S. J. Bradshaw
---

## Abstract
The question of how the solar corona is heated to millions of Kelvin (while the solar surface remains at several thousand Kelvin) is one that has puzzled astronomers and astrophysicists for nearly a century. Within the past decade, advances in both space-based instruments and computing power have resulted in an explosion of the quantity and quality of both observational and simulation data. A key component to solving the coronal heating problem is detailed and statistical comparisons between observations and simulations. In this poster, we present global hydrodynamic simulations of impulsively-heated active region cores and a subsequent time-delay analysis using cross-correlation techniques. In particular, we use a hydrodynamic model to simulate the response of many thousands of coronal "loops" (the building blocks of the solar atmosphere) to build up a global time-dependent solar active region model. We then use the resulting thermodynamic quantities to forward model (i.e. simulate the response of an observing instrument) the intensities in several channels of the Atmospheric Imaging Assembly (AIA) instrument onboard the Solar Dynamics Observatory (SDO) spacecraft. Finally, we compute the time delays between channel pairs using a cross-correlation technique in order to facilitate detailed comparisons with observations (e.g. Viall and Klimchuk, 2012, 2017) and understand the resulting plasma cooling patterns in our simulated active regions.

Generating, storing, and accessing this amount of simulation data is non-trivial. Each run of our model generates a four-dimensional dataset (2 spatial dimensions + 1 time dimension + 1 spectral dimension) that is 10-100 gigabytes in size. Furthermore, we run our model over a set of heating parameters in order to assess the viability of different heating scenarios, adding yet another dimension. To streamline this simulation and analysis process, we have built a simulation pipeline in Python that coordinates the configuration of the simulations, the reshaping of the data, and provides an interface to the results. Our pipeline heavily leverages several open source scientific Python libraries, including NumPy, scipy, Astropy, and SunPy, as well as the h5py library for reading and writing HDF5 files. Additionally, our simulation pipeline scales horizontally very efficiently and has recently been scaled to 64 cores using the dask library for distributed and parallel computing.

The focus of this poster will be twofold. First, we will discuss the details of the coronal heating problem, our methods for simulating SDO/AIA intensities from solar active regions, and the analysis of these simulations using the cross-correlation and time delay technique. Second, we will give an overview of the logistical challenges we faced when dealing with this amount of data and how we sucessfully scaled our simulation pipeline.