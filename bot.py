import os
import sys
import playsound
from speech_text import transcribe_audio, record_audio
from text_speech import transcribe_text, play_mp3
from pathlib import Path
import openai
from langchain.chains import ConversationalRetrievalChain, RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import DirectoryLoader, TextLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.indexes import VectorstoreIndexCreator
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
from langchain.llms import OpenAI
from langchain.vectorstores import Chroma

os.environ["OPENAI_API_KEY"] = "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"

PERSIST = False

query = None
if len(sys.argv) > 1:
  query = sys.argv[1]

if PERSIST and os.path.exists("persist"):
  print("Reusing index...\n")
  vectorstore = Chroma(persist_directory="persist", embedding_function=OpenAIEmbeddings())
  index = VectorStoreIndexWrapper(vectorstore=vectorstore)
else:
  loader = DirectoryLoader("data/")
  if PERSIST:
    index = VectorstoreIndexCreator(vectorstore_kwargs={"persist_directory":"persist"}).from_loaders([loader])
  else:
    index = VectorstoreIndexCreator().from_loaders([loader])

chain = ConversationalRetrievalChain.from_llm(
  llm=ChatOpenAI(model="gpt-4"),
  retriever=index.vectorstore.as_retriever(search_kwargs={"k": 1}),
)

file_name = "rec.mp3"
mp3_file_path = Path(__file__).parent / "speech.mp3"


chat_history = []
while True:
  record_audio(file_name)
  promt = transcribe_audio(file_name)

  if not query:
    query = promt
    print(promt)
  if promt in ['quit', 'Stop', 'Stop!','stop']:
    sys.exit()

  result = chain({"question": query, "chat_history": chat_history})
  transcribe_text(result['answer'])
  play_mp3(mp3_file_path)
  print(result['answer'])
  chat_history.append((query, result['answer']))
  query = None