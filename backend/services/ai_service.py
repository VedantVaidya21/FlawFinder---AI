import os
import json
import time
from typing import Dict, List, Any
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import networkx as nx
from dotenv import load_dotenv

load_dotenv()

class AIAnalysisService:
    def __init__(self):
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.llm = OpenAI(
            openai_api_key=self.openai_api_key,
            temperature=0.7,
            max_tokens=2000
        ) if self.openai_api_key else None
        
    def analyze_workflow(self, workflow_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze workflow and identify flaws."""
        start_time = time.time()
        
        # Build workflow graph
        graph = self._build_workflow_graph(workflow_data)
        
        # Analyze with AI (mock implementation for now)
        if self.llm:
            analysis = self._analyze_with_ai(workflow_data, graph)
        else:
            analysis = self._mock_analysis(workflow_data)
        
        processing_time = time.time() - start_time
        
        return {
            "flaws": analysis["flaws"],
            "fix_suggestions": analysis["fix_suggestions"],
            "brutality_score": analysis["brutality_score"],
            "total_flaws": len(analysis["flaws"]),
            "processing_time": processing_time
        }
    
    def _build_workflow_graph(self, workflow_data: Dict[str, Any]) -> nx.DiGraph:
        """Build a NetworkX graph from workflow data."""
        G = nx.DiGraph()
        
        # Mock graph building logic
        # In real implementation, this would parse the workflow data
        # and create nodes and edges based on the workflow structure
        
        if isinstance(workflow_data, dict) and "steps" in workflow_data:
            steps = workflow_data["steps"]
            for i, step in enumerate(steps):
                G.add_node(i, **step)
                if i > 0:
                    G.add_edge(i-1, i)
        
        return G
    
    def _analyze_with_ai(self, workflow_data: Dict[str, Any], graph: nx.DiGraph) -> Dict[str, Any]:
        """Analyze workflow using OpenAI."""
        
        # Create analysis prompt
        prompt_template = PromptTemplate(
            input_variables=["workflow_data"],
            template="""
            Analyze the following business workflow and identify potential flaws:
            
            Workflow Data: {workflow_data}
            
            Please identify:
            1. Bottlenecks in the process
            2. Redundancies
            3. Security vulnerabilities
            4. Inefficiencies
            5. Missing steps or validations
            
            For each flaw, provide:
            - Type (bottleneck, redundancy, security, inefficiency, missing_step)
            - Severity (low, medium, high, critical)
            - Title
            - Description
            - Location in workflow
            - Impact score (0-10)
            
            Also provide fix suggestions for each flaw with:
            - Title
            - Description
            - Implementation effort (low, medium, high)
            - Expected impact (low, medium, high)
            - Priority (1-5)
            - Estimated time
            
            Calculate a brutality score (0-10) based on the severity and number of flaws.
            
            Return the response in JSON format.
            """
        )
        
        chain = LLMChain(llm=self.llm, prompt=prompt_template)
        
        try:
            response = chain.run(workflow_data=json.dumps(workflow_data))
            # Parse AI response (in real implementation, you'd parse the JSON)
            return self._parse_ai_response(response)
        except Exception as e:
            print(f"AI Analysis failed: {e}")
            return self._mock_analysis(workflow_data)
    
    def _parse_ai_response(self, response: str) -> Dict[str, Any]:
        """Parse AI response into structured format."""
        # Mock parsing - in real implementation, parse the JSON response
        return self._mock_analysis({})
    
    def _mock_analysis(self, workflow_data: Dict[str, Any]) -> Dict[str, Any]:
        """Mock analysis for testing purposes."""
        
        mock_flaws = [
            {
                "flaw_type": "bottleneck",
                "severity": "high",
                "title": "Manual Approval Bottleneck",
                "description": "Manual approval process causes significant delays in workflow execution",
                "location": "Step 3: Approval Process",
                "impact_score": 8.5
            },
            {
                "flaw_type": "redundancy",
                "severity": "medium",
                "title": "Duplicate Data Entry",
                "description": "Customer information is entered multiple times across different steps",
                "location": "Steps 1, 4, 7",
                "impact_score": 6.0
            },
            {
                "flaw_type": "security",
                "severity": "critical",
                "title": "Unencrypted Data Transfer",
                "description": "Sensitive customer data is transmitted without encryption",
                "location": "Step 5: Data Transfer",
                "impact_score": 9.8
            },
            {
                "flaw_type": "inefficiency",
                "severity": "low",
                "title": "Unnecessary Email Notifications",
                "description": "Too many email notifications slow down the process",
                "location": "Multiple steps",
                "impact_score": 3.2
            }
        ]
        
        mock_fix_suggestions = [
            {
                "title": "Implement Automated Approval System",
                "description": "Replace manual approval with rule-based automated system for standard cases",
                "implementation_effort": "high",
                "expected_impact": "high",
                "priority": 1,
                "estimated_time": "2-3 weeks"
            },
            {
                "title": "Centralize Data Entry",
                "description": "Create a single data entry point that populates all required fields",
                "implementation_effort": "medium",
                "expected_impact": "medium",
                "priority": 2,
                "estimated_time": "1-2 weeks"
            },
            {
                "title": "Implement End-to-End Encryption",
                "description": "Add SSL/TLS encryption for all data transmission",
                "implementation_effort": "medium",
                "expected_impact": "high",
                "priority": 1,
                "estimated_time": "1 week"
            },
            {
                "title": "Optimize Notification System",
                "description": "Reduce email notifications to essential ones only",
                "implementation_effort": "low",
                "expected_impact": "low",
                "priority": 3,
                "estimated_time": "2-3 days"
            }
        ]
        
        # Calculate brutality score based on severity distribution
        severity_weights = {"critical": 10, "high": 7, "medium": 5, "low": 2}
        total_score = sum(severity_weights.get(flaw["severity"], 0) for flaw in mock_flaws)
        avg_score = total_score / len(mock_flaws) if mock_flaws else 0
        brutality_score = min(avg_score, 10.0)
        
        return {
            "flaws": mock_flaws,
            "fix_suggestions": mock_fix_suggestions,
            "brutality_score": brutality_score
        }
    
    def generate_report(self, workflow_id: int, flaws: List[Dict], fix_suggestions: List[Dict]) -> Dict[str, Any]:
        """Generate executive report."""
        
        # Calculate statistics
        total_flaws = len(flaws)
        severity_counts = {"critical": 0, "high": 0, "medium": 0, "low": 0}
        
        for flaw in flaws:
            severity = flaw.get("severity", "low")
            if severity in severity_counts:
                severity_counts[severity] += 1
        
        # Calculate brutality score
        severity_weights = {"critical": 10, "high": 7, "medium": 5, "low": 2}
        total_score = sum(severity_weights[severity] * count for severity, count in severity_counts.items())
        brutality_score = (total_score / total_flaws) if total_flaws > 0 else 0
        
        # Generate executive summary
        executive_summary = self._generate_executive_summary(
            total_flaws, severity_counts, brutality_score
        )
        
        # Calculate improvement percentage
        improvement_percentage = min(100 - (brutality_score * 10), 100)
        
        return {
            "workflow_id": workflow_id,
            "executive_summary": executive_summary,
            "total_flaws": total_flaws,
            "critical_flaws": severity_counts["critical"],
            "high_flaws": severity_counts["high"],
            "medium_flaws": severity_counts["medium"],
            "low_flaws": severity_counts["low"],
            "brutality_score": brutality_score,
            "improvement_percentage": improvement_percentage,
            "recommendations": self._generate_recommendations(fix_suggestions)
        }
    
    def _generate_executive_summary(self, total_flaws: int, severity_counts: Dict, brutality_score: float) -> str:
        """Generate executive summary text."""
        
        if total_flaws == 0:
            return "Congratulations! Your workflow analysis shows no significant flaws detected."
        
        summary = f"Workflow Analysis Summary: {total_flaws} flaws detected with a brutality score of {brutality_score:.1f}/10. "
        
        if severity_counts["critical"] > 0:
            summary += f"URGENT: {severity_counts['critical']} critical issues require immediate attention. "
        
        if severity_counts["high"] > 0:
            summary += f"{severity_counts['high']} high-priority issues need resolution within this sprint. "
        
        if brutality_score >= 8:
            summary += "This workflow requires significant improvements to meet industry standards."
        elif brutality_score >= 5:
            summary += "This workflow has room for improvement but is generally functional."
        else:
            summary += "This workflow is well-designed with minor optimization opportunities."
        
        return summary
    
    def _generate_recommendations(self, fix_suggestions: List[Dict]) -> Dict[str, Any]:
        """Generate structured recommendations."""
        
        high_priority = [s for s in fix_suggestions if s.get("priority", 5) <= 2]
        medium_priority = [s for s in fix_suggestions if s.get("priority", 5) == 3]
        low_priority = [s for s in fix_suggestions if s.get("priority", 5) >= 4]
        
        return {
            "immediate_actions": high_priority,
            "short_term_improvements": medium_priority,
            "long_term_optimizations": low_priority,
            "estimated_total_time": "4-8 weeks",
            "expected_roi": "25-40% efficiency improvement"
        }
