# dedupe-vowpal
Vowpal Wabbit Active Labeler for Dedupe

This module provides an class for active learning using Vowpal Wabbit. 

Part of the [Dedupe.io](https://dedupe.io/) cloud service and open source toolset for de-duplicating and finding fuzzy matches in your data.

# Prerequsites
* [Vowpal Wabbit](https://github.com/JohnLangford/vowpal_wabbit#getting-the-code)

# Install
```bash
pip install https://github.com/datamade/dedupe-vowpal/zipball/master
```

# To use

Instead of using the normal Dedupe classes, you will create a subclass with the ActiveLearner from this module

```python
import dedupe
from vowpal_labeler import VowpalLearner

class Dedupe(dedupe.Dedupe):
    ActiveLearner = VowpalLearner
    
....
```
