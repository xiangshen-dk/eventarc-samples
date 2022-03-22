#!/bin/bash

# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
set -v

# TO_EMAILS=youremail@gmail.com
# SENDGRID_API_KEY=yoursendgridapikey

gcloud beta functions deploy gce-vm-notifier1 \
  --gen2 \
  --runtime python38 \
  --entry-point handle_audit_log \
  --source . \
  --trigger-event-filters="type=google.cloud.audit.log.v1.written" \
  --trigger-event-filters="serviceName=compute.googleapis.com" \
  --trigger-event-filters="methodName=v1.compute.instanceGroups.addInstances" \
  --region us-central1 \
  --trigger-location us-central1 # --update-env-vars TO_EMAILS=$TO_EMAILS,SENDGRID_API_KEY=$SENDGRID_API_KEY