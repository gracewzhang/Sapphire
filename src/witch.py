from cauldron import Cauldron
from langchain.llms import OpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from cli import console


class Witch():
    def __init__(self, client, directory: str, history: list, agent, model_name="gpt-3.5-turbo") -> None:
        self.client = client
        self.cauldron = Cauldron(directory)
        self.history = history
        self.agent = agent
        self.__build_qa()

    def __build_qa(self) -> None:
        llm = OpenAI(temperature=0)
        memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        cauldron = self.cauldron.get_db()
        retriever = cauldron.as_retriever(lambda_val=0.025, k=5, filter=None)
        self.qa = ConversationalRetrievalChain.from_llm(llm, retriever, memory=memory)

    def answer_question(self, question: str) -> None:
        res = self.qa({'question': question})
        answer = res['answer']
        console.print(answer)
        self.history.append((self.agent, question, answer))

    def reingest(self) -> None:
        self.cauldron.reingest()
