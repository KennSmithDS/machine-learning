from sequence_preprocessing import *
import joblib
model_cols = ['gc_content','molecular_weight','aromaticity','instability_index','amino_acid_A','amino_acid_C','amino_acid_D',
'amino_acid_E','amino_acid_F','amino_acid_G','amino_acid_H','amino_acid_I','amino_acid_K','amino_acid_L','amino_acid_M','amino_acid_N',
'amino_acid_P','amino_acid_Q','amino_acid_R','amino_acid_S','amino_acid_T','amino_acid_V','amino_acid_W','amino_acid_Y']

# TN
BT006808_1 = "ATGGCCCTGTGGATGCGCCTCCTGCCCCTGCTGGCGCTGCTGGCCCTCTGGGGACCTGACCCAGCCGCAGCCTTTGTGAACCAACACCTGTGCGGCTCACACCTGGTGGAAGCTCTCTACCTAGTGTGCGGGGAACGAGGCTTCTTCTACACACCCAAGACCCGCCGGGAGGCAGAGGACCTGCAGGTGGGGCAGGTGGAGCTGGGCGGGGGCCCTGGTGCAGGCAGCCTGCAGCCCTTGGCCCTGGAGGGGTCCCTGCAGAAGCGTGGCATTGTGGAACAATGCTGTACCAGCATCTGCTCCCTCTACCAGCTGGAGAACTACTGCAACTAG$ATGGCCCTGTGGATGCGCCTCCTGCCCCTGCTGGCGCTGCTGGCCCTCTGGGGACCTGACCCAGCCGCAGCCTTTGTGAACCAACACCTGTGCGGCTCACACCTGGTGGAAGCTCTCTACCTAGTGTGCGGGGAACGAGGCTTCTTCTACACACCCAAGACCCGCCGGGAGGCAGAGGACCTGCAGGTGGGGCAGGTGGAGCTGGGCGGGGGCCCTGGTGCAGGCAGCCTGCAGCCCTTGGCCCTGGAGGGGTCCCTGCAGAAGCGTGGCATTGTGGAACAATGCTGTACCAGCATCTGCTCCCTCTACCAGCTGGAGAACTACTGCAACTAG"

# TN
trichoderma_test = 'MCNYTSMPACCRWHPIAACSAGAVQPVRLSRLARPTTSTVSPWEAYNSYASTYQGPAAFRFMVWLLSRLSVQLIFELLYNFSLFHNDVRRRTSKRILSGGYDYTYDMNIEEASKLSPKDIQYVVENIFLPPKLPQNGDDASIVSHEASMLAIVADALQEFSTTIQQSDRIAIDGAAKAVQRFRKIVDGSGFLNEDMLREGFGDLEKNGGFLLLHVRAQNAGIVITCDKDTAVFEPFELSPENERVMAISGRLKRSFPASSTALSLEVFNQEQCQAGLANTIATMSHQEVSEMKPKITKAGNQHIEERDTTTPAIVTDFLVAGLSAIGRPSQGSRIWKNTREEVLWSGAYSPWRRSPVWLLVRVAIQLYLSRLASNKGLYKEFMVFLMAYILQCCEGHDLPSDIFHCMMAKISKRLIKIDQNQAYPWIGTVERVLRNCQSRNEERWNVIMRKNETPVDIHPLSANETSQGRFVTCQTLDEFLEQIYSRQVIEADKDFTPPWILSKNDKDYLPSLEAVSPNDHSTIPFYLSAFETWIESSLYTWLDSHILRQDTCEMLYNSTKAYHHLALSQYHEDPESLSIMLLVIMELWVACDKAATQHHPLILNYRSEMPHELLQSLILPLRGQMERLKTVEDYLEERRARAYFSYPSIFHSFGHMHSFSVQYFQSSPAHKTLLQDIEQEAESVRQRKKDEFSRLKNEYENWMNLYNGTSHDFEDVVDWKTGVSNSEHSSSCTKCIYLNRAEKLHIDIYEWPLPEKKLDAQSTVFELRVPKCFNDWRNMSSFCRVDVLGSLYGSGSQPADWTLGSYLTSYYDNIARTIILASTTKPNAHTHRKTKLVKTAVLQDVLVANGMRYEYYDTEQRCYISGVHCTDEVPKMCTYTLSQQCASLQDFIFRPHNEPNGLTPNHVISRQSMCPDHLSLEEFKAMASIPVGYRVGWKNILVSLHTPALDFRKLDTVLILLQTSRQAGPPLPESALRGSHQDLDDENFAATLLKGLRLAVARISENWESFQALYAFISLATRLLSWAPCLAISRDCVSFIGDCRKVALVWLRSLQDRVKEAQDETQRIELIERVFQVALVCMSSFHVDDAHLRQIVKTPEEACIMIESSIAIQSTMQFAMKPEDAFYRSATNRWHQCMHQAHQLYIEEIRCGRSSWLDEAIANTWSTYPGGREWTTLSTAADHWLVTRTVAANRLGSLNVYFNLLTAELLVNGLPLSRLPAEYERHQSYETYFGRSMVEVMPTEMPGMQFSSKGAYHDCKIYLGLSGPENQDLLLVAVRAGDMEQEETFDLIPPRVFDQILPRHFIDDYSHWYRRRTGEIEFRPKSSPWDLPSEYWRMRKLELSLNSGWVMEKSGQFLLGLTDVAVQRLHKLLAPLENSDYIHVIANSDSNRVDIELPRFQLEFWYNQGSDKIYSRQFRDMHIDSCQNIDALIGLESKLVLTDGLQRRKLLLPSGKAKWHDSEGHIRVFIPYGISEKVHFYDVDTLLGRIVDNGSLQSKLIICYLHALTSYCLPDPLTRMTGTETALTILNSGAVRSFQCLSEENLERLDCIAKLSPIRHYYPDYLRVMESTSWDPCLSSLSQHIGFHRSVQSILCQSASFKFFYPGTYIGPPVLDRVDPLLEERQVIRSSCFHLFGFGAEDYTCSKDVPYHGRDRLSLSDRCNRSFKIAKSLFTMKANLFEAIPSNFADTLWPYLSKSDSMPGPDTPLPDSLISYDAKWLEDASPLLSSHWCQLYHALGRKQNEMNTIQAMFCLAAMGYSESCNLQVIQILVACAIMSPVGGITVPDSQSYQLSDGHKAASDWLQTVARCNAKPFSDSPDSHMSPYNRESTSSLRNRRYQNFHQNLDAAVMDFSSSLQSQWICQNPQNPSSYTILTYIYYERAMETVRKRWISWLSNSRLYDHFVEIVDVLRRYSIAAIDWDPPIETPLIPMQSAKRRFFNDCHLFEIFDPVLPQPVIQGTNLELLSYTADRPKNYSNGAALVERLQRDTARHNHQSNYVSDLEKSFEKLSLQDHQYFIKTSGDDLVDELDRNLQRCKEDADRVYHALATAMRPSTGNAPDTEATLAISLFMAPRVSPAFFLRQLASPWWNEISDQWKQAIVDYGLALSRLQRAKRMRYLHDNQDDLMKELLNVGHRNWQPLDYPKSLLLEIESDILIRENQESVAANMRTPPNDKNVTMQLNMGEGKSSIIVPAIAAHLANGSRLVRVIVTKPQAKELHRILVTKLGGWLGKRVYYMPFSRSLRLTANDTISLDSIYRDCMKSGGVLLAQPEHILSQKLMGIECLISGREEVGRVLLDTQRFLDSNTRDIVDESDENFSVKFELIYTMGAQGPIELSPDRWILIQKVLSLVARIVPQIQKSFPDSIEVNYHAEGCFPKTRILRQDALDSLLNQLSHEICNVGLPSFPVVHQQKSTRDAVLKYISTALLSSEQITSVQQCSCFYTELTKGPLLLLRGLIAEGILGFVFEQKRWRVNYGLAPIRQPATRLAVPYRAKDSPTPRSEFSHVDVVIILTCLSYYYGGLSNDDLFLCFEHLMKLDQAENEYSEWVQFAPSLPESFHRLVGVNIKDRYQVTHHLFPHLRYSKNVIDYFLAHIIFPKEMKEFPEKLSASGWDIGQRKIHPTTGFSGTNDSRNLLPLEIQQLDLDDQLHTNALVLERLLQPENSVVLMLRSKEEAPSGNAFLKFARSLDPPVHVILDVGAQIIELTNIQVAQEWLKIVPAEKEKEAVVFFDDADELCTIDRKGYVEKLQTSPYSCRLDLCLVYLDEAHTRGTDLKLPTGYRAAVTLGPNLTKDRLVQACMRMRKLGQGQSVVFCVPEEIQTKICSATGLSGSNKISVMNVLHWAILETYADTRRNMPLWAMQGQRFERQKAIWGEVNDQKSRQLSLDEAKMLLEVEAQSMEERYSPRLMAHTSPNIPSSSENRAMLEIQARCKQFDCLGSQQSTLLEEQERELSPEMEQERQVQRPHPADPKKHSLHPDVVGFIESGKIPSSSPAFIPAFQTLWNTSAANSFDVKEFPESIVTTLDYKDTVALSGDAPLLDSYQRPVQWILSTTGNHNTVQRLVIISPHEAQELMPSIKTSNHVTLHLYAPRPNLAFSPLDSLTLYPTPLLGRDWQLPSSMRLLLNIFSGQLYFASYADYKETCKMLSIAWQATENGAIVQADGFIPSRARDLDGIFTKSPVKFLKVLLTKIRRDCEGIDKTHWGRIFSGETLRMEDFGTETAG'

