#Routing TCL File
read_db postCts.inn
set_db design_process_node 45
set_db timing_analysis_type ocv 
set_db timing_analysis_cppr both

gui_show

set_db route_design_with_timing_driven 1
set_db route_design_with_si_driven 1
set_db route_design_top_routing_layer 11
set_db route_design_bottom_routing_layer 1
set_db route_design_detail_end_iteration 1
set_db route_design_with_timing_driven true
set_db route_design_with_si_driven true
route_design -global_detail
set_db route_special_via_connect_to_shape { noshape }
route_special -connect core_pin -layer_change_range { Metal1(1) Metal11(11) } -block_pin_target nearest_target -core_pin_target first_after_row_end -allow_jogging 1 -crossover_via_layer_range { Metal1(1) Metal11(11) } -nets { VDD VSS } -allow_layer_change 1 -target_via_layer_range { Metal1(1) Metal11(11) }

write_db route.inn
set_db extract_rc_engine post_route
set_db extract_rc_effort_level medium
time_design -post_route
time_design -post_route -hold
opt_design -post_route -setup -hold
write_db postroute.inn