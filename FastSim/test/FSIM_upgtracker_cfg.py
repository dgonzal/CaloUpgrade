import FWCore.ParameterSet.Config as cms

GEOM="phase1"
#GEOM="phase2BE"
#GEOM="phase1forward"
#GEOM="phase2BEforward"

process = cms.Process("PROD")

# Number of events to be generated
process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(20)
)

# Include DQMStore, needed by the famosSimHits
process.DQMStore = cms.Service( "DQMStore")

# Include the RandomNumberGeneratorService definition
process.load("IOMC.RandomEngine.IOMC_cff")


process.generator = cms.EDProducer("FlatRandomEGunProducer",
    PGunParameters = cms.PSet(
	MinE = cms.double(39.999),
        MaxE = cms.double(40.001),
	# Pion = 211, nu_e = 12, e = 11
        PartID = cms.vint32(11),
	# Eta limits set up to be in the end-cap
        MinEta = cms.double(2.),
        MaxEta = cms.double(2.1),
	MinPhi = cms.double(-3.14159265359),
        MaxPhi = cms.double(3.14159265359)
    ),
    Verbosity = cms.untracked.int32(0),
    psethack = cms.string('single pi pt 1'),
    AddAntiParticle = cms.bool(False),
    firstRun = cms.untracked.uint32(1)
)


# Famos sequences (MC conditions, not Fake anymore!)
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.load("FastSimulation.Configuration.FamosSequences_cff")

# needed for DQM
process.load('FastSimulation.Configuration.EventContent_cff')
process.load('FastSimulation.Configuration.Validation_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')

# Parametrized magnetic field (new mapping, 4.0 and 3.8T)
process.load("Configuration.StandardSequences.MagneticField_38T_cff")
process.VolumeBasedMagneticFieldESProducer.useParametrizedTrackerField = True

# If you want to turn on/off pile-up
process.load("FastSimulation.PileUpProducer.PileUpSimulator_NoPileUp_cff")

# You may not want to simulate everything for your study
process.famosSimHits.SimulateCalorimetry = True
process.famosSimHits.SimulateTracking = True

# this is for phase 1 geometries
if GEOM=="phase1":
    process.load('FastSimulation.Configuration.Geometries_cff')
    from Configuration.AlCa.autoCond import autoCond
    process.GlobalTag.globaltag = cms.string('DES17_62_V7::All')
elif GEOM=="phase2BE":

## this is for phase 2 geometries
    process.load('FastSimulation.Configuration.Geometriesph2_cff')
    from Configuration.AlCa.GlobalTag import GlobalTag
    process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:upgrade2019', '')
    from SLHCUpgradeSimulations.Configuration.combinedCustoms import cust_phase2_BE,noCrossing 
##turning off material effects (needed ONLY for phase2, waiting for tuning)
    process.famosSimHits.MaterialEffects.PairProduction = cms.bool(False)
    process.famosSimHits.MaterialEffects.Bremsstrahlung = cms.bool(False)
    process.famosSimHits.MaterialEffects.MuonBremsstrahlung = cms.bool(False)
    process.famosSimHits.MaterialEffects.EnergyLoss = cms.bool(False)
    process.famosSimHits.MaterialEffects.MultipleScattering = cms.bool(False)
# keep NI so to allow thickness to be properly treated in the interaction geometry
    process.famosSimHits.MaterialEffects.NuclearInteraction = cms.bool(True)
    process.KFFittingSmootherWithOutlierRejection.EstimateCut = cms.double(50.0)
elif GEOM=="phase1forward":
## this is for phase 2 geometries
    process.load('FastSimulation.Configuration.Geometriesph1Forward_cff')
    from Configuration.AlCa.GlobalTag import GlobalTag
    process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:upgradePLS3', '')
    from SLHCUpgradeSimulations.Configuration.combinedCustoms import cust_phase2_BE,noCrossing 
##turning off material effects (needed ONLY for phase2, waiting for tuning)
    process.famosSimHits.MaterialEffects.PairProduction = cms.bool(False)
    process.famosSimHits.MaterialEffects.Bremsstrahlung = cms.bool(False)
    process.famosSimHits.MaterialEffects.MuonBremsstrahlung = cms.bool(False)
    process.famosSimHits.MaterialEffects.EnergyLoss = cms.bool(False)
    process.famosSimHits.MaterialEffects.MultipleScattering = cms.bool(False)
# keep NI so to allow thickness to be properly treated in the interaction geometry
    process.famosSimHits.MaterialEffects.NuclearInteraction = cms.bool(True)
    process.KFFittingSmootherWithOutlierRejection.EstimateCut = cms.double(50.0)