# TN
streptomyces_test = 'MSWTWILLATAACFALKLAGLLVPESALDRPAVARVAGVVPVALLAALITTQTFVHQQQLAVDERAVGLAVAGVAVWLRAPFLVVVVTGAAATAGLRWLDLAG'

# FP
aerococcus_test = 'MNWLQSFIQQAEVRHAFKEASVGIEREGHRITPEGQLALTPHPKKVDGSTSSFYIQRDFAESQLELVTPPVYSADHVMEWLQAIHEVAIESLTENERIWPYSMPPALPADDLIEVADLEDPAAVDYRDYLVEVYGKKLQMISGIHFNMQISPAFIQLVHEEAKKVDGNSQSLKDFQSDFYLRLSRNFLRYQWILVYLFGAAPIADDSFFRVPSDKFDHPVRSLRNSRLGYINKDDVTFTYDNLEDYVTQLEANVTEGRLIAEKEFYSNVRLRGANKAQSLLNKGIKYLEFRLIDIQPDAAYGIKASDIEFMKYFILYLVWSCKDANMADVHYGIDLKTKVAEEETFQKTQAMDEGLAILEDMQDMLVAIEADQSVIETTQLMVDRMKDPALTPASQMMTTMKDVDGYLEAGRQFAEEVYESAWAKPYALGGFEDMELSTQILMFDAIQEGYQMDILDRNDQMLRLKYKTHKEIVKNANITSKDPYIGHYVMENKVVTKALLAEHGIHVPKSLEFNQFGEAMKVAALYQDKAFVIKPKSTNMGIGISIFKKGATADEFKAALDIAFKEDHTVLIEDFAFGTEYRFYVQEGEVLSIVNRVGANVIGDGQSTVEDLVADKNKDPKRGRDHRSPLEIIQLGDIEVNTLKQQGLTPSDVVPEGQQVILRENSNISTGGDSIEVLAEMHDSYKEIAVKMAAVLGVNITGLDLMIEDIHQPASADNYALIEANFNPMMMMHIYPAVGEGKRITKDLLSFLFPEKTKFTGGK'

