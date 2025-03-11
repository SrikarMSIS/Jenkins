#Routing TCL File
read_db postCts.inn
set_db design_process_node 45
set_db timing_analysis_type ocv 
set_db timing_analysis_cppr both

create_route_type -name srikRoute

route_design
write_db route.inn
set_db extract_rc_engine post_route
set_db extract_rc_effort_level medium
time_design -post_route
time_design -post_route -hold
opt_design -post_route -setup -hold
write_db postroute.inn

gui_show
