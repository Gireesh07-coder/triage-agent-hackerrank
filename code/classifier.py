from pydantic import BaseModel
from typing import Literal


class TicketClassification(BaseModel):
    company: Literal["HackerRank", "Claude", "Visa", "None"]
    request_type: str
    product_area: str
    status: Literal["Replied", "Escalated"]
    justification: str


def classify_ticket(issue: str, subject: str) -> TicketClassification:
    text = (issue + " " + subject).lower()

    high_risk_words = [
        "fraud", "unauthorized", "stolen", "lost",
        "payment", "charge", "refund", "money",
        "account locked", "cannot access",
        "identity", "dispute", "hack"
    ]

    if any(word in text for word in high_risk_words):
        if "visa" in text:
            return TicketClassification(
                company="Visa",
                request_type="high_risk",
                product_area="security",
                status="Escalated",
                justification="Financial risk"
            )
        elif "hackerrank" in text or "test" in text:
            return TicketClassification(
                company="HackerRank",
                request_type="high_risk",
                product_area="assessments",
                status="Escalated",
                justification="Assessment risk"
            )
        elif "claude" in text:
            return TicketClassification(
                company="Claude",
                request_type="high_risk",
                product_area="access",
                status="Escalated",
                justification="Account risk"
            )
        else:
            return TicketClassification(
                company="None",
                request_type="high_risk",
                product_area="general",
                status="Escalated",
                justification="General risk"
            )

    if "claude" in text:
        return TicketClassification(
            company="Claude",
            request_type="product_issue",
            product_area="conversation",
            status="Replied",
            justification="Claude query"
        )

    elif "visa" in text:
        return TicketClassification(
            company="Visa",
            request_type="product_issue",
            product_area="card_support",
            status="Replied",
            justification="Visa query"
        )

    elif any(k in text for k in ["hackerrank", "test", "assessment", "candidate"]):
        return TicketClassification(
            company="HackerRank",
            request_type="product_issue",
            product_area="assessments",
            status="Replied",
            justification="HR query"
        )

    return TicketClassification(
        company="None",
        request_type="invalid",
        product_area="general",
        status="Replied",
        justification="Out of scope"
    )