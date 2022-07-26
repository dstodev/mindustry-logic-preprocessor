from inspect import cleandoc

STANDARD_SIMPLE = cleandoc('''
    jump 2 notEqual @unit null
    ubind @mono
    end
''')

CUSTOM_SIMPLE = cleandoc('''
    jump :label1 notEqual @unit null
    ubind @mono
    label1:
    end
''')

STANDARD_COMPLEX = cleandoc('''
set num_conn 4
sensor upgrade_dir conveyor1 @rotation
op add disconnect_dir upgrade_dir 1
jump 5 notEqual upgrade_dir 4
set upgrade_dir 0
set i 0
op add i_p_1 i 1
getlink building1 i
getlink building2 i_p_1
sensor working building2 @payloadCount
sensor rot1 building1 @rotation
op equal is_linked rot1 upgrade_dir
op land need_unlink is_linked working
jump 18 notEqual need_unlink true
set target_rot disconnect_dir
set ret_addr @counter
set @counter 28
set @counter 25
op notEqual not_linked is_linked true
op notEqual not_working working true
op land need_link not_linked not_working
jump 25 notEqual need_link true
set target_rot upgrade_dir
set ret_addr @counter
set @counter 28
set i i_p_1
jump 6 lessThan i num_conn
end
sensor rec1_type building1 @type
sensor rec1x building1 @x
sensor rec1y building1 @y
ubind @poly
ucontrol build rec1x rec1y rec1_type target_rot 0
ucontrol unbind 0 0 0 0 0
op add @counter ret_addr 1
''')

CUSTOM_COMPLEX = cleandoc('''
set num_conn 4
sensor upgrade_dir conveyor1 @rotation
op add disconnect_dir upgrade_dir 1

jump :rot_cyc_label notEqual upgrade_dir 4
    set upgrade_dir 0
rot_cyc_label:


set i 0
i_loop_label:
    op add i_p_1 i 1
    getlink building1 i
    getlink building2 i_p_1
    sensor working building2 @payloadCount
    sensor rot1 building1 @rotation
    op equal is_linked rot1 upgrade_dir
    op land need_unlink is_linked working

    jump :if_link notEqual need_unlink true
        set target_rot disconnect_dir
        set ret_addr @counter
        set @counter :rotate_building
    set @counter :end_rebuild
    if_link:

    op notEqual not_linked is_linked true
    op notEqual not_working working true
    op land need_link not_linked not_working
    jump :end_rebuild notEqual need_link true
        set target_rot upgrade_dir
        set ret_addr @counter
        set @counter :rotate_building
    end_rebuild:
    set i i_p_1
jump :i_loop_label lessThan i num_conn
end

rotate_building:
sensor rec1_type building1 @type
sensor rec1x building1 @x
sensor rec1y building1 @y
ubind @poly
ucontrol build rec1x rec1y rec1_type target_rot 0
ucontrol unbind 0 0 0 0 0
op add @counter ret_addr 1
''')


