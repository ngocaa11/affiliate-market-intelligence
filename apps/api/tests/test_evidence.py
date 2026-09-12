from datetime import UTC, datetime


def add_evidence(client, project_id, **overrides):
    payload = {
        "evidence_type": "SOURCE_RECORD",
        "summary": "Observed source record",
        "source_ref": "SRC-001",
        "captured_at": datetime.now(UTC).isoformat(),
        "confidence": 0.8,
        "freshness": "FRESH",
        **overrides,
    }
    return client.post(f"/api/v1/projects/{project_id}/evidence", json=payload)


def test_estimates_require_explicit_method(client, project):
    response = add_evidence(client, project["id"], estimated=True)
    assert response.status_code == 422
    accepted = add_evidence(client, project["id"], estimated=True, estimation_method="FORMULA_V1")
    assert accepted.status_code == 201
    assert accepted.json()["estimated"] is True


def test_rejected_evidence_is_excluded_from_packages(client, project):
    evidence = add_evidence(client, project["id"]).json()
    rejected = client.post(
        f"/api/v1/projects/{project['id']}/evidence/{evidence['id']}/actions",
        json={"action": "REJECT", "actor_id": "reviewer"},
    )
    assert rejected.json()["rejected"] is True
    package = client.post(
        f"/api/v1/projects/{project['id']}/packages", json={"evidence_ids": [evidence["id"]]}
    )
    assert package.status_code == 422


def test_pin_reject_restore_actions_are_audited(client, project):
    evidence = add_evidence(client, project["id"]).json()
    for action in ("PIN", "REJECT", "RESTORE"):
        response = client.post(
            f"/api/v1/projects/{project['id']}/evidence/{evidence['id']}/actions",
            json={"action": action, "actor_id": "reviewer"},
        )
        assert response.status_code == 200
    assert response.json()["pinned"] is False
    assert response.json()["rejected"] is False
    audit = client.get(f"/api/v1/projects/{project['id']}/audit").json()
    assert {event["action"] for event in audit} >= {
        "EVIDENCE_PIN",
        "EVIDENCE_REJECT",
        "EVIDENCE_RESTORE",
    }
