---
menu: docs
weight: 20
---

# cdflow release

`cdflow release (--platform-config <platform_config>)... [--release-data=key=value]... <version> [options]`

The `release` command builds a release bundle which can then be deployed - it's required to run the `release` command before being able to run `deploy`. The `release` command requires a version and may require a `--platform-config` directory. Other values can be passed using `--release-data` flags and are accessible in the [release map parameter]({{ site.baseurl }}{% link reference/terraform-interface.md %}#release-map) in the Terraform code.

Running `release` will cause `terraform init` to be run against the `infra` directory of your project. Terraform will then download any providers and modules it needs to run your infrastructure code.

For some component types `cdflow release` will perform a build.

## Docker component type

If your component type is `docker` then `cdflow release` will build a Docker image using the `Dockerfile` that should be in the root of your project. It will tag it with [ECR repository address](https://docs.aws.amazon.com/AmazonECR/latest/userguide/docker-push-ecr-image.html) for your component, giving it the version number that you have passed to `cdflow release` and the Docker convention of `latest`. CDFlow will authenticate Docker with AWS and push the image to the ECR repository.

## AWS Lambda component type

If you have specified the `lambda` type in your `cdflow.yml` file then `cdflow release` will zip up a directory containing the code for your Lambda function. This directory will be either the name of your component or, if that doesn't exist, `./src/` as specified in [_Getting started - Lambda component type_](getting-started#lambda-component-type).

## Terraform initialisation

After building any artifact that the component type might require CDFlow will initialise Terraform to pull in its dependencies. Finally it will create a zip archive of everything required to perform a deployment:

- a JSON file (called `release.json` which populates the [release map parameter]({{ site.baseurl }}{% link reference/terraform-interface.md %}#release-map)) containing:
  - details of the artifact created during the build (if it was run)
  - other information relating to the release such as the name of the project, the team name, the version
  - any data passed to `cdflow release` via `--release-data`
- the platform config and local `./config/*.json` files
- and the Terraform code and its dependencies

The zip archive is stored in S3 and downloaded during [`cdflow deploy`](cdflow-deploy).
