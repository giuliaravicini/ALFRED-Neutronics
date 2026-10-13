import openmc

def get_fuel_inner_assembly(mats):

    # materials' extraction
    helium = mats['helium']
    helium = mats['helium']
    lead = mats['lead']
    ti15_15 = mats['ti15_15']
    mox_inner = mats['mox_inner']
    t91 = mats['t91']

    #plans and geometry
    clad_r_in = 0.525
    gap_r_in = 0.465
    fuel_r_in = 0.45
    hollow_r_in = 0.2

    clad_cyl_in = openmc.ZCylinder(r = clad_r_in) 
    gap_cyl_in = openmc.ZCylinder(r = gap_r_in)  
    fuel_cyl_in = openmc.ZCylinder(r = fuel_r_in)
    hollow_cyl_in = openmc.ZCylinder(r = hollow_r_in)

    #              0      1    2     3     4      5      6      7
    z_coords = [-291.24, 0.0, 7.5, 62.5, 122.5, 134.5, 142.0, 162.0]
    p_fin = [openmc.ZPlane(z0=z) for z in z_coords]

    #pin radial geometry
    gap_region_in = + fuel_cyl_in & - gap_cyl_in 
    fuel_region_in = + hollow_cyl_in & - fuel_cyl_in 
    hollow_region_in = - hollow_cyl_in

    gap_cell_in = openmc.Cell(name="Gap_in", fill = helium, region = gap_region_in) 
    fuel_cell_in = openmc.Cell(name = "Fuel_in", fill = mox_inner, region = fuel_region_in)
    hollow_cell_in = openmc.Cell(name = "Hollow_in", fill = helium, region = hollow_region_in) 
    
    pin_active_core_universe = openmc.Universe(cells=(hollow_cell_in, fuel_cell_in, gap_cell_in))

    #pin axial geometry
    region_plug_in = -gap_cyl_in & ((+p_fin[1] & -p_fin[2]) | (+p_fin[5] & -p_fin[6]))
    region_he_in   = -gap_cyl_in & ((+p_fin[2] & -p_fin[3]) | (+p_fin[4] & -p_fin[5]))
    region_mox_in  = -gap_cyl_in & (+p_fin[3] & -p_fin[4])
    
    region_cladding_in = (+gap_cyl_in & -clad_cyl_in) & (+p_fin[1] & -p_fin[6])

    region_pb_pin_in = (+clad_cyl_in) & (+p_fin[1] & -p_fin[6])

    c_plug_in = openmc.Cell(fill=ti15_15, region=region_plug_in)
    c_he_in   = openmc.Cell(fill=helium, region=region_he_in)
    c_mox_in  = openmc.Cell(fill=pin_active_core_universe, region=region_mox_in)
    c_clad_in = openmc.Cell(fill=ti15_15, region=region_cladding_in)
    c_pb_in   = openmc.Cell(fill=lead, region=region_pb_pin_in)


    fuel_pin_universe_in = openmc.Universe(cells=(c_plug_in, c_he_in, c_mox_in, c_clad_in, c_pb_in))

    #lattice
    in_surface_in = openmc.model.hexagonal_prism(edge_length=9.12, orientation='x')
    
    lattice_in = openmc.HexLattice(name='Inner FA Lattice inner')
    lattice_in.center = (0.0, 0.0)
    lattice_in.pitch = (1.386,)
    lattice_in.orientation = 'x'
    

    rings = []
    for i in range(6, -1, -1):
        if i == 0:
            rings.append([fuel_pin_universe_in])
        else:
            rings.append([fuel_pin_universe_in] * (6 * i))
    
    lattice_in.universes = rings
    lattice_in.outer = openmc.Universe(cells=[openmc.Cell(fill=lead)])

  
    outer_surface_in = openmc.model.hexagonal_prism(edge_length=9.59, orientation='x')

    #lattice's cell
    cell_lattice_in = openmc.Cell(
        name="Lattice_Cell_In",
        fill=lattice_in, 
        region=in_surface_in & +p_fin[1] & -p_fin[6]
    )
    
    #wrapper's cell
    region_wrapper_in = (~in_surface_in & outer_surface_in) & (+p_fin[1] & -p_fin[6])
    cell_wrapper_in = openmc.Cell(
        name="Wrapper_Cell_In",
        fill=t91, 
        region=region_wrapper_in
    )

    coolant_surface_fin = openmc.model.hexagonal_prism(edge_length=9.873, orientation='x')
    region_coolant_fin = (~outer_surface_in & coolant_surface_fin) & (+p_fin[1] & -p_fin[6])
    cell_coolant_fin = openmc.Cell(
        name="coolant_surface_fin",
        fill=lead, 
        region=region_coolant_fin
    )


    #lead region
    regione_up_coolantfi = coolant_surface_fin & +p_fin[6] & -p_fin[7]
    regione_down_coolantfi = coolant_surface_fin & +p_fin[0] & -p_fin[1]

    cell_up_coolantfi = openmc.Cell(fill=lead, region=regione_up_coolantfi)
    cell_down_coolantfi = openmc.Cell(fill=lead, region=regione_down_coolantfi)


    fa_inner_universe = openmc.Universe(cells=[cell_lattice_in, cell_wrapper_in,cell_coolant_fin, cell_up_coolantfi, cell_down_coolantfi])

    return {
        'universe':fa_inner_universe
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
        u = get_fuel_inner_assembly(mats)

        #color map
        col_map = {
            mats['ti15_15']:  'blue',
            mats['lead']:     'cyan',
            mats['t91']:      'darkorange',
            mats['helium']:   'green',
            mats['helium']:   'green',
            mats['mox_inner']: 'yellow'
        }

        #plot XY
        u['universe'].plot(
            width=(22, 22), 
            basis='xy', 
            origin=(0, 0, 71), 
            color_by='material', 
            colors=col_map
        )
        plt.title("Vista XY innerfuel Assembly")
        plt.savefig('plot_innerfuel_xy.png')

        #Plot XZ
        plt.figure()
        u['universe'].plot(
            width=(25, 460), 
            basis='xz', 
            origin=(0, 0, -64.62), 
            color_by='material', 
            pixels=(1000, 8000),
            colors=col_map 
        )
        plt.title("Vista XZ innerfuel Assembly")
        plt.savefig('plot_innerfuel_xz.png')
        
        print("Plot salvati correttamente.")
        
    except Exception as e:
        print(f"ERRORE: {e}")