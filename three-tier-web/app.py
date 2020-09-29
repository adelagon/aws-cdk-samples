#!/usr/bin/env python3
from aws_cdk import core

from three_tier_web.three_tier_web_stack import ThreeTierWebStack

app = core.App()
ThreeTierWebStack(app, "three-tier-web")

app.synth()
