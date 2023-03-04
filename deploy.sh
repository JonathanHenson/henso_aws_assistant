#!/bin/bash

aws s3 cp intents-deployment-package.zip s3://hensos-personal-assistant/intents/
aws cloudformation deploy --template-file chat_engine.yaml --stack-name personal-assistant-chat-engine --capabilities CAPABILITY_NAMED_IAM