# TN
gordonia_test = 'VTDVDSTASNISLTWGSRPSTLHLIAFSAGVAPSETAYEAVSGPVTFGELYARVSATAGVFIAQGLDTEAAVGAGVTQTEAAPGRAPAEIADATRRAIALIRERALELIGSTDLGSLPGLFRSAVARHADRPAVGDATGAVLSYRELDEQSDALAGGLRAAGAGPGRLVGVALPRRTELIVALLAVLKTGAAYLPLDRSQPVARAQSIIDDAAPLLVLTDAELAATWDVIDVRFVAPGDLPAGAPQGAPGAAATEAFDDRLPAYLIYTSGSTGKPKGVVVSHREVVALMKAAAEEFAFGPEDVWTLFHSYAFDFSVWEIWGPLVTGGRVVVVDQDTTRDPEAFVDLLETERVTVLSQTPSAFYQLIAAQRAKRAALALRYIVFGGEALSFEQVRRWFDDNPADPAQLVNMYGITETTVHVSYRALDRAAVSAGDASFIGRPLSSLDIHILDSRLRPVPEGVIGEMYVTGTQLAQGYLRRAGLSATRFVANPFAPNDSGDRMYRTGDLARRVGDDIEYLGRGDAQVQLRGFRIEYGEIEAALVGLDGISAGAANVVDLPDRGEILAAYVVPEPGVEVDEQLVRRRVATAVPEYMVPDVVMAVERLPLTQNGKLDRSALPRPVLASTTEFVAPENDTETALRDIFAEVLGLEDISVVESVFDVGGNSLLAARIVGRAAETLGVDLTVRDLFDAPTVRDLALAAASKRPGLPPIEPVAARPDRVPLSLAQQRMWFINRFDPSSPAYNIPMVLRLSGSVDAAALREALLDVMTRHEVLRTTYPESDGEAYQLVHEPFAAAAMLDWREVPESALPEVMLGGFDLVAELPVRVGFSRVSDSEAVLGMVVHHISCDGESLAPLVTDLITAYTARVAGNAPEFRPLPVQMADVALWQRRVFGAATDDSSLIGAQLQYWARQLDGAPDVVELPTDRPRPAVASQRGARVEFAVPQHVSERVARLARDRGLTPFMVAHGALAVLLSRLSATEDITVGTPIAGRGQSILDPMVGMFVNTLVLRTGVDLSAGFDRLLDDVRRTDLEAFANADIPFEAVVERVNPMRTEAYAPLSQVWLAFDQSAIADLASQTLTIGEGGGLAVTPVEPHDLSARVDLTVGIADNGDNWQGSVLYATDLYDAETVRLFADRFVRLLDTLTADPAAPVGDADLMTAAEHAVLDRWSGAAALPELAVTVADALAESFARNASRAAIRADGRTLDYAEYGALVHAFAQTLLRRGVGPDVPVAVGVPRSVEMLVAIHGIVLAGGTYVPLDPEAPADVVRRQLALSGASTVVVAGAVPGWAESIGPGGAGSGTLITVDLDALATAEPAPVTDADRSASLRGGHPVYTLFTSGSTGQPKGVTITHRGLHDMLSWFGAYTGDAADERVLVKTPYTFDASVWELFWPFVAGATAVVAAPDGHRDPAHLARVIADERVTSVQFVPSLLAVFLDEAFDPATGLSSVRQIFTGGEALTPAVTQQTLAAAPHAVIVNQYGPTEMTVDATIAALTEPVDVVPVGRPAPGLTARILDRRLRPVAPGVPGELYLGGAQMARGYAAAPALTAQSFIADPAGPAGARLYRTGDLARWRADGDIEYLGRTDFQVKIHGQRIELGETEAVLAAAPGVVSVAAAVSTTPAGDALVAYLTGHPGDTVDVDAVRAFAAERLLAHLRPTLWVVLDEMPRNASGKVDRRALPAPAVTESEVVEPATPAERILAGVVAEVLGVEQVSVVDSFFDLGGNSLAAMRVAARAGAALGVEVSVRDLFDAPSVRELARRVADRVPGLPPVTAVSPRPDQIPLSYAQQRIWFINQFDTASAAYNIPIALRLRGKLDLAALRAAMVDVVERQEVLRTVFPSIDGGPRQVIGDAAGVAAELDWDVVDDESELFAAAAGGFDVTVQRPIRIRVHRVDDLEHIVLIVIHHIAGDGESMRPLVTDVVTAYVARSQGRSPEFAALEVQFADVALWQRRELGSIDDPDSRVSAQVDYWRSALAGLPEVLELPADRPRPTVASMAGAEVGFEIDSATADLVRELAAERGVTEFMVIHAALAVLLSRLSATDDIAIGTPIAGRGDAALDPLVGMFVNTLVLRTVVDPAQRFADLLDAVRVTDLDAFAHADAPFEAVVDALAPSRSEAFAPLTQILLTVDPTPADPSTLVADIDDLAVEVVETEENSAKVDLTVGLRGGRGGSWIGRVNYATDLFDEATVAQMMDRFARLLHELVTDSTVPVGDADLLDTIERDMLTPVGRRPATPAVPLAELFAGAVENAGTDRIAVVDPERTLTYGELDSASNRLARHLLAQGIDRETLVALVIPRSVDLMVAIWAVAKTGAGYVPIDPDYPADRVAHMMSDSGATIGLTLTGVADVAAFGGQWVHLDSPESAEAVAGLSDAPVTDSDRPAPVRTGDTAYVIYTSGSTGLPKGVEVTAGGLRNFGVEAVRRSGITRDSRVLGFASPSFDAFVLEYLLAFTAGAAVVYRDRDAVAGAPLADFMRAHRVTHTFLTPTVLASLDPAELPHLESVWAGGEAVPESLRDRWSRFVAFRNVYGPTETTIVITVAPPTEPGERLHIGPPIDGVDLLVLDARLRPVPVGVAGELYVSGPALARGYLGRRGLTAERFVANPFGRPGERIYRTGDVVRWARHGDGSLSVDYVGRSDDQIKLRGLRIELGEIESALGDHPAVASAVVTGVDSDGALAAGGQSVVSALAAYVVLRADVDIAALREHLADRLPLFMVPASIVALDALPLTPVGKLDRRALPAPTIEIESDHVAAETPVEQQLASIIGGLLGLERVSVGDSFFALGGDSIMSIQVASAARAAGIDVSPRDIFEHKTVRAIARAVGARGARVPALAELPGGGIGPMAVPPVVSWILDHTDEVTDFGDFSQSMVLGAPAGLTVEIAQELLTQVVAVHPMLAAAVESGPDGEWHMRTGVVPLDSGAVTALASPARTGEPGFADTVVAAFEDASRRLDPTAGRLVAAVLVTDPDDDARLVVVIHHLGVDAVSWRVIIEDLLTAWAQHQGGQAYSLRPETTSARAFTAALDAQRAERAGELRYWLERSPEHVTDLGARLDRERDRMSTTDTVVHRVASPVTEALLTTVPTAFRGNVNDALVAALARAVRTWQQDRGIVDDRPVTLLLEGHGRYEEALLHGPDPRAVDLSRTVGWFTTIAPMAIDVRGDSVHTVKVAKEERAGAPDNGIGYGLLRYGGTELSRRPMPSIGFNYLGNVTGTGAAGENTTAGEAGMPFLPDPAAPRLPGTVTGAMVAPNLLSINAGTVVGDAGREFVAEFTFPRGALSAADVDDLARRWDAELATIVEEVARIGDPGLSPSDVLGARVTQDDLDHLARRHPGADVWPLSPLQRGLQFQAELAAAGRAAGAVDVYTAQAVVTLKGQVDADRLADAVREVFARHRVLRSSFVRVPSGEVVAVVPETVDIPWRTVDLDAVSAAGPDGDRGVADVAQVERATPFDLESGPLMRFVLVRSGARSTLVVTSHHILIDGWSSPLIMADLFALYATGQTYTGTVAAESGARGDYLDYLRYIAASDTEAGLAAWRSVLSAVDEPTLVGSGREATSDQLPRDHSVLLPPEITSAVDDLTRARGVTVSTVMQFAWAVLLSRITGQRTVVFGETVSGRPADLDGVETMVGLFINTLPAVADVDPNARAVDVLDALQASKVAVLDHQHLGLPELTALVGRGQLFDTLAVHESYPVDAQSLKQGADAGGIGIEDLDATDSTHYPLNLVTGVVGDRIELKLKYLPAAFDDRQVQVYSDALIRILTGVVADPTVEIGAISLRDDAEYRRAITPPVARTANTDSSLVELFGRSVLAHAGRPAVTDTATTVDYRELDERSAAVAAALQARGVSAGDLVAVATSRDVDLVTSILGVLRCGAGYLPLDTTNPIDRLRFIVSDAAPSAVIIDDTTADVELWSELGSTPVVPVAQLLADGAGADARPVAIHPDSRAYVIYTSGSTGRPKGVEVTHRDVVTLMDTAADDFDVDETDVWTMFHSYAFDFSVWELWGPLLTGGRLVLVDRDRARAPEEFLDLLARERVTVLSQTPSAFYQLAETRRRREAALSLRYIVFGGEALSFEQVRRWFDDHPGESTSLVNMYGITETTVHVSFRPLDPQSVTADDASFIGRPLSSLAIHVLDDRLRPVPEGIVGEMYVTGGQLAQGYLKRAGLSSTRFVASPYGGPGARMYRTGDLARRVGDDIEYLGRGDAQVQLRGYRIEFGEIEAALLAVPGVSAAAARVVDIPGRGEQLIGYLVRTAENAVDTAEVRRIAGRAVPSYMIPDQIVDLETLPLTANGKLDREALPVPDSATVVEDVVAPAGPQETATAQVFAEVLGVDEIGVTTSFFDLGGNSLSATRLASRVADALGTEVSVRDVFEAPSVRDLVAAVSGRGASLPSVVAVSPRPDRIPLSFAQQRLWFINRFEPASSTYNIPIGLRLRGPVDAEALHAAVEDLVVRQAVLRTTFPDVDGVPYQRIHGRDEVDRLDWAIVDSQEHLETAITSGFDVTADWPIRARLWPVAADEFVFVVVVHHIAADGESMKPMLADLITAYGARVSGQEPEYAELEVEFADYALWQHDVFGSAGDPNSLIAAQLDFWTSRLAGTPDVLELPTDRPRPPVASQRGARFDFDIPAPVGDAIERVASERGVTPFMVVHAALTVLLARLSATDDIVVGTPIAGRGKAALDALVGMFVNTLVLRVPVTGEETFDALLDRVRTIDLDAFANADVPFETLVEALNPVRTESFAPLAQVNLTFDQSASADFAIDAEQSGSIGDLDFEPLPPAAPGAKVDLNFAIDRGDDGRRWAGSVIYATDLFDESTIDALTQRLVAVLQSVLAAPSRPVGDVDLVLPAEAVRLQDFEAGPRAEVGAPDTVADLVSAWAAATPDVPAVIYDDRVVDAAEFGARVSLLARELIDAGVGPDAAVGVCLDRSVEIMVAVHAIVAAGGQYVPIDPESPVERSRYILETARVATVVTGPGDTPEALAGFAGRIVRADSTVPLPDAPVPPVTGAERLGVVHPDNAVYTIFTSGSTGRPKGVTVTHGALRNTLAWFSDSNGEGAHRFLMKTPYTFDASVWEFFGPVFNRSAVVVAEPGGHRDPRYLAGLIERHGVTSVKFVPSMLAAFLDGATGAGIEKLATLRRIFSGGEALLPGLATGLATELPDALLVNQYGPTEAVVDITYGAVTDPSAQNIPIGTPVWNSSVHVLDARLRPVPVGVAGELYLGGVQLARGYASRSGLTAETFVADPFGPAGARLYRTGDRGRWNANGELEYLGRNDFQVKLRGQRIELGEIESILGSAPGVVHTAVVVSAPAGGGEQLVAYLAGGPGVTPDLDTVKDLARRGLPQFMVPTTWMVLDQMPLTTSGKVDRRALPTPDVSQREVVAPANDIEAAVAEAFSGLLGVDDIGVTESFFDIGGTSLSAMRLAARVSDVLGVEVSVRDIFDAPTVRELVAGTTERDRALPPVVAVSPRPQRIPLSFAQQRMWFINQFDPTLPTYNIPTVVRLAGDIDVPALQAAIADVVARHDVLHTTFPQDEQGPYQLISDAAEVASRLDFSIVSTAEEFERTITRGFDVSTEWPVRACLWRAEDDTHILGLIAHHIAFDGESRKPLVADLVAAYVARSAGEVPALAPLDVQFADFAIWQHDVLGSADDPESVLGRQLAHWTERLTGLPDVLELPTDHARPAVASARGGRLGFEIPAEVADAVAATARTHGVTPFMVVHAALAVLLARLSATDDIAIATPVAGRGSRVLDPLVGMFVNTLVLRSRIAPEMSVDELLAQVRGTDLDAFTNADIPFETLVEHLDPIRSEAFAPLAQVLLTLGEALPAGPGVLGEDAAAGAAELPGLAITPVEPPEVSAQLDLAVAVSVGAAGQAWSGSVIYALDLFEAGTVAGFADRLVSLLRDMTGAGRDTVAVGDLALVSADDRARVDGWSVGETEVFGSPVIADAVAARIAEDPTQVAIDFEGRRLTYGEFGSRVADLARTLIGLGIGPEVAVGVCIDRSVEMVVAVHAVLAAGGQYVPIDTAAPADRVQYMIETARVAVVLSAGDARPEAIDGLDDGITLVQVDATSAVADTAPVTDADRLAPLRGDHAAYTLFTSGSTGRPKGVTVSHASVMNRLWWGLGEFPWTVGDRIVQKTPYTFDVSVPELFGPLISGATMIVARPGGHTDPDYLVDLISSTRATSVHFVPSMMSIFLDLVPAGRFAEMSALRWVFASGEALPPAVVAKLHALLPQVSVVNLFGPTEAAVEVAVADVSTAPAIIPIGVPVANTSTWVLDARLRPVPAGVPGELYLGGVQLARGYAARADLSAERFVADPFGEPGSRLYRTGDLVRWRADGTLEYLGRTDFQVKLRGQRIELGEIESVIATVEGVVHTAVTVAKAPTGADHLVGYVAPEGVDLDLVKSTVAAELPEYMRPTVWMTLPYITLNSAGKIDRKALPEPEFGVHTEMFVAPATTTEEVLASIVAHLIGIPRVSVTESFFALGGDSIMSIQLASAARAAGVDLSPREIFEHRTIRGMAAAADDDAARLPMLEEASAGTGPVTVSPVVHWMIEHASAPSDFADFVQAAVLRAPDGLDVEQLIELLAAVVDAHPMLTATLAQTEDGWRSTVGNTFDGASAVIEVSSVAAVGTDEFDSDVRTAFGAVSATLDPEAGQLVRAALIRDRDGVGRVLLVIHHLGVDAVSWPILIEDLITGWAQLSEGRDIELRAEQTSARAWTDALAARADSWHEQRDHWLEQLPPRPTPLGVTLDRTRDLMSTERHVSLEIGAPVTRSVLTAVPEAFGGNVSDVLLGAFARAVRSWQSRREITDSAPVTVLTEGHGRYEEVLAAGESPRRADLSRSVGWFTTIVPVRLDPGTDVVHAVKAAKEARLAQPDNGIGFGWLRYGSGTADPDSDTRELATRPLPSISFNYFGAGGGAGAPDAEVLPFTHAPDAPILGSSASGRMVALSTLGVSVTTSLDEQGNRRLVAGASFPGSLFADDEVTDLLDMWAAELAALTQAIGSGTRVGLSPSDVPGTGVTQRDLDDLARTYPGAAVWPLTPLQQGLYFQAQLAASGQESGAVDVYVTQVVLTLGGRVDGDRLRGSAEQLFARHRVMRSAYLRTGSGAVVAVIPERVEIPWRVVRLDSGVTAEDADAEIRRIVEGERLARFDLGRPPLVRFVLVWHDDQAHLVVTNHHILMDGWSGPLVLADLLALYATGETYTGQVAGGEGSQRSDFADHVRRLAAADRDAGLAAWRQVLAPIEGPTLVAPGLEATDDELPRQHRVMLDEETTAGLEELTRTEGVTTATVMQFAWSVLLSRMTGNRVVVFGETVSGRPADLPGVETMVGLFINTLPSVVDVDPAATIVEVLRRLQAAKVAVMDHQHLGLSDLTALAGSAQLFDTLTVHESFPIDTEALSSQDATEGLADGLVVADVDSRSTTHYPINLITAAAGGRVSLQLKYLPAAFGDDQIRVFGEILVHILETVARTPHERTSDIPLVSTVDGLDVAEWSRGHEVQIPGEHTVVDLVADARARAADRPAVLFDDRVVHYDEFAARVSILARELISLGVGPDVAVGVCIDRSVEVMVAVHAIVAAGGQYVPIDTESPVERTQYMIDTADVAMVLIGAERPEALAGVDLPVVVVDASAPVDTAVASVSDADRPVRVLPDHAVYTIFTSGSTGRPKGVTVTHGALRNTLEWFTESNGPGEHVFFLKTPYTFDASVWDYFGGIFAASPVVVAEPGGHRDPVYLARLIERHRVTTAKFVPSMLAAFLDGATGAGDADLSSMRRIFSGGEALSPALAGGLLRLLPELGLYNQYGPTEATVDITYGRVDRPTPNIPIGAPVWNSTVRVLDDRLRPVPPGVPGEMYLGGPQLARGYASRPGLTAETFVADPFDPRGGRLYRTGDRARWNTDGVLEYLGRADFQVKLRGQRIELGEIESVLSSAPGVVHVAVVVATAPSGGEQLVAYVAGRPGEEVDLDLVRGASVRGLPEFMRPTVWMALPEMPRTTSGKVDRRALPRPEFATGDYVAPETPEETAVAEVFAELLQVERVGATDSFFELGGNSLSAMRVSARVGDALGVEVSVRDVFEAPSVRELVAALTGRGSRLAPVVAVSPRPERIPLSFAQTRMWFLNRLHPAAPTHNMTIVLRLSGDLDVEALHTALGDVVRRHEVLRTTFPSAEGVPFQLVHPPESVADRLDWEVVGSEDDIFAVVTRGFDVTEEWPFRTRLWAVEPGEFVLAVVFHHIGADGESMAPLVSDLVSAYSARVAGDEPQFPPFAVQFADYAIWQHTVLGSVDDPDSVVGRQLAYWAGHLAGVPDVLELPSDRPRPPVASGRGARARVEIPAGIGERVTEVARGADVTPFMVLHGAVAVLLARLSATDDIVVSTPIAGRGQAELDPLVGMFVNTLVLRTLVDGAQSFEQLLSAVRDVDLNAFAHADVPFETVVDRLSPVRSEAFAPLAQVMFSFSPSATAAEALGDAAGITVTPYADVMVSSQIDLWITVSSRPAGQTWPVNLDYSTDLFDEPTVLEFGERFIRLLDALTSVPDRAVGDAPFVAEDTTAAIESAEWGERVELPAVQTVSDAVSAQAQRTPDATAIVFGDREVSYAEFVARVNTLARDLIEAGVGPDVAVALCIPRSVEMMVAIHAVIAAGGQYVPVDVAAPADRVRYMYETAGVRVLLVADAEGVRDAVAAADDTGVRVVVVDASALVDVDSSAAAPVSDAERLSPLRPDDAAYTLFTSGSTGRPKGVTLSHAAVLNRLWWGLDALPIGPDDVVMQKTPYTFDCSVPELFAPLSIGARLVVLADGGHLNPRQVADEIARTGTTMIHFVPSMLSVFLEVVGREQLAALDTIRIVSTTGEALPPAVAAPVREIWPDAWFFNLYGPTEAAVEITFERIHSVAADDPTVPIGIPVWNSSAVVLDARLRRVPAGVPGELYLGGVQLARGYAARPDLTSERFVADPYGEPGSRLYRTGDLVRRRPDGVLEYLGRTDFQVKLRGQRIELGEIEAVIASAPGVVHAAATVATAPGGGEHLVGYLAGVPGEHIDLDRVKAVVAEALPGYMRPTVWMPVDDIALNTAGKIDRRALPEPVFTAGEYVAPAGEAEAAVAEVFADILGVDRVSVTDSFFDLGGNSLAAMRLVARVGEVTGTEISIRELFNAPSVRELTRVSSGLDSARAPIVAVESRPERIPLAFAQQRMWFVNQADTTSSAYNLPIVLRLSGALDTDALHAALIDVVSRHESLRTTFPSADGMPYQKINRATSVAAKLDWQEVSSQEEIEAAVSAGFDVSREWPIRARIWEVEPDEHVFAVITHHIASDGQSMTPLVRDVVTAYLAESADTDPEFADLDVQFADFAIWQHEVLGSPEDPESVVGRQLTYWTDRLAGLPDVIELPTDRPRPARASQRGGRVLFGVPASVGDRIAGFAQETGTTPFMVVHAALAALLSRLSATDDIAVGTPIAGRGQRVLDPLVGMFVNTLVLRTTVDRDRGFADLLDAAKDADLAAFANADVPFDVVADAAGAQRSAAFAPFTQVWLTFDQSTLPELAGPDLSIGEVAGLQVSSVTTERIPARVDLLVALSQPAGSEDWSGAITYATDLFDEPSVARLAEQLVTLLTEALAEPEVPLRQISLGEATMSLAELARAATQPEPQRQTVSIADSDAVVTGGPGTEPVVLGDLFAQAAAKWGPRQAVVDADNVWLSYADLDARSNRLARWLIGQGIGPEKLVALAIGRSAQLLTAIWAVAKTGGGYVPIDPDYPAERVANMVEDSGAILGLAVQASGTLPGERFSWRSLDDATLSAEIEALSDAPITSSDRRGPVRVDNVAYVIYTSGSTGRPKGVAVTHSGLANFAAEEIRRSGADEYSRVLGFASPSFDASVLEYLLAIVSGGVLIYRPADAVGGPPLQDLMMRQAITHTFLTPTVLATIEPHAVPALRVVYAGGEAVPQALKDSWAPFRRIQNLYGPTETTIGVTISAPMAVGEPVSLGGPLAGVGLMVLDAQLRPVPVGVAGELYVNGGALSRGYLDRPGLTAEKFVANPHGHPGDRMYRTGDIVRWKQDSTGAPVIEYSGRSDDQVKLRGLRIELGEIEAVLAEHPAVRSAVVVGVGGSVATALAAYVVAAGTGGGAEVDPAELRSFVGERLPAHMVPASVAVLDELPLTPVGKLDKAALPEPVIEVGEIVEPETDEEAAVAAVFAEVLGIDQVSVTESFFDLGGNSLSATRVAARVGEVLGVETSVRDLFEAPTVRALVAEVSGHAEALPPIVARADRPELVPLSFAQQRMWFINQFDPSLPTYNIPFVLQVRGALDIEALRLAIADVVERHEVLRTTFPSVDGVAHQLVHPAEQIADRLDWGIAADQHAFERAVVSGFDVAADWPIRVRVWHVDAERAVVAVVVHHIAADGESMNPLLVDVLTAYDARVSGNEPDFEPLEVQFADYALWQHEVLGDGSDPTSVIGSQLAYWTDKLADLPEVLNLPFDRSRPLVASQRGGRVGAAIPAEIGNRVRDLAREVDATPFIVVHAALAVLLARLSAGEDVAIATPVAGRGQRVLDPLVGMFVNTLVLRAQVDPSMSFAELLEQARDTDLEAFANADVAFEMLVEKLNPVRSEAFAPLAQIMLTFGQTALPEMAETAPAAVAGLEIEPMPPADPPAKLDLTIGVSVPDGDGDWPLSLVFARDLFDEDTVAQLARRFVGLLDQLTRHTDDPVADAALLEPAEIEEILRRSRGTETAIPAGSVADALSFRGARSLDSIALTYADRELTYREFGARVADLARELLGLGVGPDVAVAVCIDRGVDMVVAVHAVTAAGGRYVPIDTAAPGDRVRYMVETAGARVLLVGPRPVAADLSGLDDGVRRVTVDSTRDIDPSTPPVTDAERVRPIRGDDALYTLFTSGSTGRPKGVTVSHAAVANRLWWGLDEYPWTVGDRIIQKTPYTFDVSVPELFAPLLTGATMVIAEPGGHADPLYIVDLIASSGATSVHFVPSMLSVFLDVVPAETISRLGTLRWLFASGEALPPAVVARAHELLPHVQIVNLFGPTEAAVEVAYADVTRAPSIVPIGVPVWNTTTHVLDARLNPVPTGVPGELYLGGDQVARGYAAQPGLSAERFVADPFGRPGSRLYRTGDLVRWNTEGEIEYLGRTDFQVKLRGQRIELGEIESVVAAAPGVVHAAVSVADAPGGGQHLVAYVAPSTVDLEVLRDAVTRALPEYMRPTLWMPIDEVVLNSAGKLDRRALPAPDFAGLDADHVAPANATEEALATIVAGLLGLDRVSVTQSFFALGGDSIMSIQLASAVRAAGFTLTPRDIFEQRTIRAMARVVAGEAHRLPALDEPAGGGRGDLPLLPVMSWMIEHSTHASDFADFSQYRVLHAPADLAVDALSELLSELIAVHPMLSARLTRSDDRWRLVAGSDENAGGPSAAPYVFARSSVAPVGSPGHDADLRAAHAEALTHLDPSAGVLVAAGIVTDADGVGRVVLAIHHLGVDAVSWPILVEDLVTGWAQRASGQPIALRAEATSERAWAHAVGAQADRRATELPYWLERLPARPTDLGIDFDASRDRFATEVSVVHAFDAQVTEAALTSVPEVFRGNANDVLLGTFARAVRAWQAARGIADVAPVTVLVEGHGRKDEIDTADGERAVDLSRTVGWFTTIAPIAVDPSTDVTHAVKSAKEERLGQPDGGLGFGVLRYGADTELSQRPLPSIGFNFFGAGRAGRPAAEPAPDVIPFTGAPGAPGMPPSVSGAMVALNPLSVNVGTRSDGETRRLTANFTFPSALFGTDDITALAELWADELTALAEHVAVVGDPGRSPSDVPGTPVTQTELDALAVRFPGADVWPLTPLQAGLYFQSQMAAQNTAGADGVAPTGSDNVDVYVTQAVLHLGGEVDRARLRSAAEELVAHHRVLRSGYVRTAGGALVAVVPPRVDLPWSEVSLEPDLDGDEAARRVREIADTERIEPFDLAAPPLVRFVSVEHGSGSDTTLSLIVTNHHILLDGWSGPLVLADLLALYAGVGPYTATISADSDFGDHVRRLAAADPAAGLAAWRDVLAPLAEPTLVSGAEEATTTSLPRDHEEWIDAETTAAINRLARERGVTVSTILQFAWAVLLSRMTGNQVVAFGETVSGRPSDLDGVEGMVGLFINTVPSVVDVDPAAPIGDVLAAMQADKVAVLDHQHVGLADLTALAGIGALFDTLTVFESFPVDSDSLSTADTSLAGGLQIVGVDAGDSTHYPLNLASSPSGDRLLLKLKYLPSAFADDQVGVFGAALREILRTTVDDVDSPTSSIALLDAAAAAELTPVNGPAAPEPRLLGEVFADVAAAHAGIVAVTDGDGASLTYAELDERSNRLARWMIGRGIGVDSVVGLALGRTVDRLAGHWALAKLGAAYLSIDPTLPADRIAHMVTDSGVRLVIASASGSPEQGGPGPEAGARGDVEWIDVSAVADAMRGIEGTALAPGELVGTPRLDALAYVIYTSGSTGVPKGVAVTQRGAHAFAVAEAHRFGIDPGSRVLGYASPSFDASVLEWLLASTSGSTLVYRPDDIVGGETLTAFLREHELTHVFLTPSVLATVEPDDLPALRMLASGGEAVSTALVRTWAGRVAFHNAYGPTETSVAVAISGPLDPDEPVTIGGPVAGTGLLVLDQRLSPVPIGMAGELYATGVSSARGYLRRPQLTAERFVASPFGGPGDRMYRTGDRVRWVRSASGELVLEYLGRSDDQVKLRGLRIELGEIENALSTHPSVKTAVVLGVGGSVASSLAAYVVPASDALSTGGETPAVDTAALRDHLADRLPSYMIPATITVLADLPLTATGKLDKRALPAPDIEADDLVAPETAAEARVVAVFADLLGVDAVSVTGDFFALGGNSLSATRLAARVGDALNADIGVRDVFESPTPRALAALGQHRGGLRAPVTRVEPRPAEIPLSFAQQRIWFINRLDPASAAYNLPIGVELGGRLDVEALGAAIGDVVARHEILRTTFPAVDGRPTQVVHDADGPAALPRLVECDSEAELLEALSAGFDVTTEVPVRIRLWQRDEGSWVLLAVLHHIVGDGESMRPLMSDVVTAYRDRAASRAPDLPPLPVQFADYALWQQRELGAVDDPTSVVGRQLSYWLRQLAGVPDVLELPADRPRPTVASMRGARVDFEIPHEVATRISALARERGMTPFMVVHAGLSVLLARVTATDDIAVATPIAGRGRAEIDQLIGMFVNTLVLRAEVDPAMSFAELLEDTRVVDLDAFTNADVPFETLVERLNPTRSRAFSPLAQVMLTLTNAGNTAPVFEAEGLRVAALESPVTSAQLDLTVAVVARPDRSWSASMVYATDLFDEGTVELLAQRLVTLLDGLTARPDAAVGECPLVTPAERDRVLAWSAGAATRPTGATLPGIVGSRQSGAGEPGVGENGVAGREVGYNGRGGDESRYGDDGSDSGPGGDD'

