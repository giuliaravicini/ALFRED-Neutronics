import openmc
openmc.config["cross_sections"] = "/mnt/c/Users/giuli/corso_openmc/ALFRED/endfb71/endfb-vii.1-hdf5/cross_sections.xml" 

def get_alfred_materials():
    #TiTi-1515
    ti15_15 = openmc.Material(name='15-15Ti-sr', material_id=1)
    ti15_15.add_element('Fe', 0.648, 'wo')
    ti15_15.add_element('Cr', 0.15, 'wo')
    ti15_15.add_element('Ni', 0.15, 'wo')
    ti15_15.add_element('Ti', 0.004, 'wo')
    ti15_15.add_element('Mo', 0.015, 'wo')
    ti15_15.add_element('Mn', 0.015, 'wo')
    ti15_15.add_element('Si', 0.009, 'wo')
    ti15_15.add_element('C', 0.009, 'wo')
    ti15_15.set_density('g/cm3', 7.695)
    ti15_15.temperature = 900

    #helium
    helium = openmc.Material(name='Helium-sr', material_id=2)
    helium.add_element('He', 1.0)
    helium.set_density('g/cm3', 0.000164) 
    helium.temperature = 900

    #zircaloy
    zircaloy=openmc.Material(name='zircaloy-sr', material_id=3)
    zircaloy.set_density('g/cm3', 5.889)
    f_zro2 = 0.95
    f_y2o3 = 0.05

    aw_zr = 91.224
    aw_y = 88.906
    aw_o = 15.999

    mw_zro2 = aw_zr + (2*aw_o)
    mw_y2o3 = (2*aw_y) + (3*aw_o)

    w_zr = f_zro2 * (aw_zr / mw_zro2)
    w_y = f_y2o3 * (2 * aw_y / mw_y2o3)
    w_o = f_zro2 * (2 * aw_o / mw_zro2) + f_y2o3 * (3 * aw_o / mw_y2o3)

    zircaloy.add_element('Zr', w_zr, 'wo')
    zircaloy.add_element('Y', w_y, 'wo')
    zircaloy.add_element('O', w_o, 'wo')
    zircaloy.temperature = 900

    #b4c
    b4c=openmc.Material(name='B4C-sr', material_id=4)
    b4c.set_density('g/cm3', 2.180)
    f_c = 0.218
    f_b = 0.782
    b4c.add_element("C", f_c, 'wo')
    b4c.add_nuclide("B10", f_b * 0.90, 'wo')
    b4c.add_nuclide("B11", f_b * 0.10, 'wo')
    b4c.temperature = 900

    #mox inner
    mox_inner = openmc.Material(name='MOX_Inner', material_id=5)
    mox_inner.set_density('g/cm3', 10.256)
    f_met = 0.882
    f_ox = 0.118

    mox_inner.add_element('O', f_ox, 'wo')

    mox_inner.add_nuclide('Pu238', f_met * (2.332 / 100) * 0.207, 'wo')
    mox_inner.add_nuclide('Pu239', f_met * (56.873 / 100) * 0.207, 'wo')
    mox_inner.add_nuclide('Pu240', f_met * (26.997 / 100) * 0.207, 'wo')
    mox_inner.add_nuclide('Pu241', f_met * (6.105 / 100) * 0.207, 'wo')
    mox_inner.add_nuclide('Pu242', f_met * (7.693 / 100) * 0.207, 'wo')

    mox_inner.add_nuclide('U234', f_met * (0.003 / 100) * 0.783, 'wo')
    mox_inner.add_nuclide('U235', f_met * (0.404 / 100) * 0.783, 'wo')
    mox_inner.add_nuclide('U236', f_met * (0.01 / 100) * 0.783, 'wo')
    mox_inner.add_nuclide('U238', f_met * (99.583 / 100) * 0.783, 'wo')

    mox_inner.add_nuclide('Am241', f_met * 0.010, 'wo')
    mox_inner.temperature = 1200


    #mox outer(-10% MOX, -10% He, -2% Ti1515)
    mox_outer = openmc.Material(name='MOX_Outer', material_id=6)
    mox_outer.set_density('g/cm3', 10.283)

    mox_outer.add_element('O', f_ox, 'wo')

    mox_outer.add_nuclide('Pu238', f_met * (2.332 / 100) * 0.268, 'wo')
    mox_outer.add_nuclide('Pu239', f_met * (56.873 / 100) * 0.268, 'wo')
    mox_outer.add_nuclide('Pu240', f_met * (26.997 / 100) * 0.268, 'wo')
    mox_outer.add_nuclide('Pu241', f_met * (6.105 / 100) * 0.268, 'wo')
    mox_outer.add_nuclide('Pu242', f_met * (7.693 / 100) * 0.268, 'wo')

    mox_outer.add_nuclide('U234', f_met * (0.003 / 100) * 0.722, 'wo')
    mox_outer.add_nuclide('U235', f_met * (0.404 / 100) * 0.722, 'wo')
    mox_outer.add_nuclide('U236', f_met * (0.010 / 100) * 0.722, 'wo')
    mox_outer.add_nuclide('U238', f_met * (99.583 / 100) * 0.722, 'wo')

    mox_outer.add_nuclide('Am241', f_met * 0.010, 'wo')
    mox_outer.temperature = 1200

    #lead
    lead = openmc.Material(name='Lead', material_id=7)
    lead.add_element('Pb', 1.0)
    lead.set_density('g/cm3', 10.292)
    lead.temperature = 900

    #T91 
    t91 = openmc.Material(name='T91', material_id=8)
    t91.set_density('g/cm3', 7.604) 
    t91.add_element('C', 0.001, 'wo')
    t91.add_element('Fe', 0.884, 'wo')
    t91.add_element('Cr', 0.09, 'wo')
    t91.add_element('Mo', 0.01, 'wo')
    t91.add_element('Mn', 0.0045, 'wo')
    t91.add_element('Si', 0.0035, 'wo')
    t91.add_element('V', 0.002, 'wo')
    t91.add_element('Ni', 0.004, 'wo')
    t91.add_element('Nb', 0.001, 'wo')
    t91.temperature = 900


    return {
        'ti15_15': ti15_15,
        'helium': helium,
        'zircaloy': zircaloy,
        'b4c': b4c,
        'mox_inner': mox_inner,
        'mox_outer': mox_outer,
        'lead': lead,
        't91': t91
    }


#execution block
if __name__ == "__main__":
    mats_dict = get_alfred_materials()
    mats_collection = openmc.Materials(mats_dict.values())
    mats_collection.export_to_xml()
    print("File materials.xml generato")