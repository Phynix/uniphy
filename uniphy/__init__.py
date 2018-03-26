"""
Init file of uniphy, empty
"""
__author__ = "Jonas Eschle 'Mayou36', Johannes Lade 'SebastianJL', Jim Buffat"
__version__ = '0.0.4-dev'

__all__ = ['output', 'decorators']

from .outputs.manager import OutputManager
from . import decorators

output = OutputManager()




