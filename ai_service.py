"""
AI Service Module - Handles all AI/LLM interactions
Supports both Claude API (primary) and Groq API (fallback)
"""

import os
import requests
import json
from typing import List, Dict, Any

class AIService:
    def __init__(self):
        # Claude API (Anthropic) - Primary
        self.claude_api_key = os.environ.get('ANTHROPIC_API_KEY', '')
        self.claude_base_url = "https://api.anthropic.com/v1/messages"
        self.claude_model = "claude-sonnet-4-20250514"  # Latest Sonnet
        
        # Groq API - Fallback
        self.groq_api_key = os.environ.get('GROQ_API_KEY', '')
        self.groq_base_url = "https://api.groq.com/openai/v1/chat/completions"
        self.groq_model = "llama-3.3-70b-versatile"
        
        # Choose which API to use by default
        self.use_claude = bool(self.claude_api_key)  # Use Claude if key is available
    
    def _make_request(self, messages: List[Dict], temperature: float = 0.7, max_tokens: int = 2000) -> str:
        """Make request to Claude API (primary) or Groq API (fallback)"""
        
        if self.use_claude and self.claude_api_key:
            return self._make_claude_request(messages, temperature, max_tokens)
        elif self.groq_api_key:
            return self._make_groq_request(messages, temperature, max_tokens)
        else:
            return self._generate_mock_response(messages)
    
    def _make_claude_request(self, messages: List[Dict], temperature: float = 0.7, max_tokens: int = 2000) -> str:
        """Make request to Claude API (Anthropic)"""
        
        headers = {
            "x-api-key": self.claude_api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }
        
        # Convert messages format from OpenAI to Claude format
        system_messages = [m['content'] for m in messages if m['role'] == 'system']
        system = "\n\n".join(system_messages) if system_messages else None
        
        # Get non-system messages
        conversation = [m for m in messages if m['role'] != 'system']
        
        payload = {
            "model": self.claude_model,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "messages": conversation
        }
        
        if system:
            payload["system"] = system
        
        try:
            response = requests.post(self.claude_base_url, headers=headers, json=payload, timeout=60)
            response.raise_for_status()
            
            data = response.json()
            return data['content'][0]['text']
            
        except requests.exceptions.RequestException as e:
            print(f"Claude API Error: {e}")
            # Fallback to Groq if Claude fails
            if self.groq_api_key:
                print("Falling back to Groq API...")
                return self._make_groq_request(messages, temperature, max_tokens)
            return f"Error: {str(e)}"
    
    def _make_groq_request(self, messages: List[Dict], temperature: float = 0.7, max_tokens: int = 2000) -> str:
        """Make request to Groq API"""
        
        headers = {
            "Authorization": f"Bearer {self.groq_api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.groq_model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        
        try:
            response = requests.post(self.groq_base_url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            return data['choices'][0]['message']['content']
            
        except requests.exceptions.RequestException as e:
            print(f"Groq API Error: {e}")
            return f"Error: {str(e)}"
    
    def _generate_mock_response(self, messages: List[Dict]) -> str:
        """Generate mock response for testing without API key"""
        last_message = messages[-1]['content']
        return f"[MOCK RESPONSE] Received: {last_message[:100]}... (Set GROQ_API_KEY to enable real AI)"
    
    def chat(self, message: str, context: str = "", history: List[Dict] = None) -> str:
        """
        Chat with AI assistant
        
        Args:
            message: User's question/message
            context: Additional context (course, topic, etc.)
            history: Previous conversation messages
        """
        if history is None:
            history = []
        
        system_prompt = """You are LabMate AI, an expert STEM tutor specializing in Chemical Engineering, 
        Chemistry, Physics, and Mathematics. You help university students understand complex concepts, 
        solve problems, and excel in their studies. 
        
        Your responses should be:
        - Clear and concise
        - Use analogies and examples
        - Include step-by-step explanations when solving problems
        - Encourage critical thinking
        - Relate concepts to real-world applications
        """
        
        messages = [{"role": "system", "content": system_prompt}]
        
        # Add context if provided
        if context:
            messages.append({"role": "system", "content": f"Context: {context}"})
        
        # Add conversation history
        messages.extend(history)
        
        # Add current message
        messages.append({"role": "user", "content": message})
        
        return self._make_request(messages, temperature=0.7)
    
    def explain_concept(self, concept: str, level: str = "undergraduate", include_examples: bool = True) -> Dict[str, Any]:
        """
        Explain a STEM concept in detail
        
        Args:
            concept: The concept to explain
            level: Education level (high_school, undergraduate, graduate)
            include_examples: Whether to include examples
        """
        
        prompt = f"""Explain the concept of "{concept}" for a {level} student.

Structure your explanation as follows:
1. Simple Definition (2-3 sentences)
2. Key Principles (bullet points)
3. Mathematical Representation (if applicable)
4. Real-world Applications
{"5. Worked Examples (2-3 examples)" if include_examples else ""}

Make it clear, engaging, and easy to understand."""

        messages = [
            {"role": "system", "content": "You are an expert STEM educator."},
            {"role": "user", "content": prompt}
        ]
        
        response = self._make_request(messages, temperature=0.5, max_tokens=3000)
        
        return {
            "concept": concept,
            "level": level,
            "explanation": response
        }
    
    def solve_formula(self, formula: str, known_values: Dict, solve_for: str) -> Dict[str, Any]:
        """
        Solve a formula with step-by-step explanation
        
        Args:
            formula: The formula (e.g., "PV = nRT")
            known_values: Dictionary of known variable values
            solve_for: Variable to solve for
        """
        
        known_str = ", ".join([f"{k} = {v}" for k, v in known_values.items()])
        
        prompt = f"""Solve this formula step-by-step:

Formula: {formula}
Known values: {known_str}
Solve for: {solve_for}

Please provide:
1. Rearranged formula (isolating {solve_for})
2. Step-by-step substitution
3. Calculation with units
4. Final answer with proper significant figures
5. Brief explanation of what the answer means"""

        messages = [
            {"role": "system", "content": "You are an expert in solving scientific formulas. Show all work clearly."},
            {"role": "user", "content": prompt}
        ]
        
        response = self._make_request(messages, temperature=0.3, max_tokens=2000)
        
        return {
            "formula": formula,
            "solve_for": solve_for,
            "solution": response
        }
    
    def generate_study_guide(self, topic: str, course_code: str = "") -> str:
        """
        Generate a comprehensive study guide for a topic
        
        Args:
            topic: The topic to create a study guide for
            course_code: Optional course code for context
        """
        
        course_context = f" for {course_code}" if course_code else ""
        
        prompt = f"""Create a comprehensive study guide for: {topic}{course_context}

Include:
1. Key Concepts Overview
2. Important Formulas and Equations
3. Common Misconceptions
4. Practice Problem Types
5. Study Tips and Tricks
6. Quick Reference Summary

Make it practical and useful for exam preparation."""

        messages = [
            {"role": "system", "content": "You are creating study materials for university STEM students."},
            {"role": "user", "content": prompt}
        ]
        
        return self._make_request(messages, temperature=0.6, max_tokens=3000)
    
    def check_answer(self, question: str, student_answer: str, correct_answer: str = None) -> Dict[str, Any]:
        """
        Check a student's answer and provide feedback
        
        Args:
            question: The original question
            student_answer: Student's submitted answer
            correct_answer: Optional correct answer for comparison
        """
        
        prompt = f"""Question: {question}

Student's Answer: {student_answer}
{"Correct Answer: " + correct_answer if correct_answer else ""}

Please evaluate the student's answer:
1. Is it correct? (Yes/No/Partially)
2. What did they do well?
3. What mistakes did they make (if any)?
4. How can they improve?
5. Provide the correct solution if their answer is wrong

Be constructive and encouraging in your feedback."""

        messages = [
            {"role": "system", "content": "You are a patient tutor evaluating student work."},
            {"role": "user", "content": prompt}
        ]
        
        response = self._make_request(messages, temperature=0.4, max_tokens=2000)
        
        return {
            "question": question,
            "feedback": response
        }
    
    def simplify_complex_text(self, text: str, target_level: str = "simple") -> str:
        """
        Simplify complex scientific text
        
        Args:
            text: Complex text to simplify
            target_level: Target reading level (simple, moderate, technical)
        """
        
        prompt = f"""Simplify this text to a {target_level} level while preserving accuracy:

{text}

Make it easier to understand without losing important information."""

        messages = [
            {"role": "system", "content": "You are an expert at making complex concepts accessible."},
            {"role": "user", "content": prompt}
        ]
        
        return self._make_request(messages, temperature=0.5, max_tokens=2000)
