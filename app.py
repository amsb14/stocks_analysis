# streamlit_app.py
import streamlit as st
from fetch_prices import fetch_prices  # Assuming 'test.py' is your data fetching script
from industry_stocks import fetch_data_by_segment
from fetch_cash_flow import fetch_cash_flow
from fetch_balance_sheet import fetch_data_balance_sheet 
from fetch_income_stmt import fetch_data_income_stmt
from fetch_divs import fetch_dividends_and_info
from fetch_stocks_summary import fetch_summary
from fetch_finanical_metrics_all import aggregate_financials
import pandas as pd
from io import BytesIO
import base64


companies = ['2030.SR', '2222.SR', '2380.SR', '2381.SR', '2382.SR', '4030.SR', '4200.SR', '1201.SR', '1202.SR', '1210.SR', '1211.SR', '1301.SR', '1304.SR', '1320.SR', '1321.SR', '1322.SR', '2001.SR', '2010.SR', '2020.SR', '2060.SR', '2090.SR', '2150.SR', '2170.SR', '2180.SR', '2200.SR', '2210.SR', '2220.SR', '2223.SR', '2240.SR', '2250.SR', '2290.SR', '2300.SR', '2310.SR', '2330.SR', '2350.SR', '2360.SR', '3001.SR', '3002.SR', '3003.SR', '3004.SR', '3005.SR', '3007.SR', '3008.SR', '3010.SR', '3020.SR', '3030.SR', '3040.SR', '3050.SR', '3060.SR', '3080.SR', '3090.SR', '3091.SR', '3092.SR', '1212.SR', '1214.SR', '1302.SR', '1303.SR', '2040.SR', '2110.SR', '2160.SR', '2320.SR', '2370.SR', '4110.SR', '4140.SR', '4141.SR', '4142.SR', '1831.SR', '1832.SR', '1833.SR', '4270.SR', '6004.SR', '2190.SR', '4031.SR', '4040.SR', '4260.SR', '4261.SR', '4262.SR', '4263.SR', '1213.SR', '2130.SR', '2340.SR', '4011.SR', '4012.SR', '4180.SR', '1810.SR', '1820.SR', '1830.SR', '4170.SR', '4290.SR', '4291.SR', '4292.SR', '6002.SR', '6012.SR', '6013.SR', '6014.SR', '6015.SR', '4070.SR', '4071.SR', '4072.SR', '4210.SR', '4003.SR', '4008.SR', '4050.SR', '4051.SR', '4190.SR', '4191.SR', '4192.SR', '4240.SR', '4001.SR', '4006.SR', '4061.SR', '4160.SR', '4161.SR', '4162.SR', '4163.SR', '4164.SR', '2050.SR', '2100.SR', '2270.SR', '2280.SR', '2281.SR', '2282.SR', '2283.SR', '4080.SR', '6001.SR', '6010.SR', '6020.SR', '6040.SR', '6050.SR', '6060.SR', '6070.SR', '6090.SR', '2140.SR', '2230.SR', '4002.SR', '4004.SR', '4005.SR', '4007.SR', '4009.SR', '4013.SR', '4014.SR', '2070.SR', '4015.SR', '1010.SR', '1020.SR', '1030.SR', '1050.SR', '1060.SR', '1080.SR', '1120.SR', '1140.SR', '1150.SR', '1180.SR', '1111.SR', '1182.SR', '1183.SR', '2120.SR', '4081.SR', '4082.SR', '4130.SR', '4280.SR', '8010.SR', '8012.SR', '8020.SR', '8030.SR', '8040.SR', '8050.SR', '8060.SR', '8070.SR', '8100.SR', '8120.SR', '8150.SR', '8160.SR', '8170.SR', '8180.SR', '8190.SR', '8200.SR', '8210.SR', '8230.SR', '8240.SR', '8250.SR', '8260.SR', '8270.SR', '8280.SR', '8300.SR', '8310.SR', '8311.SR', '7200.SR', '7201.SR', '7202.SR', '7203.SR', '7204.SR', '7010.SR', '7020.SR', '7030.SR', '7040.SR', '2080.SR', '2081.SR', '2082.SR', '2083.SR', '5110.SR', '4330.SR', '4331.SR', '4332.SR', '4333.SR', '4334.SR', '4335.SR', '4336.SR', '4337.SR', '4338.SR', '4339.SR', '4340.SR', '4342.SR', '4344.SR', '4345.SR', '4346.SR', '4347.SR', '4348.SR', '4349.SR', '4020.SR', '4090.SR', '4100.SR', '4150.SR', '4220.SR', '4230.SR', '4250.SR', '4300.SR', '4310.SR', '4320.SR', '4321.SR', '4322.SR', '4323.SR']

# companies = ['ADBE', 'ADP', 'ABNB', 'GOOGL', 'GOOG', 'AMZN', 'AMD', 'AEP', 'AMGN', 'ADI', 'ANSS', 'AAPL', 'AMAT', 'ASML', 'AZN', 'TEAM', 'ADSK', 'BKR', 'BIIB', 'BKNG', 'AVGO', 'CDNS', 'CDW', 'CHTR', 'CTAS', 'CSCO', 'CCEP', 'CTSH', 'CMCSA', 'CEG', 'CPRT', 'CSGP', 'COST', 'CRWD', 'CSX', 'DDOG', 'DXCM', 'FANG', 'DLTR', 'DASH', 'EA', 'EXC', 'FAST', 'FTNT', 'GEHC', 'GILD', 'GFS', 'HON', 'IDXX', 'ILMN', 'INTC', 'INTU', 'ISRG', 'KDP', 'KLAC', 'KHC', 'LRCX', 'LIN', 'LULU', 'MAR', 'MRVL', 'MELI', 'META', 'MCHP', 'MU', 'MSFT', 'MRNA', 'MDLZ', 'MDB', 'MNST', 'NFLX', 'NVDA', 'NXPI', 'ORLY', 'ODFL', 'ON', 'PCAR', 'PANW', 'PAYX', 'PYPL', 'PDD', 'PEP', 'QCOM', 'REGN', 'ROP', 'ROST', 'SIRI', 'SBUX', 'SNPS', 'TTWO', 'TMUS', 'TSLA', 'TXN', 'TTD', 'VRSK', 'VRTX', 'WBA', 'WBD', 'WDAY', 'XEL', 'ZS']
# companies = companies[:100]

