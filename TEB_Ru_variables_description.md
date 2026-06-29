# TEB-Ru Model Variables Description

This document provides a comprehensive description of all input (namelist) and output variables used in the TEB-Ru model.

## Namelist Variables

These variables are defined in the Fortran namelist files (`namelist.nml` and `namelist_forcing.nml`) and control the model configuration.

### Basic Building Characteristics

| Variable | Type | Dimension/Value | Comment |
|:---------|:-----|:----------------|:--------|
| `dt` | External parameter | s | Model time step |
| `urb_h_bld` | External parameter | m | Average canyon height |
| `urb_fr_bld` | External parameter | - | Building area fraction |
| `urb_h2w` | External parameter | - | Canyon aspect ratio |
| `teb_road_dir` | External parameter | ° | Canyon azimuth |
| `teb_hroad_dir` | Control variable | "UNIF" / "ORIE" | Canyon orientation: ORIE - with orientation, UNIF - without |
| `teb_wall_opt` | Control variable | "UNIF" / "TWO" | Wall energy balance: TWO - separate walls, UNIF - uniform |
| `teb_ti_bld` | Prognostic variable | K | Indoor air temperature |
| `teb_qi_bld` | Prognostic variable | kg/kg | Indoor specific humidity |

### Surface Properties

| Variable | Type | Dimension/Value | Comment |
|:---------|:-----|:----------------|:--------|
| `urb_alb_rf_so` | External parameter | - | Roof surface albedo |
| `urb_alb_rf_th` | External parameter | - | Roof surface emissivity |
| `urb_hcap_rf` | External parameter | J/m³/K | Roof layers volumetric heat capacity |
| `urb_hcon_rf` | External parameter | W/m/K | Roof layers thermal conductivity |
| `urb_alb_rd_so` | External parameter | - | Road surface albedo |
| `urb_alb_rd_th` | External parameter | - | Road surface emissivity |
| `urb_hcap_rd` | External parameter | J/m³/K | Road layers volumetric heat capacity |
| `urb_hcon_rd` | External parameter | W/m/K | Road layers thermal conductivity |
| `urb_alb_wl_so` | External parameter | - | Wall surface albedo |
| `urb_alb_wl_th` | External parameter | - | Wall surface emissivity |
| `urb_hcap_wl` | External parameter | J/m³/K | Wall layers volumetric heat capacity |
| `urb_hcon_wl` | External parameter | W/m/K | Wall layers thermal conductivity |

### Building Energy Model (BEM)

| Variable | Type | Dimension/Value | Comment |
|:---------|:-----|:----------------|:--------|
| `teb_itype_bem` | Control variable | "BEM" / "DEF" | Activate BEM model |
| `teb_lbem_ac` | Flag | True / False | Activate air conditioning |
| `teb_itype_natvent` | Control variable | "NONE" / "MANU" / "AUTO" / "MECH" | Natural ventilation mode |
| `teb_itype_bem_cool` | Control variable | "DXCOIL" / "IDEAL " | Cooling system type |
| `teb_itype_bem_heat` | Control variable | "FINCAP" / "IDEAL " | Heating system type |
| `teb_frac_gz` | External parameter | - | Glazing ratio |
| `teb_tcool_target` | External parameter | K | Cooling setpoint temperature |
| `teb_theat_target` | External parameter | K | Heating setpoint temperature |
| `teb_zresidential` | External parameter | - | Residential fraction of building |
| `teb_dt_res` | External parameter | K | Temperature change threshold for unoccupied residential building |
| `teb_dt_off` | External parameter | K | Temperature change threshold for unoccupied office building |
| `teb_bem_inf` | External parameter | AC/H | Infiltration rate |
| `teb_bem_vent` | External parameter | AC/H | Ventilation rate |
| `teb_bem_cop` | External parameter | - | Nominal COP of cooling system |
| `teb_cap_sys_rat` | External parameter | W/m²(building) | Nominal cooling system capacity (for "DXCOIL" type) |
| `teb_m_sys_rat` | External parameter | kg/s/m²(building) | Nominal HVAC mass flow rate |
| `teb_cap_sys_heat` | External parameter | W/m²(building) | Heating system capacity |
| `teb_lshade` | External parameter | True / False | Activate window shading (not verified) |

### Anthropogenic Heat Fluxes

| Variable | Type | Dimension/Value | Comment |
|:---------|:-----|:----------------|:--------|
| `ahf_traffic` | External parameter | W/m² | Sensible heat flux from traffic |
| `ahf_industry` | External parameter | W/m² | Sensible heat flux from industry |

### Wind Inside Urban Canopy

| Variable | Type | Dimension/Value | Comment |
|:---------|:-----|:----------------|:--------|
| `teb_itype_wind` | Control variable | 0 / 1 | Wind speed calculation: 0 - basic scheme, 1 - Wang (2012) parameterization |
| `teb_fai` | External parameter | - | Frontal area index for 8 wind directions |

### Green Infrastructure

| Variable | Type | Dimension/Value | Comment |
|:---------|:-----|:----------------|:--------|
| `teb_lgarden` | Flag | True / False | Activate garden module |
| `fr_garden` | External parameter | - | Garden area fraction |
| `teb_lgreenroof` | Flag | True / False | Activate green roof module |
| `teb_frac_gr` | External parameter | - | Green roof fraction |

### Solar Panels

| Variable | Type | Dimension/Value | Comment |
|:---------|:-----|:----------------|:--------|
| `teb_lsolar_panel` | Flag | True / False | Activate solar panel module |
| `teb_fr_panel` | External parameter | - | Solar panel fraction on roofs |

### Street Watering

| Variable | Type | Dimension/Value | Comment |
|:---------|:-----|:----------------|:--------|
| `teb_lroad_irrig` | Flag | True / False | Activate street watering module |
| `teb_rd_irrig_start_m` | External parameter | - | Start month for watering |
| `teb_rd_irrig_end_m` | External parameter | - | End month for watering |
| `teb_rd_irrig_start_h` | External parameter | - | Start hour for watering |
| `teb_rd_irrig_end_h` | External parameter | - | End hour for watering |
| `teb_rd_irrig_sum` | External parameter | liter/m² | 24-hour water amount for road watering |

---

## Output Variables

These variables are written to output files during model simulation.

| Variable | Dimension | Comment |
|:---------|:-----------|:--------|
| `T_CANYON` | K | Canyon air temperature |
| `Q_CANYON` | kg/kg | Canyon air specific humidity |
| `U_CANYON` | m/s | Canyon wind speed |
| `P_CANYON` | Pa | Atmospheric pressure |
| `T_ROOF1` | K | Roof surface temperature |
| `T_ROAD1` | K | Road surface temperature |
| `T_WALLA1` | K | Wall A surface temperature |
| `T_WALLB1` | K | Wall B surface temperature |
| `TI_BLD` | K | Indoor air temperature |
| `H_TOWN` | W/m² | Sensible heat flux from urban canyon |
| `LE_TOWN` | W/m² | Latent heat flux from urban canyon |
| `RN_TOWN` | W/m² | Net radiation of urban canyon effective surface |
| `HVAC_COOL` | W/m²(building) | Cooling energy consumption |
| `HVAC_HEAT` | W/m²(building) | Heating energy consumption |
| `SOLAR_PROD` | W/m²(building) | Average solar panel energy production |

---

## Notes

- **External parameters**: Set in namelist files and remain constant during simulation
- **Control variables**: Enable/disable specific model features
- **Flags**: Boolean switches for module activation
- **Prognostic variables**: Evolve over time during the simulation
- **Output variables**: Model results written to output files

For more information, see the model documentation and the original TEB references.
