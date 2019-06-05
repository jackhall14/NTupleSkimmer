import os
import time
import sys
import subprocess
import shutil
import ROOT
sys.path.insert(0, '../')

def GetSampleNameAndType(InputFile):
    if InputFile.split("/")[-1].split("_")[1] == "Z":
        sampleName = InputFile.split("/")[-1].split("_")[1] + "_" + InputFile.split("/")[-1].split("_")[2]
        sampleType = InputFile.split("/")[-1].split("_")[0]
    elif InputFile.split("/")[-1].split("_")[1] == "W":
        sampleName = InputFile.split("/")[-1].split("_")[1] + "_" + InputFile.split("/")[-1].split("_")[2]
        sampleType = InputFile.split("/")[-1].split("_")[0]
    else:
        sampleName = InputFile.split("/")[-1].split("_")[1]
        sampleType = InputFile.split("/")[-1].split("_")[0]
    return sampleName, sampleType

def GetTreeName(sampleName,sampleType):
    if sampleType == "Sig":
        if sampleName == "Gbb.offshell":
            treeName = ['Gbb_1400_5000_1000_nominal','Gbb_2000_5000_1000_nominal','Gbb_2200_5000_1_nominal']
        elif sampleName == "Gtb.offshell":
            treeName = ['Gtb_2100_5000_1_nominal','Gtb_2000_5000_1000_nominal','Gtb_1400_5000_1000_nominal']
        elif sampleName == "Gtb.onshell":
            treeName = ['Gtb_2100_1850_1200_600_nominal','Gtb_2100_1450_1200_600_nominal','Gtb_1600_1420_1240_1000_nominal']
    elif sampleType == "Bkg": 
        treeName = sampleName + "_nominal"
    elif sampleType == "Data":
        treeName = "data"
    return treeName

def GetRootListOfBranches(File, TreeName):
    # Get the branches we want
    file = ROOT.TFile(File)
    TreeFromFile = file.Get(TreeName)
    list_of_branches = list(TreeFromFile.GetListOfBranches())
    NewListOfBranches = ROOT.vector('string')()
    for branch in list_of_branches:
        variable = str(branch).split()[2].split("\"")[1]
        if variable in list_of_good_variables:
            NewListOfBranches.push_back(variable)
    file.Close()
    return NewListOfBranches

def GetAlias(file, treename,branchname):
    print("Opening up original root file ... ")
    root_file = ROOT.TFile(file,"r")
    tree_from_file = root_file.Get(treename)
    NewAliasFormula = tree_from_file.GetAlias(branchname)
    root_file.Close()
    print("Successfully retrieved alias ... ")
    return NewAliasFormula

def SetNewAlias(NewFile, Treename, AliasFormula):
    print("Opening up new file to add the alias .. ")
    output_file = ROOT.TFile(NewFile,"update")
    TreeFromFile = output_file.Get(Treename)
    TreeFromFile.SetAlias("weight_lumi_real", AliasFormula)
    TreeFromFile.Write()
    output_file.Close()
    print("Successfully applied alias ... ")

def NTuplerReducer(FileNameIn, ListOfBranches, SampleName, SampleType, TreeName):
    # Build RDF from root file
    print(" TreeName: " + TreeName)
    RDF = ROOT.ROOT.RDataFrame
    d = RDF(TreeName, FileNameIn)

    # Entries to begin with:
    entries = d.Count().GetValue()
    print(str(entries) +" events to begin ")

    # Apply cuts
    Cuts = 'mettst > 200.0 && pass_MET == 1 && jets_n > 1 && bjets_n > 1'
    d2 = d.Filter(Cuts)
    entries1 = d2.Count().GetValue()
    print(str(entries1) + " entries passed all filters")

    # Output to new rootfile
    FileExtension = FileNameIn.split("/")[-1].split(SampleName)[-1]
    if SampleType == "Sig":
        FileNameOut = SampleType + "_" + SampleName + "_" + TreeName + "_skimmed" + FileExtension
    else:
        FileNameOut = SampleType + "_" + SampleName + "_skimmed" + FileExtension
    print(" Outputting to: " + FileNameOut)
    d2.Snapshot(TreeName, FileNameOut, ListOfBranches)

    # Get the weight lumi real alias
    branch_name = "weight_lumi_real"
    alias_formula = GetAlias(FileNameIn,TreeName,branch_name)
    SetNewAlias(FileNameOut,TreeName,alias_formula)


