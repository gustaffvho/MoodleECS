# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import os
from aws_cdk import (
    aws_ec2 as _ec2,
    aws_ecs as _ecs,
    aws_rds as _rds,
    aws_efs as _efs,
    aws_ecr_assets as _ecr_assets,
    aws_elasticloadbalancingv2 as _elbv2,
    aws_logs as _logs,
    core as cdk
)

class MoodleDatabaseStackProperties:

    def __init__(
            self,
            vpc: _ec2.Vpc,
    ) -> None:

        self.vpc = vpc

class MoodleDatabaseStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str,
                 properties: MoodleDatabaseStackProperties, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # define mysql rds database
        self.database = _rds.DatabaseInstance(
            self, "MoodleDatabase",
            engine=_rds.DatabaseInstanceEngine.mysql(
                version=_rds.MysqlEngineVersion.VER_8_0_21
            ),
            database_name="MoodleDatabase",
            vpc=properties.vpc,
            port=3306,
            instance_type=_ec2.InstanceType.of(
                _ec2.InstanceClass.MEMORY6_GRAVITON,
                _ec2.InstanceSize.LARGE,
            ),
            deletion_protection=False,
            publicly_accessible=False,
            storage_encrypted=True,
            backup_retention=cdk.Duration.days(7),
            removal_policy=cdk.RemovalPolicy.DESTROY,
        )



