
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


A few things here about CDK and

## CDK Configuration Paramaters

* Configruation Paramaters
* Number 2
* Number 3

## AWS System Manager - Machine Setup

Before we get started with installing PowerShell DSC via the Invoke-ArcGIS Command we need to do a little machine prep.  The prep includes:
* Downloading the software and licenses from the S3 bucketll
* Downloading the PowerShell DSC modules and adding to PowerShe
* Adding a local account to each machine for Windows Remote Management (WInRM)
* Changing the execution policy
* 

A template PowerShell - EC2 Instance Prep file has been provided "EC2-Instance-Prep.ps1".  Edit the following sections with your paramaters
* Bucket name 
* License file name
* IP Addresses of machines

1. Ensure the ArcGIS Enterprise Software has been uploaded to the S3 bucekt created by the CDK
2. Navigate to Amazon Sysetms Manager -> Run Command
3. Create a new run command
4. Search for the PowerShell Image

    Note: If you've run the CDK, these variables will be provided as outputs in the log.....
6. Paramaters for Run Command
    * This....
    * That....
7. Execute the Run Command!!

![Image place holder](https://www.fillmurray.com/640/360)

## AWS System Manager - PowerShell DSC Command

At this point the infrastructure should have been stood up with CDK, the EC2 Instances should have been prepped by the first Run Command in System Manager.  It's time to Deploy Some SOftware.

1. Head back to the System Manager --? Run Command Section
2. Create a new run command
3. Search for the PowerShell Template