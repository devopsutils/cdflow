---
menu: docs
weight: 10
---

# Getting started

Here you will find all of the steps to get started using CDFLow in your project.

## Project structure

The `cdflow` tool expects a few different conventions for your project:

- a Git remote configured, from where `cdflow` will take the name of the component e.g. from `git@github.com:organisation/project-name.git`, the component name will be `project-name`
- a folder named `./infra/` containing `*.tf` files to be consumed by Terraform
- a `./config/` folder with JSON config files [per environment]({{ site.baseurl }}{% link reference/config-env-json.md %}) and one named [`common.json`]({{ site.baseurl }}{% link reference/config-common-json.md %})
- a [`cdflow.yml`]({{ site.baseurl }}{% link reference/cdflow-yaml.md %}) file in its root

```shell
localhost:project-name# tree
.
├── cdflow.yml
├── config
│   ├── test.json
│   ├── common.json
│   └── live.json
└── infra
    ├── main.tf
    └── variables.tf
```

Some of the component types, specified in the `cdflow.yml` file, require other files and directories.

### Docker component type

The `docker` component type requires a [`Dockerfile`](https://docs.docker.com/engine/reference/builder/) in the root of the project so that it can build a container image from it.

### Lambda component type

The `lambda` component type requires a folder containing the source code for the AWS Lambda function. This can either be named with the same name as the component i.e. if the Git remote is `git@github.com:organisation/project-name.git` then there should be a folder named `./project-name` at the root of the project, or if that doesn't exist then `cdflow` will look for a directory called `./src` and treat that as the code for the Lambda function.

## Runtime requirements

The tool requires some additional components to be able to build and deploy releases.

### cdflow.yml

As specified above, the project must have a [`cdflow.yml`]({{ site.baseurl }}{% link reference/cdflow-yaml.md %}) file in its root. This has information about the type of project, the team who owns it and the account scheme to tell `cdflow` about which AWS accounts it should use for deployment.

See the [cdflow.yml reference]({{ site.baseurl }}{% link reference/cdflow-yaml.md %}).

### Account Scheme

To work out where to store releases and which account corresponds to which environment `cdflow` uses an account scheme. This is a JSON file which needs to be stored in an S3 bucket in an AWS account and the IAM user running the `cdflow` command needs to be able to access that S3 URL.

The URL is included in the [`cdflow.yml`]({{ site.baseurl }}{% link reference/cdflow-yaml.md %}) file under the `account-scheme-url` key.

See the [account-scheme.json reference]({{ site.baseurl }}{% link reference/account-scheme-json.md %}).

### Platform Config

This defines information about common resources that are needed by components being deployed e.g. VPC, subnets etc. It's passed as a JSON file to the Terraform and the map is then accessible within the Terraform code.

See the [Platform config reference]({{ site.baseurl }}{% link reference/platform-config-json.md %}).
