import os


def test_tclean_success():
    # An EXTREMELY HACKY way to test whether tclean succeeded on the previous iteration
    with open(casalog.logfile(), "r") as fh:
        lines = fh.readlines()

    for line in lines[-5:]:
        if 'SEVERE  tclean::::      An error occurred running task tclean.' in line:
            raise ValueError("tclean failed.  See log for detailed error report.\n{0}".format(line))
        if 'SEVERE' in line:
            raise ValueError("SEVERE error message encountered: {0}".format(line))

def check_model_is_populated(msfile):
    casalog.post("Checking for populated model column in "+msfile)
    ms.open(msfile)
    modelphase = ms.getdata(items=['model_phase'])
    if 'model_phase' not in modelphase:
        raise ValueError("model_phase not acquired")
    if modelphase['model_phase'].shape == (0,):
        raise ValueError("Model phase column was not populated")
    if np.all(modelphase['model_phase'] == 0):
        raise ValueError("Phase is zero.")
    ms.close()


# Set the ms and continuum image name.
contvis = 'calibrated_final_cont.ms'

print("field", field)
print("cleanmask", cleanmask)
print("cleanmask2", cleanmask2)
print("startmodel", startmodel)


# Set the ms and continuum image name.
#contvis = 'calibrated_final_cont_'+field+'selfcal_startmod.ms'
contvis = 'calibrated_final_cont_spw9_19_linefree.ms'
#spwcont1='0:88~92;167~170;285~295;525~530;814~817;872~875;943~947;1085~1090;1470~1478;1845~1850,1:20~30;188~200;380~420,3:20~30;80~87;300~320,7:52~64;226~238;300~320,9:105~107;150~170;492~497;550~580;600~610;1257~1263,10:88~92;167~170;285~295;525~530;814~817;872~875;943~947;1085~1090;1470~1478;1845~1850,11:20~30;188~200;380~420,13:20~30;80~87;300~320,17:52~64;226~238;300~320,19:105~107;150~170;492~497;550~580;600~610;1257~1263'
if not os.path.exists(contvis):
    split(vis='calibrated.ms',
      outputvis=contvis,
      field=field,
      spw='9:105~107;150~170;492~497;550~580;600~610;1257~1263,19:105~107;150~170;492~497;550~580;600~610;1257~1263',
      datacolumn='data')
else:
    clearcal(contvis)


# beamsize: Beam : 0.0669461 arcsec, 0.0421181 arcsec, -44.3619 deg
# >>> 0.0421181 / 0.007 / 2**0.5
# 4.254570588670446
selfcalpars = {0: {'imaging': {'threshold': '0.2mJy', 'nterms': 2, 'robust': 0, 'weighting':'briggs',
                               'mask': cleanmask2,
                            'cell':'0.004arcsec', 'imsize':14500, 'scales':[0,6,18], 'niter':200000},
                'calibration': {'calmode': 'p', 'gaintype': 'T', 'solint': 'inf', 'solnorm': True},},
               1: {'imaging': {'threshold': '0.2mJy', 'nterms': 2, 'robust': 0,
                               'weighting':'briggs', 'cell':'0.004arcsec',
                               'mask': cleanmask2,
                               'imsize':14500, 'scales':[0,6,18],
                               'niter':200000},
                   'calibration': {'calmode': 'p', 'gaintype': 'T', 'solint': 'inf', 'solnorm': True},},
               2: {'imaging': {'threshold': '0.15mJy', 'nterms': 2, 'robust': 0,
                               'weighting':'briggs', 'cell':'0.004arcsec',
                               'imsize':14500, 'scales':[0,6,18],
                               'mask': cleanmask2,
                               'niter':200000},
                   'calibration': {'calmode': 'p', 'gaintype': 'T', 'solint': 'inf', 'solnorm': True},},
               3: {'imaging': {'threshold': '0.15mJy', 'nterms': 2, 'robust': 0,
                               'weighting':'briggs', 'cell':'0.004arcsec',
                               'imsize':14500, 'scales':[0,6,18],
                               'mask': cleanmask,
                               'niter':200000},
                   'calibration': {'calmode': 'p', 'gaintype': 'T',
                                   'solint': 'inf', 'solnorm': True},},
               4: {'imaging': {'threshold': '0.15mJy', 'nterms': 2, 'robust': 0,
                               'weighting':'briggs', 'cell':'0.004arcsec',
                               'imsize':14500, 'scales':[0,6,18],
                               'mask': cleanmask,
                               'niter':200000},
                   'calibration': {'calmode': 'p', 'gaintype': 'T',
                                   'solint': 'inf', 'solnorm': True},},
               5: {'imaging': {'threshold': '0.15mJy', 'nterms': 2, 'robust': 0,
                               'weighting':'briggs', 'cell':'0.004arcsec',
                               'imsize':14500, 'scales':[0,6,18],
                               'mask': cleanmask,
                               'niter':200000},
                   'calibration': {'calmode': 'p', 'gaintype': 'T',
                                   'solint': 'inf', 'solnorm': True},},
               6: {'imaging': {'threshold': '0.1mJy', 'nterms': 2, 'robust': 0,
                               'weighting':'briggs', 'cell':'0.004arcsec',
                               'imsize':14500, 'scales':[0,6,18],
                               'mask': cleanmask,
                               'niter':200000},
                   'calibration': {'calmode': 'p', 'gaintype': 'T',
                                   'solint': 'inf', 'solnorm': True},},
               7: {'imaging': {'threshold': '0.1mJy', 'nterms': 2, 'robust': 0,
                               'weighting':'briggs', 'cell':'0.004arcsec',
                               'imsize':14500, 'scales':[0,6,18],
                               'usemask': 'pb',
                               'pbmask': 0.1,
                               'niter':200000},
                   'calibration': {'calmode': 'p', 'gaintype': 'T',
                                   'solint': 'inf', 'solnorm': True},},
              }

