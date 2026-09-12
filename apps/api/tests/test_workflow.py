def scoped_project(client, project):
    client.post(
        f"/api/v1/projects/{project['id']}/scopes",
        json={"platforms": ["SHOPEE"], "created_by": "user-1"},
    )
    return project["id"]


def transition(client, project_id, target):
    return client.post(
        f"/api/v1/projects/{project_id}/machine-transitions", json={"target_state": target}
    )


def test_workflow_enforces_machine_sequence_and_human_data_gate(client, project):
    project_id = scoped_project(client, project)
    assert transition(client, project_id, "DATA_REVIEW").status_code == 409
    for target in ("COLLECTING", "DATA_VALIDATION", "DATA_REVIEW"):
        assert transition(client, project_id, target).status_code == 200
    blocked = transition(client, project_id, "DATA_APPROVED")
    assert blocked.status_code == 409
    approved = client.post(
        f"/api/v1/projects/{project_id}/decisions",
        json={"decision": "APPROVE", "actor_type": "HUMAN", "actor_id": "reviewer"},
    )
    assert approved.status_code == 200
    assert approved.json()["state"] == "DATA_APPROVED"


def test_ai_cannot_approve_and_analysis_requires_package(client, project):
    project_id = scoped_project(client, project)
    for target in ("COLLECTING", "DATA_VALIDATION", "DATA_REVIEW"):
        transition(client, project_id, target)
    denied = client.post(
        f"/api/v1/projects/{project_id}/decisions",
        json={"decision": "APPROVE", "actor_type": "AI", "actor_id": "model"},
    )
    assert denied.status_code == 403
    client.post(
        f"/api/v1/projects/{project_id}/decisions",
        json={"decision": "APPROVE", "actor_type": "HUMAN", "actor_id": "reviewer"},
    )
    transition(client, project_id, "ANALYZING")
    transition(client, project_id, "ANALYSIS_REVIEW")
    missing = client.post(
        f"/api/v1/projects/{project_id}/decisions",
        json={"decision": "APPROVE", "actor_type": "HUMAN", "actor_id": "reviewer"},
    )
    assert missing.status_code == 409
    package = client.post(
        f"/api/v1/projects/{project_id}/packages",
        json={"selected_entities": [], "evidence_ids": []},
    )
    assert package.status_code == 201
    approved = client.post(
        f"/api/v1/projects/{project_id}/decisions",
        json={"decision": "APPROVE", "actor_type": "HUMAN", "actor_id": "reviewer"},
    )
    assert approved.json()["state"] == "STAGE_APPROVED"
    packages = client.get(f"/api/v1/projects/{project_id}/packages").json()
    assert packages[0]["status"] == "APPROVED"
    assert packages[0]["approved_by"] == "reviewer"


def test_mode_specific_next_stage_is_deterministic(client, project):
    project_id = scoped_project(client, project)
    for target in ("COLLECTING", "DATA_VALIDATION", "DATA_REVIEW"):
        transition(client, project_id, target)
    client.post(
        f"/api/v1/projects/{project_id}/decisions",
        json={"decision": "APPROVE", "actor_type": "HUMAN", "actor_id": "reviewer"},
    )
    transition(client, project_id, "ANALYZING")
    transition(client, project_id, "ANALYSIS_REVIEW")
    client.post(f"/api/v1/projects/{project_id}/packages", json={})
    client.post(
        f"/api/v1/projects/{project_id}/decisions",
        json={"decision": "APPROVE", "actor_type": "HUMAN", "actor_id": "reviewer"},
    )
    transition(client, project_id, "NEXT_STAGE")
    result = transition(client, project_id, "COLLECTING")
    assert result.json()["current_stage"] == "MARKET"
