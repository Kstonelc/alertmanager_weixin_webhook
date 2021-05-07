import json
from dateutil import parser
from flask import Flask
from flask import request
from flask import current_app
from WorkWeixinRobot.work_weixin_robot import WWXRobot

app = Flask(__name__)
app.secret_key = 'lAlAlA123'

# weChart
chatKey = "xchatKeyx"
wwxrbt = WWXRobot(key=chatKey)
env = "xenvx"


@app.route('/alert', methods=['POST'])
def postAlertmanager():
    try:
        content = json.loads(request.get_data())
        for alert in content['alerts']:
            if alert['status'] == "resolved":
                message = "**********恢复通知**********\n"
            elif alert['status'] == "firing":
                message = "**********告警通知**********\n"
            else:
                message = "**********其他通知**********\n"
            if env:
                message += "告警环境: " + str(env) + "\n"
            if alert.get('labels').get('alertname'):
                message += "告警类型: "+alert['labels']['alertname']+"\n"
            if alert.get('severity'):
                message += "告警级别: "+alert['severity']+"\n"
            if alert.get('labels').get('instance'):
                message += "告警实例: "+alert['labels']['instance']+"\n"
            message += "告警详情:\n"
            for k, v in alert['annotations'].items():
                message += "\t{}: {}\n".format(k, v)
            if alert['status'] == "resolved":
                correctDate = parser.parse(alert['endsAt']).strftime('%Y-%m-%d %H:%M:%S%Z')
                message += "恢复时间: "+correctDate
            elif alert['status'] == "firing":
                correctDate = parser.parse(alert['startsAt']).strftime('%Y-%m-%d %H:%M:%S%Z')
                message += "故障时间: "+correctDate
            message += "\n******************************"
            wwxrbt.send_text(content=message)
        return "Alert OK", 200
    except Exception as error:
        wwxrbt.send_text(content="Error: "+str(error))
        current_app.logger.error("\t%s", error)
        return "Alert fail", 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
