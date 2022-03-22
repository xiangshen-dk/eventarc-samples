# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import functions_framework

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

to_emails = os.environ.get('TO_EMAILS')
sendgrid_api_key = os.environ.get('SENDGRID_API_KEY')

@functions_framework.cloud_event
def handle_audit_log(cloud_event):
    # See https://github.com/cloudevents/spec/blob/v1.0.1/spec.md#type
    print(f"Event type: {cloud_event['type']}")

    # Parse the event body
    message = read_event_data(cloud_event)

    notify(message)

    return 'OK', 200

def read_event_data(cloud_event):

    # Assume custom event by default
    event_data = cloud_event.data

    protoPayload = event_data['protoPayload']
    request = protoPayload['request']
    principalEmail = protoPayload['authenticationInfo']['principalEmail']
    instance = request['instances'][0]['instance']
    
    resource = event_data['resource']
    project_id = resource['labels']['project_id']
    instance_group_name = resource['labels']['instance_group_name']
    location = resource['labels']['location']
    receiveTimestamp = event_data['receiveTimestamp']

    message = f"""
The following instance has been added to {instance_group_name}:
principalEmail: {principalEmail}
instance: {instance}
instance_group_name: {instance_group_name}
project_id: {project_id}
location: {location}
receiveTimestamp: {receiveTimestamp}"""

    print(message)

    return message


def notify(message):

    if to_emails is None or sendgrid_api_key is None:
        print("Email notification skipped as TO_EMAILS or SENDGRID_API_KEY is not set")
        return

    print(f"Sending email to {to_emails}")

    message = Mail(
        from_email='your-verified-email@example.com',
        to_emails=to_emails,
        subject='An instance is created',
        html_content=f'<html><pre>{message}</pre></html>')
    try:
        print(f"Email content {message}")
        sg = SendGridAPIClient(sendgrid_api_key)
        response = sg.send(message)
        print(f"Email status code {response.status_code}")
    except Exception as e:
        print(e)