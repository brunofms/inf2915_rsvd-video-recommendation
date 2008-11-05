#!/usr/bin/python

# Item based recommendation media system

import similarity

from logParser import mediaUserDict

# TODO: dictionary -> matrix NxM
# TODO: SVD

print similarity.topMatches(mediaUserDict, '904968', 10, similarity.sim_distance)