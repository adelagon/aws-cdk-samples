#!/usr/bin/env python3

import aws_cdk as cdk

from smri_workshop.smri_workshop_stack import SmriWorkshopStack


app = cdk.App()
SmriWorkshopStack(app, "smri-workshop")

app.synth()
