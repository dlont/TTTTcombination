#!/usr/bin/python

import sys, getopt, json, re

from ROOT import gROOT
from ROOT import TKey, TClass
from ROOT import TFile, TObject, TList, TIter
from ROOT import TH1

def parseArgs(argv):
   """
   Parse commandline arguments
   """     
   scriptName = "remaphistograms.py"
    
   rootfile = ''
   dic = {}
   try:
      opts, args = getopt.getopt(argv,"ur:d:",["usage","rootfile=","dictionary="])
   except getopt.GetoptError:
      print scriptName + ' -r <rootfile>'
      sys.exit(2)
   for opt, arg in opts:
      if opt in ('-u', "--usage"):
         print scriptName + ' -r <rootfile>'
         sys.exit()
      elif opt in ("-r", "--rootfile"):
         rootfile = arg
      elif opt in ("-d", "--dictionary"):
         print arg
         dic = json.loads(arg)
   print 'ROOT file is "', rootfile, '"'
   
   return rootfile, dic

def remaphistnames(rootFileName,labelMap):
    
    rootKeyList = ''
    rootFile = TFile.Open(rootFileName,"UPDATE")
    if rootFile is None:
        sys.exit("Can't open root file: "+rootFileName+" Terminating...")
    
    matchstring = r'(^' + '$|^'.join(labelMap.keys()) + r'$)'
    print 'search pattern: ' + matchstring
    pattern = re.compile(matchstring)
    
    rootKeyList = rootFile.GetListOfKeys()
    for key in rootKeyList:
        cl = gROOT.GetClass(key.GetClassName());
        if not cl.InheritsFrom("TH1"):
            continue
        hist = key.ReadObj();
        origHistName = hist.GetName()
#        find any key in the labelMap dic
#        replace matching key with its value in the dic
        resultHistName = pattern.sub(lambda x: labelMap[x.group()], origHistName )
        print origHistName + ':' + resultHistName
        if origHistName != resultHistName:
            hist.Write("",TObject.kOverwrite)
            hist.Write(resultHistName,TObject.kOverwrite)
            break
    rootFile.Close()    

def main(argv):
    rootFileName, labelMapDic = parseArgs(argv)
    print labelMapDic
    remaphistnames(rootFileName, labelMapDic)

if __name__ == "__main__":
    main(sys.argv[1:])
    
