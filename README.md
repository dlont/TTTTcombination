Four top (tttt) 2015 data combination

Extensive combine tool manual is available at:

https://twiki.cern.ch/twiki/bin/view/CMS/SWGuideHiggsAnalysisCombinedLimit
more information can be obtained from the CMSDAS2014 exercise
https://twiki.cern.ch/twiki/bin/viewauth/CMS/SWGuideCMSDataAnalysisSchool2014HiggsCombPropertiesExercise

Combination of multiple datacards
combineCards.py Name1=card1.txt Name2=card2.txt .... > card.txt


Parse combine output and convert it different formats
```
make -B -f make/Makefile.fmtcmbout format FMT=txt INPUT=result/16-08-12-18-25/combine.asymptotic.out
```
where 
FMT=[txt|tex] possible output format
INPUT=[path to file] output of combine job


good SED manual
http://www.grymoire.com/Unix/Sed.html



Rename histograms in ROOT file.
WARNING: this command modifies original file
```
./util/remaphistograms.py -r tttt_histos_hihi_2.3ifb.root
```

Remap labels in datacards
```
make -B remaplabels INPUT=../uaf-6.t2.ucsd.edu/~namin/dump/fourtop_combination_Aug10/v6.02-tttt/card_tttt_2.3ifb-all.txt OUTPUT=data/v0.1.1/16-08-24-02-01/card_tttt_2.3ifb-all.txt
```


Comparison of multiple limits
./util/compareLimit.py fit1.json fit2.json

Replacement of single systematic label by multiple options. Save alternatives in different files.
```
for VAR in {btagWeightCSVCFErr1,btagWeightCSVCFErr2,btagWeightCSVHF,btagWeightCSVHFStats1,btagWeightCSVHFStats2,btagWeightCSVLF,btagWeightCSVLFStats1,btagWeightCSVLFStats2}; do for i in card_tttt_2.3ifb-all.txt;do sed "/^btag/ s/btag/$VAR/" $i> $i.$VAR; echo $i.$VAR;done; done
```

```
for file in ../uaf-6.t2.ucsd.edu/~namin/dump/fourtop_combination_Aug10_histrelabel_v3/v6.02-tttt/*.root; do for VAR in btagWeightCSVCFErr1 btagWeightCSVCFErr2 btagWeightCSVHF btagWeightCSVHFStats1 btagWeightCSVHFStats2 btagWeightCSVLF btagWeightCSVLFStats1 btagWeightCSVLFStats2; do ./util/remaphistograms_sig_only.py -r $file -d {\"btagDown\":\"$VAR'Down'\"};done;done
```
