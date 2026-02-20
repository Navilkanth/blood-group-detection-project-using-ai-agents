"""
Integration tests for consensus engine and multi-agent analysis
"""
import pytest
from agents.consensus_engine import ConsensusEngine

class TestConsensusEngine:
    """Test consensus engine functionality"""
    
    def test_initialization(self):
        """Test engine initialization"""
        engine = ConsensusEngine()
        assert engine.consensus_threshold == 0.6
        assert engine.min_agent_count == 3
    
    def test_unanimous_consensus(self, sample_agent_outputs):
        """Test unanimous agreement scenario"""
        engine = ConsensusEngine()
        result = engine.process_multi_agent_analysis(sample_agent_outputs)
        
        assert result["consensus_prediction"] == "O"
        assert result["voting_ratio"] == 1.0
        assert result["consensus_met"] == True
        assert len(result["agreeing_agents"]) == 3
        assert len(result["disagreeing_agents"]) == 0
    
    def test_majority_consensus(self, sample_agent_outputs):
        """Test majority agreement scenario"""
        # Modify one agent to disagree
        outputs = sample_agent_outputs.copy()
        outputs[1]["prediction"] = "A"
        
        engine = ConsensusEngine()
        result = engine.process_multi_agent_analysis(outputs)
        
        assert result["consensus_prediction"] == "O"
        assert 0.5 <= result["voting_ratio"] < 1.0
        assert result["consensus_met"] == True
        assert len(result["disagreeing_agents"]) == 1
    
    def test_conflicting_predictions(self, sample_agent_outputs):
        """Test conflicting predictions scenario"""
        outputs = sample_agent_outputs.copy()
        outputs[0]["prediction"] = "A"
        outputs[1]["prediction"] = "B"
        outputs[2]["prediction"] = "AB"
        
        engine = ConsensusEngine()
        result = engine.process_multi_agent_analysis(outputs)
        
        # Should pick one arbitrarily or by confidence
        assert result["consensus_prediction"] in ["A", "B", "AB"]
        assert result["voting_ratio"] < 1.0
    
    def test_insufficient_outputs(self):
        """Test handling of insufficient agent outputs"""
        engine = ConsensusEngine()
        result = engine.process_multi_agent_analysis([])
        
        assert result["consensus_prediction"] == "ERROR"
        assert result["consensus_met"] == False
        assert "error" in result
    
    def test_consensus_reasoning_generation(self, sample_agent_outputs):
        """Test reasoning text generation"""
        engine = ConsensusEngine()
        result = engine.process_multi_agent_analysis(sample_agent_outputs)
        
        assert "reasoning" in result
        assert len(result["reasoning"]) > 0
        assert "O" in result["reasoning"]  # Blood type mentioned
        assert "agents" in result["reasoning"].lower()  # Agents mentioned
