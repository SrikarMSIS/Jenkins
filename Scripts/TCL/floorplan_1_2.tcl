#Floorplan

#Necessary file paths are 
#.lib files - Liberty file
#.lef files - Library Exchange Format
#.mmmc files - Multi Mode Multiple Corners file
#.upf file - Power Intent file - Paused for now
#.v - Generated Netlist file
#.sdc file - Post Design Constraints FIle

#The following is the flow for the floorplan.tcl

set conf_qxconf_file {NULL}
set conf_qxlib_file {NULL}
set defHierChar {/}
set init_design_settop 0
set init_gnd_net {VSS}
set init_lef_file {lef}
set designName {module}
#Path to MMMC TCL file to be called
set init_mmmc_file [file normalize /home/vlsi/srikar/jenkins_auto/Jenkins/Jenkins/mmmc.tcl]
set init_pwr_net {VDD}
set init_verilog [file normalize {netlist}]
set init_design_setup ${designName}

#Reading MMMC file
read_mmmc $init_mmmc_file

#Reading LEF file
read_physical -lef $init_lef_file

read_netlist $init_verilog

init_design
create_floorplan -site CoreSite -core_density_size 1 0.7 10 10 10 10

check_power_domains -nets_missing_iso
check_power_domains -nets_missing_shifter

#Adding TAP Cells
set TAPCell "TIELO"
catch {add_well_taps -cell ${TAPCell} -cell_interval 28}

#Power Planning
create_net -power -name VDD
create_net -ground -name VSS

add_rings -nets {VSS VDD} -type core_rings -follow core -layer {top M9 bottom M9 left M8 right M8} -width {top 2 bottom 2 left 2 right 2} -spacing {top 2 bottom 2 left 2 right 2} -offset {top 0 bottom 0 left 0 right 0} -center 0 -threshold 0 -jog_distance 0 -snap_wire_center_to_grid none

add_stripes -direction vertical -nets {VDD VSS} -width 2 -spacing 2 -layer M8 -start_offset 1 -set_to_set_distance 10

add_stripes -direction horizontal -nets {VDD VSS} -width 2 -spacing 2 -layer M9 -start_offset 1 -set_to_set_distance 10

connect_global_net VDD -type pg_pin -pin_base_name VDD -all
connect_global_net VSS -type pg_pin -pin_base_name VSS -all


write_db setupComplete.inn

exit
 



