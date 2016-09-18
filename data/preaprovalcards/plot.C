{
	const int nPoints = 21;
	const double x[] = {0.0,1.0,2.0,3.0,4.0,5.0,6.0,7.0,8.0,9.0,10.0,11.0,12.0,13.0,14.0,15.0,16.0,17.0,18.0,19.0,20.0};
	const double y[] = {0.00426,1.00000,2.01511,2.9786,4.00487,5.01044,6.00652,7.01073,8.00521,8.99265,10.0013,10.988,11.9992,12.9995,13.9999,14.9992,15.9956,17.0001,17.9963,18.9981,19.9665};
	const double eyl[] = {0.00426,1.0000,2.01511,2.9786,3.82273,5.01044,4.22909,4.37166,4.49199,4.59712,4.71938,4.81561,4.93342,5.03839,5.14178,5.24294,5.34028,5.44473,5.54089,5.64261,5.71046};
	const double eyh[] = {+4.10365,+4.3161,+4.46881,+4.65776,+4.77473,+4.31697,+5.0426,+5.16786,+5.30048,+5.43816,+5.55365,+5.6901,+5.80108,+5.92242,+6.00014,+5.00079,+4.00445,+2.99989,+2.00371,+1.0019,+0.0335167};

	TCanvas *c = new TCanvas("c","CMS",5,45,500,500);
	TGraphAsymmErrors *gr = new TGraphAsymmErrors(nPoints,x,y,0,0,eyl,eyh);
	gr->Draw("APE");
	gr->SetMarkerStyle(20);
	gr->SetTitle("Signal injection test");
	gr->GetXaxis()->SetLimits(-2.,22.);
	gr->GetXaxis()->SetRangeUser(-2.,22.);
	gr->GetYaxis()->SetLimits(-2.,22.);
	gr->GetYaxis()->SetRangeUser(-2.,22.);
	gr->GetXaxis()->SetTitle("Injected signal strength");
	gr->GetYaxis()->SetTitle("Signal strength best fit value");
	c->Update();

	c->Print("SignalInjectionTest.png");
	c->Print("SignalInjectionTest.pdf");
}
