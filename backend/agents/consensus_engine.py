from typing import Dict, Any, List
import numpy as np
from datetime import datetime

class ConsensusEngine:
    """Orchestrates multi-agent analysis and consensus decision making"""
    
    def __init__(self):
        self.consensus_threshold = 0.6
        self.min_agent_count = 3
    
    def process_multi_agent_analysis(
        self,
        agent_outputs: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Process outputs from all agents and generate consensus decision
        """
        if not agent_outputs or len(agent_outputs) < self.min_agent_count:
            return self._generate_error_consensus("Insufficient agent outputs")
        
        # Extract predictions and confidences
        predictions = [a.get("prediction") for a in agent_outputs]
        confidences = [a.get("confidence", 0.5) for a in agent_outputs]
        
        # Find consensus prediction (voting)
        unique_predictions = list(set(predictions))
        prediction_votes = {pred: predictions.count(pred) for pred in unique_predictions}
        consensus_prediction = max(prediction_votes, key=prediction_votes.get)
        
        # Calculate consensus metrics
        voting_ratio = prediction_votes[consensus_prediction] / len(agent_outputs)
        avg_confidence = np.mean(confidences)
        std_confidence = np.std(confidences)
        
        # Identify agreeing and disagreeing agents
        agreeing_agents = [a for a in agent_outputs if a.get("prediction") == consensus_prediction]
        disagreeing_agents = [a for a in agent_outputs if a.get("prediction") != consensus_prediction]
        
        # Generate reasoning for consensus
        if consensus_prediction in ["INVALID", "WRONG_IMAGE"]:
            reasoning = "System rejected the input: This does not appear to be a valid blood group sample image."
        else:
            reasoning = self._generate_consensus_reasoning(
                consensus_prediction,
                agreeing_agents,
                disagreeing_agents,
                voting_ratio,
                avg_confidence
            )
        
        # Determine overall confidence
        overall_confidence = (
            0.6 * voting_ratio +
            0.4 * avg_confidence
        )
        
        # Check if consensus is strong enough
        consensus_met = voting_ratio >= self.consensus_threshold
        
        return {
            "consensus_prediction": consensus_prediction,
            "consensus_confidence": float(min(1.0, overall_confidence)),
            "consensus_met": bool(consensus_met),
            "voting_ratio": float(voting_ratio),
            "agent_votes": {str(k): int(v) for k, v in prediction_votes.items()},
            "agreeing_agents": [a.get("agent_name") for a in agreeing_agents],
            "disagreeing_agents": [a.get("agent_name") for a in disagreeing_agents],
            "average_confidence": float(avg_confidence),
            "confidence_std": float(std_confidence),
            "reasoning": reasoning,
            "all_agent_outputs": agent_outputs,
            "timestamp": datetime.now().isoformat(),
        }
    
    def _generate_consensus_reasoning(
        self,
        prediction: str,
        agreeing: List[Dict],
        disagreeing: List[Dict],
        ratio: float,
        avg_conf: float
    ) -> str:
        """Generate human-readable consensus explanation"""
        agreement_text = (
            f"{len(agreeing)}/{len(agreeing) + len(disagreeing)} agents "
            f"({ratio:.0%}) agree on blood type: {prediction}"
        )
        
        confidence_text = f"Average confidence: {avg_conf:.0%}"
        
        if disagreeing:
            disagreement_text = (
                f"Disagreement: {', '.join([a.get('agent_name') for a in disagreeing])} "
                f"predicted differently. {' '.join([a.get('reasoning', '') for a in disagreeing])}"
            )
        else:
            disagreement_text = "All agents are in agreement."
        
        return f"{agreement_text}. {confidence_text}. {disagreement_text}"
    
    def _generate_error_consensus(self, error_msg: str) -> Dict[str, Any]:
        """Generate error consensus response"""
        return {
            "consensus_prediction": "ERROR",
            "consensus_confidence": 0.0,
            "consensus_met": False,
            "agent_votes": {},
            "reasoning": f"Consensus failed: {error_msg}",
            "error": error_msg,
            "timestamp": datetime.now().isoformat(),
        }
