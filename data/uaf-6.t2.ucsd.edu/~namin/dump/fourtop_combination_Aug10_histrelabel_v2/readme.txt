### To quickly reproduce SS TTTT PAS numbers (12.9 fb-1)

1. Using release CMSSW_7_4_7_patch1, run `combine -M Asymptotic v8.04_tttt_July26/card_tttt_12.9ifb-all.txt --noFitAsimov`.

2. Paste the signal strength limits output by combine into the top of `parseLimits.py` and run `python parseLimits.py`. (Note, maybe `curl` won't work on the python script, so just rename `parseLimits_py.txt`.) This should yield

```
Limits for TTTT
  Obs: 56.6 fb
  Exp: 46.2 + 23.0 - 14.7 fb
```


### For 2015 

1. `combine -M Asymptotic v6.02-tttt/card_tttt_2.3ifb-all.txt --noFitAsimov` and then rest follows as above

