import sys
cp = "lhpohes gvjhe ztytwojmmtel lgsfcgver segpsltjyl vftstelc djfl rml catrroel jscvjqjyfo mjlesl lcjmmfqe egvj gsfyhtyq sjfgver csfaotyq lfxtyq gjywplesl lxljm dxcel mpyctyq ztytwojmmtelel mfcgv spres mjm psgvty bfml ofle mjlc dtc tygfycfctjy dfsyl zpygvel csfao yealqsjpml atyl lgsjql qyfsotelc fseyf ojllel gjzmselltyq wpyhtelc zpltgl weygel afyher rstnesl aefleo rtyhes mvflel yphe rstnes qojder dtwwer lojml mfcgvel reocfl djzder djpygtyq gstmmoeafsel reg cpdel qspyqe mflctel csflvtyq vfcl avfghtyq vftsdfool mzer rsjye wjjol psol mplvtyq catrroe mvfqe lgseey leqzeycer wjseqsjpyrer lmjtoes msjwtoel docl djpyger cjpstlcl goefy gojddesl mjrl qjddoe gjy gpdtyql lyftotyq rjayojfr swgl vjle atrqec gjzmfgces frfl qotcgver gspzd zftodjzdl lyfsh"
pt = "skulker choke minifloppies scratched recursions hairiest boas dps twiddles orthogonal posers stoppage echo cranking roached trawling saying confusers sysop bytes punting minifloppieses patch ruder pop urchin zaps lase post bit incantation barns munches trawl newsgroups wins scrogs gnarliest arena losses compressing funkiest musics fences wanked drivers weasel dinker phases nuke driver globed biffed slops patches deltas bombed bouncing cripplewares dec tubes grunge pasties trashing hats whacking hairballs pmed drone fools urls pushing twiddle phage screen segmented foregrounded spoiler profiles blts bounced tourists clean clobbers pods gobble con cubings snailing download rfcs hose widget compacter adas glitched crumb mailbombs snark"


dic = ["cp_letter", "pt_letter", "diff"]
map__ = []
final_map_dic = [chr(i) for i in range (ord("a"), ord("z")+1)]
final_map = dict(zip(final_map_dic, [i for i in range(len(final_map_dic))]))

cpl = cp.split(" ")
ptl = pt.split(" ")

flg = 0

for i in range (ord("a"), ord("z")+1):
	for cpitms, ptitms in zip(cpl,ptl):
		for j in range(len(cpitms)):
			if ord(cpitms[j]) == i:
				map__.append(dict(zip(dic, [chr(i), ptitms[j], ord(ptitms[j]) - i])))
				flg = 1 
				break;
		if flg:
			flg = 0
			break

print("CP Letter\t\t||PT Letter\t\t||Difference")
print("=========================================")
for itms in map__:
	final_map[itms['cp_letter']] = itms['pt_letter']
'''
	print("{}\t\t\t||{}\t\t\t||\{}".format(itms['cp_letter'],
															  itms['pt_letter'],
															  str(itms['diff'])))
'''

t = input()

d = ""
for i in range(len(t)):
	d += str(final_map[t[i]])

print(d)