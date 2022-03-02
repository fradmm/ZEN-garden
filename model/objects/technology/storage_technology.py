"""===========================================================================================================================================================================
Title:          ENERGY-CARBON OPTIMIZATION PLATFORM
Created:        October-2021
Authors:        Alissa Ganter (aganter@ethz.ch)
                Jacob Mannhardt (jmannhardt@ethz.ch)
Organization:   Laboratory of Risk and Reliability Engineering, ETH Zurich

Description:    Class defining the parameters, variables and constraints that hold for all storage technologies.
                The class takes the abstract optimization model as an input, and returns the parameters, variables and
                constraints that hold for the storage technologies.
==========================================================================================================================================================================="""
import logging
import pyomo.environ as pe
import numpy as np
from sympy import E
from model.objects.technology.technology import Technology
from model.objects.energy_system import EnergySystem

class StorageTechnology(Technology):
    # empty list of elements
    listOfElements = []
    
    def __init__(self, tech):
        """init storage technology object
        :param tech: name of added technology"""

        logging.info(f'Initialize storage technology {tech}')
        super().__init__(tech)
        # store input data
        self.storeInputData()
        # add StorageTechnology to list
        StorageTechnology.addElement(self)

    def storeInputData(self):
        """ retrieves and stores input data for element as attributes. Each Child class overwrites method to store different attributes """   
        # get attributes from class <Technology>
        super().storeInputData()
        # get system information
        paths               = EnergySystem.getPaths()   
        # set attributes for parameters of parent class <Technology>
        self.inputPath          = paths["setStorageTechnologies"][self.name]["folder"]
        setBaseTimeSteps    = EnergySystem.getEnergySystem().setBaseTimeSteps
        # add all raw time series to dict
        self.rawTimeSeries                  = {}
        self.rawTimeSeries["minLoad"]       = self.dataInput.extractInputData(self.inputPath,"minLoad",indexSets=["setNodes","setTimeSteps"],timeSteps=setBaseTimeSteps) # TODO maybe rename: minLoad = minimum specific power to charge/discharge, probably 0
        self.rawTimeSeries["maxLoad"]       = self.dataInput.extractInputData(self.inputPath,"maxLoad",indexSets=["setNodes","setTimeSteps"],timeSteps=setBaseTimeSteps) # TODO maybe rename: maxLoad = maximum specific power to charge/discharge, i.e., 1/(hours until entirely charged/discharged)
        self.rawTimeSeries["opexSpecific"]  = self.dataInput.extractInputData(self.inputPath,"opexSpecific",indexSets=["setNodes","setTimeSteps"],timeSteps= setBaseTimeSteps)
        # non-time series input data
        self.capacityLimit                  = self.dataInput.extractInputData(self.inputPath,"capacityLimit",indexSets=["setNodes"])
        self.carbonIntensityTechnology      = self.dataInput.extractInputData(self.inputPath,"carbonIntensity",indexSets=["setNodes"])
        # set attributes for parameters of child class <StorageTechnology>
        self.efficiencyCharge               = self.dataInput.extractInputData(self.inputPath,"efficiencyCharge",indexSets=["setNodes"])
        self.efficiencyDischarge            = self.dataInput.extractInputData(self.inputPath,"efficiencyDischarge",indexSets=["setNodes"])
        self.selfDischarge                  = self.dataInput.extractInputData(self.inputPath,"selfDischarge",indexSets=["setNodes"]) 
        self.capexSpecific                  = self.dataInput.extractInputData(self.inputPath,"capexSpecific",indexSets=["setNodes","setTimeSteps"],timeSteps= self.setTimeStepsInvest)
        self.convertToAnnualizedCapex()

    def calculateTimeStepsStorageLevel(self):
        """ this method calculates the number of time steps on the storage level, and the order in which the storage levels are connected """
        # setTimeSteps                        = self.setTimeStepsOperation
        orderTimeSteps                      = self.orderTimeSteps
        # calculate connected storage levels, i.e., time steps that are constant for 
        IdxLastConnectedStorageLevel        = np.append(np.flatnonzero(np.diff(orderTimeSteps)),len(orderTimeSteps)-1)
        # ConnectedStorageLevels              = orderTimeSteps[IdxLastConnectedStorageLevel]
        # empty setTimeStep
        self.setTimeStepsStorageLevel       = []
        self.timeStepsStorageLevelDuration  = {}
        self.orderTimeStepsStorageLevel     = np.zeros(np.size(orderTimeSteps)).astype(int)
        counterTimeStep                     = 0
        for idxTimeStep,idxStorageLevel in enumerate(IdxLastConnectedStorageLevel):
            self.setTimeStepsStorageLevel.append(idxTimeStep)
            self.timeStepsStorageLevelDuration[idxTimeStep] = len(range(counterTimeStep,idxStorageLevel+1))
            self.orderTimeStepsStorageLevel[counterTimeStep:idxStorageLevel+1] = idxTimeStep
            counterTimeStep                 = idxStorageLevel + 1 
        # add order to energy system
        EnergySystem.setOrderTimeSteps(self.name+"StorageLevel",self.orderTimeStepsStorageLevel)

    ### --- classmethods to construct sets, parameters, variables, and constraints, that correspond to StorageTechnology --- ###
    @classmethod
    def constructSets(cls):
        """ constructs the pe.Sets of the class <StorageTechnology> """
        model = EnergySystem.getConcreteModel()
        # time steps of storage levels
        model.setTimeStepsStorageLevel = pe.Set(
            model.setStorageTechnologies,
            initialize = cls.getAttributeOfAllElements("setTimeStepsStorageLevel"),
            doc="Set of time steps of storage levels for all storage technologies. Dimensions: setStorageTechnologies"
        )

    @classmethod
    def constructParams(cls):
        """ constructs the pe.Params of the class <StorageTechnology> """
        model = EnergySystem.getConcreteModel()
        
        # time step duration of storage level
        model.timeStepsStorageLevelDuration = pe.Param(
            cls.createCustomSet(["setStorageTechnologies","setTimeStepsStorageLevel"]),
            initialize = cls.getAttributeOfAllElements("timeStepsStorageLevelDuration"),
            doc="Parameter which specifies the time step duration in StorageLevel for all technologies. Dimensions: setStorageTechnologies, setTimeStepsStorageLevel"
        )
        # efficiency charge
        model.efficiencyCharge = pe.Param(
            cls.createCustomSet(["setStorageTechnologies","setNodes"]),
            initialize = cls.getAttributeOfAllElements("efficiencyCharge"),
            doc = 'efficiency during charging for storage technologies. Dimensions: setStorageTechnologies, setNodes'
        )
        # efficiency discharge
        model.efficiencyDischarge = pe.Param(
            cls.createCustomSet(["setStorageTechnologies","setNodes"]),
            initialize = cls.getAttributeOfAllElements("efficiencyDischarge"),
            doc = 'efficiency during discharging for storage technologies. Dimensions: setStorageTechnologies, setNodes'
        )
        # self discharge
        model.selfDischarge = pe.Param(
            cls.createCustomSet(["setStorageTechnologies","setNodes"]),
            initialize = cls.getAttributeOfAllElements("selfDischarge"),
            doc = 'self discharge of storage technologies. Dimensions: setStorageTechnologies, setNodes'
        )
        # capex specific
        model.capexSpecific = pe.Param(
            cls.createCustomSet(["setStorageTechnologies","setNodes","setTimeStepsInvest"]),
            initialize = cls.getAttributeOfAllElements("capexSpecific"),
            doc = 'specific capex of storage technologies. Dimensions: setStorageTechnologies, setNodes, setTimeStepsInvest'
        )
        #

    @classmethod
    def constructVars(cls):
        """ constructs the pe.Vars of the class <StorageTechnology> """
        def carrierFlowBounds(model,tech ,node,time):
            """ return bounds of carrierFlow for bigM expression 
            :param model: pe.ConcreteModel
            :param tech: tech index
            :param node: node index
            :param time: time index
            :return bounds: bounds of carrierFlow"""
            # convert operationTimeStep to investTimeStep: operationTimeStep -> baseTimeStep -> investTimeStep
            investTimeStep = EnergySystem.convertTechnologyTimeStepType(tech,time,"operation2invest")
            bounds = model.capacity[tech,node,investTimeStep].bounds
            return(bounds)

        model = EnergySystem.getConcreteModel()
        # flow of carrier on node into storage
        model.carrierFlowCharge = pe.Var(
            cls.createCustomSet(["setStorageTechnologies","setNodes","setTimeStepsOperation"]),
            domain = pe.NonNegativeReals,
            bounds = carrierFlowBounds,
            doc = 'carrier flow into storage technology on node i and time t. Dimensions: setStorageTechnologies, setNodes, setTimeStepsOperation. Domain: NonNegativeReals'
        )
        # flow of carrier on node out of storage
        model.carrierFlowDischarge = pe.Var(
            cls.createCustomSet(["setStorageTechnologies","setNodes","setTimeStepsOperation"]),
            domain = pe.NonNegativeReals,
            bounds = carrierFlowBounds,
            doc = 'carrier flow out of storage technology on node i and time t. Dimensions: setStorageTechnologies, setNodes, setTimeStepsOperation. Domain: NonNegativeReals'
        )
        # loss of carrier on node
        model.levelCharge = pe.Var(
            cls.createCustomSet(["setStorageTechnologies","setNodes","setTimeStepsStorageLevel"]), #setTimeStepsStorageLevel setBaseTimeSteps
            domain = pe.NonNegativeReals,
            doc = 'carrier flow through storage technology on node i and time t. Dimensions: setStorageTechnologies, setNodes, setTimeStepsStorageLevel. Domain: NonNegativeReals'
        )
        
    @classmethod
    def constructConstraints(cls):
        """ constructs the pe.Constraints of the class <StorageTechnology> """
        model = EnergySystem.getConcreteModel()
        # Limit storage level
        model.constraintStorageLevelMax = pe.Constraint(
            cls.createCustomSet(["setStorageTechnologies","setNodes","setTimeStepsStorageLevel"]), #setTimeStepsStorageLevel setBaseTimeSteps 
            rule = constraintStorageLevelMaxRule,
            doc = 'limit maximum storage level to capacity. Dimensions: setStorageTechnologies, setNodes, setTimeStepsStorageLevel'
        ) 
        # couple storage levels
        model.constraintCoupleStorageLevel = pe.Constraint(
            cls.createCustomSet(["setStorageTechnologies","setNodes","setTimeStepsStorageLevel"]), #setTimeStepsStorageLevel setBaseTimeSteps
            rule = constraintCoupleStorageLevelRule,
            doc = 'couple subsequent storage levels (time coupling constraints). Dimensions: setStorageTechnologies, setNodes, setTimeStepsStorageLevel'
        )
        # Linear Capex
        model.constraintStorageTechnologyLinearCapex = pe.Constraint(
            cls.createCustomSet(["setStorageTechnologies","setNodes","setTimeStepsInvest"]),
            rule = constraintCapexStorageTechnologyRule,
            doc = 'Capital expenditures for installing storage technology. Dimensions: setStorageTechnologies, setNodes, setTimeStepsInvest'
        ) 

    # defines disjuncts if technology on/off
    @classmethod
    def disjunctOnTechnologyRule(cls,disjunct, tech, node, time):
        """definition of disjunct constraints if technology is on"""
        model = disjunct.model()
        # get invest time step
        baseTimeStep = EnergySystem.decodeTimeStep(tech,time,"operation")
        investTimeStep = EnergySystem.encodeTimeStep(tech,baseTimeStep,"invest")
        # disjunct constraints min load charge
        disjunct.constraintMinLoadCharge = pe.Constraint(
            expr=model.carrierFlowCharge[tech, node, time] >= model.minLoad[tech,node,time] * model.capacity[tech,node, investTimeStep]
        )
        # disjunct constraints min load discharge
        disjunct.constraintMinLoadDischarge = pe.Constraint(
            expr=model.carrierFlowDischarge[tech, node, time] >= model.minLoad[tech,node,time] * model.capacity[tech,node, investTimeStep]
        )

    @classmethod
    def disjunctOffTechnologyRule(cls,disjunct, tech, node, time):
        """definition of disjunct constraints if technology is off"""
        model = disjunct.model()
        # off charging
        disjunct.constraintNoLoadCharge = pe.Constraint(
            expr=model.carrierFlowCharge[tech, node, time] == 0
        )
        # off discharging
        disjunct.constraintNoLoadDischarge = pe.Constraint(
            expr=model.carrierFlowDischarge[tech, node, time] == 0
        )

    @classmethod
    def getStorageLevelTimeStep(cls,tech,time):
        """ gets current and previous time step of storage level """
        sequenceStorageLevel    = cls.getAttributeOfSpecificElement(tech,"sequenceStorageLevel")
        setTimeStepsOperation   = cls.getAttributeOfSpecificElement(tech,"setTimeStepsOperation")
        indexCurrentTimeStep    = setTimeStepsOperation.index(time)
        currentLevelTimeStep    = sequenceStorageLevel[indexCurrentTimeStep]
        # if first time step
        if indexCurrentTimeStep == 0:
            previousLevelTimeStep = sequenceStorageLevel[-1]
        # if any other time step
        else:
            previousLevelTimeStep = sequenceStorageLevel[indexCurrentTimeStep-1]
        return currentLevelTimeStep,previousLevelTimeStep

