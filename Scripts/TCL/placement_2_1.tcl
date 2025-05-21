#Read the setupComplete.inn directory
#Use this info to continue placement

read_db setupComplete.inn
set_db design_process_node {tech}
#On Chip Variation of Deciding Metal Layers - Delay Caluclation
set_db timing_analysis_type ocv
#This is used to look into the best case for BOTH setup and hold conditions along the clock path
set_db timing_analysis_cppr both

place_opt_design -place_global_place_io_pins TRUE

write_db placeCompleted.inn

gui_show
