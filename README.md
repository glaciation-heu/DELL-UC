# UC2: Data-driven energy-efficient manufacturing

```python
.
├── custom                # Java code for custom processor 
├── DAYTON.ttl            # dummy data for triple store
├── fuseki-configuration  # fuseki configuration file
├── input                 # dummpy input data for data flow test
├── NiFi_Flow.json        # exported NiFi flow file
├── nifi-jsonld-nar-2.0.0-M2.nar # created custom processor
├── README.md
└── simulate.py           # simulation code for workload genration
```



## Introduction

This repository contains code and file related to UC2 data collection and workload generation.

* Robot navigates a manufacturing site, using Computer Vision tools (YOLO) to generate object detection results
* YOLO results (JSON files) are streamed into GLACIATION platform, more specifically, semantification or [Apache NiFi data flow management tool](https://github.com/glaciation-heu/glaciation-semantification-service/blob/main/DESCRIPTION.md) running on the platform
* Apache NiFi has a ```HTTPListening``` component to take the input and store the results into DKG
* [Example Workload repo](https://github.com/glaciation-heu/glaciation-uc2-workload-service/blob/main/WORKLOAD.md)
* UC2 data/graphs stored in DKG needs to start with ```https://glaciation-project.eu/uc/2/```, so that it is not removed from DKG during periodical clean-up of DKG 



## Requriements

* Apache NiFi 2.0.0-M2
* Custom processor needs to be in ```extensions``` folder


## Apache NiFi data flow
Check the [semantification component repo](https://github.com/glaciation-heu/glaciation-semantification-service/blob/main/DESCRIPTION.md) for more details

## UC2 ontology for storing YOLO results
![UC2Ontology](20241023_ontology.png)
* Use case 2 ontology with some extentions following the upper ontology defined in T6.1
