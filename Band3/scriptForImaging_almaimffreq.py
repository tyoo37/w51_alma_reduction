########################################
# Check CASA version

import os
import re
import sys
#import casadef

#if casadef.casa_version < '4.4.0':
#    sys.exit("Please use CASA version greater than or equal to 4.4.0 with this script")

finalvis = 'calibrated_final.ms'

# Requested spectral-window sets
spwset_wide = '2,14,6,18,10,3,15,7,19,11'
spwset_narrow = '3,15,7,19,11'

# Width mapping consistent with original script:
# spw 0,4,8,12,16 -> 256, all others -> 128
# All selected spws here are in the 128 group.
width_wide = [128, 128, 128, 128, 128, 128, 128, 128, 128, 128]
width_narrow = [128, 128, 128, 128, 128]

# Output measurement sets
contvis_wide_all = 'calibrated_final_spw2_14_6_18_10_3_15_7_19_11_all.ms'
contvis_wide_linefree = 'calibrated_final_spw2_14_6_18_10_3_15_7_19_11_linefree.ms'
contvis_narrow_all = 'calibrated_final_spw3_15_7_19_11_all.ms'
contvis_narrow_linefree = 'calibrated_final_spw3_15_7_19_11_linefree.ms'

# Existing line-channel flags to remove line emission from continuum
flagchannels = '0:62~76;180~192;219~247;317~334;366~390;465~480;512~519;548~555;572~580;605~617;649~669;795~806;812~826;925~931;948~960;1125~1132;1209~1239;1250~1259;1345~1380;1398~1420;1453~1467;1479~1497;1558~1573;1596~1612;1716~1739;1796~1816;1847~1885;2063~2078;2442~2606;2793~2813;2928~2936;3105~3122;3203~3223;3261~3285;3663~3698;3770~3787,1:85~96;146~180;196~211;380~413;560~577;887~897;911~922;946~954;961~970;1213~1232;1414~1435;1490~1521;1665~1675;1686~1693;1740~1749,2:268~283;369~382;393~401;675~695;728~740;880~906;971~999;1135~1159;1233~1254;1311~1343;1384~1443;1455~1479;1504~1524;1695~1708;1722~1807,3:0~8;138~183;229~280;312~347;430~444;466~485;520~536;544~560;672~692;719~738;819~831;984~995;1029~1050;1184~1213;1251~1292;1426~1472;1581~1592;1608~1621;1651~1666;1678~1692,4:62~77;135~153;176~192;238~246;366~386;607~618;650~668;793~811;1211~1237;1355~1385;1401~1417;1454~1467;1481~1500;1563~1574;1597~1612;1718~1736;1795~1815;1848~1885;2040~2083;2459~2605;2795~2808;3204~3232;3257~3287;3582~3595;3665~3697;3765~3787,5:81~93;147~174;197~206;379~411;561~576;848~863;882~893;909~921;943~975;1216~1233;1419~1432;1496~1519;1665~1697,6:269~292;347~417;675~695;728~741;874~905;976~1004;1130~1156;1237~1247;1315~1342;1376~1413;1424~1440;1462~1475;1508~1521;1697~1711;1720~1804,7:0~10;149~181;234~251;262~274;429~439;519~530;676~694;716~740;822~835;982~992;1029~1051;1180~1208;1254~1292;1428~1472;1611~1620;1651~1667;1677~1692,8:61~84;177~195;218~250;366~392;543~561;601~616;644~665;794~807;946~963;1209~1239;1351~1381;1399~1415;1450~1465;1483~1496;1564~1578;1593~1611;1714~1734;1800~1812;1843~1881;2061~2078;2441~2605;2789~2814;3187~3218;3249~3292;3657~3698;3754~3787,9:85~95;147~179;196~213;377~416;560~574;880~979;1220~1235;1413~1432;1492~1521;1669~1696,10:272~283;367~381;396~417;667~703;727~739;875~912;971~1000;1130~1161;1227~1254;1274~1291;1314~1337;1379~1480;1511~1522;1724~1808,11:0~12;137~182;231~282;314~350;520~534;666~739;982~998;1030~1050;1253~1292;1425~1477;1605~1629;1653~1665;1681~1693,12:55~81;172~197;236~246;360~392;608~618;650~664;1213~1246;1357~1415;1449~1497;1719~1735;1801~1816;1848~1888;2057~2083;2470~2600;2790~2816;3204~3294;3658~3704;3763~3792,13:79~94;144~180;197~213;374~413;562~574;885~953;1220~1230;1414~1432;1492~1523;1663~1697,14:269~292;371~409;669~695;875~891;982~996;1127~1162;1305~1350;1371~1484;1720~1807,15:0~9;139~192;230~277;519~528;670~693;718~730;1008~1052;1256~1294;1420~1468;1603~1625;1649~1666,16:62~80;176~195;366~392;607~621;644~663;799~807;1214~1235;1357~1383;1400~1415;1498~1502;1593~1619;1714~1736;1793~1816;1846~1891;2064~2083;2451~2605;2789~2816;3202~3222;3261~3286;3666~3697;3760~3800,17:79~94;155~178;197~208;348~421;562~577;879~973;1217~1233;1416~1433;1490~1521;1668~1696,18:268~283;367~404;674~695;878~908;978~999;1131~1160;1236~1247;1307~1336;1372~1443;1461~1479;1503~1521;1697~1809,19:0~13;130~187;231~283;672~689;722~735;980~999;1031~1058;1254~1297;1425~1471;1605~1624;1647~1666;1681~1693'

