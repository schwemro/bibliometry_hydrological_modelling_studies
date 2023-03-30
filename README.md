# Bibliometric analysis of hydrological modelling studies

## Data retrieval

Data has been retrieved from [Web of Science](https://www.webofscience.com/) by searching for publications since year 2010 querying the fields
hydrologic model OR hydrological model OR hydrologic modeling OR hydrological modelling in the following journals:

- Journal of Hydrology
- Hydrological Processes  
- Water Resources Research  
- Hydrol. Earth Syst. Sci.  
- Hydrological Sciences Journal  
- Journal of Hydrometeorology  
- Environmental Software & Modelling  
- Geophysical Research Letters  
- Advances in Water Resources  
- Environmental Research Letters  
- Geosci. Model Dev.

and searching the following models in the above mentioned journals:
- Hydrogeosphere
- HYDRUS
- mesoscale Hydrologic Model (mHM)
- ParFlow

All search queries have been repeated by selection open-acces publications only. Data has been written to text format using the build-in function `Analyze results` (Category: Publication years).
Since code and data availability statements are not recorded in the [Web of Science](https://www.webofscience.com/) database, I manually
inspected open-acces publications of mesoscale Hydrologic Model (mHM)
and ParFlow.

## Data analysis

`bibliometry.py` runs a simple analysis and visualises cumulative
number of publications since introduction of code and data sharing platforms.