# CLI tool for managing Labelbox resoruces in the workspace.
This is small CLI tool written in Python for the people who appreciate the productivity of the terminal over UI interfaces.

Basically, this tool allows you to peform simple (CRUD) actions using the Labelbox SDK through the command line. 

- [Installation](#installation)
- [Install from PIP registry](#install-from-pip-registry)
- [Authentication](#authentication)
- [Available commands](#available-commands)
- [Usage](#usage)
    + [Print more information about the command](#print-more-information-about-the-command)
  * [Projects](#projects)
    + [Get project by ID](#get-project-by-id)
    + [Create image based project](#create-image-based-project)
    + [Delete project by ID](#delete-project-by-id)
    + [Export project's information using Export V2](#export-project-s-information-using-export-v2)
    + [Export project's infomration with different flags](#export-project-s-infomration-with-different-flags)
    + [Save export output to file](#save-export-output-to-file)
  * [Ontology](#ontology)
    + [Get ontology by ID](#get-ontology-by-id)
    + [Create ontology](#create-ontology)
    + [Delete ontology](#delete-ontology)
  * [Batch](#batch)
    + [Get batch by ID](#get-batch-by-id)
    + [Create batch from data row ids](#create-batch-from-data-row-ids)
    + [Create batch from text file containing data row ids](#create-batch-from-text-file-containing-data-row-ids)
    + [Create batch from dataset](#create-batch-from-dataset)
    + [Delete batch by ID](#delete-batch-by-id)
    + [Delete labels from batch](#delete-labels-from-batch)

## Installation

First clone the repository:

``` sh
git clone https://github.com/mihhail-m/labelbox-cli.git
```

Navigate to the repository:

``` sh
cd labelbox-cli
```

Finally install current package:

``` sh
python -m pip install --editable .
```

## Install from PIP registry

[WIP]

## Authentication

In order to use `labelbox-cli` you need to create profile that will be stored locally on your machine with
necessary information for interacting with your workspace.

Firstly, execute any arbitrary subcommand to create new profile. For exaple:

``` sh
labelbox projects
```

When executed for the very first time it will ask you to provide `API_KEY` for the `Workspace`, GraphQL `ENDPOINT` if you have one and `PROFILE`name under which it will be stored. This information will be saved into 
your home folder under `.labelbox-cli.json` file.

This file is later used to retrieve `API_KEY` and executed SDK commands to your `Workspace`.


## Available commands

``` sh
Usage: labelbox [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  ontology  Command for interacting with Ontologies.
  projects  Command for interacting with Projects in the workspace.
```

## Usage

Section with examples on how to use different commands.

#### Print more information about the command

This will print more information about command eg like usage, necessary arguments etc.

``` sh
labelbox [command] --help
```

---

### Projects

``` sh
Usage: labelbox projects [OPTIONS] COMMAND [ARGS]...

  Command for interacting with Projects in the workspace. Use subcommands for
  retrieveing necessary data.

Options:
  --help  Show this message and exit.

Commands:
  create  Creates new project.
  delete  Delete project by ID.
  export  Exports project's information.
  get     Retrieves project by ID.
  list    Lists available projects with matching name.
```

#### Get project by ID

``` sh
labelbox projects get PROJECT_ID
```

#### Create image based project

``` sh
labelbox projects create --name "New project" --project_type image
```

#### Delete project by ID

``` sh
labelbox projects delete PROJECT_ID
```

#### Export project's information using Export V2

``` sh
labelbox projects export PROJECT_ID
```

#### Export project's infomration with different flags

Just provide the flag you would like to export:

``` sh
labelbox projects export PROJECT_ID --attachments --data_row_details
```

Commands above are equivalent of the following code sample:

``` python
export_params= {
  "attachments": True,
  "metadata_fields": True,
  "data_row_details": True,
  "project_details": True,
  "performance_details": True
}

export_task = project.export_v2(params=export_params)
export_task.wait_till_done()
print(export_task.result)
```

#### Save export output to file

``` sh
labelbox projects export PROJECT_ID --save
```

---

### Ontology

``` sh
Usage: labelbox ontology [OPTIONS] COMMAND [ARGS]...

  Command for interacting with Ontologies. Use subcommands to perform CRUD
  operation.

Options:
  --help  Show this message and exit.

Commands:
  create  Create new ontology from existing tools and classifications.
  delete  Deletes unused ontology by ID.
  get     Retrieve ontology by ID.
  list    List available ontologies in the workspace.
```

#### Get ontology by ID

``` sh
labelbox ontology get ONTOLOGY_ID
```

#### Create ontology

You can create new ontology from existing tools and classifications. 
However, if `--tools` and `--classifications` parameters are not given, will simply create new empty ontology.

``` sh
labelbox ontology create --name "new-ontology" --media_type "image" --tools "toolId1, toolId2" --classifications "classificationId1, classificationId2"
```

#### Delete ontology

You can only delete **unused** ontologies, meaning ontologies that are not connected to any projects.

``` sh
labelbox ontology delete ONTOLOGY_ID
```

---

### Batch

``` sh
Usage: labelbox batch [OPTIONS] COMMAND [ARGS]...

  Command for interacting with batches in the projects.

Options:
  --help  Show this message and exit.

Commands:
  create               Creates a batch for the Benchmark project using...
  create-from-dataset  Creates batch from the dataset.
  delete               Deletes batch by Project and Batch ID.
  delete-labels        Deletes labels from the batch.
  get                  Retrieves batch by Project and Batch ID.
```

#### Get batch by ID

``` sh
labelbox batch get PROJECT_ID BATCH_ID
```

#### Create batch from data row ids

``` sh
labelbox batch create --project-id PROJECT_ID --name "unique-batch-name" --rows "datarowId1, datarowId2" --priority 1
```

#### Create batch from text file containing data row ids

This is useful when there are a lot of data row IDs that you wish to add to the project 
and you don't have that fancy 34" inch curve monitor.

``` sh
labelbox batch create --project-id PROJECT_ID --name "unique-batch-name" --fp path_to_txt_file --priority 1
```

#### Create batch from dataset

``` sh
labelbox batch create-from-dataset --project-id PROJECT_ID --n "prefix-name" --dataset-id DATASET_ID
```

#### Delete batch by ID

``` sh
labelbox batch delete PROJECT_ID BATCH_ID
```

#### Delete labels from batch

You can also set `--set-as-template` flag to requeue labels for the future usage.

``` sh
labelbox batch delete-labels PROJECT_ID BATCH_ID
```
