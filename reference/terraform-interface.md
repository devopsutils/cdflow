---
title: Terraform interface
menu: reference
weight: 50
---

# Terraform interface

CDFlow is a thin wrapper around [Terraform](https://www.terraform.io/) allowing you to take advantage of that tool, and its development community, to manage your infrastructure programmatically. The purpose of this document is to show the interface between the `cdflow` tool and `terraform` so that users can take full advantage of Terraform itself.

## Terraform variables

There are a number of standard variables that `cdflow` passes to `terraform` when it is invoked so these need to be defined in `variable` blocks in your `./infra/*.tf` files:

- `env` is a string with the name of the environment
- `platform_config` is a [map](https://www.terraform.io/docs/configuration-0-11/variables.html#maps) type variable containing information about the environment the infrastructure is provisioned into e.g. VPC and subnet IDs
- `release` is a [map](https://www.terraform.io/docs/configuration-0-11/variables.html#maps) type variable containing information about this version of the software - there is more information below

Note that as well as the `env` variable the current environment during `cdflow deploy` is also available from the built-in [Terraform variable `workspace`](https://www.terraform.io/docs/state/workspaces.html#current-workspace-interpolation) i.e. `${terraform.workspace}` in your `*.tf` files.

### HCL code

The code under `./infra/*.tf` should have definitions for these variables, by convention in a `variables.tf` file:

```hcl
variable "env" {
  description = "Environment name"
  type        = "string"
}

variable "platform_config" {
  description = "Platform configuration"
  type        = "map"
}

variable "release" {
  description = "Metadata about the release"
  type        = "map"
}
```

### Release map

The release map always has a standard set of variables available in it, plus other information depending on the component `type`. All components will have:

- `commit`: the Git commit hash for the repo when the release was created
- `version`: the version passed to `cdflow release`
- `component`: the name of the component, obtained from the name of the Git remote
- `team`: the team specified in the `cdflow.yml` file when the release was created

As well as these standard keys and values in the map there is extra data for `docker` and `lambda` component types.

#### Docker component

If the component type is specified as `docker` in the `cdflow.yml` file then there will be an extra key in the release map Terraform variable:

- `image_id`: the address of the Docker image in the ECR repo

#### Lambda component

For a component type of `lambda` there will be the following extra keys in the the release map:

- `s3_bucket`:  the S3 bucket where the zip archive containing the Lambda code is uploaded
- `s3_key`: the key in the S3 bucket under which the Lambda zip archive is uploaded

#### Release data CLI argument

When calling `cdflow release` it is possible to pass `--release-data` flags with extra information to put into the release map. This is useful if the output from one step in a build pipeline needs to feed into the next which is managed by CDFlow.

Any flags passed as `--release-data=key=value` will appear in the release map like:

```json
{
  "key": "value"
}
```

### Config files

The JSON files under `./config/*.json` in the root of your project are passed to the `terraform` executable as [`-var-file` flags](https://www.terraform.io/docs/configuration-0-11/variables.html#variable-files), so any top-level keys in those files need to be defined as `variable` blocks to be able to able to access them in code.

### Platform config

The `platform_config` variable is a special case for the `-var-file` flag and CDFlow expects there to be a top-level `platform_config` key in that JSON file.
