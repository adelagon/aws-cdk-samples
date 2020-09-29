#!/usr/bin/env python3
import yaml
from aws_cdk import core

from three_tier_web.three_tier_web_stack import ThreeTierWebStack

config = yaml.load(open('./config.yaml'), Loader=yaml.FullLoader)

app = core.App()
stack_name = "three-tier-web-" + config["environment"]

ThreeTierWebStack(app, "three-tier-web", config)

app.synth()
