# CLI tool for managing Labelbox resoruces in the workspace.
This is small CLI tool written in Python for the people who appreciate the productivity of the terminal over UI interfaces.

Basically, this tool allows you to peform simple (CRUD) actions using the Labelbox SDK through the command line. 

* [Installation](#installation)
* [Install from PIP registry](#install-from-pip-registry)
* [Authentication](#authentication)
* [Available commands:](#available-commands)
* [Usage](#usage)
    + [Print more information about the command](#print-more-information-about-the-command)
    + [Projects](#projects)
        - [Get project:](#get-project)
        - [Create image based project:](#create-image-based-project)
        - [Delete project by ID:](#delete-project-by-id)
        - [Export project's information using Export V2:](#export-project-s-information-using-export-v2)
        - [Export project's infomration with different flags:](#export-project-s-infomration-with-different-flags)
        - [Save export output to file:](#save-export-output-to-file)

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
  projects  Command for interacting with Projects in the workspace.
```

## Usage

Section with examples on how to use different commands.

#### Print more information about the command

This will print more information about command eg like usage, necessary arguments etc.

``` sh
labelbox [command] --help
```


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

#### Get project

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

This is equivalent of the following parametrs:

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

Just provide the flag you would like to export:

``` sh
labelbox projects export PROJECT_ID --attachments --data_row_details
```

#### Save export output to file

``` sh
labelbox projects export PROJECT_ID --save
```

