import re
import glob

#if re.search('^4.5', casadef.casa_version) == None:
# sys.exit('ERROR: PLEASE USE THE SAME VERSION OF CASA THAT YOU USED FOR GENERATING THE SCRIPT: 4.5')


thesteps = []
step_title = {0: 'Run a split to make Calibrated into source file',
              1: 'Image continuum of both sources W51e2 and W51n',
              2: 'Image line SiO - W51e2 no contsub',
              3: 'Image line CH3CN v8=1 - W51e2 with contsub',
              4: 'Image line CH3CN K=3 - W51e2 no contsub',
              5: 'Image line CH3CN K=8 - W51e2 no contsub',
              6: 'Image line C18O - W51e2 no contsub',
              7: 'Image line 34SO2 - W51e2 no contsub',
              8: 'Image line 13CH3CN K=4 - W51e2 no contsub',
              9: 'Image line H2CO - W51e2 no contsub',
              10: 'Image line H30alpha - W51e2 no contsub',
              11: 'Image line SO2 at 234.18705 GHz - W51e2 no contsub',
              12: 'Image line SiO - W51n no contsub',
              13: 'Image line CH3CN v8=1 - W51n with contsub',
              14: 'Image line CH3CN K=3 - W51n no contsub',
              15: 'Image line CH3CN K=8 - W51n no contsub',
              16: 'Image line C18O - W51n no contsub',
              17: 'Image line 34SO2 - W51n no contsub',
              18: 'Image line 13CH3CN K=4 - W51n no contsub',
              19: 'Image line H2CO - W51n no contsub',
              20: 'Image line H30alpha - W51n no contsub',
              21: 'Image line SO2 at 234.18705 GHz - w51n no contsub',
              22: 'Generate fits files of any *.image in the directory',
              99: 'test of UV contsub and image test - w51e2 CH3CN K=8',
              999:'test uvrange limited - w51e2 CH3CN K=8',
              9999: 'test multiscale cleann - w51e2 CH3CN K=8'}

try:
  print 'List of steps to be executed ...', mysteps
  thesteps = mysteps
except:
  print 'global variable mysteps not set.'
if (thesteps==[]):
  thesteps = range(0,len(step_title))
  print 'Executing all steps: ', thesteps


# below are list of visual line detections using plotms
# the PI should throughly check the ranges select to have line and used for contsub
# both channel averaging and with and without baseline averaging is
# use to identify the lines

# targetted lines accoring to SPW and proposal (freq in GHz)
# spw 0 - SiO 5-4 - 217.10498
# spw 1 - CH3CN v8=1 - Array of line for J and K and F transitions
# Use a rest of 12(7)-11(7) i=1 221.26513
# spw 2 - CH3CN v=0 
# K=8 220.53932, K=7 220.59442, K=6 220.59442, K=5 220.64108, 
# K=4 220.67929, K=3 220.70902, K=2 220.73026, K=1 220.74301
# K=0 220.74726
# spw 3 - C18O 2-1 - 219.56036
# spw 4 - CH3CN v=0 K    (match with spw 2)
# spw 5 - 34SO2 - 233.29640
# spw 6 - 13CH3CN
# K=7 232.02061, K=6 232.07720, K=5 232.12512, K=4 232.16436,
#  K=3 232.19489, K=2 232.21671, K=1 232.22980, K=0 232.23417
# spw 7 - H2CO - 232.86122
# spw 8 - H30alpha - 231.90093 
# spw 9 - Various -


# W51e2 - VLSR = 57.0 km/s
# W51n - VLSR = 60.0 km/s

##########
# W51e2
# spw 0 - Various lines are present
# Hard to quantify line free, shortest BL <150m has some 'line-free'
# that is coincident with emission for the next consecutively longer BLs (plot uvrange < 230m
# max scale ~1.1 arcsec) also the source has absorption present -- NO CONTSUB
#
# spw 1 - again strong line emission <230 m 
# some channels appear free -but also absorption -- NO CONTSUB
# 
# spw 2,4 - these are paired for the CH3CN Ladder
# Detected well, some line free ranges BUT there is absorption
#- possibly 13CO that is shifted? 
# image the K=3 and K=8 in spw 2 and 4 respectively-- NO CONTSUB
#
# spw 3 - lots of lines and also absorption like dips again - unclear if C18O detected
# possible line free region at least to use for continuum -- NO CONTSUB
#
# spw 5 - line rich, no clear line free areas in shortest 3 baselines <230m
# also absorption of some lines
# not clear that the targetted 34SO2 is detected but - NO CONTSUB
#
# spw 6 -13CH3CN - lines are detected
# again there is absorption it would appear
# image K=4, appears to be present and 'clean'  line
# although methyl formate is close in frequency. - NO CONTSUB
#
# spw 7 - H2CO - possible detect, there is a line ~ at the correct frequency
# there is a clear detection of CH3OH lines in the region
# there is again absorption but also some line free that can be used for the continuum
# - NO CONTSUB
#
# spw 8 - H30alpha
# line appears at correct shifted frequency
# also line rich in the region and aparent absoption again - NO CONTSUB
#
# spw 9 - Various
# also quite line rich region
# some line free channels maybe used for continuum
# also appears to be absorption again so avoid uvcont sub
# image the SO2 line at 234.18705
# note also a methyl formate line maybe detect close at 234.17742
#
# Line free channels (approx)
# 0:88~92;167~170;285~295;525~530;814~817;872~875;943~947;1085~1090;1470~1478;1845~1850
# 1:20~30;188~200;380~420
# 2 and 4 - not clear (grouped due to all CH3CN ladder)
# 3:20~30;80~87;300~320 
# 5 not clear
# 6 not clear
# 7:52~64;226~238;300~320
# 8 not clear 
# 9:105~107;150~170;492~497;550~580;600~610;1257~1263
#############