# TN
phytophthora_test = 'MLTPIQYRDRILYTEATHVSMGSLQSLVLYLVTSLLFLTPTNPIEPAPQAADADTVVNADTSKSIRLDANLLIPDGGELLLNIQVPHEPIQIHPKGPAKVSRVYSDHVDGKLGVGEVINIFVKFTSPVKLSGAGTPYIVLKTGCHATSCHVKEIQRLRCMATKGKFAVGFGSQKVGNIPWDASAKLFAAYLRRMNRINKVNVKYSIDEDRACTFFGNNITITFDSMNIGGTDGDLVELTGDTTNAVGDGVVLGHVMYTPLVTSTAWEIRKGVLVPDRKAFFVAQTAPDTLKFGYTVQKGDNSTRLEYVNSDSLALSLRSIGGVRIVNDDDTNTIANCILPPPGFEGDWERGIGTSLSKSNALEIDVTPPYVTTVTSPHEDGTFGIGEVILVHVHFSQPIVVTGLPTVVLETGAVDRIIPFNQVVAGNIAEFKYIVQAMDTSPDLTYTGTTALQLNGGSIKRKSTTPTTNAVLKLPFNGESGSLSVSKNMVIDTTKPKIVSVTTTAKDGIYTAGDDIPVIITFDTPVVVSGTPQLVLSTGSVDLFPGQFVLEAPTFTSNETVVFPSYYLGLSTQSSKGLQFKIDGQILTVDSVNRDEVTMIEKYAGTKVEPVTLSNRANVPIYSPGYRPAKYSSGSGTKMLTFVYTVQIGDVSNRLAYLSTSALQLGSGSIKRLSTTPFTNADLTLATPGTSGSLSAGAALGINTDAPRVTQVKAVTRDGVYKAGDEIYFEVVFNLPVVVSPTASLVTNIVSAGVERLAIYSDGSGTTSLKFKFDCLEDDQVTVLDVKNVNSLRASYGSILGWIRRKSAAPMLPALLDLPVSGLSSKGISINQGCETVTDVFTSHEEGTYGVGESIDLLVKYFASVSVDTTGGIPTLVTSTGNSAVYQSGTGTQTLVFNYVVQQSDISGRLVYPDRYSLKTNGAVIKGVTSSALSSTLLPSPELSQLKTKDNLFIQTSPPVVVEVSTRTQDRVITVGDTIVVLVSFNYPIYVPPLSVKAGAPTLLLNVGTGSGIASSYVAAEENAAYFSFTVAADQSTSKLSYFGRSALKCTGGNGLNKDPRQSAGPPSAVLFGDVFFTSWAEMSSTTNTRQIRVKSFDLQQFPPLLSFEDGGEVLSIVNLDSTMDATSPELVTFSSKLYLVWVEASTAPNNPTQIRVAVLASRSPVQWAFVDAKPATNFGINKVPTANAAEPHAVVHDSKLYIAWNENPSGVAQIRVAVFNGHDSTPGWTYSDGNQNARGLNYAALQSAQSVRLCSCGSKGSMTNNLYAAWSEISTLSGTAQIRVAVQTGTDSLPNWRFIDGNTATGLNIGTQKIAISPSIQCIGGSSVAVGWQETTGATGSVIFIKKFNGDFTTPQWIRLGGDKGLNFDATQPAQNLKLSVQLLGTTETLFATWDEADSTGTATQIRVAQLLTGANSWKFLDGGAKISVINDDVSHSASRPVLVCKKSRDTTIAAWLETHSNGKNHIRCSVLDASVNEWQPLSQGCILRKATSSVTSANLLLPELNSPGSLDFGHSIRVETSKPKVQSVSLAGDIYSSITSVSTIQTVDIFNVASIKQGDYELVYGDTKTSCISWNAPATGTGSIQSALESMTGLAIKVSATQDTTSFHDGYRYTITFVFPTMGILPLQVKKNPDAKCKKFTCDPTLTRFPCNLDLVQPNQNSDIRATAGVVDAVVRFSFPVVIPIGIPKLSIDTGVTVRDAIYMTRSALQEFDVGINMASSVLGGGFRLSYGDFSSGVGVAPIYTTDCIQLLINDDDGVQEMQSKLEEIALIKTIGIRSVSRRKYRNGYRFTIENRNSGDMLDLVPADSSTCPAIAASTQTIDIKADTEILSGEIKIQLGDTKSGCIPWNVRAKGPSNSMEAIMKYLEGDRIIPVQVVKDPSVYVHGIKYYVRFSNLVDANSPLLAFMDATCATFTCKLAGGATGACTSLSVTSNADFKVTRAESGAISFRYLVQPSDEAISLMYKSTTSLTGTILRSSKNPILAASLTLPPPTALVAQDGVTSMAVVRSDTIPVVTRVYSTTVDDTYTAGDVIIVIAEFSEKVIVEGKPVLELDSKGEAFYTSGSGTNVLKFYYEVKPGEATADLNYASVAALRTFTVPNSKIICALCSGSGIDADTTLPALHSAASLAGNNALVIDTTVPIVTLITSSRPGTAAGGVGYGPGDIVDIMVTFSTDVAVTGTPSLTLNSGGTAKFTYAGYRQLLDIGVNAVVPVTSGQFAVIFDGKVSGCIDFDDASSVAATSLKTRLLEFKAIARIGILSVTMTKKKNGNRFEILFDSTKVVDVPLAIELTVSDMCDPLQPSSAAQETLVSRVTDNQIVFHYTVGVGDTTAVLGVTSTSISLNSGTDSILRQSGSPVIVANVALPISTSPQSLAQTKNLKIDGIPAQISDVISDSAAGTYGVGFPALASPLTVAPGEILLHLVFTRPVVVIGTPAVELATGSLRPSGEFIPNRLAKFINQPQPNHVAFLYHIEPDDYSTNLAFPNVSVLNGANIYCASSTMSVRASLVLPKLTISNGIIKIDAFSVPATVKLASSHEDGEYGAGELIEIQVSFSKQIVLLSGLNRNQDWHARYPVALEFKRNIYIMWTERDDMQAPSKSFLYLRVFSSDTLDVVATTSVSAVNRVPNTFIEKVAMTVWKQNLYAAWDEGGLLYCALFEGIPSINPWTLIPNMGINKNMAMAASDPALLVYNLELVVVWREKALPVGSSALVGQIRVAVLNYDIDAPLWIFHDGNQLDSGLNKNKLMDADDPATVVYRGRMYVSWTEMNKDGAYEIVIARRNIQTRDFSTWTYLDALPSSYPAYSFLSAYKPQFTVRRKGIEDMALLISWYRDTVTSNVSEVITGQVLDLDWEASVTGSIPQTINAAEGNTTVDKVNPNSIEQKFVTCGDNIYSSWLDLEGNNDEDAAYVLKFATLPPGAHIYTGWTSAVNQSNLNHNPKRDAIDSSLVCSTSSNGNPHPGLVWTEYDGYSIKLRFRHYTVVPRTPGTTSTYYGETIAGAPVLMLATQSNPLGYAACIDKSGITTTMLSFTYIVQPGESSPQLEIMGQDALKLNGAVIRDIAGKDPDFTLFPDSANLRSLSYNSKLAINTTPPTVLSVTSKNPSGEYGVGQILEIQVTFSCPVVVIKGDPATPPTLSLRSDELHLLTSSQGIATYAGGSGSSVLTFEYTTGLQDYCEQLDYMDTASLALHGSTWAIKRNATRPTTDAVLTLPPIKSANSLSGSRTIVIKSTQPSVVKVTSSTPDGTYYPGDIVLVDVLFSLPVFVFGFPVLLLETGGNAPTRSSLRSGNGTDKLTFEYGIKVGDKSARLDVVDDRVGDDKAYFVMSLMLEGYAEIKRASTNPFTTAVAALPAPGLTGSLSFSKNIIVDSTPPTIIDIRSPVIDGTYDIGEQIDFLLVFSRQVVVTSIPEVILNVPSEYSRTAVYTDGSGTSILRFSYFPKVGDNSRNLALDILDENSLILRPLLRGKELLQNPAEILCSSSNPVLRADIKLPIPGVAVRSDAVLSLVGNNRKIFVRTDGFRVKAIQADIPSGIYSPGQRIVISVVFTGPTVVQGSPRLKLNSNTAAYAVYIGGTGTSKLRFEYIVATGDSCSVLEAASRGALELNGGVISDTGGIYVPLRLGIPTQPGSLSDDYNIEITSAPPSVLHVYCKDGDGSYGVGDTLHIAVVFSRKVTLSNPPPLLLLQVDVGTRAATYLSGDKTDTLEFTLQILNGDSTALLDYASKNALTGTILALSTTPTTAANLELPVPGAEGSLADSTSIRVISTPPVIMDVRAVSRDGNYGLYDNLRIQIRFSFPVYVSPVASQTCTLTLAVGDVEFRKAIYVGGSTTTKMEFEYIVQNGDRSSRLDYIGANSLHCTILQATAVPSLQASRILPLPGAEGSLSYNSALQIDAFSPRITSVSSGTENGVYGAGQVIDIAITFSEAVLVPSGAKPRLRLAIASNVPVDTLIESSIEPYATYNGGSGSSVLKFVFTVRVGDIALPLEYAGIDALSMTIHSAQLTAVEKIYRFASIRLPVPGATGSLSNNRDIHIDTLETPRVIGVGSLTANGIYTAGDTLTISVTFSTPVTVTGSPPTLLLNTGNPDTQDSAKKAVYVAGSGTSVLLFEYKVQIGDSVDRLEYKPCSLSERNAFIQRKWDKLVRCSSTANALQLGGIGSSIKRSSTVPVTDAVLDLPEVNDWAELRVATTGDNFVYVTQVEPTTGAEKSTLKLLENEFSISHQKAAINIYSNGIPSHDTILHEKIKEQKYFIELQRFPTLQSQILNLSRIPDAFSGIFLNGILFKNSNKRAKSTDDCGGAINADGHYFYVDLPKCYLAAIHEPREPKVSLTGQIKRPMSVVVAYALDGFPIYGYYDEDGELPSDLDECHGHIRRDGQYAYHLIPPETSASPFMPCLRGLASTSQLSVFRYPADISAVEGLPLSELAKFNSFVIDENPATYNADTWLNPESVSVVYTSTTVIVRSNGMPAGTYGPFPNAYNRFSVYEQDYVFQFPRNPVIAATTTSLPRDTPIGVMVNGVPFFAAKSDVYGGIVVDITNSAYILLDKCNGLVDAGGDYRYYASPDCLLHELGDKVGQPSPLIGFAFDGFPLYGPYGENGQMPNALDACNGRVGDDGTYRYHVTLTAPYLLGCFRGTPAIDQKNLYAANDLYRSLSYAHALRINTDRPQVTHVFTNKRPGVYVTGESIDVVVEWSTPVQVIGTPTISILNSSRVATYDATRSSAQQTVFLYVVNRNDVNIEDFSYDAHVAIQLNGGRVARFATIPILDADLDLIPSDLDNIDLIRSRTPGLSSKFQLVRDLRVVLRGLYHPRAHDLRARVFHGNRESIIFDGCCTARDAFGIPDVPDVLTNRAQLASEARNPTSGIGWDYSFSDFNGDKNLALDGGATALQSSTSDTCGPMNAIDGRIRGVDVSTQTVVRTLPAKGVNESAWWELRLVDVATVGTIRIWIADSDPTVAADVFMLRVDSSDGVSTVTGNFTLIFTTQDNKQLETESISYNAVAMIADEKARIISSGIGRGESIQAKLLALGDIVPRLVIKRDPRDASLSRNGAFTWHITFLDNSRAALSVGVNNVSSGTGIVNVGPPLSIDDDSDPIVYRKGEAAEPSASTSVRATEQSMFPFWVLLFDSSAVMDVESFADAYARAIFSYRVDERHANRSVISVVPPLGTKAQYVRVVAELPRGVISIAEVEVFTEQSHVLSQYAGGTPVRTAYHPGSKTWSPEEPFRYTFSGMPSEGSWTLAIEDMAVNGSNLSSPKLNSTAGGMSDWVLYITNQAGETVSYYMDFQAQLHALPRHGTLYVGLDETERDHLDIDRNGLLDSIEADTYLRRYSPNSYSDLSANIRDRELKEFMLSYEEYGAVQVLRDSSERQLRLPSRVCNAECLAAIKLDPYFYVGLEGDKALKLLRVVGDRVVKYVPDAGFRGLDAFTFSVAVTGHESRVLGTIQLTVKECEDAECRMSSFLLHRSTR'

