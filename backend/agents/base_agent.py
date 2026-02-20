from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, Any

class BaseAgent(ABC):
    """Base class for all specialized agents"""
    
    def __init__(self, agent_id: str, agent_name: str):
        self.agent_id = agent_id
        self.agent_name = agent_name
        self.created_at = datetime.now()
    
    @abstractmethod
    def analyze(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze input data and return agent's assessment
        
        Returns:
            {
                "agent_id": str,
                "agent_name": str,
                "prediction": str or float,
                "confidence": float (0-1),
                "reasoning": str,
                "agree": bool,
                "metadata": dict
            }
        """
        pass
    
    def _format_output(
        self,
        prediction: Any,
        confidence: float,
        reasoning: str,
        agree: bool = True,
        metadata: Dict = None
    ) -> Dict[str, Any]:
        """Format agent output consistently"""
        return {
            "agent_id": self.agent_id,
            "agent_name": self.agent_name,
            "prediction": prediction,
            "confidence": max(0.0, min(1.0, confidence)),  # Clamp 0-1
            "reasoning": reasoning,
            "agree": agree,
            "metadata": metadata or {},
            "timestamp": datetime.now().isoformat(),
        }