selfcaliter=0
impars = selfcalpars[selfcaliter]['imaging']
calpars = selfcalpars[selfcaliter]['calibration']

"""
We want to regrid the ALMA-IMF data to the target image size for the long-baseline data

In order to do this, we need a template image, so we make a dirty image _without_ any startmodel (even though the filename says startmod)
"""
contimagename = dirtyimage = field+'.spw0thru19.{imsize}.robust{robust}.thr{threshold}.startmod.mfs.I.dirty'.format(**impars)

if not os.path.exists(contimagename+'.image.tt0.pbcor'):
    for ext in ['.image','.mask','.model','.image.pbcor','.psf','.residual','.pb','.sumwt',]:
        for extext in ('','.tt0','.tt1','.tt2'):
            if os.path.exists(contimagename+ext+extext):
                rmtables(contimagename+ext+extext)

    assert os.path.exists(cleanmask)

    impars = impars.copy()
    impars['niter'] = 0
    print('cleanmask',cleanmask)
    tclean(vis=contvis, imagename=contimagename, field=field, specmode='mfs',
           deconvolver='mtmfs',
           interactive=False, gridder='standard', pbcor=True,
           savemodel='none',
# mask=cleanmask,
           **impars
          )
    test_tclean_success()

# Regrid the ALMA-IMF model to the template from the dirty image we just made.  This is now our low-resolution startmodel
for sm in startmodel:
    imregrid(imagename=sm, template=dirtyimage+".image.tt0", output=sm+".regrid")

# startmodel is a list of model images that should probably include tt0 and tt1
startmodel = [sm+".regrid" for sm in startmodel]


impars = selfcalpars[selfcaliter]['imaging']
preselfcal_imagename = contimagename = field+'.spw0thru19.{imsize}.robust{robust}.thr{threshold}.startmod.mfs.I.startmod'.format(
    **impars)

if not os.path.exists(contimagename+'.image.tt0.pbcor'):
    for ext in ['.image','.mask','.model','.image.pbcor','.psf','.residual','.pb','.sumwt']:
        if os.path.exists(contimagename+ext):
            rmtables(contimagename+ext)

    assert os.path.exists(cleanmask)

    tclean(vis=contvis, imagename=contimagename, field=field, specmode='mfs',
           deconvolver='mtmfs',
           interactive = False, gridder = 'standard', pbcor = True,
           savemodel='none',
           startmodel=startmodel,
           **impars
          )
    test_tclean_success()

#caltable = field+'_b3_startmodselfcal_phase{selfcaliter}_T.startmod.cal'.format(selfcaliter=selfcaliter)

