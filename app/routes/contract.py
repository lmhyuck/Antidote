from fastapi import APIRouter
from app.controller import contract

router = APIRouter(prefix="/api/legal", tags=["Legal Analysis"])


router.add_api_route("/contract", contract.contract, methods=["POST"])

