# Auto generated configuration file
# using: 
# Revision: 1.284.2.2 
# Source: /cvs_server/repositories/CMSSW/CMSSW/Configuration/PyReleaseValidation/python/ConfigBuilder.py,v 
# with command line options: SinglePiPt1_cfi.py -s GEN,FASTSIM,HLT --pileup=NoPileUp --geometry DB --conditions=auto:mc --eventcontent=RECOSIM --datatier GEN-SIM-RECO -n 10
import FWCore.ParameterSet.Config as cms

process = cms.Process('HLT')

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('FastSimulation.PileUpProducer.PileUpSimulator_NoPileUp_cff')
process.load('FastSimulation.Configuration.Geometries_MC_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
process.load('Configuration.StandardSequences.Generator_cff')
process.load('GeneratorInterface.Core.genFilterSummary_cff')
process.load('FastSimulation.Configuration.FamosSequences_cff')
process.load('IOMC.EventVertexGenerators.VtxSmearedParameters_cfi')
process.load('FastSimulation.Configuration.HLT_GRun_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.load('FastSimulation.Configuration.EventContent_cff')
process.load('DQMServices.Components.DQMFileSaver_cfi')
#process.GlobalTag.globaltag = 'MC_50_V13::All'
#process.GlobalTag.globaltag = 'MC_42_V15A::All'
process.GlobalTag.globaltag = 'MC_60_V4::All'


# -------- This is what you would need if you want to do the multilayers ECAL ---------- 
## from Configuration.AlCa.GlobalTag import GlobalTag
## process.GlobalTag = GlobalTag(process.GlobalTag, 'MC_60_V4::All', '')
## process.GlobalTag.toGet = cms.VPSet(
## 	    cms.PSet(record = cms.string('PEcalEndcapRcd'),
## 				                          tag = cms.string('EERECO_Geometry_newTag'),
## 				                          connect = cms.untracked.string('sqlite_file:/afs/cern.ch/user/m/mgouzevi/scratch0/GEOMETRY/INTERMEDIATE/CMSSW_6_0_0/src/ForwardCaloUpgrade/FastSim/test/EERECO_Geometry.db')
## 				                                                   )
## 		) 





process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(50)
)


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


# Input source
process.source = cms.Source("EmptySource")

process.options = cms.untracked.PSet()

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    version = cms.untracked.string('$Revision: 1.24 $'),
    annotation = cms.untracked.string('SinglePiPt1_cfi.py nevts:10'),
    name = cms.untracked.string('PyReleaseValidation')
)

# Output definition


process.RECOSIMoutput = cms.OutputModule("PoolOutputModule",
    splitLevel = cms.untracked.int32(0),
    outputCommands = process.RECOSIMEventContent.outputCommands,
    fileName = cms.untracked.string('SinglePigun_FASTSIM.root'),
    dataset = cms.untracked.PSet(
        filterName = cms.untracked.string(''),
        dataTier = cms.untracked.string('GEN-SIM-RECO')
    ),
    SelectEvents = cms.untracked.PSet(
        SelectEvents = cms.vstring('generation_step')
    )
)

# Additional output definition

# Other statements
process.famosSimHits.SimulateCalorimetry = True
process.famosSimHits.SimulateTracking = True
process.simulation = cms.Sequence(process.simulationWithFamos)
process.HLTEndSequence = cms.Sequence(process.reconstructionWithFamos)
process.Realistic7TeVCollisionVtxSmearingParameters.type = cms.string("BetaFunc")
process.famosSimHits.VertexGenerator = process.Realistic7TeVCollisionVtxSmearingParameters
process.famosPileUp.VertexGenerator = process.Realistic7TeVCollisionVtxSmearingParameters


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


# ---------------------------
# Switch off different noises
# ---------------------------

# this is important for particle gun studies
# you might like to change the noise parameters to those you expect from
# your detector model and then study.

process.ecalRecHit.doMiscalib = True
process.ecalRecHit.RecHitsFactory.ECALBarrel.Noise = cms.double(0)
process.ecalRecHit.RecHitsFactory.ECALBarrel.Threshold = cms.double(0.001)
process.ecalRecHit.RecHitsFactory.ECALBarrel.HighNoiseParameters = cms.vdouble()
process.ecalRecHit.RecHitsFactory.ECALBarrel.SRThreshold = cms.double(0.0)

process.ecalRecHit.RecHitsFactory.ECALEndcap.Noise = cms.double(0)
process.ecalRecHit.RecHitsFactory.ECALEndcap.Threshold = cms.double(0.001)
process.ecalRecHit.RecHitsFactory.ECALEndcap.SRThreshold = cms.double(0.0)
process.ecalRecHit.RecHitsFactory.ECALEndcap.HighNoiseParameters = cms.vdouble()

process.ecalPreshowerRecHit.RecHitsFactory.Noise = cms.double(0.000001)
process.ecalPreshowerRecHit.RecHitsFactory.Threshold = cms.double(4.5e-10)

process.hbhereco.doMiscalib = True
process.horeco.doMiscalib = True
process.hfreco.doMiscalib = True

process.hbhereco.RecHitsFactory.HCAL.Noise = cms.vdouble(0, 0)
process.horeco.RecHitsFactory.HCAL.Noise = cms.vdouble(0)
process.hfreco.RecHitsFactory.HCAL.Noise = cms.vdouble(0)

# -----------------------------------------------------------------------------
# Switch off interactions in the CMS tracker
# -----------------------------------------------------------------------------

# this allow to have a more clean particles sample arriving to the calorimeters
# for more "physics oriented studies" you would probably like to switch them back

