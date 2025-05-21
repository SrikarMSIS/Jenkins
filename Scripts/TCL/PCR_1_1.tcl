#Read the setupComplete.inn directory
#Use this info to continue placement

read_db setupComplete.inn
set_db design_process_node {tech}
#On Chip Variation of Deciding Metal Layers - Delay Caluclation
set_db timing_analysis_type ocv
set_db place_global_place_io_pins true
#This is used to look into the best case for BOTH setup and hold conditions along the clock path
set_db timing_analysis_cppr both

place_opt_design

write_db placeCompleted.inn

create_clock_tree_spec
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
set_db check_drc_disable_rules {}
set_db check_drc_ndr_spacing auto
set_db check_drc_check_only default
set_db check_drc_inside_via_def true
set_db check_drc_exclude_pg_net false
set_db check_drc_ignore_trial_route false
set_db check_drc_ignore_cell_blockage false
set_db check_drc_use_min_spacing_on_block_obs auto
set_db check_drc_report {module}.drc.rpt
set_db check_drc_limit 1000
check_drc
set_db check_drc_area {0 0 0 0}
write_stream {module}_GDS -lib_name DesignLib -unit 2000 -mode all

write_db routeCompleted.inn

exit