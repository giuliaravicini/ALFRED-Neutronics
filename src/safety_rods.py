import openmc
import math

def get_safety_rods_assembly(mats):

    # materials' extraction
    helium = mats['helium']
    lead = mats['lead']
    ti15_15 = mats['ti15_15']
    b4c = mats['b4c']
    t91 = mats['t91']
    zircaloy = mats['zircaloy']

    #z plans and clad
    #              0        1       2       3       4      5      6    7     8
    z_coords = [-291.24, -142.0, -122.0, -116.0, -32.0, -26.0, -20.0, 0.0, 162.0]
    p_s = [openmc.ZPlane(z0=z) for z in z_coords]


    r_cyl_inner_s = 1.43
    r_cyl_outer_s = 1.55
    safety_cyl = openmc.ZCylinder(r=r_cyl_inner_s)
    clad_cyl_s = openmc.ZCylinder(r=r_cyl_outer_s)


    #surfaces
    region_15_15Ti_s = -safety_cyl & ((+p_s[1] & -p_s[2]) | (+p_s[6] & -p_s[7]))
    region_insulator_s = -safety_cyl & ((+p_s[2] & -p_s[3]) | (+p_s[4] & -p_s[5]))
    region_active_s = -safety_cyl & +p_s[3] & -p_s[4]
    region_plenum_s = -safety_cyl & +p_s[5] & -p_s[6]
    
    region_clad_s = (+safety_cyl & -clad_cyl_s) & (+p_s[1] & -p_s[7])

    #cells
    c_ti_s   = openmc.Cell(fill=ti15_15, region=region_15_15Ti_s)
    c_ins_s  = openmc.Cell(fill=zircaloy, region=region_insulator_s)
    c_act_s  = openmc.Cell(fill=b4c, region=region_active_s)
    c_ple_s  = openmc.Cell(fill=helium, region=region_plenum_s)
    c_clad_s = openmc.Cell(fill=ti15_15, region=region_clad_s)

    safety_pin_univ = openmc.Universe(cells=(c_ti_s, c_ins_s, c_act_s, c_ple_s, c_clad_s))

    #assembly
    main_sr_univ = openmc.Universe()
    R_inner_s = 2.0
    R_outer_s = 5.3
    
    pin_positions_s = []

    for i in range(3):
        angle = math.radians(i * 120)
        pin_positions_s.append((R_inner_s * math.cos(angle), R_inner_s * math.sin(angle)))

    for i in range(9):
        angle = math.radians(i * 40)
        pin_positions_s.append((R_outer_s * math.cos(angle), R_outer_s * math.sin(angle)))

    all_pin_surfaces_s = []
    for i, (pos_x, pos_y) in enumerate(pin_positions_s):
        p_surf_s = openmc.ZCylinder(x0=pos_x, y0=pos_y, r=r_cyl_outer_s)
        all_pin_surfaces_s.append(p_surf_s)
        
        p_cell_s = openmc.Cell(name=f'sr_pin_{i}')
        p_cell_s.fill = safety_pin_univ
        p_cell_s.region = -p_surf_s & +p_s[1] & -p_s[7]
        p_cell_s.translation = (pos_x, pos_y, 0)
        main_sr_univ.add_cell(p_cell_s)


    #hexagonal and cylindrical surfaces
    r_in_s, r_out_s = 7.35, 8.35
    wrapper_in_s = openmc.ZCylinder(r=r_in_s)
    wrapper_out_s = openmc.ZCylinder(r=r_out_s)

    hex_inner_s = openmc.model.hexagonal_prism(edge_length=9.12, orientation='x')
    hex_outer_s = openmc.model.hexagonal_prism(edge_length=9.873, orientation='x')

    pins_region_s = openmc.Union([ -s for s in all_pin_surfaces_s ])

    #lead between pins
    region_pb_inside_s = hex_outer_s & ~pins_region_s & +p_s[1] & -p_s[7]
    cell_pb_inside_s = openmc.Cell(name="Pb_inside_tube_sr", fill=lead, region=region_pb_inside_s)

    #guide tube
    region_tube_wall_s = (+wrapper_in_s & -wrapper_out_s) & +p_s[7] & -p_s[8]
    cell_tube_wall_s = openmc.Cell(name="Tube_Wall_sr", fill=t91, region=region_tube_wall_s)

    #lead outside the guide tube
    region_corners_s = (+wrapper_out_s & hex_outer_s) & +p_s[7] & -p_s[8]
    cell_corners_s = openmc.Cell(name="Pb_corners_sr", fill=lead, region=region_corners_s)

    #lead inside the guide tube
    region_coo = -wrapper_in_s & +p_s[7] & -p_s[8]
    cell_regionincoo = openmc.Cell(fill=lead, region=region_coo)

    #lead region
    regione_down_controlsr = hex_outer_s & +p_s[0] & -p_s[1]
    cell_down_controlsr = openmc.Cell(fill=lead, region=regione_down_controlsr)

    main_sr_univ.add_cells([cell_pb_inside_s, cell_tube_wall_s, cell_corners_s, cell_down_controlsr, cell_regionincoo])

    return {
        'universe':main_sr_univ}


#execution block
if __name__ == "__main__":
    import sys
    from pathlib import Path
    import matplotlib.pyplot as plt

    sys.path.append(str(Path(__file__).parent.parent))
    
    try:
        from materials import get_alfred_materials
        mats = get_alfred_materials()
        u = get_safety_rods_assembly(mats)

        #color map
        col_map = {
            mats['zircaloy']: 'lightgray',
            mats['ti15_15']:  'blue',
            mats['lead']:     'cyan',
            mats['t91']:      'darkorange',
            mats['helium']:   'green',
            mats['b4c']:      'purple' 
        }

        #plot XY
        u['universe'].plot(
            width=(22, 22), 
            basis='xy', 
            origin=(0, 0, -64.62), 
            color_by='material', 
            colors=col_map
        )
        plt.title("Vista XY safety Assembly")
        plt.savefig('plot_safety_xy.png')

        #plot XZ
        plt.figure() 
        u['universe'].plot(
            width=(25, 460),
            basis='xz', 
            origin=(0, 0, -64.62), 
            color_by='material', 
            pixels=(1000, 8000),
            colors=col_map 
        )
        plt.title("Vista XZ safety Assembly")
        plt.savefig('plot_safety_xz.png')
        
        print("Plot salvati correttamente.")
        
    except Exception as e:
        print(f"ERRORE: {e}")