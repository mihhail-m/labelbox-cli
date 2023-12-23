# CLI tool for managing Labelbox resoruces in the workspace.
This is small CLI tool written in Python for the people who appreciate the productivity of the terminal over UI interfaces.

Basically, this tool allows you to peform simple (CRUD) actions using the Labelbox SDK through the command line. 

- [Installation](#installation)
- [Install from PIP registry](#install-from-pip-registry)
- [Authentication](#authentication)
- [Available commands](#available-commands)
- [Usage](#usage)
    + [Print more information about the command](#print-more-information-about-the-command)
  * [Project](#project)
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
    + [Delete feature from ontology](#delete-feature-from-ontology)
  * [Batch](#batch)
    + [Get batch by ID](#get-batch-by-id)
    + [Create batch from data row ids](#create-batch-from-data-row-ids)
    + [Create batch from text file containing data row ids](#create-batch-from-text-file-containing-data-row-ids)
    + [Create batch from dataset](#create-batch-from-dataset)
    + [Delete batch by ID](#delete-batch-by-id)
    + [Delete labels from batch](#delete-labels-from-batch)
  * [Feature](#feature)
    + [Get feature by ID](#get-feature-by-id)
    + [Get feature by name](#get-feature-by-name)
    + [Create tool](#create-tool)
    + [Create classification](#create-classification)
    + [Create classificaiton with option](#create-classificaiton-with-option)
    + [Delete feature by ID](#delete-feature-by-id)
  * [Dataset](#dataset)
    + [Get dataset by ID](#get-dataset-by-id)
    + [Create new dataset](#create-new-dataset)
    + [Append data to dataset](#append-data-to-dataset)
    + [Export data from dataset](#export-data-from-dataset)
    + [Save export output to file](#save-export-output-to-file-1)
    + [Delete dataset by ID](#delete-dataset-by-id)
    + [Update dataset name](#update-dataset-name)


## Installation

First clone the repository:

``` sh
git clone https://github.com/mihhail-m/labelbox-cli.git
```

Navigate to the repository:

``` sh
cd labelbox-cli
```

Create virtual enironment to avoid dependency conflicts with installed packages:

```sh
python -m venv .venv
```

Acitave virtual environment:

```sh
source ./.venv/bin/activate
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

This file is later used to retrieve `API_KEY` and execute SDK calls using commands for your `Workspace`.


## Available commands


``` sh
Usage: labelbox [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  batch     Command for interacting with batches in the projects.
  feature   Command for interacting with Features in the workspace.
  ontology  Command for interacting with Ontologies.
  project   Command for interacting with Projects in the workspace.
```


## Usage

Section with examples on how to use different commands.

#### Print more information about the command

This will print more information about command eg like usage, necessary arguments etc.

``` sh
labelbox [command] --help
```

---

### Project

``` sh
Usage: labelbox project [OPTIONS] COMMAND [ARGS]...

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
labelbox project get PROJECT_ID
```

#### Create image based project

``` sh
labelbox project create --name "New project" --project-type image
```

#### Delete project by ID

``` sh
labelbox project delete PROJECT_ID
```

#### Export project's information using Export V2

``` sh
labelbox project export PROJECT_ID
```

#### Export project's infomration with different flags

Just provide the flag you would like to export:

``` sh
labelbox project export PROJECT_ID --attachments --data-row-details
```

Commands above are equivalent of the following code sample:

``` python
export_params= {
  "attachments": True,
  "metadata_fields": False,
  "data_row_details": True,
  "project_details": False,
  "performance_details": False
}

export_task = project.export_v2(params=export_params)
export_task.wait_till_done()
print(export_task.result)
```

#### Save export output to file

``` sh
labelbox project export PROJECT_ID --save
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
labelbox ontology create --name "new-ontology" --media-type "image" --tools "toolId1, toolId2" --classifications "classificationId1, classificationId2"
```

#### Delete ontology

You can only delete **unused** ontologies, meaning ontologies that are not connected to any projects.

``` sh
labelbox ontology delete ONTOLOGY_ID
```


#### Delete feature from ontology

``` sh
labelbox ontology delete-feature ONTOLOGY_ID FEATURE_SCHEMA_ID
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

---

### Feature

``` sh
Usage: labelbox feature [OPTIONS] COMMAND [ARGS]...

  Command for interacting with Features in the workspace.

Options:
  --help  Show this message and exit.

Commands:
  create-classification  Creates a Classification of choosen type.
  create-tool            Creates a Tool of a choosen type.
  delete                 Deletes ununsed feature schema by ID...
  get                    Get Feature by ID (featureSchemaId).
  get-by-name            Get Feature by name.
```

#### Get feature by ID

``` sh
labelbox feature get FEATURE_SCHEMA_ID
```

#### Get feature by name

``` sh
labelbox feature get-by-name FEATURE_SCHEMA_NAME
```

#### Create tool

``` sh
labelbox feature create-tool --n "my-tool" --t bbox 
```

You can also supply `--color` argument to specify color and `--required` to mark `Tool` as required.

Get more information with 

```sh
labelbox feature create-tool --help

```

#### Create classification

**NB!** For now nested classifications are not supported.

``` sh
labelbox feature create-classification --name "my-classification" --type text
```

Get more information with 

```sh
labelbox feature create-classification --help

```


#### Create classificaiton with option

``` sh
labelbox feature create-classification --n "my-classificaiton" --type radio --options "option1,option2,option3"
```


#### Delete feature by ID

***NB!** Only unused features can be deleted freely. 

``` sh
labelbox feature delete FEATURE_SCHEMA_ID
```

---

### Dataset

``` sh
Usage: labelbox dataset [OPTIONS] COMMAND [ARGS]...

  Commands for interacting with Datasets in the workspace.

Options:
  --help  Show this message and exit.

Commands:
  append  Add data rows to a selected Dataset.
  create  Creates new empty Dataset in the Catalog.
  delete  Deletes Dataset by ID.
  export  Exports dataset's information.
  get     Get Dataset by ID.
  update  Updates dataset name.
```

#### Get dataset by ID

``` sh
labelbox dataset get DATASET_ID
```

#### Create new dataset
This will create just an empty dataset. You would then need to append data separately.

``` sh
labelbox dataset --n new_empty_dataset
```

#### Append data to dataset

There are many ways to append assets to the desired dataset via CLI.

You can also provide desired values for __global keys__ with `--global-keys` flag. However, if this argument is not specified random UUID values would be assigned to global keys instead.

1. Append assets as comma separated list of URLs

``` sh
labelbox dataset append DATASET_ID --r "urlToMyImage.png,urlToMyImage2.png"
```

2. Append assets as comma separate list of URLs with Global Keys.

``` sh
labelbox dataset append DATASET_ID --r "urlToMyImage.png,urlToMyImage2.png" --global-keys "uniqueKeyForFirstUrl,uniqueKeyForSecondsUrl"
```

3. Upload single local file to dataset.

``` sh
labelbox dataset append DATASET_ID --f path-to-local-file
```

4. Append assets from JSON file (most common way of uploading data). 

In this case it is assumed that global keys are already present in the JSON file for each `row_data`.

``` sh
labelbox dataset append DATASET_ID --json path-to-json-file
```

5. Appends assets from CSV file.

For now most basic way of csv file is supported.

__NB!__ Don't forget to specify column headers!

Example of `.csv` file:

``` csv
row_data,global_key
url-some-file,unique-key-1
url-to-another-file,unique-key-2
```

Feel free to drop `global_key` column if don't need it.

``` sh
labelbox dataset append DATASET_ID --csv path-to-csv-file
```

#### Export data from dataset

Just provide the flag you would like to export information with. You can see all the flag by adding `--help` subcommand.

``` sh
labelbox dataset export DATASET_ID --data-row-details
```

Commands above are equivalent of the following code sample:

``` python
export_params= {
  "attachments": False,
  "metadata_fields": False,
  "data_row_details": True,
  "project_details": False,
  "performance_details": False
}

export_task = dataset.export_v2(params=export_params)
export_task.wait_till_done()
print(export_task.result)
```

If you want to export information for particular projects

``` sh
labelbox dataset export DATASET_ID --project-details --project-ids "projectId1,projectId2"
```

Python equivalent would be:

``` python
export_params= {
  "attachments": False,
  "metadata_fields": False,
  "data_row_details": True,
  "project_details": True,
  "performance_details": False,
  "project_ids": ["projectId1","projectId2"]
}

export_task = dataset.export_v2(params=export_params)
export_task.wait_till_done()
print(export_task.result)
```

#### Save export output to file

``` sh
labelbox dataset export DATASET_ID --s
```

#### Delete dataset by ID

``` sh
labelbox dataset delete DATASET_ID
```

#### Update dataset name

``` sh
labelbox dataset update DATASET_ID new-name
```
