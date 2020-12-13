
# Welcome to the arcgis_cdk project

This project uses AWS Cloud Development Kit, AWS Systems Manager, and ArcGIS PowerShellDSC Libraries to automate the deployment of AWS Infrastructure and ArcGIS Enterprise.

## Prerequisites

* An AWS Account
* Access to ArcGIS Insallation and License files
* [AWS Command Line Interface (CLI)](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html)
* [AWS Cloud Development Kit](https://docs.aws.amazon.com/cdk/latest/guide/getting_started.html)
* Ability to create DNS Records to Point to A Record
* Amazon Certificate Manage Certificate

## Configuring, Synthesesing, and Deploying the CDK

The Amazon Cloud Development Kit is a relatively newer tool that allows developers to create code in the language that they are most comfortable in and translate that into AWS Infrastructure by generating CloudFormation templates.  

Before proceeding, ensure you have both the AWS CLI and AWS CDK available and working (see prerequisites for more information)

### CDK Overview

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


### CDK Configuration Paramaters

Now that you have your virtual envrionment setup with AWS CDK, lets take a look at how this repo is using it.  There is a arcgis_cdk_config.json file in the arcgis_cdk directory.  The following parameters can be used.

* `stack_name` - the name of your stack (will also show up as )
* `high_availability` - true/false depending on if you want site to be HA
* `cert_arn` - ARN for your ACM certificate
* `file_server_size` - size of file server ( m5.large)
* `kp_name` - key pair name
* `public_hosted_zone_id` - zone id for your Route53 public hosted zone
* `build_dsc_file` - comming soon

Once the arcgis_cdk_config.json has been updated run the following commands to deploy your code.

```
$ cdk synth
```
Note: you can find the resulting CloudFormation template that was created in the cdk.out directory

```
$ cdk deploy
```
Take a look in your AWS Account and notice everything that was deployed

### CDK Results

What did it deploy? Mayb architeture diagram....

## AWS System Manager - Machine Setup

Before we get started with installing PowerShell DSC via the Invoke-ArcGIS Command we need to do a little machine prep.  The prep includes:

* Downloading the software and licenses from the S3 bucket created by the arcgis_cdk run
    - Portal for ArcGIS (and license)
    - ArcGIS Server (and license)
    - ArcGIS DataStore
    - ArcGIS Web Adaptor for Microsoft IIS
* Downloading the PowerShell DSC modules and adding the ArcGIS Modules to PowerShell
* Adding a local account to each machine for Windows Remote Management (WInRM)
* Changing the execution policy
* Enabling Windows Remote Management (WinRM) to that one machine can execute the commands

A template PowerShell - EC2 Instance Prep file has been provided "EC2InstancePrep.ps1".  Edit the following sections with your paramaters
* Bucket name & Object Keys
* License file name
* IP Addresses of machines
* Username / Password of service account

1. Ensure the ArcGIS Enterprise Software has been uploaded to the S3 bucekt created by the CDK
2. Navigate to Amazon Sysetms Manager
3. Chose the Run Command from the options on the left
4. Create a new run command
5. Search for the existing PowerShell Run Document
    * `AWS-RunPowerShellScript`
6. Paramaters for Run Command
    * `Document` - 1 (Default)
    * `Command paramaters` - Copy the contents from EC2InstancePrep.ps1 file (updated with your paramaters)
    * `Working Directory` - Leave Blank
    * `Execution Timeout` - Leave at 3600
    * `Targets` - Choose the instances that were deployed above
    * Other parameters can be left as default
    * (Optionally) COnfigure an S3 Bucket where Command output will be added
7. Execute the Run Command!!

![arcgis_cdk](https://github.com/jturco/arcgis_cdk/blob/main/images/arcgis_cdk_instance_prep.png)

## AWS System Manager - PowerShell DSC Command

At this point the infrastructure should have been stood up with CDK, the EC2 Instances should have been prepped by the first Run Command in System Manager.  It's time to Deploy Some SOftware.

1. Ensure the ArcGIS Enterprise Software has been uploaded to the S3 bucekt created by the CDK
2. Navigate to Amazon Sysetms Manager
3. Chose the Run Command from the options on the left
4. Create a new run command
5. Search for the existing PowerShell Run Document
    * `AWS-RunPowerShellScript`
6. Paramaters for Run Command
    * `Document` - 1 (Default)
    * `Command paramaters` - Copy the contents from InvokeDSC.ps1 file (updated with your paramaters)
    * `Working Directory` - Leave Blank
    * `Execution Timeout` - Change to 28.800 (we want to give the commands at least 8 hours to complete)
    * `Targets` - Choose ONLY the orchestration instance
    * Other parameters can be left as default
    * (Optionally) COnfigure an S3 Bucket where Command output will be added
7. Execute the Run Command!!