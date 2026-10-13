import openmc

def get_dummy_assembly(mats):

    # materials' extraction
    zircaloy = mats['zircaloy'] 
    ti15_15 = mats['ti15_15']
    lead = mats['lead']
    t91 = mats['t91']

    #z plans and region
    #              0      1     2      3
    z_coords = [-291.24, 0.0, 142.0, 162.0]
    p_d = [openmc.ZPlane(z0=z) for z in z_coords]

    dummy_r = 0.465
    clad_dummy_r = 0.525
    dummy_cyl = openmc.ZCylinder(r=dummy_r) 
    clad_dummy_cyl = openmc.ZCylinder(r=clad_dummy_r) 

    #cells
    c_dummy = openmc.Cell(fill=zircaloy, region=-dummy_cyl & +p_d[1] & -p_d[2])
    c_clad = openmc.Cell(fill=ti15_15, region=+dummy_cyl & -clad_dummy_cyl & +p_d[1] & -p_d[2])

    #lead between pins
    c_pb_pin = openmc.Cell(fill=lead, region=+clad_dummy_cyl & +p_d[1] & -p_d[2]) 
    pin_dummy_univ = openmc.Universe(cells=(c_dummy, c_clad, c_pb_pin))

    #exagonal surfaces
    hex_inner = openmc.model.hexagonal_prism(edge_length=9.12, orientation='x')
    hex_outer = openmc.model.hexagonal_prism(edge_length=9.59, orientation='x')
    hex_coolant = openmc.model.hexagonal_prism(edge_length=9.873, orientation='x')
    
    #Lattice
    common_z = +p_d[1] & -p_d[2]
    lattice_d = openmc.HexLattice(name='Dummy Lattice')
    lattice_d.center = (0.0, 0.0)
    lattice_d.pitch = (1.386,)
    lattice_d.orientation = 'x'
    
    rings = []
    for i in range(6, -1, -1):
        rings.append([pin_dummy_univ] * (max(1, 6 * i)))
    
    lattice_d.universes = rings
    lattice_d.outer = openmc.Universe(cells=[openmc.Cell(fill=lead)])

    cell_lattice_d = openmc.Cell(fill=lattice_d, region=hex_inner & common_z)

    cell_wrapper_d = openmc.Cell(fill=t91, region=~hex_inner & hex_outer & common_z)

    cell_coolant_d = openmc.Cell(fill=lead, region=~hex_outer & hex_coolant & common_z)

    #upper and lower zones
    cell_up_controldu = openmc.Cell(fill=lead, region=hex_coolant & +p_d[2] & -p_d[3])
    cell_down_controldu = openmc.Cell(fill=lead, region=hex_coolant & +p_d[0] & -p_d[1])

    fa_dummy_universe = openmc.Universe(cells=[
        cell_lattice_d, 
        cell_wrapper_d, 
        cell_coolant_d, 
        cell_up_controldu, 
        cell_down_controldu
    ])

    return {
        'universe': fa_dummy_universe
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
        u = get_dummy_assembly(mats)

        #color map
        col_map = {
            mats['zircaloy']: 'lightgray',
            mats['ti15_15']:  'blue',
            mats['lead']:     'cyan',
            mats['t91']:      'darkorange'
        }

        #plot XY
        u['universe'].plot(
            width=(22, 22), 
            basis='xy', 
            origin=(0, 0, 71), 
            color_by='material', 
            colors=col_map
        )
        plt.title("Vista XY Dummy Assembly")
        plt.savefig('plot_dummy_xy.png')

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
        plt.title("Vista XZ Dummy Assembly")
        plt.savefig('plot_dummy_xz.png')
        
        print("Plot salvati correttamente.")
        
    except Exception as e:
        print(f"ERRORE: {e}")