#!/usr/bin/env python3

from aws_cdk import core

from cdk_app_python.cdk_app_python_stack import CdkAppPythonStack


app = core.App()
CdkAppPythonStack(app, "cdk-app-python")

app.synth()
