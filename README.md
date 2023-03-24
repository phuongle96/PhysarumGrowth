# PhysarumGrowth
Fast algorithm for calculating the Reeb graph of Physarum evolution

Here are descriptions for different sub-folders in the root folder:
* Example: Simple test data set
* Data: Main 3 data sets of sequences of images for Physarum growth.
* reeb_graph_1d: Contain all necessary files to run the algorithm
* Image: All the output produced by the algorithm

The reeb_graph_1d further contains the following files:
* disjointSet.py: Union-find algorithm for finding connected components.
* hierarchy.py: all the necessary functions to construct a divide-and-conquer algorithm.
* reebGraph.py: contains the main algorithm for extracting the Reeb Graph of the evolution.
* main.py: the main interface to run algorithm on 3 data sets.
