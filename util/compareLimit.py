#!/usr/bin/python

import argparse, json, logging
import sys, re
import pprint

import ROOT
from ROOT import TFile, TTree
from ROOT import TCanvas, TH1, TH2, TProfile, TColor
from ROOT import TGraph, TGraphAsymmErrors, TMultiGraph
from ROOT import TF1
from ROOT import gROOT, gDirectory, gStyle, gPad
from ROOT import gStyle, gPad, TLegend, TAxis
from ROOT import SetOwnership

import tdrstyle 

logger = 0

gcSaver = []

def applyFigureStyle(obj,dic):
    '''
    Apply style to drawable object like Histograms or Graphs. ROOT API specific.
    Example dictionary: {"SetMarkerColor":ROOT.kBlue, "SetMarkerSize":2, "SetMarkerStyle":20}
    '''
    logger.debug('Started')
    for element_command, style in dic.iteritems():
        logger.debug('Apply command: %s.%s(%s)' % (obj,element_command, style))
        getattr(obj, element_command)(style)
    logger.debug('Finished')
    
def setBinLabels(axis,dic):
    '''
    dic provides the binID:Label mapping 
    '''
    for iBin, label in dic.iteritems():
        axis.SetBinLabel(iBin,label)
    
class comparisonFac:
    '''
    Class provides human-readable comparison of multiple limit points
    either in graphical or table format.
    
    result_format: supported options ("pdf","png","eps","C","tex")
    currently "tex" is a stub.
    '''
    def __init__(self,result_format):
        logger.debug('Started')
        self.result_format = result_format
        self.points_list = []
        logger.debug('Finished')
        
    def addPoint(self,point):
        logger.debug('Started')
        self.points_list.append(point)
        logger.debug('Finished')
    
    def getResult(self):
        logger.debug('Started')
        logger.debug('Format: %s' % self.result_format)
        
        
        if any(fmt in self.result_format for fmt in ['pdf','png','eps','C']):
            self.getPlot()
        elif 'tex' in self.result_format:
            self.getTable()
        else:
            raise ValueError('Invalid output format: %s' % self.result_format)
        logger.debug('Finished')
        pass
    
    def getObservedGraph(self,style_dic):
        '''
        Retrive graph with observed limit points.
        Assumes "obs" key in input JSON object
        '''
        gr = TGraph()
        for pointID, point in enumerate(self.points_list):
            yObs = point['obs']
            x = float(pointID)
            logger.debug('Point (id, x, yObs): %s' % pprint.pformat([x,yObs]) )
            gr.SetPoint(pointID,x,yObs)
    
        applyFigureStyle(gr, style_dic) 
        return gr;
    
    def getExpectedGraph(self,style_dic):
        '''
        Retrive graph with expected limit points and uncertainties.
        Assumes "exp_(16.0,50.0,84.0)" keys in input JSON object
        '''
        gr = TGraphAsymmErrors()
        for pointID, point in enumerate(self.points_list):
            yObs = point['obs']
            x, yExp = float(pointID),point['exp_50.0']
            exlow, exhigh = 0.,0.
            eylow, eyhigh = yExp-point['exp_16.0'], point['exp_84.0']-yExp
            
            logger.debug('Point (id, x, yObs, yExp, exl, exh, eyl, eyh): %s' %
                            pprint.pformat([x,yObs,yExp,exlow,exhigh,eylow,eyhigh]) )
            gr.SetPoint(pointID,x,yExp)
            gr.SetPointError(pointID,exlow,exhigh,eylow,eyhigh)

        applyFigureStyle(gr, style_dic) 
        return gr
    
    def getGraph(self,type,style_dic):
        if type == 'Exp':
            return self.getExpectedGraph(style_dic)
        elif type == 'Obs':
            return self.getObservedGraph(style_dic)
    
    def getPlot(self):
        '''
        Retrive ROOT canvas with comparison plot
        '''
        logger.debug('Started')
        mg = TMultiGraph()
        
        grExpected_style_dic = {'SetMarkerColor':ROOT.kBlue, 'SetMarkerSize':2, 'SetMarkerStyle':20, 'SetName':"Expected"}
        grExpected = self.getGraph('Exp', grExpected_style_dic)
        mg.Add(grExpected,"p")
        grObserved_style_dic = {'SetMarkerColor':ROOT.kRed, 'SetMarkerSize':2, 'SetMarkerStyle':20, 'SetName':"Observed"}
        grObserved = self.getGraph('Obs', grObserved_style_dic)
        mg.Add(grObserved,"p")
        
        canvas = TCanvas('canvas', 'CMS')
        gcSaver.append(canvas)
        
        mg.Draw('A')
        mg.GetYaxis().SetTitle("Asymptotic CL_{S} upper limit (#sigma/#sigma_{SM})")
        axis = mg.GetXaxis()
        binID_list = [(axis.FindBin(grExpected.GetX()[ipoint]),str('fit%s'%ipoint)) for ipoint in 
                            range(0,grExpected.GetN())]
        axis_labels = dict((binID, label) for (binID, label) in binID_list)
        setBinLabels(mg.GetXaxis(),axis_labels)
        
        canvas.BuildLegend()
        tdrstyle.cmsPrel(-1., 13., False)
        
        canvas.Print('limitComparison.'+self.result_format)
        logger.debug('Finished')
    
    def getTable(self):
        '''
        Retrive LaTeX table with limit comparison
        '''
        logger.debug('Started')
        logger.debug('Finished')
        pass
    
def compare(json_list,format='pdf'):
    '''
    make figure or table with limit comparison
    '''
    logger.debug('Started')
    logger.info(pprint.pformat(json_list))
    logger.info('Output format: ' + format)
    
    comparison = comparisonFac(format)
    for json_name in json_list:
        with open(json_name) as json_file:
            point = json.load(json_file)
            logger.info('Reading JSON: '+json_name)
            logger.debug(pprint.pformat(point))
            comparison.addPoint(point)
    comparison.getResult()
    logger.debug('Finished')

def main(argv):
    global logger
    TH1.AddDirectory(False);
    
    #setup logger
    logformat = '[%(filename)s:%(lineno)s:%(levelname)s - %(funcName)20s() ] %(message)s'
    logging.basicConfig(format=logformat, level=logging.WARNING)
    logger = logging.getLogger()
    
    #setup command-line parser
    parser = argparse.ArgumentParser(description='Compare multiple limits in the same plot.',
                    add_help=False)
    parser.add_argument('-u', '--usage', action='help', help='show this help message and exit')
    parser.add_argument('-l','--loglevel', help='verbosity threshold: DEBUG, INFO, WARNING, ERROR', required=False)
    parser.add_argument('-f','--format', help='comprison output format: pdf,png,eps,C,tex', required=False)
    parser.add_argument('json_files', metavar='JSON', type=str, nargs='+',
                    help='JSON objects with points definitions')
                        
    args = parser.parse_args()
    
    #modify logging message severity
    if args.loglevel is not None:
        numeric_level = getattr(logging, args.loglevel.upper(), None)
        if not isinstance(numeric_level, int):
            raise ValueError('Invalid log level: %s' % args.loglevel)
        logger.setLevel(numeric_level)
    
    #make comparison
    logger.debug('Started')
    compare(args.json_files)
    logger.debug('Finished')
    
if __name__ == "__main__":
   main(sys.argv)