### --- functions with constraint rules --- ###
def constraintStorageLevelMaxRule(model, tech, node, time):
    """limit maximum storage level to capacity"""
    # get invest time step
    baseTimeStep    = EnergySystem.decodeTimeStep(tech+"StorageLevel",time)
    elementTimeStep = EnergySystem.encodeTimeStep(tech,baseTimeStep)
    investTimeStep  = EnergySystem.convertTechnologyTimeStepType(tech,elementTimeStep,"operation2invest")
    # investTimeStep = EnergySystem.encodeTimeStep(tech,time,"invest")
    return(model.levelCharge[tech, node, time] <= model.capacity[tech, node, investTimeStep])

def constraintCoupleStorageLevelRule(model, tech, node, time):
    """couple subsequent storage levels (time coupling constraints)"""
    baseTimeStep                = EnergySystem.decodeTimeStep(tech+"StorageLevel",time)
    elementTimeStep             = EnergySystem.encodeTimeStep(tech,baseTimeStep)
    currentLevelTimeStep        = time
    if time != 0:
        previousLevelTimeStep   = time-1
    else:
        previousLevelTimeStep   = model.setTimeStepsStorageLevel[tech].at(-1)
    return(
        model.levelCharge[tech, node, currentLevelTimeStep] == 
        model.levelCharge[tech, node, previousLevelTimeStep]*(1-model.selfDischarge[tech,node])**model.timeStepsStorageLevelDuration[tech,time] + 
        (model.carrierFlowCharge[tech, node, elementTimeStep]*model.efficiencyCharge[tech,node] - 
        model.carrierFlowDischarge[tech, node, elementTimeStep]/model.efficiencyDischarge[tech,node])*sum((1-model.selfDischarge[tech,node])**interimTimeStep for interimTimeStep in range(0,model.timeStepsStorageLevelDuration[tech,time]))
    )

