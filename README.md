Four top (tttt) 2015 data combination

Extensive combine tool manual is available at:

https://twiki.cern.ch/twiki/bin/view/CMS/SWGuideHiggsAnalysisCombinedLimit
more information can be obtained from the CMSDAS2014 exercise
https://twiki.cern.ch/twiki/bin/viewauth/CMS/SWGuideCMSDataAnalysisSchool2014HiggsCombPropertiesExercise

Combination of multiple datacards
combineCards.py Name1=card1.txt Name2=card2.txt .... > card.txt


Parse combine output and convert it different formats
```
make -B  format FMT=txt INPUT=result/16-08-12-18-25/combine.asymptotic.out
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
