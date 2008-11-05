#!/usr/bin/python

# Item based recommendation media system

import similarity

from logParser import mediaUserDict

# TODO: dictionary -> matrix NxM
# TODO: SVD

# TEST: Item similarity dataset
print similarity.calculateSimilarItems(mediaUserDict)