##################
#### Main ########
##################


# Get list of all files
path_to_samples = "/atlas/shatlas/NTUP_SUSY/StrongMultiB/merged_output_tree/"
file_array = os.listdir(path_to_samples)
file_array = [path_to_samples + elm for index, elm in enumerate(file_array)]
print("Files to run over:")
for i in file_array:
    print(i)

# muons_vars = ["baselineLep_n",'muons_n', 'muons_pt', 'muons_phi''muons_eta', 'muons_e']
muons_vars = ["baselineLep_n",'muons_n', 'muons_pt']
# elec_vars = ['electrons_n', 'electrons_pt', 'electrons_phi', 'electrons_eta', 'electrons_e']
elec_vars = ['electrons_n', 'electrons_pt']
jet_vars = ['jets_n', 'bjets_n', 'jets_pt', 'jets_phi', 'jets_eta', 'jets_e', 'jets_jvt']
# discrim_vars = ['asymmetry', 'ht', 'ht_jets', 'meff_incl', 'm_4j', 'mT_4j', 'm_2j', 'mT_2j', 'm_bb', 'mT_bb', 'mCT_bb', 'mTb_min', 'mTb_max', 'metcst', 'mettst', 'met_nomuon', 'metsoft']
discrim_vars = ['asymmetry', 'ht', 'meff_incl', "MJSum_RCJ_r08pt10", 'mT_non_bb','mT_bb', "mT_2j", 'mTb_min','mettst',"dphi_1jet"]
weights_vars = ["pass_MET","weight_mc","weight_lumi","weight_btag","weight_elec","weight_muon","weight_jvt","weight_pu"]
other = ["run_number","dphi_min"]

list_of_good_variables = muons_vars + elec_vars + jet_vars + discrim_vars + weights_vars + other

# Loop over files and reduce them
for i in range(0,len(file_array)):
    print("File running over: " + file_array[i])
    sample_name,sample_type = GetSampleNameAndType(file_array[i])
    print(" The sample name is: " + sample_name + " and type is: " + sample_type)

    if sample_name == "Gtt.offshell":
        print("Skipping Gtt")
    elif sample_name == "Gtb.onshell":
        tree_name = GetTreeName(sample_name, sample_type)
        for sig_tree in tree_name:
            new_list_of_branches = GetRootListOfBranches(file_array[i],sig_tree)
            NTuplerReducer(file_array[i],new_list_of_branches, sample_name, sample_type, sig_tree)        
    elif sample_name == "Gbb.offshell":
        tree_name = GetTreeName(sample_name, sample_type)
        for sig_tree in tree_name:
            new_list_of_branches = GetRootListOfBranches(file_array[i],sig_tree)
            NTuplerReducer(file_array[i],new_list_of_branches, sample_name, sample_type, sig_tree)
    elif sample_name == "Gtb.offshell":
        tree_name = GetTreeName(sample_name, sample_type)
        for sig_tree in tree_name:
            new_list_of_branches = GetRootListOfBranches(file_array[i],sig_tree)
            NTuplerReducer(file_array[i],new_list_of_branches, sample_name, sample_type, sig_tree)
    else:
        tree_name = GetTreeName(sample_name, sample_type)
        new_list_of_branches = GetRootListOfBranches(file_array[i],tree_name)
        NTuplerReducer(file_array[i],new_list_of_branches, sample_name, sample_type, tree_name)
    print("")
    print("------------------------------------------------------")
    print("")