from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Dict, Optional
from databases import Database
from db import database
from services import RefundService  # Assuming RefundService is in a `services` module

# Pydantic models for requests and responses
class RefundRequest(BaseModel):
    orderid: int
    products: List[Dict[str, int]]  # List of {"productid": int, "quantity": int}

class RefundResponse(BaseModel):
    orderid: int
    refunded_amount: Optional[float] = None
    status: str

class RefundValidityResponse(BaseModel):
    orderid: int
    valid: bool
    reason: Optional[str] = None

class RefundSelectionResponse(BaseModel):
    orderid: int
    products: List[Dict[str, int]]  # List of {"productid": int, "quantity": int}

class RefundDecision(BaseModel):
    orderid: int
    approved: bool

# Create an APIRouter instance
router = APIRouter()

@router.get("/refund/validate/{orderid}", response_model=RefundValidityResponse)
async def validate_refund(orderid: int):
    """
    Validate if an order is eligible for a refund.

    Args:
        orderid (int): The ID of the order to validate.

    Returns:
        RefundValidityResponse: Indicates if the refund is valid and the reason if not.
    """
    refund_service = RefundService(database)
    try:
        await refund_service.validate_order_for_refund(orderid)
        return RefundValidityResponse(orderid=orderid, valid=True)
    except ValueError as e:
        return RefundValidityResponse(orderid=orderid, valid=False, reason=str(e))

@router.get("/refund/select/{orderid}", response_model=RefundSelectionResponse)
async def get_refundable_products(orderid: int):
    """
    Get products from an order that can be selected for a refund.

    Args:
        orderid (int): The ID of the order.

    Returns:
        RefundSelectionResponse: List of refundable products with quantities.
    """
    query_products = """
        SELECT productid, quantity
        FROM order_items
        WHERE orderid = :orderid AND quantity > 0
    """
    products = await database.fetch_all(query_products, {"orderid": orderid})
    return RefundSelectionResponse(orderid=orderid, products=[dict(product) for product in products])

@router.post("/refund/request")
async def request_refund(
    refund_request: RefundRequest,
):
    """
    Customer requests a refund for selected products.

    Args:
        refund_request (RefundRequest): Contains order ID and selected products for refund.

    Raises:
        HTTPException: If validation fails.
    """
    try:
        # Insert the refund request into a "refund_requests" table for manager approval
        async with database.transaction():
            for product in refund_request.products:
                query_insert_request = """
                    INSERT INTO refund_requests (orderid, productid, quantity)
                    VALUES (:orderid, :productid, :quantity)
                """
                await database.execute(query_insert_request, {
                    "orderid": refund_request.orderid,
                    "productid": product["productid"],
                    "quantity": product["quantity"]
                })
        return {"message": "Refund request submitted and pending manager approval."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@router.post("/refund/decision", response_model=RefundResponse)
async def manager_decision(
    decision: RefundDecision,
):
    """
    Manager accepts or denies a refund request.

    Args:
        decision (RefundDecision): Contains the order ID and manager's decision.

    Returns:
        RefundResponse: Refund details if approved, or denial status.
    """
    refund_service = RefundService(database)

    if decision.approved:
        try:
            # Fetch pending refund requests
            query_pending_request = """
                SELECT productid, quantity
                FROM refund_requests
                WHERE orderid = :orderid
            """
            products = await database.fetch_all(query_pending_request, {"orderid": decision.orderid})

            if not products:
                raise HTTPException(status_code=404, detail="No pending refund request found.")

            # Process the refund
            refunded_amount = await refund_service.process_refund(
                decision.orderid, [dict(product) for product in products]
            )

            # Clear pending refund requests after processing
            query_clear_requests = """
                DELETE FROM refund_requests
                WHERE orderid = :orderid
            """
            await database.execute(query_clear_requests, {"orderid": decision.orderid})

            query_remaining_items = """
                SELECT COUNT(*) AS remaining_items
                FROM order_items
                WHERE orderid = :orderid AND quantity > 0
            """
            remaining_items = await database.fetch_one(
                query_remaining_items, {"orderid": decision.orderid}
            )

            status = "Partially Refunded" if remaining_items["remaining_items"] > 0 else "Refunded"

            return RefundResponse(
                orderid=decision.orderid,
                refunded_amount=refunded_amount,
                status=status
            )
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    else:
        # Deny refund request
        query_deny_request = """
            DELETE FROM refund_requests
            WHERE orderid = :orderid
        """
        await database.execute(query_deny_request, {"orderid": decision.orderid})
        return RefundResponse(
            orderid=decision.orderid,
            refunded_amount=0.0,
            status="Denied"
        )
