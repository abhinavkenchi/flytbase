def rank_score(alert):
    sev = {"HIGH": 3, "MEDIUM": 2, "LOW": 1}
    return (sev.get(alert["severity"], 0), -alert["eta"])


def group_alerts(raw_alerts):
    grouped = {}

    for alert in raw_alerts:
        a = alert["a"]
        b = alert["b"]

        for drone in [a, b]:
            if drone not in grouped:
                grouped[drone] = {
                    "drone": drone,
                    "count": 0,
                    "highest": alert["severity"],
                    "nearest_eta": alert["eta"],
                    "conflicts": [],
                }

            grouped[drone]["count"] += 1
            grouped[drone]["conflicts"].append(alert)

            if alert["eta"] < grouped[drone]["nearest_eta"]:
                grouped[drone]["nearest_eta"] = alert["eta"]

            if rank_score(alert) > rank_score(
                {"severity": grouped[drone]["highest"], "eta": grouped[drone]["nearest_eta"]}
            ):
                grouped[drone]["highest"] = alert["severity"]

    return sorted(
        grouped.values(),
        key=lambda x: (
            {"HIGH": 3, "MEDIUM": 2, "LOW": 1}[x["highest"]],
            -x["count"],
            -x["nearest_eta"],
        ),
        reverse=True,
    )