# Cross lingual question answering
This repository contains the implementation of related [article](/article/report.pdf) that was written as a part
of *Natural Language Processing* course at the *Faculty of Computer and Information Science at the 
University of Ljubljana*.

## Description
The goal of the project is to prepare an english, slovene and multilingual english and slovene model for question 
answering system. Stanford Question Answering Dataset ([SQuAD 2.0](https://rajpurkar.github.io/SQuAD-explorer/))
is used as the main corpora. For training a slovene model, SQuAD corpora is automatically translated to Slovene, using the 
[EK translator](https://ec.europa.eu/info/resources-partners/machine-translation-public-administrations-etranslation_en).


## Repository structure
The repository contains the following folders:
- `article` contains the latex files and the article in pdf
- `data` contains the data used for teaching the models
- `docs` contains the files for generating documentation in [Sphinx](https://www.sphinx-doc.org/en/master/index.html)
- `src` contains the code

## Documentation
Documentation is generated using [Sphinx](https://www.sphinx-doc.org/en/master/index.html) and is deployed on 
[GitHub pages](https://blarc.github.io/cross-lingual-question-answering/index.html).