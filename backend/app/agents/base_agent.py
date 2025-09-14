from abc import ABC, abstractmethod
from typing import Dict, Any, List
import asyncio
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BaseAgent(ABC):
    """Base class for all AI agents in the system"""

    def __init__(self, name: str):
        self.name = name
        self.logger = logging.getLogger(f"agent.{name}")

    @abstractmethod
    async def execute(self, **kwargs) -> Dict[str, Any]:
        """Execute the agent's main functionality"""
        pass

    async def log_execution(self, action: str, data: Dict[str, Any] = None):
        """Log agent execution details"""
        self.logger.info(f"Agent {self.name}: {action}", extra=data or {})

class AgentOrchestrator:
    """Orchestrates multiple agents working together"""

    def __init__(self):
        self.agents: Dict[str, BaseAgent] = {}
        self.logger = logging.getLogger("orchestrator")

    def register_agent(self, agent: BaseAgent):
        """Register an agent with the orchestrator"""
        self.agents[agent.name] = agent
        self.logger.info(f"Registered agent: {agent.name}")

    async def execute_workflow(self, workflow: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Execute a series of agent tasks in sequence or parallel"""
        results = {}

        for step in workflow:
            agent_name = step.get("agent")
            action = step.get("action", "execute")
            params = step.get("params", {})
            parallel = step.get("parallel", False)

            if agent_name not in self.agents:
                raise ValueError(f"Agent {agent_name} not registered")

            agent = self.agents[agent_name]

            try:
                self.logger.info(f"Executing {action} on agent {agent_name}")
                if parallel:
                    # For parallel execution, we'd need to modify this
                    # For now, executing sequentially
                    result = await agent.execute(**params)
                else:
                    result = await agent.execute(**params)

                results[agent_name] = result
                await agent.log_execution(f"Completed {action}", {"result_keys": list(result.keys())})

            except Exception as e:
                self.logger.error(f"Error executing {action} on agent {agent_name}: {str(e)}")
                results[agent_name] = {"error": str(e)}

        return results