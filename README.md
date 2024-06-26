# Data Bridge

## Welcome
This repository hosts the source code for the project we did for PostNL. We created an application that translates data requests from natural language to a SQL Query. 

## Running the application

### Data
First, the application needs a database. In order to get one, insert the raw anonimized `.csv` files to `/data`, then run `/data/db_init/db_init.py` which is a script that creates a database. Please note, this takes several minutes.

### Application Container
In order to run the application we set up a Dockerfile. The image requires an OPEN AI API key to be inserted as environment variable. Run the following commands to test the application locally:

**Building the image**

`docker build -t databridge .
`

**Running the image**

`docker run -d -p 8080:5000 -e OPENAI_API_KEY=<your-key> databridge
`

## Repository Structure
In this section you will find a high level explanation of the contents of this repository.

```txt
.
├── Dockerfile
├── README.MD
├── data
├── requirements.txt
├── services
│   ├── querier
│   └── ui
└── test
```

### Description

- **data**: In this directory all data and the related scripts are kept.
- **querier**: in this directory the source code of the backend is kept.
- **ui**: in this directory, you will find the source code of the front-end application
- **Dockerfile**: the blueprint for building a docker image that hosts the application.
- **test**: in this directory all scripts, results and data is kept related to testing the application.
