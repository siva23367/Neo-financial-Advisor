'''
from groq import Groq
from config.config import load_config
import requests
import json

class ChatModel:
    def __init__(self, provider=None, model_name=None):
        config = load_config()
        self.provider = provider or config.get("llm_provider", "groq")
        self.model_name = model_name or config.get("model_name", "gemma2-9b-it")
        
        if self.provider == "groq":
            try:
                self.client = Groq(api_key=config.get("groq_api_key"))
                # Test connection
                self.client.models.list()
            except Exception as e:
                print(f"Groq initialization failed: {e}. Falling back to Hugging Face.")
                self.provider = "huggingface"
                self.hf_model = "microsoft/DialoGPT-large"
        else:
            self.provider = "huggingface"
            self.hf_model = "microsoft/DialoGPT-large"
    
    def generate_response(self, prompt, context=None, response_mode="concise"):
        try:
            if self.provider == "groq":
                return self._generate_groq_response(prompt, context, response_mode)
            else:
                return self._generate_huggingface_response(prompt, context, response_mode)
        except Exception as e:
            return f"I'm currently experiencing technical difficulties. Please try again later. Error: {str(e)}"
    
    def _generate_groq_response(self, prompt, context, response_mode):
        system_message = self._build_system_message(context, response_mode)
        
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt}
        ]
        
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            temperature=2.0 if response_mode == "detailed" else 0.3,
            max_tokens=700 if response_mode == "detailed" else 150,  # expanded for long answers
            top_p=0.9
        )
        
        return response.choices[0].message.content
    
    def _generate_huggingface_response(self, prompt, context, response_mode):
        """Fallback to Hugging Face free API"""
        API_URL = f"https://api-inference.huggingface.co/models/{self.hf_model}"
        
        instruction = (
            "Provide a concise answer (1-2 short paragraphs): "
            if response_mode == "concise"
            else "Provide a long, deeply detailed answer with structured sections, explanations, pros and cons, and examples: "
        )
        
        if context:
            full_prompt = f"Context: {context}\n\nQuestion: {prompt}\n{instruction}"
        else:
            full_prompt = f"Question: {prompt}\n{instruction}"
        
        try:
            response = requests.post(API_URL, json={"inputs": full_prompt}, timeout=15)
            response.raise_for_status()
            
            result = response.json()
            
            if isinstance(result, list) and len(result) > 0:
                if 'generated_text' in result[0]:
                    return result[0]['generated_text']
                elif 'summary_text' in result[0]:
                    return result[0]['summary_text']
                else:
                    return str(result[0])
            elif isinstance(result, dict):
                if 'generated_text' in result:
                    return result['generated_text']
                else:
                    return str(result)
            else:
                return "I couldn't generate a response at the moment. Please try again."
                
        except requests.exceptions.Timeout:
            return "The request timed out. Please try again in a moment."
        except requests.exceptions.RequestException:
            return "Network error: Please check your connection and try again."
        except json.JSONDecodeError:
            return "Invalid response format. Please try again."
        except Exception as e:
            return f"Error: {str(e)}. Please try a different question."
    
    def _build_system_message(self, context, response_mode):
        base_message = "You are a helpful financial advisor chatbot. Provide clear, accurate advice."
        
        if context:
            base_message += f"\n\nRelevant context: {context}"
        
        if response_mode == "concise":
            base_message += "\n\nProvide a concise answer (1-2 short paragraphs maximum). Be direct and to the point."
        else:
            base_message += """
            
            Provide a comprehensive, well-structured answer:
            - Start with a clear summary.
            - Explain the reasoning in detail with supporting facts or examples.
            - Add step-by-step breakdowns where helpful.
            - Include practical advice, pros and cons, and potential risks.
            - End with a short actionable conclusion.
            """
        
        return base_message
'''

# models/llm.py
from groq import Groq
from config.config import load_config
import requests
import json

class ChatModel:
    def __init__(self, provider=None, model_name=None):
        config = load_config()
        self.provider = provider or config.get("llm_provider", "groq")
        self.model_name = model_name or config.get("model_name", "gemma2-9b-it")
        
        if self.provider == "groq":
            try:
                self.client = Groq(api_key=config.get("groq_api_key"))
                self.client.models.list()
            except Exception as e:
                print(f"Groq init failed: {e}. Falling back to Hugging Face.")
                self.provider = "huggingface"
                self.hf_model = "HuggingFaceH4/zephyr-7b-beta"
        elif self.provider == "openai":
            print("⚠️ OpenAI requires billing. Falling back to Hugging Face.")
            self.provider = "huggingface"
            self.hf_model = "HuggingFaceH4/zephyr-7b-beta"
        elif self.provider == "gemini":
            print("⚠️ Gemini requires billing. Falling back to Hugging Face.")
            self.provider = "huggingface"
            self.hf_model = "HuggingFaceH4/zephyr-7b-beta"
        else:
            self.provider = "huggingface"
            self.hf_model = "HuggingFaceH4/zephyr-7b-beta"
    
    def generate_response(self, prompt, context=None, response_mode="concise"):
        try:
            if self.provider == "groq":
                return self._generate_groq_response(prompt, context, response_mode)
            else:
                return self._generate_huggingface_response(prompt, context, response_mode)
        except Exception as e:
            return f"❌ Error generating response: {str(e)}"
    
    def _generate_groq_response(self, prompt, context, response_mode):
        system_message = self._build_system_message(context, response_mode)
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt}
        ]
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            temperature=0.7 if response_mode == "detailed" else 0.3,
            max_tokens=700 if response_mode == "detailed" else 150,
            top_p=0.9
        )
        return response.choices[0].message.content
    
    def _generate_huggingface_response(self, prompt, context, response_mode):
        API_URL = f"https://api-inference.huggingface.co/models/{self.hf_model}"
        instruction = (
            "Provide a concise answer (1-2 short paragraphs): "
            if response_mode == "concise"
            else "Provide a long, deeply detailed answer with structured sections, explanations, pros and cons, and examples: "
        )
        if context:
            full_prompt = f"Context: {context}\n\nQuestion: {prompt}\n{instruction}"
        else:
            full_prompt = f"Question: {prompt}\n{instruction}"
        try:
            response = requests.post(API_URL, json={"inputs": full_prompt}, timeout=15)
            response.raise_for_status()
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                return result[0].get("generated_text", str(result[0]))
            elif isinstance(result, dict):
                return result.get("generated_text", str(result))
            else:
                return "⚠️ No response generated."
        except Exception as e:
            return f"⚠️ Hugging Face error: {str(e)}"
    
    def _build_system_message(self, context, response_mode):
        base_message = "You are a helpful financial advisor chatbot. Provide clear, accurate advice."
        if context:
            base_message += f"\n\nRelevant context: {context}"
        if response_mode == "concise":
            base_message += "\n\nProvide a concise answer (1-2 short paragraphs maximum). Be direct and to the point."
        else:
            base_message += """
            
            Provide a comprehensive, well-structured answer:
            - Start with a clear summary.
            - Explain the reasoning in detail with supporting facts or examples.
            - Add step-by-step breakdowns where helpful.
            - Include practical advice, pros and cons, and potential risks.
            - End with a short actionable conclusion.
            """
        return base_message
