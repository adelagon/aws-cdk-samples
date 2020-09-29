#!/usr/bin/env python3

from aws_cdk import core

from hello.hello_stack import HelloStack


app = core.App()
HelloStack(app, "hello")

app.synth()
