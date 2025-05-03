from fastapi.testclient import TestClient
from app.main import create_app

# Optionally set config path for test context
import os

os.environ["ENV"] = "testing"


app = create_app()
client = TestClient(app)
