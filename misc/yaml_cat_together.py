#!/usr/bin/env python
dcObserver={
"t133": "aircar_airTemperature_133",

    }

# header
listHeader=[
  "basic_config/mpasjedi_en3dvar.yaml",
  "basic_config/mpasjedi_getkf_observer.yaml",
  "basic_config/mpasjedi_getkf_solver.yaml"
    ]
# ~~~~
# determine dcObserverUser
#
dcObserverUser=dcObserver
# ~~~~
# write out rrfs-workflow yaml files
#
obdir="obtype_config/"
for fheader in listHeader:
  output_name=fheader.replace("basic_config/mpasjedi_","")
  if not "getkf" in fheader:
    output_name="jedivar.yaml"
  #
  skip_zone=False
  change_output_filename=False
  with open(fheader, 'r') as infile1, open(output_name, 'w') as outfile:
    for line in infile1:
      if "&analysisDate" in line:
        line=line.replace("2024-05-27T00:00:00Z","@analysisDate@")
      elif "mem%iMember%/mpasout.2024-05-27_00.00.00.nc" in line:
        line=line.replace("mem%iMember%/mpasout.2024-05-27_00.00.00.nc","mem%iMember%.nc")
      elif "begin:" in line:
        line=line.replace("2024-05-26T21:00:00Z", "@beginDate@")
      elif "PT6H" in line:
        line=line.replace("PT6H","PT4H")
      elif "output:" in line:
        change_output_filename=True
      elif "./bkg.$Y-$M-$D_$h.$m.$s.nc" in line:
        line=line.replace("./bkg.$Y-$M-$D_$h.$m.$s.nc","./prior_mean.nc")
      elif "filename:" in line:
        if change_output_filename and "getkf" in fheader:
          line=line.replace("./ana.$Y-$M-$D_$h.$m.$s.nc","./data/ens/mem%{member}%.nc")
        elif change_output_filename: # for JEDIVAR
          line=line.replace("./ana.$Y-$M-$D_$h.$m.$s.nc","mpasin.nc")
      elif "data/mpasout.2024-05-27_00.00.00.nc" in line:
        line=line.replace("data/mpasout.2024-05-27_00.00.00.nc", "mpasin.nc")
      elif "@OBSERVATIONS@" in line:
        skip_zone=True
      #
      if not skip_zone:
        outfile.write(line)
    # ~~~~
    # loop through user defined obserers
    for key, value in dcObserverUser.items():
      fobs=obdir+value+".yaml"
      with open(fobs,'r') as infile2:
        for line in infile2:
          if "seed_time:" in line:
            line=line.replace("2024-05-27T00:00:00Z","@analysisDate@")
          elif "@DISTRIBUTION@" in line:
            if "getkf_solver" in fheader:
              line=line.replace("@DISTRIBUTION@","Halo")
            else:
              line=line.replace("@DISTRIBUTION@","RoundRobin")
          elif value in line:
            line=line.replace(value,key)
          # ~~~~~~
          outfile.write(line)
# ~~~~~~~~~~~~
# extra processing for solver: put the jdiag file names to obsdatin
#
