import openmc
import math

def get_control_rods_assembly(mats):

    # materials' extraction
    helium = mats['helium']
    lead = mats['lead']
    ti15_15 = mats['ti15_15']
    b4c = mats['b4c']
    t91 = mats['t91']
    zircaloy = mats['zircaloy']

    #z plans
    #             0         1       2         3        4       5     6     7
    z_coords = [-291.24, -271.24, -271.12, -203.12, -135.12, -0.12, 0.0, 162.0]
    p_z = [openmc.ZPlane(z0=z) for z in z_coords]

    #pin definition
    r_inner = 1.33
    r_outer = 1.45
    c_inner = openmc.ZCylinder(r=r_inner)
    c_outer = openmc.ZCylinder(r=r_outer)

    #cells
    c_tappo_down = openmc.Cell(fill=ti15_15, region=-c_inner & (+p_z[1] & -p_z[2]))
    c_tappo_up = openmc.Cell(fill=ti15_15, region=-c_inner & (+p_z[5] & -p_z[6]))
    c_active = openmc.Cell(fill=b4c, region=-c_inner & +p_z[2] & -p_z[3])
    c_insul  = openmc.Cell(fill=zircaloy, region=-c_inner & +p_z[3] & -p_z[4])
    c_plenum = openmc.Cell(fill=helium, region=-c_inner & +p_z[4] & -p_z[5])
    
    #clad
    c_clad = openmc.Cell(fill=ti15_15, region=+c_inner & -c_outer & +p_z[1] & -p_z[6])
    pin_universe = openmc.Universe(cells=[c_active, c_insul, c_plenum, c_clad, c_tappo_down, c_tappo_up])

    #assembly
    main_cr_univ = openmc.Universe()
    
    #pin positioning 
    R_rings = [0.0, 3.3, 6.6]
    pin_positions = [(0, 0)]
    for i in range(6): 
        angle = math.radians(i * 60 + 90)
        pin_positions.append((R_rings[1] * math.cos(angle), R_rings[1] * math.sin(angle)))
    for i in range(12):
        angle = math.radians(i * 30 + 45)
        pin_positions.append((R_rings[2] * math.cos(angle), R_rings[2] * math.sin(angle)))

    all_pin_surfaces = []
    for i, (pos_x, pos_y) in enumerate(pin_positions):
        s = openmc.ZCylinder(x0=pos_x, y0=pos_y, r=r_outer)
        all_pin_surfaces.append(s)
        
        p_cell = openmc.Cell(name=f'pin_{i}', fill=pin_universe, region=-s & +p_z[1] & -p_z[6])
        p_cell.translation = (pos_x, pos_y, 0)
        main_cr_univ.add_cell(p_cell)

    #cylindrical and hexagonal surfaces
    r_tube_in, r_tube_out = 8.05, 8.35
    c_tube_in = openmc.ZCylinder(r=r_tube_in)
    c_tube_out = openmc.ZCylinder(r=r_tube_out)

    hex_inner = openmc.model.hexagonal_prism(edge_length=9.12, orientation='x')
    hex_coolant = openmc.model.hexagonal_prism(edge_length=9.873, orientation='x')
    
    #lead between pins
    pin_regions = [-s for s in all_pin_surfaces]
    pins_union = openmc.Union(pin_regions)
    region_pb_inside = hex_coolant & ~pins_union & +p_z[1] & -p_z[6]
    cell_pb_inside = openmc.Cell(fill=lead, region=region_pb_inside)

    #guide tube wall
    region_tube_wall = +c_tube_in & -c_tube_out & +p_z[6] & -p_z[7]
    cell_tube_wall = openmc.Cell(fill=t91, region=region_tube_wall)

    #lead inside the guide tube
    region_co = -c_tube_in & +p_z[6] & -p_z[7]
    cell_co = openmc.Cell(fill=lead, region=region_co)

    #lead outside the guide tube
    region_ext_coolant = hex_coolant & +c_tube_out & +p_z[6] & -p_z[7]
    cell_ext_coolant = openmc.Cell(fill=lead, region=region_ext_coolant)

    #lead down
    cell_down = openmc.Cell(fill=lead, region=hex_coolant & +p_z[0] & -p_z[1])

    main_cr_univ.add_cells([
        cell_pb_inside, cell_tube_wall, cell_ext_coolant, 
        cell_down, cell_co
    ])
    return {
        'universe': main_cr_univ
    }


#execution block
if __name__ == "__main__":
    import sys
    from pathlib import Path
    import matplotlib.pyplot as plt

    sys.path.append(str(Path(__file__).parent.parent))
    
    try:
        from materials import get_alfred_materials
        mats = get_alfred_materials()
        u = get_control_rods_assembly(mats)

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
        plt.title("Vista XY control Assembly")
        plt.savefig('plot_control_xy.png', dpi=300)

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
        plt.title("Vista XZ control Assembly")
        plt.savefig('plot_control_xz.png', dpi=300)
        
        print("Plot salvati correttamente.")
        
    except Exception as e:
        print(f"ERRORE: {e}")