# Save current flags once
if not os.path.exists(finalvis + '.flagversions/before_cont_flags.flagcmd'):
    flagmanager(vis=finalvis, mode='save', versionname='before_cont_flags')

lockfile = finalvis + '/table.lock'
if os.path.exists(lockfile):
    os.system('rm -f ' + lockfile)
    print('Removed lockfile: ' + lockfile)

initweights(vis=finalvis, wtmode='weight', dowtsp=True)

def build_cont_ms(outputvis, spwsel, widthsel, linefree=False):
    if not os.path.exists(outputvis):
        if linefree:
            flagdata(
                vis=finalvis,
                mode='manual',
                spw=flagchannels,
                flagbackup=False
            )

        split(
            vis=finalvis,
            spw=spwsel,
            outputvis=outputvis,
            width=widthsel,
            datacolumn='data'
        )

        if linefree:
            flagmanager(vis=finalvis, mode='restore', versionname='before_cont_flags')

# Build 4 continuum MS products
build_cont_ms(contvis_wide_all, spwset_wide, width_wide, linefree=False)
build_cont_ms(contvis_wide_linefree, spwset_wide, width_wide, linefree=True)
build_cont_ms(contvis_narrow_all, spwset_narrow, width_narrow, linefree=False)
build_cont_ms(contvis_narrow_linefree, spwset_narrow, width_narrow, linefree=True)

# Quick checks
plotms(vis=contvis_wide_all, xaxis='freq', yaxis='amp', field='4')
plotms(vis=contvis_wide_linefree, xaxis='freq', yaxis='amp', field='4')
plotms(vis=contvis_narrow_all, xaxis='freq', yaxis='amp', field='4')
plotms(vis=contvis_narrow_linefree, xaxis='freq', yaxis='amp', field='4')

#############################################
# Image the continuum products

cell = '0.005arcsec'
imsize = [14700, 14700]
weighting = 'briggs'
robust = 0
niter = 1000
threshold = '0.0mJy'
field = '4'
gridder = 'standard'

def remove_old_mtmfs_products(imagename):
    old_exts = [
        '.image', '.image.tt0', '.image.tt1',
        '.image.pbcor', '.image.tt0.pbcor', '.image.tt1.pbcor',
        '.model', '.model.tt0', '.model.tt1',
        '.mask',
        '.psf', '.psf.tt0', '.psf.tt1',
        '.residual', '.residual.tt0', '.residual.tt1',
        '.pb',
        '.sumwt',
        '.alpha',
        '.alpha.error',
        '.flux',
    ]

    for ext in old_exts:
        path = imagename + ext
        if os.path.exists(path):
            os.system('rm -rf ' + path)

def clean_continuum(visname, imagename):
    if not os.path.exists(imagename + '.image.tt0.pbcor'):
        remove_old_mtmfs_products(imagename)

    

        tclean(
            vis=visname,
            imagename=imagename,
            field=field,
            specmode='mfs',
            deconvolver='mtmfs',
            nterms=2,
            imsize=imsize,
            cell=cell,
            weighting=weighting,
            robust=robust,
            niter=niter,
            threshold=threshold,
            interactive=False,
            gridder=gridder,
            pbcor=True,
            mask='cleanmask_e2.crtf'
        )

# Image all 4 products
clean_continuum(
    contvis_wide_all,
    'w51e2_spw2_14_6_18_10_3_15_7_19_11_all.mfs.I.manual'
)

clean_continuum(
    contvis_wide_linefree,
    'w51e2_spw2_14_6_18_10_3_15_7_19_11_linefree.mfs.I.manual'
)

clean_continuum(
    contvis_narrow_all,
    'w51e2_spw3_15_7_19_11_all.mfs.I.manual'
)

clean_continuum(
    contvis_narrow_linefree,
    'w51e2_spw3_15_7_19_11_linefree.mfs.I.manual'
)