elif GEOM=="phase2BEforward":
## this is for phase 2 geometries
    process.load('FastSimulation.Configuration.Geometriesph2Forward_cff')
    from Configuration.AlCa.GlobalTag import GlobalTag
    process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:upgrade2019', '')
    from SLHCUpgradeSimulations.Configuration.combinedCustoms import cust_phase2_BE,noCrossing 
##turning off material effects (needed ONLY for phase2, waiting for tuning)
    process.famosSimHits.MaterialEffects.PairProduction = cms.bool(False)
    process.famosSimHits.MaterialEffects.Bremsstrahlung = cms.bool(False)
    process.famosSimHits.MaterialEffects.MuonBremsstrahlung = cms.bool(False)
    process.famosSimHits.MaterialEffects.EnergyLoss = cms.bool(False)
    process.famosSimHits.MaterialEffects.MultipleScattering = cms.bool(False)
# keep NI so to allow thickness to be properly treated in the interaction geometry
    process.famosSimHits.MaterialEffects.NuclearInteraction = cms.bool(True)
    process.KFFittingSmootherWithOutlierRejection.EstimateCut = cms.double(50.0)

else:
    print "GEOM is undefined or ill-defined, stopping here"
    sys.exit(1)


# ========= Set up Shashlik parametrization

from ForwardCaloUpgrade.FastSim.Shashlik_PbLSO_cff import myForwardECAL
myForwardECAL( process )
# simulate in layer units or in 1 X0 units
process.famosSimHits.Calorimetry.ECAL.bFixedLength = cms.bool(True)

#Set up the endcap HCAL parameterization

from ForwardCaloUpgrade.FastSim.HCALWithECALPbLSO_cff import myEndcapHCAL
myEndcapHCAL( process )





process.load('RecoParticleFlow.PFTracking.pfTrack_cfi')
process.pfTrack.TrajInEvents = cms.bool(True)
process.load('RecoParticleFlow.PFProducer.particleFlowSimParticle_cff')

#Rechit validation
process.load("FastSimulation.TrackingRecHitProducer.GSRecHitValidation_cfi")
process.testanalyzer.outfilename = cms.string('RecHitValidation.root') 

# Famos with everything !

process.source = cms.Source("EmptySource")

process.csc2DRecHits.readBadChannels = cms.bool(False)
process.simulation = cms.Path(process.generator*process.famosWithEverything)


# To write out events (not need: FastSimulation _is_ fast!)
#process.load("FastSimulation.Configuration.EventContent_cff")
process.o1 = cms.OutputModule("PoolOutputModule",
    outputCommands = cms.untracked.vstring('keep *', 
                                           'drop *_mix_*_*'),
#                              process.AODSIMEventContent,
                              fileName = cms.untracked.string('MyFirstFamosFile_2.root')
)

process.load("RecoParticleFlow.Configuration.Display_EventContent_cff")
process.display = cms.OutputModule("PoolOutputModule",
    process.DisplayEventContent,
    fileName = cms.untracked.string('display.root')

)

process.DQMoutput = cms.OutputModule("PoolOutputModule",
    splitLevel = cms.untracked.int32(0),
    outputCommands = process.DQMEventContent.outputCommands,
    fileName = cms.untracked.string('DQM.root'),
    dataset = cms.untracked.PSet(
        filterName = cms.untracked.string(''),
        dataTier = cms.untracked.string('DQM')
    )
)

process.prevalidation_step = cms.Path(process.prevalidation)
process.validation_step = cms.EndPath(process.tracksValidationFS)
process.endjob_step = cms.EndPath(process.endOfProcess)
process.DQMoutput_step = cms.EndPath(process.DQMoutput)

process.validation_test = cms.EndPath(process.trackingTruthValid+process.tracksValidationFS)

process.trackValidator.outputFile='trackvalidation.root'
process.trackValidator.associators = cms.vstring('TrackAssociatorByChi2','TrackAssociatorByHitsRecoDenom')


process.outpath = cms.EndPath(process.o1)


#---------- Configure message logger ------------
# to get the ECAL calorimeter parameters printed into readCalorimeters.log
 
process.MessageLogger.readCalorimeters = cms.untracked.PSet( 
	threshold = cms.untracked.string('INFO'),
	INFO  = cms.untracked.PSet(limit = cms.untracked.int32(0)),
	ECALProperties = cms.untracked.PSet(limit = cms.untracked.int32(10))
	)

process.MessageLogger.categories = cms.untracked.vstring('ECALProperties')
process.MessageLogger.destinations = cms.untracked.vstring('readCalorimeters','cerr')
process.MessageLogger.cerr.FwkReport.reportEvery = 10


# Make the job crash in case of missing product
process.options = cms.untracked.PSet( Rethrow = cms.untracked.vstring('ProductNotFound') )

process.schedule = cms.Schedule( process.simulation,process.prevalidation_step,process.validation_step,process.endjob_step)



# End of customisation functions

