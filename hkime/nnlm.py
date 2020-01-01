import torch
import torch.nn as nn
import torch.nn.functional as F

class FeedForward(nn.Module):

    def __init__(self, n, vocab_size, dim, h):
        super(Net, self).__init__()
        self.embedding = nn.Embedding(vocab_size, dim)
        self.linear =  nn.linear(dim, vocab_size)
        self.tanh = nn.tanh()
        self.softmax = nn.softmax()

    def forward(self, x):
        output = self.embedding(x)
        output = self.linear(output)
        output = self.tanh(output)
        output = self.softmax(output)
        return output
