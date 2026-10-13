import openmc

def get_fuel_outer_assembly(mats):

    # materials' extraction
    helium = mats['helium']
    helium = mats['helium']
    lead = mats['lead']
    ti15_15 = mats['ti15_15']
    mox_outer = mats['mox_outer']
    t91 = mats['t91']

    #plans and geometry
    clad_r_out = 0.525
    gap_r_out = 0.465
    fuel_r_out = 0.45
    hollow_r_out = 0.1

    clad_cyl_out = openmc.ZCylinder(r = clad_r_out) 
    gap_cyl_out = openmc.ZCylinder(r = gap_r_out)  
    fuel_cyl_out = openmc.ZCylinder(r = fuel_r_out)
    hollow_cyl_out = openmc.ZCylinder(r = hollow_r_out)

    #              0      1    2     3     4      5      6      7
    z_coords = [-291.24, 0.0, 7.5, 62.5, 122.5, 134.5, 142.0, 162.0]
    p_out = [openmc.ZPlane(z0=z) for z in z_coords]

    #pin radial geometry
    gap_region_out = + fuel_cyl_out & - gap_cyl_out 
    fuel_region_out = + hollow_cyl_out & - fuel_cyl_out 
    hollow_region_out = - hollow_cyl_out

    gap_cell_out = openmc.Cell(name="Gap_in", fill = helium, region = gap_region_out) 
    fuel_cell_out = openmc.Cell(name = "Fuel_in", fill = mox_outer, region = fuel_region_out)
    hollow_cell_out = openmc.Cell(name = "Hollow_in", fill = helium, region = hollow_region_out) 
    
    pin_active_core_universe_out = openmc.Universe(cells=(hollow_cell_out, fuel_cell_out, gap_cell_out))

    #pin axial geometry
    region_plug_out = -gap_cyl_out & ((+p_out[1] & -p_out[2]) | (+p_out[5] & -p_out[6]))
    region_he_out   = -gap_cyl_out & ((+p_out[2] & -p_out[3]) | (+p_out[4] & -p_out[5]))
    region_mox_out  = -gap_cyl_out & (+p_out[3] & -p_out[4])
    
    region_cladding_out = (+gap_cyl_out & -clad_cyl_out) & (+p_out[1] & -p_out[6])

    region_pb_pin_out = (+clad_cyl_out) & (+p_out[1] & -p_out[6])

    c_plug_out = openmc.Cell(fill=ti15_15, region=region_plug_out)
    c_he_out   = openmc.Cell(fill=helium, region=region_he_out)
    c_mox_out  = openmc.Cell(fill=pin_active_core_universe_out, region=region_mox_out)
    c_clad_out = openmc.Cell(fill=ti15_15, region=region_cladding_out)
    c_pb_out   = openmc.Cell(fill=lead, region=region_pb_pin_out)


    fuel_pin_universe_out = openmc.Universe(cells=(c_plug_out, c_he_out, c_mox_out, c_clad_out, c_pb_out))

    #lattice
    in_surface_out = openmc.model.hexagonal_prism(edge_length=9.12, orientation='x')
    
    lattice_out = openmc.HexLattice(name='Inner FA Lattice out')
    lattice_out.center = (0.0, 0.0)
    lattice_out.pitch = (1.386,)
    lattice_out.orientation = 'x'
    

    rings = []
    for i in range(6, -1, -1):
        if i == 0:
            rings.append([fuel_pin_universe_out])
        else:
            rings.append([fuel_pin_universe_out] * (6 * i))
    
    lattice_out.universes = rings
    lattice_out.outer = openmc.Universe(cells=[openmc.Cell(fill=lead)])

  
    outer_surface_out = openmc.model.hexagonal_prism(edge_length=9.59, orientation='x')

    #lattice's cell
    cell_lattice_out = openmc.Cell(
        name="Lattice_Cell_out",
        fill=lattice_out, 
        region=in_surface_out & +p_out[1] & -p_out[6]
    )
    
    #wrapper's cell
    region_wrapper_out = (~in_surface_out & outer_surface_out) & (+p_out[1] & -p_out[6])
    cell_wrapper_out = openmc.Cell(
        name="Wrapper_Cell_out",
        fill=t91, 
        region=region_wrapper_out
    )

    coolant_surface_out = openmc.model.hexagonal_prism(edge_length=9.873, orientation='x')
    region_coolant_out = (~outer_surface_out & coolant_surface_out) & (+p_out[1] & -p_out[6])
    cell_coolant_out = openmc.Cell(
        name="coolant_surface_out",
        fill=lead, 
        region=region_coolant_out
    )


    #lead region
    regione_up_coolantout = coolant_surface_out & +p_out[6] & -p_out[7]
    regione_down_coolantout = coolant_surface_out & +p_out[0] & -p_out[1]

    cell_up_coolantout = openmc.Cell(fill=lead, region=regione_up_coolantout)
    cell_down_coolantout = openmc.Cell(fill=lead, region=regione_down_coolantout)


    fa_out_universe = openmc.Universe(cells=[cell_lattice_out, cell_wrapper_out,cell_coolant_out, cell_up_coolantout, cell_down_coolantout])

    return {
        'universe':fa_out_universe
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
        u = get_fuel_outer_assembly(mats)

        #color map
        col_map = {
            mats['ti15_15']:  'blue',
            mats['lead']:     'cyan',
            mats['t91']:      'darkorange',
            mats['helium']:   'green',
            mats['helium']:   'green',
            mats['mox_outer']: 'yellow'
        }
        #plot XY
        u['universe'].plot(
            width=(22, 22), 
            basis='xy', 
            origin=(0, 0, 71), 
            color_by='material', 
            colors=col_map
        )
        plt.title("Vista XY outerfuel Assembly")
        plt.savefig('plot_outerfuel_xy.png')

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
        plt.title("Vista XZ outerfuel Assembly")
        plt.savefig('plot_outerfuel_xz.png')
        
        print("Plot salvati correttamente.")
        
    except Exception as e:
        print(f"ERRORE: {e}")