# streamlit_app.py
import streamlit as st
from fetch_prices import fetch_prices  # Assuming 'test.py' is your data fetching script
from industry_stocks import fetch_data_by_segment
from fetch_cash_flow import fetch_cash_flow
from fetch_balance_sheet import fetch_data_balance_sheet 
from fetch_income_stmt import fetch_data_income_stmt
from fetch_divs import fetch_dividends_and_info
from fetch_stocks_summary import fetch_summary
from fetch_finanical_metrics_all import aggregate_financials as aggregate_financials_by_year
from fetch_finanical_metrics_all_by_quarters import aggregate_financials as aggregate_financials_by_quarter
import pandas as pd
from io import BytesIO
import base64


# TASI
companies = ['2030.SR', '2222.SR', '2380.SR', '2381.SR', '2382.SR', '4030.SR', '4200.SR', '1201.SR', '1202.SR', '1210.SR', '1211.SR', '1301.SR', '1304.SR', '1320.SR', '1321.SR', '1322.SR', '2001.SR', '2010.SR', '2020.SR', '2060.SR', '2090.SR', '2150.SR', '2170.SR', '2180.SR', '2200.SR', '2210.SR', '2220.SR', '2223.SR', '2240.SR', '2250.SR', '2290.SR', '2300.SR', '2310.SR', '2330.SR', '2350.SR', '2360.SR', '3001.SR', '3002.SR', '3003.SR', '3004.SR', '3005.SR', '3007.SR', '3008.SR', '3010.SR', '3020.SR', '3030.SR', '3040.SR', '3050.SR', '3060.SR', '3080.SR', '3090.SR', '3091.SR', '3092.SR', '1212.SR', '1214.SR', '1302.SR', '1303.SR', '2040.SR', '2110.SR', '2160.SR', '2320.SR', '2370.SR', '4110.SR', '4140.SR', '4141.SR', '4142.SR', '1831.SR', '1832.SR', '1833.SR', '4270.SR', '6004.SR', '2190.SR', '4031.SR', '4040.SR', '4260.SR', '4261.SR', '4262.SR', '4263.SR', '1213.SR', '2130.SR', '2340.SR', '4011.SR', '4012.SR', '4180.SR', '1810.SR', '1820.SR', '1830.SR', '4170.SR', '4290.SR', '4291.SR', '4292.SR', '6002.SR', '6012.SR', '6013.SR', '6014.SR', '6015.SR', '4070.SR', '4071.SR', '4072.SR', '4210.SR', '4003.SR', '4008.SR', '4050.SR', '4051.SR', '4190.SR', '4191.SR', '4192.SR', '4240.SR', '4001.SR', '4006.SR', '4061.SR', '4160.SR', '4161.SR', '4162.SR', '4163.SR', '4164.SR', '2050.SR', '2100.SR', '2270.SR', '2280.SR', '2281.SR', '2282.SR', '2283.SR', '2284.SR', '4080.SR', '6001.SR', '6010.SR', '6020.SR', '6040.SR', '6050.SR', '6060.SR', '6070.SR', '6090.SR', '2140.SR', '2230.SR', '4002.SR', '4004.SR', '4005.SR', '4007.SR', '4009.SR', '4013.SR', '4014.SR', '4017.SR', '2070.SR', '4015.SR', '4016.SR', '1010.SR', '1020.SR', '1030.SR', '1050.SR', '1060.SR', '1080.SR', '1120.SR', '1140.SR', '1150.SR', '1180.SR', '1111.SR', '1182.SR', '1183.SR', '2120.SR', '4081.SR', '4082.SR', '4130.SR', '4280.SR', '8010.SR', '8012.SR', '8020.SR', '8030.SR', '8040.SR', '8050.SR', '8060.SR', '8070.SR', '8100.SR', '8120.SR', '8150.SR', '8160.SR', '8170.SR', '8180.SR', '8190.SR', '8200.SR', '8210.SR', '8230.SR', '8240.SR', '8250.SR', '8260.SR', '8270.SR', '8280.SR', '8300.SR', '8310.SR', '8311.SR', '7200.SR', '7201.SR', '7202.SR', '7203.SR', '7204.SR', '7010.SR', '7020.SR', '7030.SR', '7040.SR', '2080.SR', '2081.SR', '2082.SR', '2083.SR', '5110.SR', '4330.SR', '4331.SR', '4332.SR', '4333.SR', '4334.SR', '4335.SR', '4336.SR', '4337.SR', '4338.SR', '4339.SR', '4340.SR', '4342.SR', '4344.SR', '4345.SR', '4346.SR', '4347.SR', '4348.SR', '4349.SR', '4020.SR', '4090.SR', '4100.SR', '4150.SR', '4220.SR', '4230.SR', '4250.SR', '4300.SR', '4310.SR', '4320.SR', '4321.SR', '4322.SR', '4323.SR']

