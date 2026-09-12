def test_create_project_persists_draft_workflow_and_audit(client):
    response = client.post(
        "/api/v1/projects",
        json={
            "name": "Keyword study",
            "mode": "KEYWORD_FIRST",
            "objective": "Understand easy-clean demand",
            "created_by": "human-1",
        },
    )
    assert response.status_code == 201
    project = response.json()
    workflow = client.get(f"/api/v1/projects/{project['id']}/workflow").json()
    assert workflow["current_stage"] == "SCOPE"
    assert workflow["state"] == "DRAFT"
    audit = client.get(f"/api/v1/projects/{project['id']}/audit").json()
    assert audit[0]["action"] == "PROJECT_CREATED"
    assert audit[0]["actor_type"] == "HUMAN"


def test_scopes_are_versioned_and_not_overwritten(client, project):
    first = client.post(
        f"/api/v1/projects/{project['id']}/scopes",
        json={"seed_keywords": ["máy sữa hạt"], "created_by": "user-1"},
    )
    assert first.status_code == 201
    second = client.post(
        f"/api/v1/projects/{project['id']}/scopes",
        json={
            "seed_keywords": ["máy sữa hạt dễ vệ sinh"],
            "created_by": "user-1",
            "parent_scope_id": first.json()["id"],
        },
    )
    assert second.status_code == 201
    scopes = client.get(f"/api/v1/projects/{project['id']}/scopes").json()
    assert [scope["version"] for scope in scopes] == [2, 1]
    assert scopes[1]["seed_keywords"] == ["máy sữa hạt"]
