# Fake News Detection

## Team members

* [Yuanchu Dang](https://www.linkedin.com/in/yuanchu-dang-6364a562/) - Bert model
* Yanmin Ji - LSTM model
* Wei Luo - Twitter API

## Previous work & Acknowledgement
* We forked and built on this [fake news challenge repo](https://github.com/uclmr/fakenewschallenge).

## Problem Formulation
Given a headline and a body concerning a subject, determine if their views agree or disagree with each other, or, are simply unrelated. 

## Reproducibility

## Getting started

To get started, simply download the files in this repository to a local
directory.

### Prerequisites

The system was developed, trained and tested using the
following:

```
Python==3.5.2
NumPy==1.11.3
scikit-learn==0.18.1
TensorFlow==0.12.1
```

Please note that compatibility of the saved model with newer versions
of `TensorFlow` has not been checked. Accordingly, please use the
`TensorFlow` version listed above.

### Installing

Other than ensuring the dependencies are in place, no separate
installation is required.

Simply execute the `pred.py` file once the repository has been
saved locally.

## Reproducing the submission

The `pred.py` script can be run in two different modes: 'load' or
'train'. Upon running the `pred.py` file, the user is requested to input
the desired mode.

Execution of the `pred.py` file in 'load' mode entails the
following:

* The train set will be loaded from `train_stances.csv` and
`train_bodies.csv` using the corresponding `FNCData` class defined in
`util.py`.
* The test set will be loaded from `test_stances_unlabeled.csv` and
`train_bodies.csv` using the same `FNCData` class. Please note that
`test_stances_unlabeled.csv` corresponds to the second, amended release
of the file.
* The train and test sets are then respectively processed by the
`pipeline_train` and `pipeline_test` functions defined in `util.py`.
* The `TensorFlow` model saved in the `model` directory is then loaded
in place of the model definition in `pred.py`. The associated
`load_model` function can be found in `util.py`.
* The model is then used to predict the labels on the processed test
set.
* The predictions are then saved in a `predictions_test.csv` file in the
top level of the local directory. The corresponding `save_predictions`
function is defined in `util.py`. The predictions made are equivalent to
those submitted during the competition.

Execution of the `pred.py` file in 'train' mode encompasses steps
identical to those outlined above with the exception of the model being
trained as opposed to loaded from file. In this case, the predictions
will not be identical to those submitted during the competition.

The file name for the predictions can be changed in section '# Set file
names' at the top of `pred.py`, if required.

Please note that the predictions are saved in chronological order with
respect to the `test_stances_unlabeled.csv` file, however, only the
predictions are saved and not combined with the `Headline` and `Body ID`
fields of the source file.


## Citation

If you use this work in your research, please cite the [short paper](http://arxiv.org/abs/1707.03264)
on arXiv using the following BibTeX entry.

```
@article{riedel2017fnc,
    author = {Benjamin~Riedel and Isabelle~Augenstein and Georgios~P.~Spithourakis and Sebastian~Riedel},
    title = {A simple but tough-to-beat baseline for the {Fake News Challenge} stance detection task},
    journal = {CoRR},
    volume = {abs/1707.03264},
    year = {2017},
    url = {http://arxiv.org/abs/1707.03264}
}
```

## License

This project is licensed under the Apache 2.0 License. Please see the
`LICENSE.txt` file for details.

## Acknowledgements

* Richard Davis and Chris Proctor at the Graduate School of Education
at Stanford University for [the description](https://web.stanford.edu/class/cs224n/reports/2761239.pdf)
of their development efforts for FNC-1. The system presented here is
based on their setup.
* Florian Mai at the Department of Computer Science at
Christian-Albrechts Universität zu Kiel for insightful and constructive
discussions during system development.
* Anna Seg of FNC-1 team 'annaseg' for her suggestions on how to split
the training data for more realistic system evaluation.