#############
# W51n
# spw 0 - SiO
# detection of the line, complex region again lots of lines - NO CONTSUB
# 
# spw 1 - line rich, image a selected frequency for CH3CN v8=1 line although
# the 221.26513 line doesnt seem strong - if detected in plotms
# also some line free channels too - TRY CONTSUB
# 
# spw 2/4 - CH3CN ladder, good detections
# 13CO also seems to be mainly in emission here and could be imaged
# but is some absorption again - NO CONTSUB
#
# spw 3 - C18O possible detection
# absorption again - NO CONTSUB
#
# spw 5 - line rich, strong lines around 223.2 GHz (rest)
# not clear if the 34SO2 is detected in this spectram, also abs present again
# NO CONTSUB
# 
# spw 6 - lots of lines
# 13CH3CN detected, may also be may methyl formate lines
# as source 1, image K=4 line - absorption present  - NO CONTSUB
#
# spw 7 - strong lines, some in absorption at longer BL
# H2CO possible detection, maybe also a few line free regions apparent for continuum image  -- NO CONTSUB
#
# spw 8 - H30alpha appears braod but also other lines covering similar frequency
# again absoprtion - NO CONTSUB
#
# spw 9 - very line rich, also absorption on longer BL
# as source 1, image an SO2 line (shift suggests it maybe the methyl formate frequency)
# estimate some line free channels for continuum
#
# Line free ranges for continuum (approx)
# 0:815~820;880~890;900~910;1465~1500;1640~1650
# 1:18~24;395~415
# 2:100~105;239~242
# 4: not clear
# 3:461~468
# 5 no clear free channels
# 6:191~195;403~409  
# 7:305~315
# 8 no clear line free
# 9:315~320;395~400;700~708;790~796;1380~1385;1560~1565;1725~1732


visname='calibrated.ms'

#split calibrated into source fields only
mystep = 0
if(mystep in thesteps):
  casalog.post('Step '+str(mystep)+' '+step_title[mystep],'INFO')
  print 'Step ', mystep, step_title[mystep]

# split out the sources so imaging deals with a smaller file
  split(vis=visname, outputvis='w51e2_w51n.ms', datacolumn='data', field='3,4')

visname='w51e2_w51n.ms'
# Fields are:  0 -> w51e2  1 -> w51n  

# spw maps due to 2 EB
# 0  1  2  3  4  5  6  7  8  9
# 10 11 12 13 14 15 16 17 18 19

souname1 = 'W51e2'
souname2 = 'W51n'
cell='0.005arcsec'
imagesize=5120
spwcont1='0:88~92;167~170;285~295;525~530;814~817;872~875;943~947;1085~1090;1470~1478;1845~1850,1:20~30;188~200;380~420,3:20~30;80~87;300~320,7:52~64;226~238;300~320,9:105~107;150~170;492~497;550~580;600~610;1257~1263,10:88~92;167~170;285~295;525~530;814~817;872~875;943~947;1085~1090;1470~1478;1845~1850,11:20~30;188~200;380~420,13:20~30;80~87;300~320,17:52~64;226~238;300~320,19:105~107;150~170;492~497;550~580;600~610;1257~1263'


spwcont2='0:815~820;880~890;900~910;1465~1500;1640~1650,1:18~24;395~415,2:100~105;239~242,3:461~468,6:191~195;403~409,7:305~315,9:315~320;395~400;700~708;790~796;1380~1385;1560~1565;1725~1732,10:815~820;880~890;900~910;1465~1500;1640~1650,11:18~24;395~415,12:100~105;239~242,13:461~468,6:191~195;403~409,17:305~315,19:315~320;395~400;700~708;790~796;1380~1385;1560~1565;1725~1732' 

# Image continuum of the target source 1 and source 2
mystep = 1
if(mystep in thesteps):
  casalog.post('Step '+str(mystep)+' '+step_title[mystep],'INFO')
  print 'Step ', mystep, step_title[mystep]

  os.system('rm -rf '+souname1+'.cont*')
  os.system('rm -rf '+souname2+'.cont*')

  clean(vis=visname,
    spw = spwcont1,
    imagename = souname1+'.cont',
    field='0',
    cell=cell,
    imsize=imagesize,
    outframe='LSRK',
    niter=10000,  
    interactive=False,
    threshold='0.3mJy',  ## measured noise ~0.3mJy
    pbcor=False,
    weighting='briggs',
    robust=0.5,
    mode = 'mfs',
    mask= ['box[[2076pix,2301pix],[2954pix,3102pix]]','box[[2421pix,933pix],[3099pix,1590pix]]'])  ## 2 boxes as a list


  clean(vis=visname,
    spw = spwcont2,
    imagename = souname2+'.cont',
    field='1',
    cell=cell,
    imsize=imagesize,
    outframe='LSRK',
    niter=10000,  
    interactive=False,
    threshold='0.1mJy',  
    pbcor=False,
    weighting='briggs',
    robust=0.5,
    mode = 'mfs',
    mask = 'box[[2191pix,2254pix],[3947pix,3154pix]]')



  
## 
## continuum in both regions is strong
## due to absorption in the spectra then uvcontsub has not being undertaken
## see in each channel the continuum is still strong 
## and there is absorption at high resolution
## noise levels in the read_me file
## but all 0.8 km/s channels are <2 mJy/beam/channel