# companies = ['ADBE', 'ADP', 'ABNB', 'GOOGL', 'GOOG', 'AMZN', 'AMD', 'AEP', 'AMGN', 'ADI', 'ANSS', 'AAPL', 'AMAT', 'ASML', 'AZN', 'TEAM', 'ADSK', 'BKR', 'BIIB', 'BKNG', 'AVGO', 'CDNS', 'CDW', 'CHTR', 'CTAS', 'CSCO', 'CCEP', 'CTSH', 'CMCSA', 'CEG', 'CPRT', 'CSGP', 'COST', 'CRWD', 'CSX', 'DDOG', 'DXCM', 'FANG', 'DLTR', 'DASH', 'EA', 'EXC', 'FAST', 'FTNT', 'GEHC', 'GILD', 'GFS', 'HON', 'IDXX', 'ILMN', 'INTC', 'INTU', 'ISRG', 'KDP', 'KLAC', 'KHC', 'LRCX', 'LIN', 'LULU', 'MAR', 'MRVL', 'MELI', 'META', 'MCHP', 'MU', 'MSFT', 'MRNA', 'MDLZ', 'MDB', 'MNST', 'NFLX', 'NVDA', 'NXPI', 'ORLY', 'ODFL', 'ON', 'PCAR', 'PANW', 'PAYX', 'PYPL', 'PDD', 'PEP', 'QCOM', 'REGN', 'ROP', 'ROST', 'SIRI', 'SBUX', 'SNPS', 'TTWO', 'TMUS', 'TSLA', 'TXN', 'TTD', 'VRSK', 'VRTX', 'WBA', 'WBD', 'WDAY', 'XEL', 'ZS']


