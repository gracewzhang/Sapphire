from openai import OpenAI
from cauldron import Cauldron
from langchain.chat_models import ChatOpenAI
from langchain.chains.question_answering import load_qa_chain


class Witch():
    def __init__(self, client: OpenAI, model_name="gpt-3.5-turbo") -> None:
        self.client = client
        self.cauldron = Cauldron()
        self.llm = ChatOpenAI(model_name=model_name)

    def answer_question(self, question: str) -> None:
        pass

    def reingest(self) -> None:
        self.cauldron.reingest()
