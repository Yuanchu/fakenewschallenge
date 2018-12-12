
import warnings
warnings.filterwarnings('ignore')
import dataset
import random
import numpy as np
import mxnet as mx
from mxnet import gluon
import gluonnlp as nlp
from gluonnlp.data.utils import Splitter
from tokenizer import FullTokenizer

np.random.seed(100)
random.seed(100)
mx.random.seed(10000)
ctx = mx.cpu()

from bert import *
import bert

bert_base, vocabulary = nlp.model.get_model('bert_12_768_12',
                                             dataset_name='book_corpus_wiki_en_uncased',
                                             pretrained=True, ctx=ctx, use_pooler=True,
                                             use_decoder=False, use_classifier=False)
# print(bert_base)

model = BERTClassifier(bert_base, num_classes=2, dropout=0.1)
# only need to initialize the classifier layer.
model.classifier.initialize(init=mx.init.Normal(0.02), ctx=ctx)
model.hybridize(static_alloc=True)

# softmax cross entropy loss for classification
loss_function = gluon.loss.SoftmaxCELoss()
loss_function.hybridize(static_alloc=True)

metric = mx.metric.Accuracy()

data_train = dataset.DatasetWrapper('dev', root='.', field_separator = Splitter(','))
# data_train = dataset.TSVDataset('test.tsv', field_separator = Splitter(','))

sample_id = 0
# sentence a
print(data_train[sample_id][0])
# sentence b
print(data_train[sample_id][1])
# 1 means equivalent, 0 means not equivalent
print(data_train[sample_id][2])

import pdb; pdb.set_trace()

# use the vocabulary from pre-trained model for tokenization
tokenizer = FullTokenizer(vocabulary, do_lower_case=True)

# maximum sequence length
max_len = 128
all_labels = ["0", "1"]
transform = dataset.ClassificationTransform(tokenizer, all_labels, max_len)
data_train = data_train.transform(transform)

# print('token ids = \n%s'%data_train[sample_id][0])
# print('valid length = \n%s'%data_train[sample_id][1])
# print('segment ids = \n%s'%data_train[sample_id][2])
# print('label = \n%s'%data_train[sample_id][3])

import pdb; pdb.set_trace()

batch_size = 32
lr = 5e-6
bert_dataloader = mx.gluon.data.DataLoader(data_train, batch_size=batch_size,
        shuffle=True, last_batch='rollover')

trainer = gluon.Trainer(model.collect_params(), 'adam',
        {'learning_rate': lr, 'epsilon': 1e-9})

params = [p for p in model.collect_params().values() if p.grad_req != 'null']
grad_clip = 1

log_interval = 4
num_epochs = 20

import pdb; pdb.set_trace()

for epoch_id in range(num_epochs):
    metric.reset()
    step_loss = 0
    for batch_id, (token_ids, valid_length, segment_ids, label) in enumerate(bert_dataloader):
        with mx.autograd.record():

            # load data to GPU
            token_ids = token_ids.as_in_context(ctx)
            valid_length = valid_length.as_in_context(ctx)
            segment_ids = segment_ids.as_in_context(ctx)
            label = label.as_in_context(ctx)

            # forward computation
            out = model(token_ids, segment_ids, valid_length.astype('float32'))
            ls = loss_function(out, label).mean()

        # backward computation
        ls.backward()

        # gradient clipping
        grads = [p.grad(c) for p in params for c in [ctx]]
        gluon.utils.clip_global_norm(grads, grad_clip)

        # parameter update
        trainer.step(1)
        step_loss += ls.asscalar()
        metric.update([label], [out])
        # if (batch_id + 1) % (log_interval) == 0:
        print('[Epoch {} Batch {}/{}] loss={:.4f}, lr={:.7f}, acc={:.3f}'.format(epoch_id, batch_id + 1, len(bert_dataloader),step_loss / log_interval,trainer.learning_rate, metric.get()[1]))
        step_loss = 0
