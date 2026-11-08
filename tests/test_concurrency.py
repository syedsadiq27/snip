from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed

from app.db import connect


def test_concurrent_posts_same_alias(client, db_path):
    def create_once():
        return client.post(
            "/api/links",
            json={"url": "https://example.com/race", "alias": "race-alias"},
        )

    results = []
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = [executor.submit(create_once) for _ in range(8)]
        for future in as_completed(futures):
            results.append(future.result())

    statuses = sorted(response.status_code for response in results)
    assert statuses.count(201) == 1
    assert statuses.count(409) == 7

    conn = connect(db_path)
    count = conn.execute(
        "SELECT COUNT(*) AS c FROM links WHERE alias = ? COLLATE NOCASE",
        ("race-alias",),
    ).fetchone()["c"]
    conn.close()
    assert count == 1
