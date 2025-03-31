# chatbot.py
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferWindowMemory
import os

def get_llm():
    """Returns a ChatOpenAI instance using the API key from the environment."""
    api_key = os.getenv("OPENAI_API_KEY")
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.6, openai_api_key=api_key)
    return llm

def create_chat_memory(chat_history):
    """Creates a conversation buffer memory using the provided chat history."""
    return ConversationBufferWindowMemory(
        memory_key="history",
        chat_memory=chat_history,
        k=5,
        input_key="user_input"
    )

def get_llm_chain(llm, memory, transcript):
    """
    Creates an LLMChain with a prompt template for open-ended Q&A about the video transcript.
    """
    template = """
You are a helpful assistant with access to the following YouTube video transcript:

{transcript}

When the user asks a question, refer to the transcript if relevant.
If the user asks something unrelated, respond politely or clarify.

Conversation so far:
{history}

User says: {user_input}
Assistant:
"""
    prompt = PromptTemplate(
        template=template,
        input_variables=["user_input", "history", "transcript"]
    )
    chain = LLMChain(prompt=prompt, llm=llm, memory=memory)
    return chain

class ChatBot:
    """A chatbot that answers questions about a YouTube transcript."""
    def __init__(self, transcript, chat_history):
        self.transcript = transcript
        self.memory = create_chat_memory(chat_history)
        self.llm = get_llm()
        self.chain = get_llm_chain(self.llm, self.memory, self.transcript)
    
    def get_response(self, user_input):
        """Generates a response based on the user's open-ended query."""
        response = self.chain.predict(user_input=user_input, transcript=self.transcript)
        return response
