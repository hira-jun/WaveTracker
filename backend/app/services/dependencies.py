from fastapi import Header, HTTPException

from app.services.admin_auth import AdminAuthService
from app.services.storage.local_blob_adapter import LocalBlobAdapter
from app.services.storage.local_table_adapter import LocalTableAdapter


table_adapter = LocalTableAdapter()
blob_adapter = LocalBlobAdapter()
admin_auth = AdminAuthService()


def require_admin_access(authorization: str | None = Header(default=None)) -> str:
	if authorization is None or not authorization.startswith("Bearer "):
		raise HTTPException(status_code=401, detail="admin authentication required")

	token = authorization.removeprefix("Bearer ").strip()
	if not token or not admin_auth.validate_token(token):
		raise HTTPException(status_code=401, detail="invalid admin token")
	return token
