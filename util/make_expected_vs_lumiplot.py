#!/usr/bin/python
import ROOT as rt
import CMS_lumi, tdrstyle
import argparse
import array
import sys
import numpy as n

def parseArgs():
    parser = argparse.ArgumentParser(description='Make extrapolation plot.')
    parser.add_argument('-i1','--input1', help='input file name',required=True)
    parser.add_argument('-i2','--input2', help='input file name',required=False)

    args = parser.parse_args()
    return args

def main(args):
    #set the tdr style
    tdrstyle.setTDRStyle()

    #change the CMS_lumi variables (see CMS_lumi.py)
    CMS_lumi.lumi_7TeV = "2.6-2600 fb^{-1}"
    CMS_lumi.lumi_8TeV = "2.6-2600 fb^{-1}"
    #CMS_lumi.lumi_13TeV = "1-1000 fb^{-1}"
    CMS_lumi.lumi_13TeV = "1-260 fb^{-1}"
    CMS_lumi.writeExtraText = 1
    #CMS_lumi.extraText = "Simulation Preliminary"
    CMS_lumi.extraText = "Simulation"
    CMS_lumi.lumi_sqrtS = "13 TeV" # used with iPeriod = 0, e.g. for simulation-only plots (default is an empty string)


    iPeriod = 4

    iPos = 11
    if( iPos==0 ): CMS_lumi.relPosX = 0.25
    CMS_lumi.relPosX = 0.15

    H_ref = 600;
    W_ref = 800;
    W = W_ref
    H  = H_ref

    # references for T, B, L, R
    T = 0.08*H_ref
    B = 0.12*H_ref
    L = 0.12*W_ref
    R = 0.04*W_ref

    canvas = rt.TCanvas("c2","c2",50,50,W,H)
    rt.SetOwnership(canvas, False)
    canvas.SetFillColor(0)
    canvas.SetBorderMode(0)
    canvas.SetFrameFillStyle(0)
    canvas.SetFrameBorderMode(0)
    canvas.SetLeftMargin( L/W )
    canvas.SetRightMargin( R/W )
    canvas.SetTopMargin( T/H )
    canvas.SetBottomMargin( B/H )
    canvas.SetTickx(0)
    canvas.SetTicky(0)
    canvas.SetLogx(1)
    canvas.SetGridy()

    graph_a = rt.TGraphErrors(args.input1)
    rt.SetOwnership(graph_a, False)
    graph_a.SetFillColor(rt.kBlue+2)
    graph_a.SetFillStyle(3005)
    graph_a.SetLineColor(rt.kBlue+2)
    graph_b=graph_a.Clone()
    rt.SetOwnership(graph_b, False)
    graph_b.SetLineColor(rt.kBlue+2)
    graph_b.SetLineWidth(2)

    if args.input2 != None:
	graph_a1 = rt.TGraphErrors(args.input2)
	rt.SetOwnership(graph_a1, False)
	graph_a1.SetFillColor(rt.kGreen+1)
	graph_a1.SetFillStyle(3004)
	graph_a1.SetLineColor(rt.kGreen+2)
	graph_b1=graph_a1.Clone()
	rt.SetOwnership(graph_b1, False)
	graph_b1.SetLineColor(rt.kGreen+2)
	graph_b1.SetLineWidth(2)

    mg = rt.TMultiGraph()
    mg.Add(graph_a,'E3')
    mg.Add(graph_b,'CX')
    mg.Add(graph_a1,'E3')
    mg.Add(graph_b1,'CX')
    mg.Draw("A")

    theline2 = rt.TLine(2.6,0,2.6,0.8*graph_a.GetHistogram().GetMaximum())
    rt.SetOwnership(theline2, False)
    theline2.SetLineStyle(2)
    theline2.Draw("same")
    theline3 = rt.TLine(30,0,30,0.8*graph_a.GetHistogram().GetMaximum())
    rt.SetOwnership(theline3, False)
    theline3.SetLineStyle(3)

    theline = rt.TF1("theline","1",0,1000)
    rt.SetOwnership(theline, False)
    theline.Draw("same")
    theline2.Draw("same")
    mg.GetXaxis().SetTitle("(expected) integrated luminosity (fb^{-1})")
    mg.GetXaxis().SetTitleSize(graph_a.GetXaxis().GetTitleSize()*0.85)
    mg.GetYaxis().SetTitle("95 % CL limit on #sigma_{t#bar{t}t#bar{t}} (#sigma_{obs} / #sigma_{SM})")
    mg.GetYaxis().SetTitleSize(graph_a.GetYaxis().GetTitleSize()*0.95)
    mg.GetYaxis().SetTitleOffset(0.9)
    mg.GetXaxis().SetTitleOffset(1.1)



    x1_l = 0.92
    y1_l = 0.90

    dx_l = 0.40
    dy_l = 0.25
    x0_l = x1_l-dx_l
    y0_l = y1_l-dy_l


    legend =  rt.TLegend(x0_l,y0_l,x1_l, y1_l )
    rt.SetOwnership(legend, False)
    legend.SetFillColor(rt.kWhite)
    legend.SetBorderSize(0)
    #legend.AddEntry(graph_b,"2015 data","p")
    #legend.AddEntry(graph_a,"lepton+jets","lf")
    #legend.AddEntry(graph_a,"dilepton","lf")
    legend.AddEntry(graph_a,"combined limit (expected) TOP-SUS","lf")
    legend.AddEntry(graph_a1,"combined limit (expected) TOP","lf")
    legend.AddEntry(theline,"SM t#bar{t}t#bar{t}","l")
    legend.AddEntry(theline2,"2015 integrated lumi","l")
    #legend.AddEntry(theline3,"2016 integrated lumi (expected)","l")

    legend.Draw()


    canvas.Update()

    CMS_lumi.CMS_lumi(canvas, iPeriod, iPos)

    canvas.cd()
    frame = canvas.GetFrame()

    frame.Draw()
    canvas.Modified()
    canvas.Update()
    canvas.RedrawAxis()

    canvas.SaveAs("combined_limitvslumi.pdf")

    canvas.Modified()
    canvas.Update()
    canvas.RedrawAxis()


if __name__ == "__main__":
    args = parseArgs()
    main(args)
    raw_input("Press Enter to Continue: ")
