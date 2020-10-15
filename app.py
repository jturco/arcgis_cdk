#!/usr/bin/env python3

from aws_cdk import core

from arcgis_cdk.arcgis_cdk_stack import ArcgisCdkStack


app = core.App()
ArcgisCdkStack(app, "arcgis-cdk")

app.synth()