process.famosSimHits.MaterialEffects.PairProduction = False
process.famosSimHits.MaterialEffects.Bremsstrahlung = False
process.famosSimHits.MaterialEffects.EnergyLoss = False
process.famosSimHits.MaterialEffects.MultipleScattering = False
process.famosSimHits.MaterialEffects.NuclearInteraction = False

# --------- You may need to uncomment MultipleScattering and NuclearInteraction in some CMSSW version otherwise it crashes

#-------------------------------------------------------------------------
# Switch off the preshower
# ------------------------------------------------------------------------
process.famosSimHits.Calorimetry.ECAL.SimulatePreshower = cms.bool(False)

#-------------------------------------------------------------------------
# ECAL shower parameters
# ------------------------------------------------------------------------
#SpotFraction is the fraction of spots wrt. the Grindhammer parametrization
#used for the shower simulation. SpotFraction=1 corresponds to the default parametrization.
process.famosSimHits.Calorimetry.ECAL.SpotFraction = cms.double(1.0)
process.famosSimHits.Calorimetry.ECAL.CoreIntervals = cms.vdouble(100.0, 1.0)
process.famosSimHits.Calorimetry.ECAL.TailIntervals = cms.vdouble(100.0, 1.0)
#Size of the longitudinal grid we use for simulation, doesn't seems to work since hard coded in
#void EMShower::prepareSteps() from FastSimulation/ShowerDevelopment/src
process.famosSimHits.Calorimetry.ECAL.GridSize = cms.int32(7)

#--------------------------------
#--------------------------------
#Set up the Shashlik PbLSO detector for the forward ECAL
#--------------------------------
#--------------------------------


#-------------- Containment corrections ----------#:
# SimCalorimetry/EcalSimProducers/python/ecalNotContainmentSim_cff.py
# In this file the factor is: 0.975
# If you uncomment the following line the containment correction would be switched off. Those corrections
# are used to multiply the ECAL Sim energy by 1/0.975

#process.ecalRecHit.RecHitsFactory.ECALEndcap.ContFact.ecal_notCont_sim.EEs25notContainment = cms.double(1.0)


#------------- This is the way that the miscalibration is introduced
# FastSimulation/CaloRecHitsProducer/python/CaloRecHits_cff.py
# if you uncomment the following lines you remove the miscalibration
# inside FastSimulation/CaloRecHitsProducer/src/EcalEndcapRecHitsMaker.cc
# those factors contribute to modify a bit the 1/0.975 factor

#process.ecalRecHit.RecHitsFactory.ECALEndcap.Refactor = cms.double(0.),
#process.ecalRecHit.RecHitsFactory.ECALEndcap.Refactor_mean = cms.double(1.),

     
#from ForwardCaloUpgrade.FastSim.LSO_cff import myForwardECAL
#myForwardECAL( process )
#from ForwardCaloUpgrade.FastSim.PBWO_cff import myForwardECAL
#myForwardECAL( process )
#from ForwardCaloUpgrade.FastSim.Shashlik_PbYAG_cff import myForwardECAL
#myForwardECAL( process )

from ForwardCaloUpgrade.FastSim.Shashlik_PbLSO_cff import myForwardECAL
myForwardECAL( process )

#Set up the endcap HCAL parameterization

#from ForwardCaloUpgrade.FastSim.DefaultHCAL_cff import myEndcapHCAL
#myEndcapHCAL( process )

from ForwardCaloUpgrade.FastSim.HCALWithECALPbLSO_cff import myEndcapHCAL
myEndcapHCAL( process )


	
#---------------------------------------------------------------
# DQM
#---------------------------------------------------------------
# Switch on the simulation of the shower by steps of 1 X0 necessary
# to fill the shower shape histograms
process.famosSimHits.Calorimetry.ECAL.bFixedLength = cms.bool(True)
# switch on the DQM histograms in FastSimulation/CalorimeterProperties and in FastSimulation/ShowerShapes
process.famosSimHits.Calorimetry.useDQM = cms.untracked.bool(True)
# DQM file saves customization
process.dqmSaver.workflow = '/ParticleGun/FastSim/DQM'



# Path and EndPath definitions
process.generation_step = cms.Path(process.pgen_genonly)
process.reconstruction = cms.Path(process.reconstructionWithFamos)
process.genfiltersummary_step = cms.EndPath(process.genFilterSummary)
process.RECOSIMoutput_step = cms.EndPath(process.RECOSIMoutput*process.dqmSaver)
process.sim = cms.Path(process.simulationWithFamos)

# Schedule definition
process.schedule = cms.Schedule(process.generation_step,process.genfiltersummary_step,process.sim)
process.schedule.extend([process.reconstruction,process.RECOSIMoutput_step])
# filter all path with the production filter sequence
for path in process.paths:
	getattr(process,path)._seq = process.generator * getattr(process,path)._seq 



#--------------------------- Dont change those lines -----------------------------#
#------- They are used by scripts to produce automatically large data samples ----#

#FORWARD process.generator.PGunParameters.MinEta = cms.double(2.3)
#FORWARD process.generator.PGunParameters.MinEta = cms.double(2.4)

#CENTRAL process.generator.PGunParameters.MinEta = cms.double(-0.9)
#CENTRAL process.generator.PGunParameters.MinEta = cms.double(0.9)

#ENERGY process.generator.PGunParameters.MinE = cms.double(#MIN.999)
#ENERGY process.generator.PGunParameters.MaxE = cms.double(#MAX.001)

#PART process.generator.PGunParameters.PartID = cms.vint32(#PARTID)
#MEVENTS process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(#NEVENTS))
#FILENAME process.RECOSIMoutput.fileName = cms.untracked.string('SinglePigun_FASTSIM.root')
