#!/usr/bin/env python
# POC: Guoqing.Ge@noaa.gov
#
import os, sys
# list of available observers
dcObserver={
  "adpsfc_t181": "adpsfc_airTemperature_181",
  "adpsfc_t183": "adpsfc_airTemperature_183",
  "adpsfc_t187": "adpsfc_airTemperature_187",
  "adpsfc_q181": "adpsfc_specificHumidity_181",
  "adpsfc_q183": "adpsfc_specificHumidity_183",
  "adpsfc_q187": "adpsfc_specificHumidity_187",
  "adpsfc_ps181": "adpsfc_stationPressure_181",
  "adpsfc_ps187": "adpsfc_stationPressure_187",
  "adpsfc_uv281": "adpsfc_winds_281",
  "adpsfc_uv284": "adpsfc_winds_284",
  "adpsfc_uv287": "adpsfc_winds_287",
# adpupa
  "adpupa_t120": "adpupa_airTemperature_120",
  "adpupa_t132": "adpupa_airTemperature_132",
  "adpupa_q120": "adpupa_specificHumidity_120",
  "adpupa_q132": "adpupa_specificHumidity_132",
  "adpupa_ps120": "adpupa_stationPressure_120",
  "adpupa_uv220": "adpupa_winds_220",
  "adpupa_uv232": "adpupa_winds_232",
# aircar, aircft
  "aircar_t133": "aircar_airTemperature_133",
  "aircar_q133": "aircar_specificHumidity_133",
  "aircar_uv233": "aircar_winds_233",
  "aircft_t130": "aircft_airTemperature_130",
  "aircft_t131": "aircft_airTemperature_131",
  "aircft_t134": "aircft_airTemperature_134",
  "aircft_t135": "aircft_airTemperature_135",
  "aircft_q134": "aircft_specificHumidity_134",
  "aircft_uv230": "aircft_winds_230",
  "aircft_uv231": "aircft_winds_231",
  "aircft_uv234": "aircft_winds_234",
  "aircft_uv235": "aircft_winds_235",
# ztd, msonet, proflr, rassda
  "gnss_ztd": "gnss_zenithTotalDelay",
  "msonet_t188": "msonet_airTemperature_188",
  "msonet_q188": "msonet_specificHumidity_188",
  "msonet_ps188": "msonet_stationPressure_188",
  "msonet_uv288": "msonet_winds_288",
  "proflr_uv227": "proflr_winds_227",
  "rassda_t126": "rassda_airTemperature_126",
# sfcshp, vadwnd
  "sfcshp_t180": "sfcshp_airTemperature_180",
  "sfcshp_t182": "sfcshp_airTemperature_182",
  "sfcshp_t183": "sfcshp_airTemperature_183",
  "sfcshp_q180": "sfcshp_specificHumidity_180",
  "sfcshp_q182": "sfcshp_specificHumidity_182",
  "sfcshp_q183": "sfcshp_specificHumidity_183",
  "sfcshp_ps180": "sfcshp_stationPressure_180",
  "sfcshp_ps182": "sfcshp_stationPressure_182",
  "sfcshp_uv280": "sfcshp_winds_280",
  "sfcshp_uv282": "sfcshp_winds_282",
  "sfcshp_uv284": "sfcshp_winds_284",
  "vadwnd_uv224": "vadwnd_winds_224",
# satellite obs
  "amsua_n19": "amsua_n19",
  "amsua_n20": "atms_n20",
  "atmos_npp": "atms_npp",
  "abi_g16": "abi_g16",
  "abi_g18": "abi_g18",
    }

# list of header files
listHeader=[
  "basic_config/mpasjedi_hyb3denvar.yaml",
  "basic_config/mpasjedi_getkf_observer.yaml",
  "basic_config/mpasjedi_getkf_solver.yaml"
    ]

#
# determine dcObserverUser
#
args=sys.argv
nargs=len(args)-1
if nargs <1:
  print(f"{args[0]} [?|query|all|obs_str]\n")
  print(f"  obs_str specifies a subset of observers, delimited with a comma")
  print(f"  eg: t133  or t133,t187 or t133,q133,uv233 etc")
  exit()

if args[1] == "query" or args[1] == "?":
  summary=""
  detail=""
  for key,value in dcObserver.items():
    summary+=f"{key},"
    detail+=f"{key}={value}\n"
  print(f"{detail.rstrip(',')}\n")
  print(f"{summary.rstrip(',')}\n")
  exit()
elif args[1] == "all":
  obsUser=list(dcObserver.keys())
else:
  obsUser=args[1].split(",")
# create dcObserverUser
dcObserverUser={}
for key in obsUser:
  dcObserverUser[key]=dcObserver[key]
#
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
      elif "save posterior ensemble: false" in line:
        line=line.replace("save posterior ensemble: false", "save posterior ensemble: true")
      elif "@OBSERVATIONS@" in line:
        skip_zone=True
      #
      if not skip_zone:
        outfile.write(line)
    # ~~~~
    # loop through user defined obsevers
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
            if ".nc4" in line:
              line=line.replace(".nc4", ".nc")
          elif "gnss_ztd_zenithTotalDelay" in line:
            line=line.replace("gnss_ztd_zenithTotalDelay","gnss_ztd")

          # ~~~~~~
          outfile.write(line)
#
# ~~~~~~~~~~~~
# extra processing for solver
#  copy the obsfile line from the obsdatain section to the obsdataout section
#
buffer_zone = []
in_buffer_zone = False
obsfile_line = None
obsdataout = False
with open("getkf_solver.yaml", 'r') as infile, open(".tmp.solver.yaml", 'w') as outfile:
  for line in infile:
    if "RoundRobin" in line:
      line = line.replace("RoundRobin", "Halo")
    elif "obsdatain" in line:
      in_buffer_zone = True
      buffer_zone.append(line)
    elif in_buffer_zone:
      buffer_zone.append(line)
      if "obsdataout" in line:
        obsdataout=True
      elif "obsfile" in line:
        if obsdataout:
          line = line.replace("jdiag", "data/jdiag/jdiag")
          obsfile_line = line  # Store the obsdataout "obsfile" line

    if obsfile_line and in_buffer_zone:
      # Replace the previous obsfile line with the new one
      for i, buf_line in enumerate(buffer_zone):
          if "obsfile" in buf_line:
              buffer_zone[i] = obsfile_line
              break
      # Write out the buffer zone
      for buf_line in buffer_zone:
          outfile.write(buf_line)
      # Reset buffer and state tracking
      buffer_zone = []
      in_buffer_zone = False
      obsfile_line = None
      obsdataout = False
      continue

    if not in_buffer_zone:
        outfile.write(line)
# ~~~~~~~~
os.replace(".tmp.solver.yaml","getkf_solver.yaml")
#
# print out information
#
print("jedivar.yaml\ngetkf_observer.yaml\ngetkf_solver.yaml\n\ngenerated under current directory")
