from django.shortcuts import render
from .tls.DS import train as DS_train
from .hae.hae_dec import HAE_train
from .MeanTeacher.tensorflow.train_compare import MT_train

import logging
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')

def train_tls(request):
    DS_train()
    return render(request, "model_train/train_tls.html")
# Create your views here.

def train_HAE(request):
    HAE_train()
    return render(request, "model_train/train_HAE.html")

def train_MT(request):
    logging.debug("train_MT start")
    MT_train()
    return render(request, "model_train/train_MT.html")