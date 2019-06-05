int NtupleReducer()
{

  // 
  // Process multiple files
  // 

  // Files:
  //   Bkg_diboson_21.2.67_output_tree.root    Bkg_W_jets_21.2.67_output_tree.root    Data_2018_21.2.67_output_tree.2.root
  // Bkg_dijet_21.2.67_output_tree.1.root    Bkg_Z_jets_21.2.67_output_tree.1.root  Sig_Gbb.offshell_21.2.67_output_tree.root
  // Bkg_dijet_21.2.67_output_tree.2.root    Bkg_Z_jets_21.2.67_output_tree.2.root  Sig_Gtb.offshell_21.2.67_output_tree.root
  // Bkg_dijet_21.2.67_output_tree.root      Data_2015_21.2.67_output_tree.root     Sig_Gtb.onshell_21.2.67_output_tree.root
  // Bkg_singletop_21.2.67_output_tree.root  Data_2016_21.2.67_output_tree.root     Sig_Gtt.offshell_21.2.67_output_tree.root
  // Bkg_topEW_21.2.67_output_tree.root      Data_2017_21.2.67_output_tree.root
  // Bkg_ttbar_21.2.67_output_tree.root      Data_2018_21.2.67_output_tree.1.root

  // std::string path_to_samples = "/atlas/shatlas/NTUP_SUSY/StrongMultiB/merged_output_tree/";

  // // 
  // // Create and run over bkg
  // // 
  // std::vector<std::string> bkg_samples = {"diboson", "dijet","singletop","topEW","ttbar","W_jets"};
  // std::vector<std::string> bkg_files;

  // for (int i = 0; i < bkg_samples.size(); i++ ){
  //   bkg_files.push_back(path_to_samples + "Bkg_" + bkg_samples[i] + "_21.2.67_output_tree.root");
  // }

  // // Manually add .1 and .2 files:
  // bkg_files.push_back(path_to_samples + "Bkg_" + "Z_jets" + "_21.2.67_output_tree.1.root");
  // bkg_samples.push_back("Z_jets");
  // bkg_files.push_back(path_to_samples + "Bkg_" + "Z_jets" + "_21.2.67_output_tree.2.root");
  // bkg_samples.push_back("Z_jets");
  // bkg_files.push_back(path_to_samples + "Bkg_" + bkg_samples[1] + "_21.2.67_output_tree.1.root");
  // bkg_samples.push_back(bkg_samples[1]);
  // bkg_files.push_back(path_to_samples + "Bkg_" + bkg_samples[1] + "_21.2.67_output_tree.2.root");
  // bkg_samples.push_back(bkg_samples[1]);

  // for (int i = 0; i < bkg_files.size(); i++ ){
  //   std::cout << "File to run over: " << bkg_files[i] << std::endl;
  //   ROOT::RDataFrame d(bkg_samples[i] + "_nominal",bkg_files[i]);

  //   // Entries to begin with:
  //   auto entries = d.Count();
  //   std::cout << *entries << " events to begin " << std::endl;

  //   // Apply cuts
  //   auto Cuts = [](Float_t mettst, Int_t pass_MET, Int_t jets_n, Int_t bjets_n) { return mettst > 200.0 && pass_MET == 1 && jets_n > 2 && bjets_n>1; };
  //   // Alternative method for cuts:
  //   // auto entries2 = d.Filter("mettst > 200.0").Filter("pass_MET == 1").Count();
  //   auto d2 = d.Filter(Cuts, {"mettst", "pass_MET","jets_n","bjets_n"});
  //   auto entries1 = d2.Count();
  //   std::cout << *entries1 << " entries passed all filters" << std::endl;

  //   // Produce output root file
  //   std::string file_name = "Bkg_" + bkg_samples[i] + "_21.2.67_output_tree_skimmed.root";
  //   std::string branch_name = bkg_samples[i] + "_nominal";
  //   d2.Snapshot(branch_name, file_name);
  // }


//   // 
//   // Create and run over data
//   // 
//   std::vector<std::string> data_samples = {"Data_2015", "Data_2016","Data_2017"};
//   std::vector<std::string> data_files;
//   for (int i = 0; i < data_samples.size(); i++ ){
//     data_files.push_back(path_to_samples + data_samples[i] + "_21.2.67_output_tree.root");
//   }

//   // Manually add .1 and .2 files:
//   data_files.push_back(path_to_samples + "Data_2018_21.2.67_output_tree.1.root");
//   data_files.push_back(path_to_samples + "Data_2018_21.2.67_output_tree.2.root");

//   for (int i = 0; i < data_files.size(); i++ ){
//     std::cout << "File to run over: " << data_files[i] << std::endl;
  
// }


  //
  // Create Single file:
  //
  ROOT::RDataFrame d("diboson_nominal","/atlas/shatlas/NTUP_SUSY/StrongMultiB/merged_output_tree/Bkg_diboson_21.2.67_output_tree.root");

  // Entries to begin with:
  auto entries = d.Count();
  std::cout << *entries << " events to begin " << std::endl;

  // Apply cuts
  auto Cuts = [](Float_t mettst, Int_t pass_MET) { return mettst > 200.0 && pass_MET == 1; };
  // Alternative method for cuts:
  // auto entries2 = d.Filter("mettst > 200.0").Filter("pass_MET == 1").Count();
  auto d2 = d.Filter(Cuts, {"mettst", "pass_MET"});
  auto entries1 = d2.Count();
  std::cout << *entries1 << " entries passed all filters" << std::endl;

  d2.Snapshot("myNewTree", "newfile.root");

  return 0;
}
