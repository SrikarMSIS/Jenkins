if {$designName == "scr1_pipe_top"} {
    lappend libFiles ../riscvCoreSyntaCore1/ramInputs/sram_32_1024_max_1p8V_25C.lib
    lappend libMinFiles ../riscvCoreSyntaCore1/ramInputs/sram_32_1024_max_1p8V_25C.lib
    lappend libFiles ../riscvCoreSyntaCore1/ramInputs/i2c_top.lib
    lappend libFiles ../riscvCoreSyntaCore1/ramInputs/uart.lib
    lappend libMinFiles ../riscvCoreSyntaCore1/ramInputs/i2c_top.lib
    lappend libMinFiles ../riscvCoreSyntaCore1/ramInputs/uart.lib
}

set conf_qxconf_file {NULL}
set conf_qxlib_file {NULL}
set defHierChar {/}
set init_design_settop 0
set init_gnd_net {VSS}
set init_lef_file $lefFiles
set init_mmmc_file [file normalize scripts/innovus/mmmc${technology}.tcl]
set init_pwr_net {VDD}
set init_verilog [file normalize synthesis/outputs/${designName}_synth.v]
set powerIntent [file normalize synthesis/outputs/${designName}_synth1.upf]
set lsgOCPGainMult 1.000000
set init_design_setup ${designName}

set pnrDir "pnr"
if {![file exists $pnrDir]} {
  file mkdir "pnr"
  puts "Creating directory $pnrDir"
}
catch {cd $pnrDir}


set_multi_cpu_usage -local_cpu 2 -verbose

### need to generated viewDefinition_cui.tcl and use it here
read_mmmc $init_mmmc_file
###


if {$designName == "scr1_pipe_top"} {
    lappend lefFiles ../riscvCoreSyntaCore1/ramInputs/sram_32_1024.lef
    lappend lefFiles ../riscvCoreSyntaCore1/ramInputs/i2c_top.lef
    lappend lefFiles ../riscvCoreSyntaCore1/ramInputs/uart.lef
}
read_physical -lef $lefFiles

read_netlist $init_verilog

init_design
create_floorplan -site CoreSite -core_density_size 1 0.7 10 10 10 10

read_power_intent -1801 ${powerIntent}
commit_power_intent -verbose

set spareCount 500
if {$designName == "scr1_pipe_top"} {
read_def ../scripts/innovus/coreFP.def
set spareCount 2000
}

check_power_domains -nets_missing_iso
check_power_domains -nets_missing_shifter


### add tap cells
set TAPCell "TIELO"
catch {add_well_taps -cell ${TAPCell} -cell_interval 28}
catch {add_well_taps -termination_cells TAP_TERMINATION -column_cells ${TAPCell}}


### add port buffers
add_io_buffers -base_name portInBuffers -in_cells BUFX4
add_io_buffers -base_name portOutBuffers -out_cells  BUFX4


### adding spare cells

set spareList "NAND2X6 NAND2X4 NOR2X4 NOR2X6 DFFQX4 DFFQX2 BUFX3 BUFX6 INVX4 INVX16"

create_spare_module -cells $spareList -module_name spareMod
place_spare_modules   -module_name spareMod -num_modules $spareCount

#foreach cel $spareList {
#reset_spare_insts -cell $cel
#set_spare_insts -cell $cel
#}


write_db setupComplete.inn

exit
