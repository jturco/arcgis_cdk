
# Welcome to the arcgis_cdk

Over view of the project goes here

## Prerequisites

* An AWS Account
* An S3 Bucket
* Access to ArcGIS Insallation and License files
* AWS CLI --> Link
* AWS CDK --> Link
* Ability to create DNS Records to Point to A Record (optionally this can be done with CDK if use AWS Route53 --> Link)

## Getting Started

1. Upload the following files to your S3 bucket
- Portal for ArcGIS
- ArcGIS Server
- ArcGIS DataStore
- ArcGIS Web Adaptor for Microsoft IIS

2. Ensure the AWS CLI and AWS CDK have been installed and configured (see links above if you havne't already)
3. ....

## Configuring, Synthesesing, and Deploying the CDK

The `cdk.json` file tells the CDK Toolkit how to execute your app.

This project is set up like a standard Python project.  The initialization
process also creates a virtualenv within this project, stored under the .env
directory.  To create the virtualenv it assumes that there is a `python3`
(or `python` for Windows) executable in your path with access to the `venv`
package. If for any reason the automatic creation of the virtualenv fails,
you can create the virtualenv manually.

To manually create a virtualenv on MacOS and Linux:

```
$ python -m venv .env
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source .env/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .env\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```

At this point you can now synthesize the CloudFormation template for this code.

```
$ cdk synth
```

To add additional dependencies, for example other CDK libraries, just add
them to your `setup.py` file and rerun the `pip install -r requirements.txt`
command.

### Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

## Using AWS System Manager to Deploy ArcGIS Enterprise with PowerShell DSC

Stuff about how we did that. 