test_virus = Virus()

virus_df = test_virus.build_virus_dataframe('MT705205.fasta', 'nucleotide', 'fasta')
# virus_df = test_virus.build_virus_dataframe(BT006808_1, 'nucleotide', 'text')
# virus_df = test_virus.build_virus_dataframe(phytophthora_test, 'protein', 'text')
# virus_df = test_virus.build_virus_dataframe('db_sample.fasta', 'protein', 'fasta')
# virus_df = test_virus.build_virus_dataframe('covid_sequence_sample.fasta', 'nucleotide', 'fasta')

amino_cols = [col for col in virus_df.columns.tolist() if col.__contains__('amino')]
metric_cols = ['gc_content','molecular_weight','aromaticity','instability_index', 'sequence_length']
print(virus_df.head())
# print(virus_df.columns)

# testing importing ExtraTreesClassifier and running virus class prediction
etc = joblib.load('virus_extra_trees_model.joblib')
virus_df['class'] = etc.predict(virus_df[model_cols])

for prediction in virus_df['class']:
    print(f'The predicted class is {prediction}')

# print(pd.crosstab(virus_df[metric_cols], virus_df['id'], values=metric_cols, aggfun=np.mean()))

# virus_df.set_index('id', inplace=True)
# index_tuples = []
# for ids in virus_df['id'].values:
#     for col in metric_cols:
#         index_tuples.append((ids, col))

t_virus_df = virus_df[metric_cols].T
st_virus_df = t_virus_df.stack().reset_index()
st_virus_df.columns = ['metric','id','value']
# t_virus_df.columns = virus_df['id'].values
print(st_virus_df)
# print(pd.DataFrame(virus_df[metric_cols].T, index=index_tuples))
# print(t_virus_df)