# companies = ['AACI', 'AACIU', 'AACIW', 'AADI', 'AAGR', 'AAGRW', 'AAL', 'AAME', 'AAOI', 'AAON', 'AAPL', 'ABAT', 'ABCB', 'ABEO', 'ABIO', 'ABL', 'ABLLL', 'ABLLW', 'ABNB', 'ABOS', 'ABSI', 'ABVC', 'ACAB', 'ACABW', 'ACAC', 'ACAD', 'ACCD', 'ACDC', 'ACET', 'ACHC', 'ACHV', 'ACIC', 'ACIW', 'ACLS', 'ACLX', 'ACMR', 'ACNB', 'ACNT', 'ACON', 'ACOR', 'ACRS', 'ACRV', 'ACT', 'ACTG', 'ACVA', 'ACXP', 'ADBE', 'ADD', 'ADEA', 'ADI', 'ADIL', 'ADMA', 'ADN', 'ADNWW', 'ADOC', 'ADOCR', 'ADOCW', 'ADP', 'ADPT', 'ADSK', 'ADTH', 'ADTHW', 'ADTN', 'ADTX', 'ADUS', 'ADV', 'ADVM', 'ADVWW', 'AEAE', 'AEHR', 'AEI', 'AEIS', 'AEMD', 'AENT', 'AENTW', 'AEP', 'AERT', 'AERTW', 'AEYE', 'AFBI', 'AFCG', 'AFIB', 'AFJK', 'AFJKR', 'AFRM', 'AGAE', 'AGEN', 'AGFY', 'AGIO', 'AGNC', 'AGNCL', 'AGNCM', 'AGNCN', 'AGNCO', 'AGNCP', 'AGRX', 'AGYS', 'AHCO', 'AIB', 'AIMBU', 'AIMD', 'AIMDW', 'AIP', 'AIRE', 'AIRG', 'AIRJ', 'AIRJW', 'AIRS', 'AIRT', 'AIRTP', 'AISP', 'AISPW', 'AITR', 'AITRR', 'AITRU', 'AKAM', 'AKBA', 'AKLI', 'AKRO', 'AKTS', 'AKYA', 'ALBT', 'ALCE', 'ALCO', 'ALCY', 'ALCYW', 'ALDX', 'ALEC', 'ALGM', 'ALGN', 'ALGS', 'ALGT', 'ALHC', 'ALIM', 'ALKT', 'ALLK', 'ALLO', 'ALLR', 'ALNT', 'ALNY', 'ALOT', 'ALPN', 'ALPP', 'ALRM', 'ALRN', 'ALRS', 'ALSA', 'ALSAR', 'ALSAU', 'ALSAW', 'ALT', 'ALTI', 'ALTO', 'ALTR', 'ALVR', 'ALXO', 'ALZN', 'AMAL', 'AMAT', 'AMBA', 'AMCX', 'AMD', 'AMED', 'AMGN', 'AMIX', 'AMKR', 'AMLX', 'AMNB', 'AMPG', 'AMPGW', 'AMPH', 'AMPL', 'AMRK', 'AMRX', 'AMSC', 'AMSF', 'AMST', 'AMSWA', 'AMTX', 'AMWD', 'AMZN', 'ANAB', 'ANDE', 'ANEB', 'ANGI', 'ANGO', 'ANIK', 'ANIP', 'ANIX', 'ANNX', 'ANSC', 'ANSCU', 'ANSCW', 'ANSS', 'ANTX', 'AOGO', 'AONC', 'AONCW', 'AOUT', 'APA', 'APAC', 'APACU', 'APACW', 'APCX', 'APCXW', 'APDN', 'APEI', 'APGE', 'APLD', 'APLM', 'APLMW', 'APLS', 'APLT', 'APOG', 'APP', 'APPF', 'APPN', 'APPS', 'APRE', 'APVO', 'APYX', 'AQB', 'AQMS', 'AQST', 'AQU', 'ARAY', 'ARCB', 'ARCC', 'ARDX', 'AREB', 'AREBW', 'AREC', 'ARHS', 'ARKO', 'ARKOW', 'ARKR', 'ARLP', 'AROW', 'ARQ', 'ARQT', 'ARRW', 'ARRWU', 'ARRWW', 'ARRY', 'ARTL', 'ARTLW', 'ARTNA', 'ARTW', 'ARVN', 'ARWR', 'ARYD', 'ASLE', 'ASMB', 'ASNS', 'ASO', 'ASPI', 'ASRT', 'ASRV', 'ASST', 'ASTC', 'ASTE', 'ASTH', 'ASTI', 'ASTR', 'ASTS', 'ASTSW', 'ASUR', 'ASYS', 'ATEC', 'ATER', 'ATEX', 'ATHA', 'ATLC', 'ATLCL', 'ATLCP', 'ATLCZ', 'ATLO', 'ATLX', 'ATMC', 'ATMCR', 'ATMCU', 'ATMCW', 'ATMV', 'ATMVR', 'ATMVU', 'ATNF', 'ATNFW', 'ATNI', 'ATOM', 'ATOS', 'ATRA', 'ATRC', 'ATRI', 'ATRO', 'ATSG', 'ATXI', 'ATXS', 'AUBN', 'AUGX', 'AUID', 'AUR', 'AURA', 'AUROW', 'AUUD', 'AUUDW', 'AUVI', 'AUVIP', 'AVAH', 'AVAV', 'AVBP', 'AVDX', 'AVGO', 'AVGR', 'AVHI', 'AVHIU', 'AVHIW', 'AVIR', 'AVNW', 'AVO', 'AVPT', 'AVPTW', 'AVRO', 'AVT', 'AVTE', 'AVTX', 'AVXL', 'AWH', 'AWRE', 'AXDX', 'AXGN', 'AXNX', 'AXON', 'AXSM', 'AXTI', 'AYRO', 'AYTU', 'AZPN', 'AZTA', 'BACK', 'BAER', 'BAERW', 'BAFN', 'BAND', 'BANF', 'BANFP', 'BANR', 'BANX', 'BASE', 'BATRA', 'BATRK', 'BAYAR', 'BAYAU', 'BBCP', 'BBGI', 'BBIO', 'BBLG', 'BBLGW', 'BBSI', 'BCAB', 'BCAL', 'BCBP', 'BCDA', 'BCDAW', 'BCLI', 'BCML', 'BCOV', 'BCOW', 'BCPC', 'BCRX', 'BDSX', 'BDTX', 'BEAM', 'BEAT', 'BEATW', 'BECN', 'BEEM', 'BEEMW', 'BELFA', 'BELFB', 'BENF', 'BENFW', 'BFC', 'BFIN', 'BFRG', 'BFRGW', 'BFRI', 'BFRIW', 'BFST', 'BGC', 'BGFV', 'BGXX', 'BHAC', 'BHACW', 'BHF', 'BHFAL', 'BHFAM', 'BHFAN', 'BHFAO', 'BHFAP', 'BHRB', 'BIAF', 'BIAFW', 'BIGC', 'BIIB', 'BIOL', 'BIOR', 'BIRD', 'BIVI', 'BJDX', 'BJRI', 'BKNG', 'BKR', 'BKYI', 'BL', 'BLAC', 'BLACR', 'BLACW', 'BLBD', 'BLBX', 'BLDE', 'BLDEW', 'BLEU', 'BLEUR', 'BLEUW', 'BLFS', 'BLFY', 'BLIN', 'BLKB', 'BLMN', 'BLNK', 'BLTE', 'BLUE', 'BLZE', 'BMBL', 'BMEA', 'BMRA', 'BMRC', 'BMRN', 'BNAI', 'BNAIW', 'BNGO', 'BNIX', 'BNIXR', 'BNIXW', 'BNOX', 'BNTC', 'BNZI', 'BNZIW', 'BOCN', 'BOCNW', 'BOF', 'BOKF', 'BOLT', 'BOOM', 'BOTJ', 'BOWN', 'BOWNR', 'BOWNU', 'BOXL', 'BPMC', 'BPOP', 'BPOPM', 'BPRN', 'BPTH', 'BRAC', 'BREZ', 'BREZR', 'BREZW', 'BRFH', 'BRID', 'BRKH', 'BRKHW', 'BRKL', 'BRKR', 'BRLT', 'BRP', 'BRTX', 'BRY', 'BRZE', 'BSBK', 'BSET', 'BSFC', 'BSGM', 'BSRR', 'BSVN', 'BSY', 'BTAI', 'BTBD', 'BTBDW', 'BTBT', 'BTCS', 'BTCY', 'BTM', 'BTMD', 'BTMWW', 'BTOG', 'BTSG', 'BTSGU', 'BUSE', 'BVFL', 'BVS', 'BWAQ', 'BWAQR', 'BWAQW', 'BWB', 'BWBBP', 'BWEN', 'BWFG', 'BWMN', 'BYFC', 'BYND', 'BYRN', 'BYSI', 'BZFD', 'BZFDW', 'CABA', 'CAC', 'CACC', 'CADL', 'CAKE', 'CALB', 'CALC', 'CALM', 'CAMP', 'CAPR', 'CAR', 'CARA', 'CARE', 'CARG', 'CARM', 'CART', 'CARV', 'CASA', 'CASH', 'CASI', 'CASS', 'CASY', 'CATC', 'CATY', 'CAUD', 'CBAN', 'CBAY', 'CBFV', 'CBNK', 'CBRG', 'CBRGU', 'CBRL', 'CBSH', 'CBUS', 'CCAP', 'CCB', 'CCBG', 'CCCC', 'CCCS', 'CCD', 'CCLD', 'CCLDO', 'CCLDP', 'CCLP', 'CCNE', 'CCNEP', 'CCOI', 'CCRN', 'CCSI', 'CCTS', 'CCTSW', 'CDAQ', 'CDIO', 'CDIOW', 'CDLX', 'CDMO', 'CDNA', 'CDNS', 'CDT', 'CDTTW', 'CDTX', 'CDW', 'CDXC', 'CDXS', 'CDZI', 'CDZIP', 'CEAD', 'CEADW', 'CECO', 'CEG', 'CELC', 'CELH', 'CELU', 'CELUW', 'CELZ', 'CENT', 'CENTA', 'CENX', 'CERE', 'CERO', 'CEROW', 'CERS', 'CERT', 'CETX', 'CETY', 'CEVA', 'CFB', 'CFBK', 'CFFI', 'CFFN', 'CFFS', 'CFLT', 'CFSB', 'CG', 'CGABL', 'CGBD', 'CGBDL', 'CGEM', 'CGNX', 'CGO', 'CGON', 'CGTX', 'CHCI', 'CHCO', 'CHDN', 'CHEF', 'CHI', 'CHK', 'CHKEL', 'CHKEW', 'CHKEZ', 'CHMG', 'CHRD', 'CHRS', 'CHRW', 'CHSCL', 'CHSCM', 'CHSCN', 'CHSCO', 'CHSCP', 'CHTR', 'CHUY', 'CHW', 'CHX', 'CHY', 'CIFR', 'CIFRW', 'CINF', 'CING', 'CINGW', 'CISO', 'CITE', 'CITEU', 'CIVB', 'CKPT', 'CLAR', 'CLBK', 'CLDX', 'CLFD', 'CLIR', 'CLMB', 'CLMT', 'CLNE', 'CLNN', 'CLNNW', 'CLOE', 'CLOEU', 'CLOV', 'CLPT', 'CLRB', 'CLRO', 'CLSD', 'CLSK', 'CLST', 'CMAX', 'CMAXW', 'CMCA', 'CMCO', 'CMCSA', 'CMCT', 'CME', 'CMLS', 'CMPO', 'CMPOW', 'CMPX', 'CMRX', 'CMTL', 'CNDT', 'CNFR', 'CNFRZ', 'CNGL', 'CNGLW', 'CNOB', 'CNOBP', 'CNSL', 'CNSP', 'CNTX', 'CNTY', 'CNVS', 'CNXA', 'CNXC', 'CNXN', 'COCH', 'COCHW', 'COCO', 'COCP', 'CODA', 'CODX', 'COEP', 'COEPW', 'COFS', 'COGT', 'COHU', 'COIN', 'COKE', 'COLB', 'COLL', 'COLM', 'COMM', 'CONN', 'CONX', 'CONXW', 'COO', 'COOL', 'COOLW', 'COOP', 'CORT', 'CORZ', 'CORZW', 'CORZZ', 'COSM', 'COST', 'COYA', 'CPBI', 'CPHC', 'CPIX', 'CPRT', 'CPRX', 'CPSH', 'CPSS', 'CPTN', 'CPZ', 'CRAI', 'CRBP', 'CRBU', 'CRCT', 'CRDF', 'CRDO', 'CREX', 'CRGX', 'CRIS', 'CRKN', 'CRMD', 'CRMT', 'CRNC', 'CRNX', 'CROX', 'CRSR', 'CRUS', 'CRVL', 'CRVO', 'CRVS', 'CRWD', 'CRWS', 'CSBR', 'CSCO', 'CSGP', 'CSGS', 'CSLM', 'CSLMR', 'CSLR', 'CSPI', 'CSQ', 'CSSE', 'CSSEL', 'CSSEN', 'CSSEP', 'CSTL', 'CSTR', 'CSWC', 'CSWCZ', 'CSWI', 'CSX', 'CTAS', 'CTBI', 'CTCX', 'CTCXW', 'CTHR', 'CTKB', 'CTLP', 'CTMX', 'CTNT', 'CTRN', 'CTSH', 'CTSO', 'CTXR', 'CUBA', 'CUE', 'CULL', 'CURI', 'CURIW', 'CUTR', 'CVBF', 'CVCO', 'CVCY', 'CVGI', 'CVGW', 'CVII', 'CVIIU', 'CVIIW', 'CVKD', 'CVLG', 'CVLT', 'CVLY', 'CVRX', 'CVV', 'CWBC', 'CWD', 'CWST', 'CXAI', 'CXAIW', 'CXDO', 'CYCC', 'CYCCP', 'CYCN', 'CYN', 'CYRX', 'CYTH', 'CYTHW', 'CYTK', 'CZFS', 'CZNC', 'CZR', 'CZWI', 'DAIO', 'DAKT', 'DALN', 'DARE', 'DASH', 'DATS', 'DATSW', 'DAVE', 'DAVEW', 'DAWN', 'DBGI', 'DBGIW', 'DBX', 'DCGO', 'DCOM', 'DCOMP', 'DCPH', 'DCTH', 'DDOG', 'DECA', 'DECAW', 'DENN', 'DERM', 'DFLI', 'DFLIW', 'DGICA', 'DGICB', 'DGII', 'DGLY', 'DH', 'DHAC', 'DHACW', 'DHAI', 'DHAIW', 'DHC', 'DHCNI', 'DHCNL', 'DHIL', 'DIBS', 'DIOD', 'DJCO', 'DKNG', 'DLHC', 'DLPN', 'DLTH', 'DLTR', 'DMAC', 'DMLP', 'DMRC', 'DMTK', 'DNLI', 'DNTH', 'DNUT', 'DOCU', 'DOMH', 'DOMO', 'DORM', 'DPCS', 'DPCSU', 'DRCT', 'DRMA', 'DRRX', 'DRVN', 'DSGN', 'DSGR', 'DSKE', 'DSP', 'DTI', 'DTIL', 'DTST', 'DTSTW', 'DUOL', 'DUOT', 'DVAX', 'DWAC', 'DWACU', 'DWACW', 'DWSN', 'DXCM', 'DXLG', 'DXPE', 'DXR', 'DXYN', 'DYAI', 'DYN', 'DYNT', 'DZSI', 'EA', 'EAST', 'EBAY', 'EBC', 'EBMT', 'EBTC', 'ECBK', 'ECDA', 'ECOR', 'ECPG', 'EDBL', 'EDBLW', 'EDIT', 'EDSA', 'EDUC', 'EEFT', 'EEIQ', 'EFOI', 'EFSC', 'EFSCP', 'EFTR', 'EFTRW', 'EGAN', 'EGBN', 'EGHT', 'EGIO', 'EGRX', 'EHTH', 'EIGR', 'EKSO', 'ELAB', 'ELDN', 'ELEV', 'ELSE', 'ELTX', 'ELUT', 'ELVN', 'ELYM', 'EMBC', 'EMCG', 'EMCGW', 'EMKR', 'EML', 'EMLD', 'ENG', 'ENPH', 'ENSC', 'ENSG', 'ENTA', 'ENTG', 'ENVB', 'ENVX', 'EOLS', 'EOSE', 'EOSEW', 'EPSN', 'EQ', 'EQIX', 'ERAS', 'ERIE', 'ERII', 'ERNA', 'ESCA', 'ESHA', 'ESHAR', 'ESLA', 'ESLAW', 'ESOA', 'ESPR', 'ESQ', 'ESSA', 'ETAO', 'ETNB', 'ETON', 'ETSY', 'EU', 'EVBG', 'EVCM', 'EVER', 'EVGO', 'EVGOW', 'EVLV', 'EVLVW', 'EVOK', 'EVRG', 'EVTV', 'EWBC', 'EWCZ', 'EWTX', 'EXAS', 'EXC', 'EXEL', 'EXFY', 'EXLS', 'EXPE', 'EXPI', 'EXPO', 'EXTR', 'EYE', 'EYEN', 'EYPT', 'EZFL', 'EZPW', 'FA', 'FANG', 'FARM', 'FARO', 'FAST', 'FAT', 'FATBB', 'FATBP', 'FATBW', 'FATE', 'FBIO', 'FBIOP', 'FBIZ', 'FBLG', 'FBMS', 'FBNC', 'FBRX', 'FBYD', 'FBYDW', 'FCAP', 'FCBC', 'FCCO', 'FCEL', 'FCFS', 'FCNCA', 'FCNCO', 'FCNCP', 'FCUV', 'FDBC', 'FDMT', 'FDUS', 'FEAM', 'FEIM', 'FELE', 'FEMY', 'FENC', 'FEXD', 'FFBC', 'FFIC', 'FFIE', 'FFIEW', 'FFIN', 'FFIV', 'FFNW', 'FGBI', 'FGBIP', 'FGEN', 'FGF', 'FGFPP', 'FGI', 'FGIWW', 'FHB', 'FHLTU', 'FHLTW', 'FHTX', 'FIAC', 'FIBK', 'FINW', 'FIP', 'FISI', 'FITB', 'FITBI', 'FITBO', 'FITBP', 'FIVE', 'FIVN', 'FIXX', 'FIZZ', 'FKWL', 'FLFV', 'FLFVR', 'FLFVW', 'FLGT', 'FLIC', 'FLL', 'FLNC', 'FLNT', 'FLUX', 'FLWS', 'FLXS', 'FLYW', 'FMAO', 'FMBH', 'FMNB', 'FNCB', 'FNCH', 'FNGR', 'FNKO', 'FNLC', 'FNWB', 'FNWD', 'FOLD', 'FONR', 'FORA', 'FORD', 'FORL', 'FORLW', 'FORM', 'FORR', 'FOSL', 'FOSLL', 'FOX', 'FOXA', 'FOXF', 'FPAY', 'FRAF', 'FRBA', 'FREE', 'FREEW', 'FRGT', 'FRLA', 'FRME', 'FRMEP', 'FROG', 'FRPH', 'FRPT', 'FRSH', 'FRST', 'FRZA', 'FSBC', 'FSBW', 'FSEA', 'FSFG', 'FSLR', 'FSTR', 'FTAI', 'FTAIM', 'FTAIN', 'FTAIO', 'FTAIP', 'FTCI', 'FTDR', 'FTEK', 'FTHM', 'FTII', 'FTLF', 'FTNT', 'FTRE', 'FULC', 'FULT', 'FULTP', 'FUNC', 'FUND', 'FUSB', 'FUV', 'FVCB', 'FWBI', 'FWONA', 'FWONK', 'FWRD', 'FWRG', 'FXNC', 'FYBR', 'GABC', 'GAIA', 'GAIN', 'GAINL', 'GAINN', 'GAINZ', 'GALT', 'GAMCU', 'GAMCW', 'GAME', 'GANX', 'GATE', 'GBBK', 'GBBKR', 'GBBKW', 'GBDC', 'GBIO', 'GBNY', 'GCBC', 'GCMG', 'GCMGW', 'GDEN', 'GDRX', 'GDST', 'GDSTR', 'GDYN', 'GECC', 'GECCM', 'GECCO', 'GECCZ', 'GEG', 'GEGGL', 'GEHC', 'GEN', 'GENK', 'GEOS', 'GERN', 'GEVO', 'GFS', 'GH', 'GHIX', 'GHIXW', 'GHSI', 'GIFI', 'GIII', 'GILD', 'GIPR', 'GIPRW', 'GLAD', 'GLADZ', 'GLBZ', 'GLDD', 'GLLI', 'GLPI', 'GLSI', 'GLST', 'GLSTR', 'GLSTW', 'GLUE', 'GLYC', 'GMFI', 'GMFIU', 'GMFIW', 'GMGI', 'GNLN', 'GNLX', 'GNPX', 'GNSS', 'GNTX', 'GO', 'GOCO', 'GODN', 'GODNR', 'GOEV', 'GOEVW', 'GOGO', 'GOOD', 'GOODN', 'GOODO', 'GOOG', 'GOOGL', 'GORV', 'GOSS', 'GOVX', 'GPAC', 'GPACU', 'GPAK', 'GPCR', 'GPRE', 'GPRO', 'GRDI', 'GRDIW', 'GREE', 'GREEL', 'GRI', 'GROM', 'GROMW', 'GROW', 'GRPH', 'GRPN', 'GRTS', 'GRTX', 'GRWG', 'GRYP', 'GSBC', 'GSHD', 'GSIT', 'GT', 'GTAC', 'GTBP', 'GTHX', 'GTIM', 'GTLB', 'GUTS', 'GVP', 'GWAV', 'GWRS', 'GXAI', 'GYRE', 'GYRO', 'HA', 'HAFC', 'HAIN', 'HALO', 'HAS', 'HAYN', 'HBAN', 'HBANL', 'HBANM', 'HBANP', 'HBCP', 'HBIO', 'HBNC', 'HBT', 'HCAT', 'HCKT', 'HCMA', 'HCMAU', 'HCMAW', 'HCP', 'HCSG', 'HCTI', 'HCVI', 'HCVIU', 'HCWB', 'HDSN', 'HEAR', 'HEES', 'HEPA', 'HFBL', 'HFFG', 'HFWA', 'HGAS', 'HGASW', 'HGBL', 'HHS', 'HIBB', 'HIFS', 'HLIT', 'HLMN', 'HLNE', 'HLTH', 'HLVX', 'HLXB', 'HMNF', 'HMST', 'HNNA', 'HNNAZ', 'HNRG', 'HNST', 'HNVR', 'HOFT', 'HOFV', 'HOFVW', 'HOLO', 'HOLOW', 'HOLX', 'HON', 'HONE', 'HOOD', 'HOOK', 'HOPE', 'HOTH', 'HOUR', 'HOVNP', 'HOVR', 'HOVRW', 'HOWL', 'HPCO', 'HPK', 'HPKEW', 'HQI', 'HQY', 'HRMY', 'HROW', 'HROWL', 'HROWM', 'HRTX', 'HRZN', 'HSCS', 'HSCSW', 'HSDT', 'HSIC', 'HSII', 'HSON', 'HSPO', 'HSPOR', 'HSPOU', 'HSPOW', 'HST', 'HSTM', 'HTBI', 'HTBK', 'HTIA', 'HTIBP', 'HTLD', 'HTLF', 'HTLFP', 'HTZ', 'HTZWW', 'HUBG', 'HUDA', 'HUDAR', 'HUMA', 'HUMAW', 'HURC', 'HURN', 'HUT', 'HWBK', 'HWC', 'HWCPZ', 'HWH', 'HWKN', 'HYFM', 'HYMC', 'HYMCL', 'HYMCW', 'HYPR', 'HYZN', 'HYZNW', 'IAC', 'IART', 'IAS', 'IBCP', 'IBKR', 'IBOC', 'IBRX', 'IBTX', 'ICAD', 'ICCC', 'ICCH', 'ICCT', 'ICFI', 'ICHR', 'ICMB', 'ICU', 'ICUCW', 'ICUI', 'IDAI', 'IDCC', 'IDEX', 'IDN', 'IDXX', 'IDYA', 'IEP', 'IESC', 'IGMS', 'IGTA', 'IGTAU', 'IHRT', 'III', 'IIIV', 'IKNA', 'IKT', 'ILMN', 'ILPT', 'IMAQ', 'IMAQR', 'IMAQU', 'IMKTA', 'IMMR', 'IMMX', 'IMNM', 'IMNN', 'IMRX', 'IMUX', 'IMVT', 'IMXI', 'INAB', 'INAQ', 'INAQW', 'INBK', 'INBKZ', 'INBS', 'INBX', 'INCY', 'INDB', 'INDI', 'INDP', 'INFN', 'INGN', 'INHD', 'INKT', 'INMB', 'INNV', 'INO', 'INOD', 'INSE', 'INSG', 'INSM', 'INTA', 'INTC', 'INTE', 'INTG', 'INTS', 'INTU', 'INTZ', 'INVA', 'INVE', 'INVO', 'INZY', 'IONM', 'IONS', 'IOSP', 'IOVA', 'IPAR', 'IPDN', 'IPGP', 'IPSC', 'IPW', 'IPWR', 'IPX', 'IPXX', 'IPXXU', 'IRAA', 'IRBT', 'IRDM', 'IRIX', 'IRMD', 'IROH', 'IROHR', 'IROHU', 'IROHW', 'IRON', 'IROQ', 'IRTC', 'IRWD', 'ISPC', 'ISPO', 'ISPOW', 'ISPR', 'ISRG', 'ISRL', 'ISRLW', 'ISSC', 'ISTR', 'ISUN', 'ITCI', 'ITI', 'ITIC', 'ITOS', 'ITRI', 'IVAC', 'IVCP', 'IVCPW', 'IVDA', 'IVDAW', 'IVP', 'IVVD', 'IZEA', 'JACK', 'JAGX', 'JAKK', 'JAMF', 'JAN', 'JANX', 'JBHT', 'JBLU', 'JBSS', 'JCTCF', 'JEWL', 'JJSF', 'JKHY', 'JMSB', 'JNVR', 'JOAN', 'JOUT', 'JRSH', 'JSM', 'JSPR', 'JSPRW', 'JVA', 'JYNT', 'KA', 'KALA', 'KALU', 'KAVL', 'KDP', 'KE', 'KELYA', 'KELYB', 'KEQU', 'KFFB', 'KFRC', 'KGEI', 'KHC', 'KIDS', 'KINS', 'KIRK', 'KITT', 'KITTW', 'KLAC', 'KLTR', 'KLXE', 'KNSA', 'KNTE', 'KOD', 'KOPN', 'KOSS', 'KPLT', 'KPLTW', 'KPRX', 'KPTI', 'KRMD', 'KRNL', 'KRNLU', 'KRNLW', 'KRNY', 'KRON', 'KROS', 'KRRO', 'KRT', 'KRUS', 'KRYS', 'KSCP', 'KTCC', 'KTOS', 'KTRA', 'KTTA', 'KTTAW', 'KURA', 'KVAC', 'KVACU', 'KVHI', 'KYCH', 'KYCHR', 'KYCHW', 'KYMR', 'KYTX', 'KZR', 'LAB', 'LABP', 'LAKE', 'LAMR', 'LANC', 'LAND', 'LANDM', 'LANDO', 'LANDP', 'LARK', 'LASE', 'LASR', 'LAUR', 'LAZR', 'LBAI', 'LBPH', 'LBRDA', 'LBRDK', 'LBRDP', 'LCID', 'LCNB', 'LCUT', 'LDTC', 'LDTCW', 'LDWY', 'LE', 'LECO', 'LEE', 'LEGH', 'LEGN', 'LESL', 'LFCR', 'LFLY', 'LFLYW', 'LFMD', 'LFMDP', 'LFST', 'LFUS', 'LFVN', 'LGIH', 'LGMK', 'LGND', 'LGVC', 'LGVCU', 'LGVN', 'LIBY', 'LIBYU', 'LIBYW', 'LIDR', 'LIDRW', 'LIFE', 'LIFW', 'LIFWW', 'LILA', 'LILAK', 'LIN', 'LINC', 'LIND', 'LINK', 'LIPO', 'LITE', 'LIVE', 'LIXT', 'LIXTW', 'LKFN', 'LKQ', 'LLYVA', 'LLYVK', 'LMAT', 'LMB', 'LMFA', 'LMNR', 'LNKB', 'LNSR', 'LNT', 'LNTH', 'LNW', 'LNZA', 'LNZAW', 'LOAN', 'LOCO', 'LOGI', 'LOPE', 'LOVE', 'LPCN', 'LPLA', 'LPRO', 'LPSN', 'LPTH', 'LPTX', 'LQDA', 'LQDT', 'LQR', 'LRCX', 'LRFC', 'LRHC', 'LRMR', 'LSBK', 'LSCC', 'LSEA', 'LSEAW', 'LSTA', 'LSTR', 'LSXMA', 'LSXMB', 'LSXMK', 'LTBR', 'LTRN', 'LTRX', 'LTRY', 'LTRYW', 'LUCD', 'LUCY', 'LUCYW', 'LUMO', 'LUNA', 'LUNG', 'LUNR', 'LUNRW', 'LUXH', 'LUXHP', 'LVLU', 'LVO', 'LWAY', 'LWLG', 'LXEO', 'LXRX', 'LYEL', 'LYFT', 'LYRA', 'LYTS', 'LZ', 'MACA', 'MACAW', 'MACK', 'MAMA', 'MANH', 'MAPS', 'MAPSW', 'MAQC', 'MAQCW', 'MAR', 'MARA', 'MARPS', 'MARX', 'MARXU', 'MASI', 'MASS', 'MAT', 'MATW', 'MAYS', 'MBCN', 'MBIN', 'MBINM', 'MBINN', 'MBINO', 'MBINP', 'MBIO', 'MBNKP', 'MBRX', 'MBTC', 'MBTCR', 'MBTCU', 'MBUU', 'MBWM', 'MCAA', 'MCAAU', 'MCAAW', 'MCAC', 'MCAF', 'MCAFR', 'MCAFU', 'MCAG', 'MCBC', 'MCBS', 'MCFT', 'MCHP', 'MCHX', 'MCRB', 'MCRI', 'MCVT', 'MDAI', 'MDAIW', 'MDB', 'MDBH', 'MDGL', 'MDIA', 'MDLZ', 'MDRR', 'MDRRP', 'MDXG', 'ME', 'MEDP', 'MEDS', 'MEIP', 'MESA', 'META', 'METC', 'METCB', 'METCL', 'MFIC', 'MFICL', 'MFIN', 'MGAM', 'MGEE', 'MGNI', 'MGNX', 'MGOL', 'MGPI', 'MGRC', 'MGRM', 'MGRX', 'MGTX', 'MGX', 'MGYR', 'MICS', 'MIDD', 'MIND', 'MINDP', 'MINM', 'MIRA', 'MIRM', 'MITA', 'MITK', 'MKSI', 'MKTW', 'MKTX', 'MLAB', 'MLGO', 'MLKN', 'MLTX', 'MLYS', 'MMAT', 'MMLP', 'MMSI', 'MNKD', 'MNMD', 'MNOV', 'MNPR', 'MNRO', 'MNSB', 'MNSBP', 'MNST', 'MNTK', 'MNTS', 'MNTSW', 'MNTX', 'MOBX', 'MOBXW', 'MODD', 'MODV', 'MOFG', 'MOND', 'MORF', 'MORN', 'MOVE', 'MPAA', 'MPB', 'MPWR', 'MQ', 'MRAI', 'MRAM', 'MRBK', 'MRCC', 'MRCY', 'MRIN', 'MRKR', 'MRNA', 'MRNS', 'MRSN', 'MRTN', 'MRVI', 'MRVL', 'MSAI', 'MSAIW', 'MSBI', 'MSBIP', 'MSEX', 'MSFT', 'MSGM', 'MSS', 'MSSA', 'MSSAW', 'MSTR', 'MTCH', 'MTEM', 'MTEX', 'MTRX', 'MTSI', 'MTTR', 'MU', 'MULN', 'MVBF', 'MVIS', 'MVLA', 'MVLAW', 'MVST', 'MVSTW', 'MXCT', 'MXL', 'MYFW', 'MYGN', 'MYMD', 'MYPS', 'MYRG', 'NAII', 'NAOV', 'NARI', 'NATH', 'NATR', 'NAUT', 'NAVI', 'NB', 'NBBK', 'NBIX', 'NBN', 'NBSE', 'NBST', 'NBSTW', 'NBTB', 'NCMI', 'NCNO', 'NCPL', 'NCPLW', 'NCSM', 'NDAQ', 'NDLS', 'NDRA', 'NDSN', 'NECB', 'NEO', 'NEOG', 'NEOV', 'NEOVW', 'NEPH', 'NERV', 'NETD', 'NETDU', 'NETDW', 'NEWT', 'NEWTI', 'NEWTL', 'NEWTZ', 'NEXI', 'NEXT', 'NFBK', 'NFE', 'NFLX', 'NGM', 'NHTC', 'NICK', 'NIOBW', 'NKGN', 'NKGNW', 'NKLA', 'NKSH', 'NKTR', 'NKTX', 'NMFC', 'NMFCZ', 'NMHI', 'NMHIW', 'NMIH', 'NMRA', 'NMRK', 'NMTC', 'NN', 'NNAG', 'NNAGU', 'NNAGW', 'NNAVW', 'NNBR', 'NODK', 'NOTV', 'NOVT', 'NPAB', 'NPABU', 'NPCE', 'NRBO', 'NRC', 'NRDS', 'NRIM', 'NRIX', 'NRXP', 'NRXPW', 'NSIT', 'NSSC', 'NSTS', 'NSYS', 'NTAP', 'NTCT', 'NTGR', 'NTIC', 'NTLA', 'NTNX', 'NTRA', 'NTRB', 'NTRBW', 'NTRP', 'NTRS', 'NTRSO', 'NTWK', 'NURO', 'NUTX', 'NUVL', 'NUWE', 'NUZE', 'NVAC', 'NVACR', 'NVACW', 'NVAX', 'NVCT', 'NVDA', 'NVEC', 'NVEE', 'NVFY', 'NVNO', 'NVOS', 'NVTS', 'NWBI', 'NWE', 'NWFL', 'NWL', 'NWLI', 'NWPX', 'NWS', 'NWSA', 'NXGL', 'NXGLW', 'NXL', 'NXLIW', 'NXPL', 'NXPLW', 'NXST', 'NXT', 'NXTC', 'NXTP', 'NXU', 'NYMT', 'NYMTL', 'NYMTM', 'NYMTN', 'NYMTZ', 'OABI', 'OABIW', 'OB', 'OBIO', 'OBLG', 'OBT', 'OCAX', 'OCAXW', 'OCC', 'OCCI', 'OCCIN', 'OCCIO', 'OCEA', 'OCEAW', 'OCFC', 'OCFCP', 'OCGN', 'OCSL', 'OCTO', 'OCUL', 'OCUP', 'OCX', 'ODFL', 'ODP', 'OESX', 'OFLX', 'OFS', 'OFSSH', 'OKTA', 'OLB', 'OLED', 'OLLI', 'OLMA', 'OLPX', 'OM', 'OMCL', 'OMER', 'OMEX', 'OMGA', 'OMIC', 'OMQS', 'ON', 'ONB', 'ONBPO', 'ONBPP', 'ONCO', 'ONCT', 'ONDS', 'ONEW', 'ONFO', 'ONFOW', 'ONTX', 'ONVO', 'ONYX', 'ONYXW', 'OPAL', 'OPBK', 'OPCH', 'OPEN', 'OPGN', 'OPHC', 'OPI', 'OPINL', 'OPK', 'OPOF', 'OPRT', 'OPRX', 'OPTN', 'OPTX', 'OPTXW', 'OPXS', 'ORGN', 'ORGNW', 'ORGO', 'ORGS', 'ORIC', 'ORLY', 'ORRF', 'OSA', 'OSBC', 'OSIS', 'OSPN', 'OSS', 'OSUR', 'OTLK', 'OTRK', 'OTTR', 'OVBC', 'OVID', 'OVLY', 'OXLC', 'OXLCL', 'OXLCM', 'OXLCN', 'OXLCO', 'OXLCP', 'OXLCZ', 'OXSQ', 'OXSQG', 'OXSQZ', 'OZK', 'OZKAP', 'PAA', 'PACB', 'PAGP', 'PAHC', 'PALI', 'PALT', 'PANL', 'PANW', 'PARA', 'PARAA', 'PARAP', 'PASG', 'PATK', 'PAVM', 'PAVMZ', 'PAYO', 'PAYOW', 'PAYS', 'PAYX', 'PBBK', 'PBFS', 'PBHC', 'PBPB', 'PBYI', 'PCAR', 'PCB', 'PCH', 'PCRX', 'PCSA', 'PCT', 'PCTTU', 'PCTTW', 'PCTY', 'PCVX', 'PCYO', 'PDCO', 'PDEX', 'PDFS', 'PDLB', 'PDSB', 'PEBK', 'PEBO', 'PECO', 'PEGA', 'PEGR', 'PEGRW', 'PEGY', 'PENN', 'PEP', 'PEPG', 'PEPL', 'PEPLW', 'PESI', 'PET', 'PETQ', 'PETS', 'PETV', 'PETVW', 'PETWW', 'PEV', 'PFBC', 'PFC', 'PFG', 'PFIE', 'PFIS', 'PFMT', 'PFTA', 'PFTAU', 'PFTAW', 'PFX', 'PFXNZ', 'PGC', 'PGEN', 'PGNY', 'PHAT', 'PHIO', 'PI', 'PIII', 'PIIIW', 'PIK', 'PINC', 'PIRS', 'PIXY', 'PKBK', 'PKOH', 'PLAB', 'PLAY', 'PLBC', 'PLBY', 'PLCE', 'PLL', 'PLMI', 'PLMIW', 'PLMJ', 'PLMJW', 'PLMR', 'PLPC', 'PLRX', 'PLSE', 'PLTN', 'PLTNR', 'PLTNW', 'PLUG', 'PLUS', 'PLXS', 'PMCB', 'PMD', 'PMGM', 'PMGMW', 'PMTS', 'PMVP', 'PNBK', 'PNFP', 'PNFPP', 'PNRG', 'PNTG', 'POAI', 'POCI', 'PODC', 'PODD', 'POLA', 'POOL', 'POWI', 'POWL', 'POWW', 'POWWP', 'PPBI', 'PPC', 'PPIH', 'PPSI', 'PPYA', 'PPYAW', 'PRAA', 'PRAX', 'PRCH', 'PRCT', 'PRDO', 'PRFT', 'PRGS', 'PRLD', 'PRLH', 'PRLHU', 'PRME', 'PROK', 'PROP', 'PROV', 'PRPH', 'PRPL', 'PRPO', 'PRSO', 'PRST', 'PRSTW', 'PRTA', 'PRTC', 'PRTH', 'PRTS', 'PRVA', 'PSEC', 'PSMT', 'PSNL', 'PSTV', 'PSTX', 'PTC', 'PTCT', 'PTEN', 'PTGX', 'PTIX', 'PTIXW', 'PTLO', 'PTMN', 'PTON', 'PTPI', 'PTSI', 'PTVE', 'PTWO', 'PTWOU', 'PUBM', 'PUCK', 'PUCKW', 'PULM', 'PVBC', 'PWFL', 'PWOD', 'PWP', 'PWUP', 'PXLW', 'PXMD', 'PYCR', 'PYPL', 'PYXS', 'PZZA', 'QCOM', 'QCRH', 'QDEL', 'QDRO', 'QETA', 'QETAR', 'QETAU', 'QIPT', 'QLGN', 'QLYS', 'QMCO', 'QNCX', 'QNST', 'QOMO', 'QQQX', 'QRHC', 'QRTEA', 'QRTEB', 'QRTEP', 'QRVO', 'QSI', 'QSIAW', 'QTI', 'QTRX', 'QUBT', 'QUIK', 'RAIL', 'RAND', 'RANI', 'RAPT', 'RARE', 'RAVE', 'RBB', 'RBBN', 'RBCAA', 'RBKB', 'RCAT', 'RCEL', 'RCKT', 'RCKTW', 'RCKY', 'RCM', 'RCMT', 'RCRT', 'RCRTW', 'RDFN', 'RDI', 'RDIB', 'RDNT', 'RDUS', 'RDVT', 'RDZN', 'RDZNW', 'REAL', 'REBN', 'REFI', 'REFR', 'REG', 'REGCO', 'REGCP', 'REGN', 'REKR', 'RELI', 'RELIW', 'RELL', 'RELY', 'RENB', 'RENE', 'RENEU', 'RENEW', 'RENT', 'REPL', 'REVB', 'REVBW', 'REYN', 'RFIL', 'RGCO', 'RGEN', 'RGF', 'RGLD', 'RGLS', 'RGNX', 'RGP', 'RGS', 'RGTI', 'RGTIW', 'RICK', 'RIGL', 'RILY', 'RILYG', 'RILYK', 'RILYL', 'RILYM', 'RILYN', 'RILYO', 'RILYP', 'RILYT', 'RILYZ', 'RIOT', 'RIVN', 'RKDA', 'RKLB', 'RLAY', 'RLMD', 'RLYB', 'RMBI', 'RMBL', 'RMBS', 'RMCF', 'RMCO', 'RMCOW', 'RMGC', 'RMGCU', 'RMNI', 'RMR', 'RMTI', 'RNA', 'RNAC', 'RNAZ', 'RNXT', 'ROAD', 'ROCK', 'ROCL', 'ROIC', 'ROKU', 'ROOT', 'ROP', 'ROST', 'RPAY', 'RPD', 'RPHM', 'RPID', 'RPRX', 'RR', 'RRBI', 'RRGB', 'RRR', 'RSLS', 'RSSS', 'RSVR', 'RSVRW', 'RUM', 'RUMBW', 'RUN', 'RUSHA', 'RUSHB', 'RVMD', 'RVMDW', 'RVNC', 'RVPH', 'RVPHW', 'RVSB', 'RVYL', 'RWAY', 'RWAYL', 'RWAYZ', 'RWOD', 'RWODR', 'RXRX', 'RXST', 'RXT', 'RYTM', 'RZLT', 'SABR', 'SABS', 'SABSW', 'SAFT', 'SAGE', 'SAIA', 'SAIC', 'SAMG', 'SANA', 'SANM', 'SANW', 'SASR', 'SATS', 'SAVA', 'SAVAW', 'SBAC', 'SBCF', 'SBFG', 'SBGI', 'SBRA', 'SBSI', 'SBT', 'SBUX', 'SCHL', 'SCKT', 'SCLX', 'SCLXW', 'SCOR', 'SCPH', 'SCRM', 'SCRMW', 'SCSC', 'SCTL', 'SCVL', 'SCWO', 'SCWX', 'SCYX', 'SDGR', 'SDIG', 'SDOT', 'SEAT', 'SEATW', 'SEEL', 'SEER', 'SEIC', 'SELF', 'SENEA', 'SENEB', 'SEPA', 'SEPAW', 'SERA', 'SEVN', 'SEZL', 'SFBC', 'SFIX', 'SFM', 'SFNC', 'SFST', 'SGA', 'SGBX', 'SGC', 'SGD', 'SGH', 'SGHT', 'SGLY', 'SGMA', 'SGMO', 'SGMT', 'SGRP', 'SGRY', 'SHBI', 'SHC', 'SHCR', 'SHCRW', 'SHEN', 'SHFS', 'SHFSW', 'SHIM', 'SHLS', 'SHOO', 'SHOT', 'SHOTW', 'SHPH', 'SHPW', 'SHPWW', 'SHYF', 'SIBN', 'SIDU', 'SIEB', 'SIGA', 'SIGI', 'SIGIP', 'SILK', 'SILO', 'SINT', 'SIRI', 'SITM', 'SKGR', 'SKGRW', 'SKIN', 'SKWD', 'SKYT', 'SKYW', 'SKYX', 'SLAB', 'SLAM', 'SLAMU', 'SLAMW', 'SLDB', 'SLDP', 'SLDPW', 'SLE', 'SLM', 'SLMBP', 'SLNG', 'SLNH', 'SLNHP', 'SLNO', 'SLP', 'SLRC', 'SLRN', 'SLRX', 'SLS', 'SMBC', 'SMCI', 'SMFL', 'SMID', 'SMLR', 'SMMF', 'SMMT', 'SMPL', 'SMSI', 'SMTC', 'SMTI', 'SMXT', 'SNAL', 'SNAX', 'SNAXW', 'SNBR', 'SNCR', 'SNCRL', 'SNCY', 'SND', 'SNDX', 'SNES', 'SNEX', 'SNFCA', 'SNGX', 'SNOA', 'SNPO', 'SNPS', 'SNPX', 'SNSE', 'SNTI', 'SOBR', 'SOFI', 'SOHO', 'SOHOB', 'SOHON', 'SOHOO', 'SOND', 'SONDW', 'SONM', 'SONN', 'SONO', 'SOPA', 'SOTK', 'SOUN', 'SOUNW', 'SP', 'SPEC', 'SPECW', 'SPFI', 'SPGC', 'SPKL', 'SPKLU', 'SPKLW', 'SPOK', 'SPRB', 'SPRO', 'SPRY', 'SPSC', 'SPT', 'SPTN', 'SPWH', 'SPWR', 'SQFT', 'SQFTP', 'SQFTW', 'SRBK', 'SRCE', 'SRCL', 'SRDX', 'SRM', 'SRPT', 'SRRK', 'SRTS', 'SRZN', 'SRZNW', 'SSBI', 'SSBK', 'SSIC', 'SSKN', 'SSNC', 'SSNT', 'SSP', 'SSSS', 'SSSSL', 'SSTI', 'SSYS', 'STAA', 'STAF', 'STBA', 'STCN', 'STEP', 'STER', 'STHO', 'STI', 'STIM', 'STIX', 'STIXW', 'STKS', 'STLD', 'STOK', 'STRA', 'STRC', 'STRCW', 'STRL', 'STRM', 'STRO', 'STRR', 'STRRP', 'STRS', 'STRT', 'STSS', 'STSSW', 'STTK', 'SUPN', 'SURG', 'SURGW', 'SVC', 'SVII', 'SVIIR', 'SVIIU', 'SVIIW', 'SVRA', 'SWAG', 'SWAGW', 'SWAV', 'SWBI', 'SWIM', 'SWKH', 'SWKHL', 'SWKS', 'SWSS', 'SWSSW', 'SWTX', 'SXTP', 'SXTPW', 'SYBT', 'SYBX', 'SYM', 'SYNA', 'SYPR', 'SYRA', 'SYRE', 'SYRS', 'TACT', 'TAIT', 'TALK', 'TALKW', 'TARA', 'TARS', 'TASK', 'TAST', 'TAYD', 'TBBK', 'TBIO', 'TBLD', 'TBLT', 'TBMC', 'TBMCR', 'TBNK', 'TBRG', 'TCBC', 'TCBI', 'TCBIO', 'TCBK', 'TCBS', 'TCBX', 'TCMD', 'TCON', 'TCPC', 'TCRT', 'TCRX', 'TDUP', 'TECH', 'TECTP', 'TELA', 'TELO', 'TENB', 'TENK', 'TENKR', 'TENX', 'TER', 'TERN', 'TFFP', 'TFIN', 'TFINP', 'TFSL', 'TGAN', 'TGL', 'TGTX', 'TH', 'THAR', 'THCP', 'THFF', 'THMO', 'THRD', 'THRM', 'THRY', 'TIL', 'TILE', 'TIPT', 'TITN', 'TIVC', 'TKNO', 'TLF', 'TLGY', 'TLGYW', 'TLIS', 'TLPH', 'TLRY', 'TLS', 'TLSI', 'TLSIW', 'TMCI', 'TMDX', 'TMTC', 'TMTCR', 'TMTCU', 'TMUS', 'TNDM', 'TNGX', 'TNON', 'TNONW', 'TNXP', 'TNYA', 'TOI', 'TOMZ', 'TOWN', 'TPCS', 'TPG', 'TPGXL', 'TPIC', 'TPST', 'TRDA', 'TREE', 'TRIN', 'TRINL', 'TRIP', 'TRMB', 'TRMK', 'TRML', 'TRNR', 'TRNS', 'TRON', 'TRONU', 'TRONW', 'TROW', 'TRS', 'TRST', 'TRUE', 'TRUG', 'TRUP', 'TRVI', 'TRVN', 'TSBK', 'TSBX', 'TSCO', 'TSHA', 'TSLA', 'TSRI', 'TSVT', 'TTD', 'TTEC', 'TTEK', 'TTGT', 'TTMI', 'TTNP', 'TTOO', 'TTSH', 'TTWO', 'TURN', 'TUSK', 'TVGN', 'TVGNW', 'TVTX', 'TW', 'TWIN', 'TWKS', 'TWLV', 'TWLVW', 'TWOU', 'TWST', 'TXG', 'TXMD', 'TXN', 'TXRH', 'TYGO', 'TYRA', 'TZOO', 'UAL', 'UBCP', 'UBFO', 'UBSI', 'UBX', 'UCBI', 'UCBIO', 'UCTT', 'UDMY', 'UEIC', 'UFCS', 'UFPI', 'UFPT', 'UG', 'UGRO', 'UHG', 'UHGWW', 'UK', 'UKOMW', 'ULBI', 'ULCC', 'ULH', 'ULTA', 'ULY', 'UMBF', 'UNB', 'UNCY', 'UNIT', 'UNTY', 'UONE', 'UONEK', 'UPBD', 'UPLD', 'UPST', 'UPWK', 'UPXI', 'URBN', 'USAP', 'USAU', 'USCB', 'USCT', 'USCTW', 'USEG', 'USGO', 'USGOW', 'USIO', 'USLM', 'UTHR', 'UTMD', 'UVSP', 'VABK', 'VALU', 'VANI', 'VAXX', 'VBFC', 'VBIV', 'VBTX', 'VC', 'VCEL', 'VCNX', 'VCSA', 'VCTR', 'VCYT', 'VECO', 'VEEE', 'VERA', 'VERB', 'VERBW', 'VERI', 'VERO', 'VERU', 'VERV', 'VERX', 'VERY', 'VGAS', 'VIA', 'VIASP', 'VIAV', 'VICR', 'VIEW', 'VIEWW', 'VIGL', 'VINC', 'VINO', 'VIR', 'VIRC', 'VIRI', 'VIRT', 'VIRX', 'VISL', 'VITL', 'VIVK', 'VKTX', 'VLCN', 'VLGEA', 'VLY', 'VLYPO', 'VLYPP', 'VMCA', 'VMD', 'VMEO', 'VNDA', 'VNOM', 'VOR', 'VOXX', 'VRA', 'VRAR', 'VRCA', 'VRDN', 'VREX', 'VRM', 'VRME', 'VRMEW', 'VRNS', 'VRNT', 'VRPX', 'VRRM', 'VRSK', 'VRSN', 'VRTX', 'VSAC', 'VSACW', 'VSAT', 'VSEC', 'VSTM', 'VTGN', 'VTNR', 'VTRS', 'VTSI', 'VTVT', 'VTYX', 'VUZI', 'VVOS', 'VWE', 'VWEWW', 'VXRT', 'VYGR', 'VYNE', 'WABC', 'WAFD', 'WAFDP', 'WALD', 'WALDW', 'WASH', 'WATT', 'WAVD', 'WAVS', 'WBA', 'WBD', 'WDAY', 'WDC', 'WDFC', 'WEN', 'WERN', 'WEST', 'WESTW', 'WEYS', 'WFCF', 'WFRD', 'WGS', 'WGSWW', 'WHF', 'WHFCL', 'WHLM', 'WHLR', 'WHLRD', 'WHLRP', 'WINA', 'WING', 'WINT', 'WINV', 'WINVR', 'WIRE', 'WISA', 'WISH', 'WKHS', 'WLDN', 'WLFC', 'WMG', 'WMPN', 'WNEB', 'WOOF', 'WORX', 'WRAP', 'WRLD', 'WSBC', 'WSBCP', 'WSBF', 'WSC', 'WSFS', 'WTBA', 'WTFC', 'WTFCM', 'WTFCP', 'WTMA', 'WTMAR', 'WULF', 'WVVI', 'WVVIP', 'WW', 'WWD', 'WYNN', 'XAIR', 'XBIO', 'XBIT', 'XBP', 'XBPEW', 'XCUR', 'XEL', 'XELA', 'XELAP', 'XELB', 'XERS', 'XFIN', 'XFINW', 'XFOR', 'XGN', 'XLO', 'XMTR', 'XNCR', 'XOMA', 'XOMAO', 'XOMAP', 'XOS', 'XOSWW', 'XPEL', 'XPON', 'XRAY', 'XRX', 'XTIA', 'XWEL', 'XXII', 'YHGJ', 'YMAB', 'YORW', 'YOSH', 'YOTA', 'YOTAR', 'YOTAU', 'YOTAW', 'YTEN', 'Z', 'ZBRA', 'ZCAR', 'ZCARW', 'ZD', 'ZEO', 'ZEOWW', 'ZEUS', 'ZFOX', 'ZFOXW', 'ZG', 'ZI', 'ZIMV', 'ZION', 'ZIONL', 'ZIONO', 'ZIONP', 'ZLS', 'ZM', 'ZNTL', 'ZS', 'ZUMZ', 'ZVRA', 'ZVSA', 'ZYME', 'ZYXI']


