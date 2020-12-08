#!/usr/bin/env python3

from aws_cdk import core

from arcgis_cdk.arcgis_cdk_stack import ArcgisCdkStack


# env_us_east_1 = core.Environment(region='us-east-1')
# env_us_east_2 = core.Environment(region='us-east-2')

app = core.App()
ArcgisCdkStack(app, "arcgis-cdk",  env={'region': 'us-east-1'})

app.synth()
