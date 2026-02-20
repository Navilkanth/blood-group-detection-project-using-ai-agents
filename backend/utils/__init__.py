"""Utils module for Blood Group Classification Backend"""
from .logger import setup_logger

# Lazy imports to avoid circular dependencies
def get_database_functions():
    """Lazy import database functions"""
    from .database import init_db, save_prediction, get_prediction, log_audit
    return init_db, save_prediction, get_prediction, log_audit

__all__ = [
    "setup_logger",
    "get_database_functions",
]
