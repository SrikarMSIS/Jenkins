#Read the setupComplete.inn directory
#Use this info to continue placement

read_db setupComplete.inn
set_db design_process_node 45
set_db timing_analysis_type ocv
set_db timing_analysis_cppr both

place_opt_design

write_db placeCompleted.inn

gui_show
