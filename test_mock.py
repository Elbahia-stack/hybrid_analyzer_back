from main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_analyze_text_full_mock(mocker):
    mocker.patch("main.verify_token", return_value=True)

    mocker.patch("main.classify_text", return_value=("science", 0.95))

    
    mocker.patch("main.analyze_with_gemini", return_value={"ton": "positive"})

    resp = client.post(
        "/analyze",
        json={"text": "I love coding"},
        headers={"Authorization": "Bearer fake_token"}
    )

   
    assert resp.status_code == 200
    data = resp.json()

    assert data["hf_category"] == "science"
    assert data["gemini_analysis"]["ton"] == "positive"
    assert data["input_text"] == "I love coding"
