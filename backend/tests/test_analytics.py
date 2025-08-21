from sqlmodel import select

from backend.app.models.analytics import AnalyticsEvent


def test_post_events(client, session):
    resp = client.post(
        "/analytics/events",
        json={"events": [{"name": "effect_toggle", "payload": {"enabled": True}}]},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["saved"] == 1

    events = session.exec(select(AnalyticsEvent)).all()
    assert len(events) == 1
    assert events[0].name == "effect_toggle"
    assert events[0].payload["enabled"] is True
