#Floorplan

#Necessary file paths are 
#.lib files - Liberty file
#.lef files - Library Exchange Format
#.mmmc files - Multi Mode Multiple Corners file
#.upf file - Power Intent file
#.v - Generated Netlist file

#The following is the flow for the floorplan.tcl

set conf_qxconf_file {NULL}
set conf_qxlib_file {NULL}
set defHierChar {/}
set init_design_settop 0
set init_gnd_net {VSS}
set init_lef_file "{lef_file_path}"
set init_mmmc_file [file normalize "{path_to_mmmc_fle}"]
set init_pwr_net {VDD}
set init_verilog [file normalize "{path_to_netlist_v}"]
set lsgOCPGainMult 1.000000
set init_design_setup "{pass_design_name}"

#Reading MMMC file
read_mmmc $init_mmmc_file

#Reading LEF file
read_physical -lef $lefFiles

init_design
create_floorplan -site CoreSite -core_density_size 1 0.7 10 10 10 10

read_def "{path_to_def_file}"
set spareCount 2000

check_power_domains -nets_missing_iso
check_power_domains -nets_missing_shifter

#Adding TAP Cells
set TAPCell "TIELO"
catch {add_well_taps -cell ${TAPCell} -cell_interval 28}
catch {add_well_taps -termination_cells TAP_TERMINATION -column_cells ${TAPCell}}

#Add IO Buffers
add_io_buffers -base_name portInBuffers -in_cells BUFX4
add_io_buffers -base_name portOutBuffers -out_cells  BUFX4

#Adding Spare Cells
set spareList "NAND2X6 NAND2X4 NOR2X4 NOR2X6 DFFQX4 DFFQX2 BUFX3 BUFX6 INVX4 INVX16"

create_spare_module -cells $spareList -module_name spareMod
place_spare_modules   -module_name spareMod -num_modules $spareCount

write_db setupComplete.inn

exit