st.title("Stock Data Exporter")

def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    writer.save()
    processed_data = output.getvalue()
    return processed_data

def main():
    # Dropdown menu for selection
    menu_selection = st.selectbox("Choose the data to display", ["", "Prices and Divs Details", "Prices By Industry", "Prices By Sector", "Cash Flow",
                                                                 "Balance Sheet", "Income Statement", "Divs", "Stocks Summary (for assessing valuation)", "Aggregated Financials"])

    # If the user selects "Prices and Divs Details"
    if menu_selection == "Prices and Divs Details":
        if st.button('Fetch Data'):
            # Display a message while data is being fetched
            with st.spinner('Data is being fetched, please wait!'):
                df = fetch_prices(companies)
                
                # Once data is fetched, clear the previous message and display a new message
                st.success('Data has been fetched correctly. You can download it now!')

            # Display the DataFrame in the app
            st.write(df)

            # Generate download link for Excel file
            to_download = to_excel(df)
            b64 = base64.b64encode(to_download).decode()
            href = f'<a href="data:application/octet-stream;base64,{b64}" download="price_stats_compare.xlsx">Download Excel file</a>'
            st.markdown(href, unsafe_allow_html=True)
            
    elif menu_selection == "Prices By Industry":
        if st.button('Fetch Data'):
            # Display a message while data is being fetched
            with st.spinner('Data is being fetched, please wait!'):
                df = fetch_data_by_segment(companies, "Industry")
                
                # Once data is fetched, clear the previous message and display a new message
                st.success('Data has been fetched correctly. You can download it now!')

            # Display the DataFrame in the app
            st.write(df)

            # Generate download link for Excel file
            to_download = to_excel(df)
            b64 = base64.b64encode(to_download).decode()
            href = f'<a href="data:application/octet-stream;base64,{b64}" download="price_stats_compare_by_industry.xlsx">Download Excel file</a>'
            st.markdown(href, unsafe_allow_html=True)

    elif menu_selection == "Prices By Sector":
        if st.button('Fetch Data'):
            # Display a message while data is being fetched
            with st.spinner('Data is being fetched, please wait!'):
                df = fetch_data_by_segment(companies, "Sector")
                
                # Once data is fetched, clear the previous message and display a new message
                st.success('Data has been fetched correctly. You can download it now!')

            # Display the DataFrame in the app
            st.write(df)

            # Generate download link for Excel file
            to_download = to_excel(df)
            b64 = base64.b64encode(to_download).decode()
            href = f'<a href="data:application/octet-stream;base64,{b64}" download="price_stats_compare_by_sector.xlsx">Download Excel file</a>'
            st.markdown(href, unsafe_allow_html=True)
            
    elif menu_selection == "Cash Flow":
        if st.button('Fetch Data'):
            # Display a message while data is being fetched
            with st.spinner('Data is being fetched, please wait!'):
                df = fetch_cash_flow(companies)
                
                # Once data is fetched, clear the previous message and display a new message
                st.success('Data has been fetched correctly. You can download it now!')

            # Display the DataFrame in the app
            st.write(df)

            # Generate download link for Excel file
            to_download = to_excel(df)
            b64 = base64.b64encode(to_download).decode()
            href = f'<a href="data:application/octet-stream;base64,{b64}" download="cash_flow_compare.xlsx">Download Excel file</a>'
            st.markdown(href, unsafe_allow_html=True)

    elif menu_selection == "Balance Sheet":
        if st.button('Fetch Data'):
            # Display a message while data is being fetched
            with st.spinner('Data is being fetched, please wait!'):
                df = fetch_data_balance_sheet(companies)
                
                # Once data is fetched, clear the previous message and display a new message
                st.success('Data has been fetched correctly. You can download it now!')

            # Display the DataFrame in the app
            st.write(df)

            # Generate download link for Excel file
            to_download = to_excel(df)
            b64 = base64.b64encode(to_download).decode()
            href = f'<a href="data:application/octet-stream;base64,{b64}" download="balance_sheet_compare.xlsx">Download Excel file</a>'
            st.markdown(href, unsafe_allow_html=True)

    elif menu_selection == "Income Statement":
        if st.button('Fetch Data'):
            # Display a message while data is being fetched
            with st.spinner('Data is being fetched, please wait!'):
                df = fetch_data_income_stmt(companies)
                
                # Once data is fetched, clear the previous message and display a new message
                st.success('Data has been fetched correctly. You can download it now!')

            # Display the DataFrame in the app
            st.write(df)

            # Generate download link for Excel file
            to_download = to_excel(df)
            b64 = base64.b64encode(to_download).decode()
            href = f'<a href="data:application/octet-stream;base64,{b64}" download="income_stmt_compare.xlsx">Download Excel file</a>'
            st.markdown(href, unsafe_allow_html=True)
            

    elif menu_selection == "Divs":
        if st.button('Fetch Data'):
            # Display a message while data is being fetched
            with st.spinner('Data is being fetched, please wait!'):
                df = fetch_dividends_and_info(companies)
                
                # Once data is fetched, clear the previous message and display a new message
                st.success('Data has been fetched correctly. You can download it now!')

            # Display the DataFrame in the app
            st.write(df)

            # Generate download link for Excel file
            to_download = to_excel(df)
            b64 = base64.b64encode(to_download).decode()
            href = f'<a href="data:application/octet-stream;base64,{b64}" download="stock_dividends_info.xlsx">Download Excel file</a>'
            st.markdown(href, unsafe_allow_html=True)
            
    elif menu_selection == "Stocks Summary (for assessing valuation)":
        
        if st.button('Fetch Data'):
            # Display a message while data is being fetched
            with st.spinner('Data is being fetched, please wait!'):
                df = fetch_summary(companies)
                
                # Once data is fetched, clear the previous message and display a new message
                st.success('Data has been fetched correctly. You can download it now!')

            # Display the DataFrame in the app
            st.write(df)

            # Generate download link for Excel file
            to_download = to_excel(df)
            b64 = base64.b64encode(to_download).decode()
            href = f'<a href="data:application/octet-stream;base64,{b64}" download="stocks_summary_values.xlsx">Download Excel file</a>'
            st.markdown(href, unsafe_allow_html=True)            

    elif menu_selection == "Aggregated Financials":
        
        if st.button('Fetch Data'):
            # Display a message while data is being fetched
            with st.spinner('Data is being fetched, please wait!'):
                df = aggregate_financials(companies)
                
                # Once data is fetched, clear the previous message and display a new message
                st.success('Data has been fetched correctly. You can download it now!')

            # Display the DataFrame in the app
            st.write(df)

            # Generate download link for Excel file
            to_download = to_excel(df)
            b64 = base64.b64encode(to_download).decode()
            href = f'<a href="data:application/octet-stream;base64,{b64}" download="aggregated_financials.xlsx">Download Excel file</a>'
            st.markdown(href, unsafe_allow_html=True) 
            

if __name__ == "__main__":
    main()
