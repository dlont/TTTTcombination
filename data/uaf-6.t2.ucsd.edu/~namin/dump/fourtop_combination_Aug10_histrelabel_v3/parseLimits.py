# v8.04_tttt_July26/card_tttt_12.9ifb-all.txt
#lim_tttt = """
# -- Asymptotic --
# Observed Limit: r < 6.2128
# Expected  2.5%: r < 2.5093
# Expected 16.0%: r < 3.4626
# Expected 50.0%: r < 5.0781
# Expected 84.0%: r < 7.6083
# Expected 97.5%: r < 10.9437
#"""
# v6.02-tttt/card_tttt_2.3ifb-all.txt
lim_tttt = """
 -- Asymptotic -- 
 Observed Limit: r < 13.0276
 Expected  2.5%: r < 5.0485
 Expected 16.0%: r < 7.2446
 Expected 50.0%: r < 11.0938
 Expected 84.0%: r < 17.3288
 Expected 97.5%: r < 25.9161
"""

xsec_tttt = 0.009103 # pb

def get_lim(lim_str, xsec, name):
    d = {}
    for line in lim_str.splitlines():
        if "Observed" in line: d["obs"] = float(line.split("<")[-1])
        elif "Expected" in line: d["exp_"+line.split("%")[0].replace("Expected","").strip()] = float(line.split("<")[-1])

    unit = "pb"
    if d["obs"]*xsec < 0.1:
        xsec *= 1000.0
        unit = "fb"
    obs = d["obs"]*xsec
    exp = d["exp_50.0"]*xsec
    exp_sm1 = d["exp_16.0"]*xsec
    exp_sp1 = d["exp_84.0"]*xsec

    print "Limits for %s" % name
    print "  Obs: %.3f %s" % (obs, unit)
    print "  Exp: %.3f + %.4f - %.4f %s" % (exp, exp_sp1-exp, exp-exp_sm1, unit)

get_lim(lim_tttt, xsec_tttt, "TTTT")

