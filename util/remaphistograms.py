#!/usr/bin/python

import sys, getopt, json, re

from ROOT import gROOT
from ROOT import TKey, TClass
from ROOT import TFile, TObject, TList, TIter

def parseArgs(argv):
   """
   Parse commandline arguments
   """     
   scriptName = "remaphistograms.py"
    
   rootfile = ''
   try:
      opts, args = getopt.getopt(argv,"ur:",["usage","rootfile="])
   except getopt.GetoptError:
      print scriptName + ' -r <rootfile>'
      sys.exit(2)
   for opt, arg in opts:
      if opt in ('-u', "--usage"):
         print scriptName + ' -r <rootfile>'
         sys.exit()
      elif opt in ("-r", "--rootfile"):
         rootfile = arg
   print 'ROOT file is "', rootfile, '"'
   
   return rootfile

def remaphistnames(rootFileName,labelMap):
    
    rootKeyList = ''
    rootFile = TFile.Open(rootFileName,"UPDATE")
    if rootFile is None:
        sys.exit("Can't open root file: "+rootFileName+" Terminating...")
    
    rootKeyList = rootFile.GetListOfKeys()
    for key in rootKeyList:
        cl = gROOT.GetClass(key.GetClassName());
        if not cl.InheritsFrom("TH1"):
            continue
        hist = key.ReadObj();
        origHistName = hist.GetName()
#        find any key in the labelMap dic
        matchstring = r'(' + '|'.join(labelMap.keys()) + r')'
        pattern = re.compile(matchstring)
#        replace matching key with its value in the dic
        resultHistName = pattern.sub(lambda x: labelMap[x.group()], origHistName )
        print origHistName + ':' + resultHistName
        hist.Write(resultHistName)
        

def main(argv):
    rootFileName = parseArgs(argv)
    labelMapDic = {
    'tttt_':'NP_overlay_ttttNLO_',
    'pu':'PU',
    'jes':'JES'
    }
    remaphistnames(rootFileName, labelMapDic)

if __name__ == "__main__":
    main(sys.argv[1:])
    