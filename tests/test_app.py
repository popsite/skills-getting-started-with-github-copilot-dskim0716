from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_unregister_participant_from_activity():
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    response = client.delete(f"/activities/{activity_name}/signup?email={email}")

    assert response.status_code == 200
    assert response.json()["message"] == f"Removed {email} from {activity_name}"

    # Ensure the participant is no longer present
    activities_response = client.get("/activities")
    activity = activities_response.json()[activity_name]
    assert email not in activity["participants"]


def test_unregister_unknown_participant_returns_404():
    activity_name = "Chess Club"
    email = "unknown@mergington.edu"

    response = client.delete(f"/activities/{activity_name}/signup?email={email}")

    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"
