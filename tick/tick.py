from __future__ import print_function
from cfnrespond import send, SUCCESS

import boto3
import datetime
import json

def handler(event, context):

    # Get message body (stack update or alarm).
    message = json.loads(event['Records'][0]['Sns']['Message'])

    # Detect source event.
    source = message.get('RequestType', 'Alarm')

    # Confirm stack deletion.
    if source == 'Delete':
        return send(message, context, SUCCESS)

    # Set/toggle state.
    if source == 'Alarm':
        state = int(not float(message['Trigger']['Threshold']))
    else :
        state = 0

    # Set metric to state.
    cw = boto3.client('cloudwatch')
    cw.put_metric_data(
        Namespace = 'Tick',
        MetricData = [ {
            'MetricName': 'Tick',
            'Value': state
        } ]
    )

    # Re-trigger alarms on stack create/update.
    if source != 'Alarm':
        cw.set_alarm_state(AlarmName = 'TickState0', StateValue = 'OK', StateReason = 'Go!')
        cw.set_alarm_state(AlarmName = 'TickState1', StateValue = 'OK', StateReason = 'Go!')
        return send(message, context, SUCCESS)

    #
    # Do work here...
    #

    print('>>> ' + str(datetime.datetime.now()) + ' <<<')
    return 'OK'