caltable = field+'_b6_startmodselfcal_phase{selfcaliter}_T.startmod.cal'.format(selfcaliter=selfcaliter)
if not os.path.exists(caltable):
    impars['niter'] = 0
    if 'mask' in impars:
        impars.pop('mask')
    tclean(vis=contvis, imagename=contimagename, field=field, specmode='mfs',
           deconvolver='mtmfs', interactive=False, gridder='standard',
           calcres=False, calcpsf=False,
           pbcor=True, savemodel='modelcolumn', **impars)
    test_tclean_success()
    check_model_is_populated(contvis)

    gaincal(vis=contvis, field=field, caltable=caltable, **calpars)

cals = [caltable]

applycal(vis=contvis,
         gaintable=cals,
         gainfield=[field],
         interp="linear",
         applymode='calonly',
         calwt=False)

prevcal_imagename = preselfcal_imagename

for selfcaliter in selfcalpars:
    #why I did skipped 0 iter?
    if selfcaliter == 0:
        continue

    impars = selfcalpars[selfcaliter]['imaging']
    calpars = selfcalpars[selfcaliter]['calibration']

    contimagename = field+'.spw0thru19.{imsize}.robust{robust}.thr{threshold}.mfs.I.startmod.selfcal{selfcaliter}'.format(
        selfcaliter=selfcaliter,
        **impars)
    
    prevcal_imagename = field+'.spw0thru19.{imsize}.robust{robust}.thr{threshold}.mfs.I.startmod.selfcal{selfcaliter}'.format(selfcaliter=selfcaliter,**selfcalpars[selfcaliter]['imaging'])
   # prevcal_imagename = field+'.spw0thru19.{imsize}.robust{robust}.thr{threshold}.mfs.I.startmod.selfcal{selfcaliter}'.format(selfcaliter=selfcaliter-1,**selfcalpars[selfcaliter-1]['imaging'])
    if not os.path.exists(prevcal_imagename+'.image.tt0'):
        pre_imagename = preselfcal_imagename
    else:
        pre_imagename = prevcal_imagename
    if not os.path.exists(contimagename+'.image.tt0.pbcor'):
        for ext in ['.image','.mask','.model','.image.pbcor','.psf','.residual','.pb','.sumwt']:
            for extext in ('','.tt0','.tt1','.tt2'):
                if os.path.exists(contimagename+ext+extext):
                    rmtables(contimagename+ext+extext)

        assert os.path.exists(cleanmask)

        # do a shallow clean so we can inspect the results
        niter = impars.pop('niter')
        tclean(vis=contvis, imagename=contimagename, field=field, specmode='mfs',
               startmodel=[pre_imagename + ".model.tt0",
                           pre_imagename + ".model.tt1"],
               niter=10,
               deconvolver='mtmfs', interactive=False, gridder='standard',
               pbcor=True, savemodel='none',
               **impars
              )
        test_tclean_success()

        if 'mask' in impars:
            impars.pop('mask')

        tclean(vis=contvis, imagename=contimagename, field=field, specmode='mfs',
               # don't need to re-specify startmodel
               #startmodel=[preselfcal_imagename + ".model.tt0",
               #            preselfcal_imagename + ".model.tt1"],
               niter=niter,
               deconvolver='mtmfs', interactive=False, gridder='standard',
               pbcor=True, savemodel='none',
               calcpsf=False, calcres=True, # don't need to recalc PSF
               # mask=cleanmask, # already created
               **impars
              )
        test_tclean_success()
    caltable = field+'_b6_startmodselfcal_phase{selfcaliter}_T.startmod.cal'.format(selfcaliter=selfcaliter)
    if not os.path.exists(caltable):
        impars['niter'] = 0
        if 'mask' in impars:
            impars.pop('mask')
        tclean(vis=contvis, imagename=contimagename, field=field, specmode='mfs',
               deconvolver='mtmfs', interactive=False, gridder='standard',
               pbcor=True, savemodel='modelcolumn',
               calcres=False, calcpsf=False,
               **impars
              )
        test_tclean_success()
        check_model_is_populated(contvis)

        gaincal(vis=contvis, field=field, caltable=caltable,
                gaintable=cals, **calpars)


    cals += [caltable]

    # double-check that there are no repeated entries
    assert len(cals) == len(set(cals))

    applycal(vis=contvis,
             gaintable=cals,
             gainfield=[field]*len(cals),
             interp="linear",
             applymode='calonly',
             calwt=False)

    prevcal_imagename = contimagename

