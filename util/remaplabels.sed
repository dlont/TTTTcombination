#!/bin/sed -f

# Find lines starting with 'process' and
# replace every occurence of tttt with NP_overlay_ttttNLO  
/^process/ s/ tttt / NP_overlay_ttttNLO /g

# Find lines starting with 'pu' and
# replace every occurence of 'pu' with 'PU'
/^pu/ s|pu|PU|

# Find lines starting with 'jes' and
# replace every occurence of 'jes' with 'JES'
/^pu/ s|jes|JES|

