"""
AI Service Module - Handles all AI/LLM interactions
Uses Groq API for fast, affordable AI generation
"""

import os
import requests
import json
from typing import List, Dict, Any

class AIService:
    def __init__(self):
        self.api_key = os.environ.get('GROQ_API_KEY', '')
        self.base_url = "https://api.groq.com/openai/v1/chat/completions"
        
        # Model selection (Groq offers multiple models)
        self.model = "llama-3.3-70b-versatile"  # Fast and smart
        # Alternative: "mixtral-8x7b-32768" for longer context
        
    def _make_request(self, messages: List[Dict], temperature: float = 0.7, max_tokens: int = 2000) -> str:
        """Make request to Groq API"""
        
        if not self.api_key:
            # Fallback for testing without API key
            return self._generate_mock_response(messages)
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        
        try:
            response = requests.post(self.base_url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            return data['choices'][0]['message']['content']
            
        except requests.exceptions.RequestException as e:
            print(f"API Error: {e}")
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
