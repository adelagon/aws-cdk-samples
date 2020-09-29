#!/usr/bin/env python3
import yaml
from aws_cdk import core

from three_tier_web.three_tier_web_stack import ThreeTierWebStack

# Demonstrates how to externalize configurations on your stack
config = yaml.load(open('./config.yaml'), Loader=yaml.FullLoader)

app = core.App()

# Create a different stack depending on the environment
# Useful if you are just deploying on a single AWS account
# Otherwise use core.Environments
stack_name = "three-tier-web-" + config["environment"]

ThreeTierWebStack(app, stack_name, config)

app.synth()
