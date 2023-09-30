import datetime
import os

import requests
from bs4 import BeautifulSoup


def get_activity(d):
    URL = "https://web.metro.taipei/arena/index.aspx"
    year = d.year
    month = d.month
    day = d.day

    if year and month and day:
        URL = URL + f"?y={year}&m={month}"
        request = requests.get(URL)
        html_data = request.text

        # Find value of specific div class
        soup = BeautifulSoup(html_data, "html.parser")
        # find div with content text is month/day
        activity = soup.find(
            "div", string=f"{month}/{day}"
        ).find_parent(
            "table"
        ).findChildren("td")[0]

        if activity.findChildren("a"):
            activity_name = activity.findChildren("a")[0].text
        else:
            activity_name = activity.text.strip()

        return {
            "activity": activity_name,
            "day": day,
            "month": month,
            "year": year
        }


if __name__ == "__main__":
    if os.getenv("DATE") is not None and os.getenv("WEBHOOK_URL") is not None:
        d = datetime.datetime.strptime(os.getenv("DATE"), "%Y-%m-%d").date()

        act = get_activity(d)

        if act['activity'] != "已承租" and act['activity'] != "未開放":
            # Send to Discord channel by Webhook
            webhook_url = os.getenv("WEBHOOK_URL")
            requests.post(webhook_url, json={
                "content": f"{d.year}/{d.month}/{d.day} {act['activity']}",
                "embeds": [
                    {
                        "title": "明日小巨蛋活動通知",
                        "color": 15258703,
                        "fields": [
                            {
                                "name": "活動名稱",
                                "value": act['activity']
                            },
                            {
                                "name": "活動日期",
                                "value": f"{d.year}/{d.month}/{d.day}"
                            }
                        ]
                    }
                ]
            })
    else:
        print("Please pass DATE and WEBHOOK_URL env variable.")
