#Libraries
from rs_bpe.bpe import openai
import nltk
import torch
from torchtext.vocab import GloVe 

#Tokenization and Embedding
sample_input = "The dark brown fox jumped over the small road."

cl100k_tokenizer = openai.cl100k_base()
tokens = cl100k_tokenizer.encode(sample_input)

#maybe implent byte tokenization myself

model = Word2Vec(sentences=common_texts, vector_size=100, window=5, min_count=1, workers=4)
model.save("word2vec.model")