# full time series
# def constraintStorageLevelMaxRule(model, tech, node, time):
#     """limit maximum storage level to capacity"""
#     # get invest time step
#     # baseTimeStep    = EnergySystem.decodeTimeStep(tech+"StorageLevel",time)
#     elementTimeStep = EnergySystem.encodeTimeStep(tech,time)
#     investTimeStep  = EnergySystem.convertTechnologyTimeStepType(tech,elementTimeStep,"operation2invest")
#     # investTimeStep = EnergySystem.encodeTimeStep(tech,time,"invest")
#     return(model.levelCharge[tech, node, time] <= model.capacity[tech, node, investTimeStep])

# def constraintCoupleStorageLevelRule(model, tech, node, time):
#     """couple subsequent storage levels (time coupling constraints)"""
#     # baseTimeStep                = EnergySystem.decodeTimeStep(tech+"StorageLevel",time)
#     elementTimeStep             = EnergySystem.encodeTimeStep(tech,time)
#     currentLevelTimeStep        = time
#     if time != 0:
#         previousLevelTimeStep   = time-1
#     else:
#         previousLevelTimeStep   = model.setBaseTimeSteps.at(-1)
#     return(
#         model.levelCharge[tech, node, currentLevelTimeStep] == 
#         model.levelCharge[tech, node, previousLevelTimeStep]*(1-model.selfDischarge[tech,node])+#**model.timeStepsStorageLevelDuration[tech,time] + 
#         (model.carrierFlowCharge[tech, node, elementTimeStep]*model.efficiencyCharge[tech,node] - 
#         model.carrierFlowDischarge[tech, node, elementTimeStep]/model.efficiencyDischarge[tech,node])#*model.timeStepsStorageLevelDuration[tech,time]
#     )

def constraintCapexStorageTechnologyRule(model, tech, node, time):
    """ definition of the capital expenditures for the storage technology"""
    return (model.capex[tech,node, time] == 
            model.builtCapacity[tech,node, time] *
            model.capexSpecific[tech,node, time])