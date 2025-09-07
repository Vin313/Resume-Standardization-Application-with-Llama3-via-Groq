import json
import groq
from tenacity import retry, stop_after_attempt, wait_exponential
from typing import Dict, Any
import config
import re

class LLMIntegration:
    def __init__(self):
        self.config = config.Config()
        
        if self.config.LLM_PROVIDER == "groq" and self.config.GROQ_API_KEY:
            self.client = groq.Groq(api_key=self.config.GROQ_API_KEY)
        else:
            raise ValueError("LLM provider not properly configured. Please set GROQ_API_KEY.")

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def extract_resume_info(self, text: str, tone_guidelines: str = None) -> Dict[str, Any]:
        """Extract structured resume information using Llama3 via Groq API"""
        
        prompt = self._build_extraction_prompt(text, tone_guidelines)
        return self._extract_with_groq(prompt)

    def _build_extraction_prompt(self, text: str, tone_guidelines: str = None) -> str:
        """Build the prompt for resume extraction"""
        
        tone_instruction = f"""
        Additionally, please follow these tone guidelines:
        {tone_guidelines}
        """ if tone_guidelines else ""
        
        prompt = f"""
        You are an expert resume parser. Extract the following information from the resume text below and return it as a JSON object with the exact structure specified.

        Required JSON structure:
        {{
            "name": "Full Name",
            "email": "email@example.com",
            "education": [
                {{
                    "degree": "Degree Name",
                    "institution": "Institution Name",
                    "duration": "Start Date - End Date",
                    "details": "Additional details"
                }}
            ],
            "skills": ["Skill 1", "Skill 2", "Skill 3"],
            "certifications": [
                {{
                    "name": "Certification Name",
                    "issuer": "Issuing Organization",
                    "date": "Date earned (if available)",
                    "link": "URL (if available)"
                }}
            ],
            "experience": [
                {{
                    "role": "Job Title",
                    "company": "Company Name",
                    "duration": "Start Date - End Date",
                    "responsibilities": [
                        "Responsibility 1",
                        "Responsibility 2"
                    ]
                }}
            ],
            "achievements": [
                "Achievement 1",
                "Achievement 2"
            ]
        }}

        {tone_instruction}

        Resume text to parse:
        {text}

        Return ONLY the JSON object, without any additional text or explanation.
        """
        
        return prompt

    def _extract_with_groq(self, prompt: str) -> Dict[str, Any]:
        """Extract information using Groq API with Llama3"""
        try:
            response = self.client.chat.completions.create(
                model=self.config.MODEL_NAME,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that extracts resume information and returns only valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=self.config.MAX_TOKENS,
                temperature=self.config.TEMPERATURE,
                response_format={"type": "json_object"}
            )
            
            result = response.choices[0].message.content
            return json.loads(result)
            
        except Exception as e:
            raise Exception(f"Groq API error: {str(e)}")

    @retry(stop=stop_after_attempt(2), wait=wait_exponential(multiplier=1, min=2, max=5))
    def refine_content(self, content: Dict[str, Any], tone_guidelines: str = None) -> Dict[str, Any]:
        """Refine the extracted content based on tone guidelines"""
        if not tone_guidelines:
            return content
            
        prompt = f"""
        Refine the following resume content according to these tone guidelines:
        {tone_guidelines}
        
        Current content:
        {json.dumps(content, indent=2)}
        
        Return the refined content in the exact same JSON structure, without any additional text.
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.config.MODEL_NAME,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that refines resume content and returns only valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=self.config.MAX_TOKENS,
                temperature=self.config.TEMPERATURE,
                response_format={"type": "json_object"}
            )
            
            result = response.choices[0].message.content
            return json.loads(result)
        except Exception as e:
            print(f"Error refining content: {e}")
            return content  # Fallback to original content