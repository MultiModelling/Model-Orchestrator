# Airflow MMvIB Orchestrator Service

A generic Airflow Workflow Orchestrator with integrated Handler and Model Adapter services written in 
Python. Extended with in-flow cycle properties for the standard DAG framework.

---

## Getting started

This project requires Airflow, suggested is to run Airflow on Docker. 

### Requirements
- Python 3.10
- Docker 4.6+
- Airflow 2.2.4+
- WSL 2 (Win Only)

---

## Usage

To use the model orchestrator, first we need to provide permissions to mount several shared folders from 
which the orchestrator can pull data, graphs and plugins. Running the following batch script gives 
the required read-write permission when using the WSL2 version of Docker.

**WSL Configuration (Windows Only)**
```
.\docker-init.bat
```

We can then proceed to deploy through Docker. First initialize the databases and create the user accounts 
using the airflow-init container. Run the following command and wait for it to finish.

**Airflow Initialization**
```
docker-compose up airflow-init
```

After that the Airflow orchestrator can be deployed.

**Airflow Deployment**
```
docker-compose up -d
```

By default the command-line interface is reachable on [http://localhost:8080/](http://localhost:8080/).
In addition, a shared bash or shell command line interface can be interacted with by using `docker exec` 
on any of the Airflow services. For example:

```
BASH:      docker exec -it model-orchestrator_airflow-worker_1 bash
SHELL:     docker exec -it model-orchestrator_airflow-worker_1 /bin/sh
```

In Airflow, all directed acyclic graphs (DAGs) are defined in the `./dags` folder. These DAGs can be 
ran from the user interface by selecting the appropriate dag and then clicking the run option (▶) and 
then selecting Trigger DAG. This can also be parameterized with a JSON specification by selecting Trigger
DAG /w Config. 

---

## ETM ESSIM Demo

To demonstrate the model orchestrator, there is a demo available under the `etm_essim_demo` DAG. The 
complete specification of this demo is found in [`./dags/etm_essim_demo.py`](https://github.com/MultiModelling/Model-Orchestrator/blob/main/dags/etm_essim_demo.py). This demo is based on the 
concept of model-handler interaction. Inside the task graph nodes of a DAG, handlers are instantiated 
that interact with external handlers.

First make sure all the adapters and infrastructure is up and running by downloading the respective 
repositories and running the Docker containers with `docker-compose up -d`:

* minio-object-store
* etm-price-profile-adapter
* esdl-add-price-profile-adapter
* essim-adapter

Now we can run the demo by running the DAG. For this we also need the appropriate configuration file, 
which can be found in [`./common/configs/etm_essim_demo.json`](https://github.com/MultiModelling/Model-Orchestrator/blob/main/common/configs/etm_essim_demo.json). We copy this configuration and then in 
Airflow we select the `etm_essim_demo` DAG. We then select the run button (▶) and select to Trigger 
DAG /w Config. In the config box we paste the JSON configuration that we have previously copied. 
Finally, by pressing `Trigger` the DAG will be scheduled to run by the orchestrator.

From the user interface the status of the run can be monitored, and the log of any specific task can 
be analyzed by selecting the task from the Tree or Graph view in the current run. From there the 
log option is available, which provides all logging messages for that specific task.

All inputs and outputs are written to and loaded from minio, which is locally available at 
[http://localhost:9090](http://localhost:9090).


---

## Milestones

- [x] Trial Workflow Cycle
- [x] Implement Handler Wrapper
- [x] Generic Handler Services
  - [x] REST API
  - [ ] Message Bus
- [x] Dynamic Adapter Register
- [x] DB Ingress/Egress Wrappers
- [x] Execution order after Trigger
- [x] Managing Parallel Workflows
- [x] Syncing from git Repository
- [ ] Advanced User Run Management

***
