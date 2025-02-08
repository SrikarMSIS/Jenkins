create_library_set -name fast\
   -timing\
    [list $libMinFiles]
create_library_set -name slow\
   -timing\
    [list $libFiles]
create_timing_condition -name tc_slow -library_sets slow 
create_timing_condition -name tc_fast -library_sets fast
create_rc_corner -name rc_best\
   -cap_table $capTableMin\
   -pre_route_res 1.34236\
   -post_route_res 1.34236\
   -pre_route_cap 1.10066\
   -post_route_cap 0.960235\
   -post_route_cross_cap 1.22327\
   -pre_route_clock_res 0\
   -pre_route_clock_cap 0\
   -post_route_clock_cap {0.969117 0 0}\
   -T 0\
   -qrc_tech $qxTechFile

create_rc_corner -name rc_worst\
   -cap_table $capTableMax\
   -pre_route_res 1.34236\
   -post_route_res 1.34236\
   -pre_route_cap 1.10066\
   -post_route_cap 0.960234\
   -post_route_cross_cap 1.22327\
   -pre_route_clock_res 0\
   -pre_route_clock_cap 0\
   -post_route_clock_cap {0.969117 0 0}\
   -T 125\
   -qrc_tech $qxTechFile


create_delay_corner -name slow_max\
   -timing_condition tc_slow\
   -rc_corner rc_worst
create_delay_corner -name fast_min\
   -timing_condition tc_fast\
   -rc_corner rc_best
create_constraint_mode -name functional_func_slow_max\
   -sdc_files\
    [list ../synthesis/outputs/${designName}_synth.sdc]
create_analysis_view -name func_slow_max -constraint_mode functional_func_slow_max -delay_corner slow_max
create_analysis_view -name func_fast_min -constraint_mode functional_func_slow_max -delay_corner fast_min
set_analysis_view -setup [list func_slow_max] -hold [list func_fast_min]
