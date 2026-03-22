"""Central tool registry.

Both graph nodes and any agent executor import TOOLS from here.
Adding a new tool = adding one line to this list.
"""

from langchain_core.tools import BaseTool

from agent.tools.faq import search_faq
from agent.tools.ticketing import create_support_ticket

TOOLS: list[BaseTool] = [search_faq, create_support_ticket]

__all__ = ["TOOLS", "search_faq", "create_support_ticket"]