# companies = ['MSFT', 'AAPL', 'NVDA', 'GOOG', 'GOOGL', 'AMZN', 'META', 'AVGO', 'TSLA', 'COST', 'NFLX', 'AMD', 'PEP', 'QCOM', 'ADBE', 'LIN', 'TMUS', 'CSCO', 'AMAT', 'TXN', 'INTU', 'AMGN', 'CMCSA', 'MU', 'ISRG', 'INTC', 'HON', 'BKNG', 'LRCX', 'ADI', 'VRTX', 'REGN', 'KLAC', 'PANW', 'ADP', 'ABNB', 'MDLZ', 'SNPS', 'SBUX', 'CRWD', 'CDNS', 'GILD', 'CME', 'EQIX', 'CEG', 'CTAS', 'MRVL', 'MAR', 'CSX', 'PYPL', 'COIN', 'MRNA', 'ROP', 'WDAY', 'PCAR', 'ORLY', 'MNST', 'MCHP', 'SMCI', 'CPRT', 'DXCM', 'AEP', 'ROST', 'DASH', 'KDP', 'FTNT', 'ADSK', 'PAYX', 'KHC', 'IDXX', 'DDOG', 'CHTR', 'ODFL', 'FAST', 'MPWR', 'EXC', 'GEHC', 'VRSK', 'FANG', 'EA', 'NDAQ', 'CSGP', 'CTSH', 'BKR', 'HBANM', 'BIIB', 'ON', 'TSCO', 'CDW', 'FSLR', 'XEL', 'MSTR', 'ANSS', 'GFS', 'APP', 'TTWO', 'EBAY', 'TW', 'TROW', 'FCNCA', 'HBANP', 'FITB', 'WDC', 'DLTR', 'ZS', 'TER', 'AXON', 'PTC', 'LPLA', 'STLD', 'SBAC', 'QRTEP', 'ENTG', 'HBAN', 'WBD', 'ZM', 'ALGN', 'PFG', 'ALNY', 'ULTA', 'COO', 'CINF', 'HOOD', 'AGNCL', 'NTNX', 'FITBI', 'ERIE', 'DKNG', 'HOLX', 'SLMBP', 'VRSN', 'FWONK', 'NTRS', 'ZBRA', 'ILMN', 'UAL', 'JBHT', 'OKTA', 'RPRX', 'FITBP', 'BSY', 'TPG', 'NWS', 'FOXA', 'FWONA', 'GEN', 'CG', 'WMG', 'NWSA', 'LOGI', 'SSNC', 'SWKS', 'EXPE', 'FITBO', 'FOX', 'NBIX', 'BMRN', 'AKAM', 'MANH', 'AZPN', 'IBKR', 'PARAA', 'TRMB', 'POOL', 'NTRA', 'NDSN', 'WBA', 'ARCC', 'INCY', 'HST', 'LNT', 'SWAV', 'TECH', 'CASY', 'MORN', 'PODD', 'VTRS', 'VLYPO', 'AGNCN', 'EVRG', 'MEDP', 'LAMR', 'AGNCM', 'GLPI', 'UTHR', 'PAA', 'CHK', 'DOCU', 'JKHY', 'TXRH', 'LKQ', 'WING', 'TTEK', 'LECO', 'WWD', 'VLYPP', 'APA', 'BRKR', 'REG', 'ALAB', 'SRPT', 'LSCC', 'SIRI', 'SAIA', 'WYNN', 'RIVN', 'EWBC', 'CHRW', 'CHKEL', 'FFIV', 'CHDN', 'CFLT', 'CROX', 'Z', 'QRVO', 'COKE', 'ZG', 'AFRM', 'HSIC', 'WFRD', 'AAL', 'SEIC', 'MKSI', 'RGEN', 'OLED', 'HAS', 'LNW', 'RGLD', 'PCTY', 'PPC', 'CART', 'FTAI', 'GTLB', 'DUOL', 'AMKR', 'ROKU', 'CGNX', 'PARA', 'GNTX', 'SFM', 'ONBPP', 'ONBPO', 'BTSGU', 'MKTX', 'MTCH', 'LSXMB', 'CHRD', 'LEGN', 'NXT', 'ALTR', 'DBX', 'MTSI', 'IEP', 'PCVX', 'LBRDA', 'LBRDK', 'LSXMA', 'LSXMK', 'FIVE', 'CCCS', 'SOFI', 'UFPI', 'CZR', 'INSM', 'ETSY', 'SPSC', 'CBSH', 'HLNE', 'SAIC', 'AGNC', 'ITCI', 'VNOM', 'HQY', 'ENSG', 'MASI', 'NSIT', 'HCP', 'MIDD', 'BPMC', 'BPOP', 'LFUS', 'CGABL', 'AAON', 'LSTR', 'FYBR', 'LYFT', 'LCID', 'CRUS', 'CHX', 'ZION', 'RVMD', 'BECN', 'MAT', 'PNFP', 'RMBS', 'WTFC', 'ALGM', 'EXEL', 'CACC', 'BOKF', 'NOVT', 'ACHC', 'REYN', 'CWST', 'SIGI', 'XRAY', 'AVAV', 'IONS', 'HALO', 'FCFS', 'RCM', 'ONB', 'QLYS', 'OZK', 'BBIO', 'NXST', 'OPCH', 'EEFT', 'RRR', 'NFE', 'TENB', 'VRNS', 'LANC', 'CYTK', 'ITRI', 'SATS', 'PEGA', 'AVT', 'BCPC', 'APLS', 'EXLS', 'STEP', 'COLM', 'ACT', 'CVLT', 'ZI', 'EXPO', 'MDGL', 'MMSI', 'SRCL', 'IBRX', 'KRYS', 'FORM', 'SLM', 'FELE', 'PTEN', 'PI', 'POWI', 'WIRE', 'UBSI', 'CRVL', 'OXLCM', 'NUVL', 'LOPE', 'FFIN', 'FIZZ', 'IAC', 'FLNC', 'REGCP', 'NTRSO', 'BRZE', 'BGC', 'ASO', 'OXLCN', 'OXLCL', 'IMVT', 'CNXC', 'OXLCP', 'REGCO', 'SLAB', 'OXLCZ', 'BWIN', 'BLKB', 'AEIS', 'CSWI', 'FRSH', 'HWC', 'CAR', 'COLB', 'UMBF', 'URBN', 'OXLCO', 'IPAR', 'IPGP', 'PECO', 'AUR', 'STRL', 'ACLS', 'SANM', 'OTTR', 'SYNA', 'CRNX', 'VLY', 'ACIW', 'VIRT', 'IRDM', 'LLYVK', 'TFSL', 'IBOC', 'WEN', 'FROG', 'PAGP', 'RUSHA', 'NCNO', 'GT', 'FULTP', 'LLYVA', 'AXNX', 'DIOD', 'VCTR', 'PCH', 'CRDO', 'DHCNL', 'ALRM', 'RUSHB', 'SBRA', 'ABCB', 'KTOS', 'RARE', 'SGRY', 'LBRDP', 'ROAD', 'IOSP', 'NWL', 'GH', 'SHOO', 'DHCNI', 'JJSF', 'SWTX', 'SHC', 'AMED', 'NWE', 'WDFC', 'PLXS', 'ACVA', 'ARLP', 'CENT', 'LITE', 'UCBI', 'VC', 'FULT', 'BL', 'RUN', 'ARWR', 'CALM', 'QDEL', 'NEOG', 'NARI', 'CVCO', 'CCOI', 'SKYW', 'BANF', 'MQ', 'DORM', 'IDYA', 'UCBIO', 'MGEE', 'IDCC', 'GBDC', 'PTCT', 'STRA', 'FIBK', 'AZTA', 'TCBI', 'ACLX', 'AGYS', 'ALKT', 'IRTC', 'GDRX', 'FTDR', 'TXG', 'MRVI', 'MGRC', 'DNLI', 'INTA', 'CERT', 'HUBG', 'BHF', 'ICFI', 'WSFS', 'MYRG', 'CENTA', 'DYN', 'SMTC', 'CATY', 'CSQ', 'FHB', 'RELY', 'PRFT', 'BATRA', 'ICUI', 'FTAIP', 'ZD', 'FTAIO', 'PSMT', 'PGNY', 'PATK', 'FTAIN', 'TRIP', 'ACAD', 'LAUR', 'GSHD', 'POWL', 'TWST', 'ARHS', 'FA', 'CARG', 'NTAP', 'ARCB', 'BATRK', 'ARVN', 'SNEX', 'OSIS', 'PSEC', 'EBC', 'VECO', 'PYCR', 'WERN', 'LION', 'PENN', 'IART', 'CVBF', 'FTRE', 'LGIH', 'FLYW', 'ROCK', 'WAFD', 'AVDX', 'DCPH', 'PTVE', 'AGIO', 'LFST', 'GO', 'NVAX', 'NYMTM', 'PRGS', 'SFNC', 'PDCO', 'INDB', 'RXRX', 'FFBC', 'MYGN', 'JAMF', 'PPBI', 'JSM', 'AMRX', 'UPST', 'AMBA', 'PRVA', 'AMPH', 'HWCPZ', 'PLMR', 'PLUS', 'TOWN', 'UCTT', 'BEAM', 'SONO', 'GERN', 'PINC', 'PLAY', 'VSAT', 'USLM', 'NYMTN', 'SBCF', 'BTSG', 'CAKE', 'VRNT', 'FRME', 'IBTX', 'MLKN', 'NSSC', 'TTMI', 'DRVN', 'EVCM', 'FOXF', 'MRCY', 'HWKN', 'OZKAP', 'ENVX', 'HTLF', 'ADUS', 'JBLU', 'BPOPM', 'BLMN', 'DNUT', 'NYMTL', 'PNFPP', 'TRMK', 'ANDE', 'NWLI', 'CNXN', 'NMRK', 'MGNI', 'CENX', 'NYMTZ', 'HEES', 'XRX', 'PLAB', 'SANA', 'NBTB', 'TFIN', 'SNDX', 'LILA', 'LILAK', 'TBBK', 'UPBD', 'AVPT', 'DSGR', 'MGPI', 'NAVI', 'MFICL', 'VIAV', 'KURA', 'QRTEB', 'WSBC', 'THRM', 'LZ', 'SDGR', 'EWTX', 'HURN', 'BANR', 'IAS', 'KALU', 'MXL', 'OCSL', 'CHEF', 'LKFN', 'VICR', 'PZZA', 'CLBK', 'PRDO', 'ACDC', 'WTFCP', 'ROIC', 'NVEE', 'COCO', 'OPEN', 'STER', 'NMRA', 'WTFCM', 'DVAX', 'CHCO', 'COHU', 'EXTR', 'FRMEP', 'PWP', 'OMCL', 'SKWD', 'NTCT', 'BHFAO', 'WSBCP', 'VIR', 'BMBL', 'APOG', 'OCFCP', 'ATEC', 'UPWK', 'EFSC', 'MRTN', 'HTZ', 'ALHC', 'ODP', 'UDMY', 'HLIT', 'PCRX', 'BHFAP', 'NWBI', 'AMWD', 'BHFAL', 'PDFS', 'IMKTA', 'ASTS', 'CRCT', 'METCL', 'TLRY', 'KNSA', 'GIII', 'AKRO', 'CASH', 'SYBT', 'NMFC', 'GOGO', 'SYRE', 'CGEM', 'INFN', 'DMLP', 'TARS', 'CLMT', 'FBNC', 'FDMT', 'BUSE', 'BASE', 'BCRX', 'WABC', 'ICHR', 'CSGS', 'TASK', 'CMCO', 'ADEA', 'TRINZ', 'WAFDP', 'HOPE', 'SRCE', 'TCBK', 'CIFR', 'VSEC', 'STBA', 'MCRI', 'SCSC', 'ULH', 'CRSR', 'FWRG', 'ULCC', 'DAWN', 'CRAI', 'BHFAN', 'SABR', 'CSWCZ', 'JBSS', 'GPRE', 'SAFT', 'ADV', 'CSWC', 'COLL', 'SIGIP', 'PTON', 'EYE', 'SGH', 'ELVN', 'TRS', 'PFBC', 'HTLFP', 'ANGI', 'PRTA', 'SCHL', 'WOOF', 'ECPG', 'OLPX', 'JACK', 'CBRL', 'PEBO', 'ARQT', 'HIBB', 'QNST', 'SEAT', 'MFIC', 'SASR', 'RBCAA', 'BHFAM', 'LESL', 'SCVL', 'RWAYZ', 'SLP', 'BELFA', 'RWAYL', 'INVA', 'SHEN', 'GABC', 'OPK', 'LAB', 'TWKS', 'GAINL', 'OXLC', 'IRWD', 'TCPC', 'DGII', 'MSEX', 'GOODN', 'CGBD', 'AMRK', 'HTLD', 'SVC', 'TILE', 'ALGT', 'CECO', 'HUMA', 'TCBIO', 'GAINN', 'SLRC', 'CORZ', 'ATSG', 'FIP', 'OCFC', 'PRAA', 'MATW', 'AVO', 'BELFB', 'TYRA', 'HTZWW', 'SILK', 'GAINZ', 'AMSF', 'ROOT', 'BBSI', 'HSTM', 'SRRK', 'HUT', 'SNPO', 'BJRI', 'GOODO', 'KELYB', 'COGT', 'ATRI', 'SBSI', 'ERII', 'DXPE', 'HCSG', 'CTKB', 'PLRX', 'KELYA', 'PRAX', 'CNOBP', 'BRKL', 'METC', 'CTBI', 'EMBC', 'HAYN', 'XMTR', 'AMCX', 'EFSCP', 'UNIT', 'ASTE', 'ATRO', 'CNOB', 'WRLD', 'RGNX', 'RDFN', 'TRIN', 'STOK', 'SWBI', 'LAZR', 'DCOM', 'PNTG', 'NRC', 'MNRO', 'PFC', 'HA', 'HSII', 'CRGX', 'LYEL', 'SPTN', 'NKLA', 'DCOMP', 'CNDT', 'CFFN', 'EWCZ', 'CORZZ', 'ALXO', 'IIIV', 'PLPC', 'VMEO', 'DH', 'CFB', 'UVSP', 'OSBC', 'ANAB', 'SSYS', 'HAIN', 'HLVX', 'FDUS', 'EVGO', 'HFWA', 'FCBC', 'LASR', 'PTLO', 'GRPN', 'CVLG', 'DSP', 'MCBS', 'GLDD', 'MLAB', 'ZYME', 'VREX', 'TREE', 'CLNE', 'MBWM', 'HBT', 'TSHA', 'MLYS', 'PHAT', 'HCKT', 'FLWS', 'ACCD', 'GSBC', 'METCB', 'ORIC', 'PETQ', 'ZEUS', 'WHFCL', 'FRPH', 'CCB', 'CASS', 'LQDT', 'DMRC', 'DHC', 'UFCS', 'SVRA', 'KRT', 'KYTX', 'KE', 'LEGH', 'APLD', 'BAND', 'GOOD', 'EZPW', 'ACTG', 'BVS', 'RBBN', 'GLADZ', 'INNV', 'IGMS', 'NCMI', 'SVCO', 'NYMT', 'ADPT', 'MSBIP', 'WGS', 'BFST', 'AVAH', 'YMAB', 'TRST', 'HBNC', 'FOSLL', 'BRY', 'SCWX', 'DAKT', 'SBGI', 'IBCP', 'SPWR', 'YORW', 'OLMA', 'CCRN', 'CABA', 'CTLP', 'CNSL', 'PACB', 'TBLD', 'GAIN', 'SNCY', 'TFINP', 'CLOV', 'SRDX', 'MXCT', 'RDUS', 'HTBK', 'FSBC', 'ALEC', 'MSBI', 'AMSC', 'GLAD', 'ABSI', 'MCBC', 'HTBI', 'CCNEP', 'PEPG', 'CAC', 'HAFC', 'CVGW', 'CEVA', 'BYND', 'FNKO', 'RWAY', 'LYTS', 'ANNX', 'CCBG', 'NKTX', 'HONE', 'VLGEA', 'CHUY', 'ZIMV', 'ADTN', 'WASH', 'SENEB', 'VERV', 'THFF', 'EDIT', 'ERAS', 'DGICA', 'VYGR', 'SPFI', 'REAL', 'SWIM', 'SHYF', 'SENEA', 'AROW', 'RXT', 'BMEA', 'LXRX', 'ALLO', 'DHIL', 'CCNE', 'TERN', 'TITN', 'HRZN', 'HCAT', 'DGICB', 'SLRN', 'ATLC', 'NFBK', 'FWRD', 'NTGR', 'LENZ', 'MODV', 'CRMT', 'PGC', 'AVNW', 'CCSI', 'CTNM', 'RGP', 'ZUMZ', 'FFIC', 'CHSCP', 'LINC', 'EGHT', 'SHBI', 'CCCC', 'ANIK', 'FARO', 'LMNR', 'PAL', 'ATNI', 'VTYX', 'KRNY', 'JOUT', 'OSUR', 'ARTNA', 'AMSWA', 'TRML', 'STTK', 'MNMD', 'NWPX', 'PGEN', 'AVXL', 'FORR', 'RBB', 'PKOH', 'MOFG', 'AUROW', 'MGTX', 'ATLCP', 'FCNCO', 'CHSCO', 'CIFRW', 'LOCO', 'TNYA', 'RRBI', 'ZYXI', 'REPL', 'IMMR', 'APEI', 'USAP', 'SHCR', 'FCNCP', 'CHSCL', 'CHSCN', 'SLP', 'TMCI', 'EBTC', 'LUNG', 'CHSCM', 'ITIC', 'BSRR', 'SNBR', 'ASTSW', 'WHF', 'CPZ', 'AVIR', 'NRIM', 'SPOK', 'MTRX', 'TTEC', 'SGHT', 'HBCP', 'FSTR', 'MRSN', 'CARE', 'SLDB', 'WTBA', 'QRTEA', 'WEYS', 'TCBX', 'XERS', 'FBIZ', 'PFIS', 'CBNK', 'NATH', 'BSVN', 'PSTX', 'HNST', 'SFIX', 'IRBT', 'FISI', 'IPSC', 'INZY', 'MGNX', 'FNLC', 'CRBU', 'PBPB', 'BOOM', 'TRUE', 'RCKY', 'CLAR', 'BDTX', 'INBK', 'ENTA', 'ANGO', 'COMM', 'ILPT', 'VRA', 'UTMD', 'PFMT', 'WSBF', 'MGX', 'XBIT', 'DSGN', 'GPRO', 'AVPTW', 'LCUT', 'TDUP', 'FUND', 'SSBK', 'NAUT', 'OB', 'BCML', 'CDXS', 'HUMAW', 'SSP', 'PYXS', 'TSVT', 'BLFY', 'OVID', 'PCB', 'HOWL', 'BOLD', 'GLUE', 'INBKZ', 'ELEV', 'CHMG', 'OM', 'GBIO', 'PRLD', 'CTRN', 'ALCO', 'INGN', 'JAKK', 'ABOS', 'MFIN', 'TWIN', 'PBYI', 'FFNW', 'BPRN', 'ZVRA', 'STRS', 'CALB', 'PTMN', 'OXSQ', 'GTHX', 'ESSA', 'TUSK', 'FLXS', 'HOFT', 'CVGI', 'HMST', 'LFCR', 'KLTR', 'EHTH', 'PLCE', 'MYFW', 'VIASP', 'AXTI', 'RELL', 'RIGL', 'MRCC', 'NNBR', 'CVRX', 'CRNC', 'ARAY', 'EXFY', 'CFFI', 'PWOD', 'TBRG', 'WNEB', 'DLTH', 'MAPS', 'MCRB', 'CTMX', 'GEOS', 'SCPH', 'UEIC', 'GOSS', 'SYRS', 'HWBK', 'FUNC', 'OPTN', 'LOGC', 'BANX', 'SPWH', 'SGMO', 'BSET', 'OFS', 'FGEN', 'PRPL', 'SEATW', 'BFIN', 'UBFO', 'VIGL', 'IHRT', 'HYZN', 'ALLK', 'MMLP', 'SEER', 'OPRT', 'HNVR', 'HURC', 'KPTI', 'WW', 'FEAM', 'OMGA', 'AMLX', 'GIFI', 'AKYA', 'IMUX', 'MRBK', 'ISSC', 'RRGB', 'OPI', 'MPAA', 'TZOO', 'MVST', 'INSG', 'IVAC', 'PMVP', 'VOR', 'BLUE', 'AOUT', 'KVHI', 'ATHA', 'SSSS', 'BIRD', 'SND', 'BCOV', 'GREEL', 'KLXE', 'RLMD', 'PETS', 'PROV', 'GRTS', 'ALVR', 'VCSA', 'NICK', 'CONN', 'NDLS', 'VOXX', 'ASMB', 'ASYS', 'LEE', 'RVSB', 'SPRO', 'VIA', 'ACRS', 'BGFV', 'ATRA', 'PASG', 'FOSL', 'CMTL', 'TBNK', 'RAIL', 'GSIT', 'AVRO', 'PRTS', 'RLYB', 'SCOR', 'ANTX', 'MCHX', 'FARM', 'DWSN', 'LRFC', 'LPSN', 'GEG', 'APYX', 'KZR', 'ICMB', 'KRON', 'EVGOW', 'HSON', 'NXTC', 'CUTR', 'HYFM', 'QNCX', 'SLDPW', 'SOND', 'RPID', 'XLO', 'VIRX', 'BOLT', 'KIRK', 'SPRB', 'GREE', 'RVMDW', 'UBX', 'TXMD', 'TWOU', 'CPIX', 'VRM', 'QTI', 'MTEX', 'CMAX', 'MAPSW', 'MVSTW', 'HYZNW', 'SHCRW', 'TBIO', 'CAMP', 'WGSWW', 'AGNCP', 'AGNCO', 'SONDW', 'CMAXW', 'CGON', 'BANFP', 'OXSQZ', 'QQQX', 'OXSQG', 'CCD', 'CHI', 'CHY', 'CGO', 'CHW', 'CORZW', 'FTAIM', 'HBANL']
# companies = companies[:1000]

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
                                                                 "Balance Sheet", "Income Statement", "Divs", "Stocks Summary (for assessing valuation)", "Aggregated Financials (By Year)",
                                                                 "Aggregated Financials (By Quarter)"])

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

    elif menu_selection == "Aggregated Financials (By Year)":
        
        if st.button('Fetch Data'):
            # Display a message while data is being fetched
            with st.spinner('Data is being fetched, please wait!'):
                df = aggregate_financials_by_year(companies)
                
                # Once data is fetched, clear the previous message and display a new message
                st.success('Data has been fetched correctly. You can download it now!')

            # Display the DataFrame in the app
            st.write(df)

            # Generate download link for Excel file
            to_download = to_excel(df)
            b64 = base64.b64encode(to_download).decode()
            href = f'<a href="data:application/octet-stream;base64,{b64}" download="aggregated_financials_by_year.xlsx">Download Excel file</a>'
            st.markdown(href, unsafe_allow_html=True) 
        
    elif menu_selection == "Aggregated Financials (By Quarter)":
        
        if st.button('Fetch Data'):
            # Display a message while data is being fetched
            with st.spinner('Data is being fetched, please wait!'):
                df = aggregate_financials_by_quarter(companies)
                
                # Once data is fetched, clear the previous message and display a new message
                st.success('Data has been fetched correctly. You can download it now!')

            # Display the DataFrame in the app
            st.write(df)

            # Generate download link for Excel file
            to_download = to_excel(df)
            b64 = base64.b64encode(to_download).decode()
            href = f'<a href="data:application/octet-stream;base64,{b64}" download="aggregated_financials_by_quarter.xlsx">Download Excel file</a>'
            st.markdown(href, unsafe_allow_html=True) 

if __name__ == "__main__":
    main()
