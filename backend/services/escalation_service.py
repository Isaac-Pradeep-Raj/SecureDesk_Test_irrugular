ESCALATION_CONTACTS = {
    "HR": {
        "name": "HR Department",
        "email": "hr@company.com",
        "phone": "Ext 204"
    },
    "IT": {
        "name": "IT Support",
        "email": "it@company.com",
        "phone": "Ext 310"
    },
    "DEV": {
        "name": "Development Team",
        "email": "dev@company.com",
        "phone": "Ext 415"
    },
    "Security": {
        "name": "Security Office",
        "email": "security@company.com",
        "phone": "Ext 500"
    }
}


def build_escalation_response(domain, classification):
    contact = ESCALATION_CONTACTS.get(domain)

    if classification == "CONFIDENTIAL":
        message = (
            "This information is confidential and cannot be displayed."
        )

    elif classification == "RESTRICTED":
        message = (
            "This information has restricted access."
        )
    else:
        message = "Contact department for clarification."

    return {
        "message": message,
        "contact": contact
    }