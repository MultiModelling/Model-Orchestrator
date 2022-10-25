# Model-Repository
Repository for DAG Definitions





# DOTS Code Generator

A service code generator based on the open source [**cookiecutter**](https://github.com/cookiecutter/cookiecutter), [**protobuf**](https://github.com/protocolbuffers/protobuf) and [**black**](https://github.com/psf/black) libraries. Generates, compiles and lints a boilerplate service project which can then be supplied with customizable naming schemes, service calculations and requirements.



## Getting started

To generate projects, only Python3.9+ with [*pip*](https://pip.pypa.io/en/stable/installation/) and [*virtualenv*](https://virtualenv.pypa.io/en/latest/installation.html) are required. This will be automatically installed by running the project generation script. After running this script, you will be able to define the service calculation details to be used in the DOTS framework

### Requirements

- Python 3.9

- Docker

  

## Usage

Before proceeding, make sure that you prepare the following:

* *Active Docker Daemon*
  * The easiest way to do this is to launch the Docker Desktop application.
* *WSL/Ubuntu Terminal with Root Privileges*
  * Windows: Open WSL terminal in administrator mode.
  * Ubuntu: Login to an admin account with sudo privileges and open terminal.



Then the following command can be ran to generate service templates.

* *[repo root folder]* Run Command on Terminal

```
./build.sh [optional arguments]
```

* Optional Arguments

	-c <path> : Config file path (optional, path, default: config.yaml)
	-o <path> : Output path (optional, path, default: .)
	-m <str>  : Generation mode (optional, [readonly, overwrite], default: overwrite)
	-k <str>  : API key for Gitlab (optional, string, default: none)" >&2



***
