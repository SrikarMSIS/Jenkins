#CTS TCL File
read_db placeCompleted.inn
set_db design_process_node 45
set_db timing_analysis_type ocv 
set_db timing_analysis_cppr both

create_route_rule -width {M1 0.12 M2 0.14 M3 0.14 M4 0.14 M5 0.14 M6 0.14 M7 0.14 M8 0.14 M9 0.14 } \
		-spacing {M1 0.12 M2 0.14 M3 0.14 M4 0.14 M5 0.14 M6 0.14 M7 0.14 M8 0.14 M9 0.14 } -name 2w2s
create_route_type -name clkroute -route_rule 2w2s -bottom_preferred_layer M5 -top_preferred_layer M6

set_db cts_route_type_trunk clkroute
set_db cts_route_type_leaf clkroute
set_db cts_buffer_cells {CLKBUFX8 CLKBUFX12}
set_db cts_inverter_cells {CLKINVX8 CLKINVX12}
set_db cts_clock_gating_cells TLATNTSCA*
create_clock_tree_spec -out_file ccopt_cui.spec
source  ccopt_cui.spec
ccopt_design

write_db ctsCompleted.inn

time_design -post_cts
opt_design -post_cts

write_db postCts.inn

gui_show
