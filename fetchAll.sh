#!/bin/bash

sudo python3.5 fetchPackages.py cran
sudo python3.5 fetchPackages.py rubygems
sudo python3.5 fetchPackages.py npm
sudo python3.5 fetchDependencies.py cran
sudo python3.5 fetchDependencies.py rubygems
sudo python3.5 fetchDependencies.py npm