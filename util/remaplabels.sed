#!/bin/sed -f

# Find lines starting with 'process' and
# replace every occurence of tttt with TTTT
/^process/ s/ tttt / TTTT /g

# Find lines starting with 'pu' and
# replace every occurence of 'pu' with 'PU'
/^pu/ s|pu|PU|

