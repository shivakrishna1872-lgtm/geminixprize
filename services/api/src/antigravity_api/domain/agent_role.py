from enum import Enum


class AgentRole(str, Enum):
    CEO = "ceo"
    RESEARCH = "research"
    BRANDING = "branding"
    PRODUCT = "product"
    STORE = "store"
    MARKETING = "marketing"
    SALES = "sales"
    FINANCE = "finance"
    SUPPORT = "support"
