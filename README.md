# TEB-Ru: Single-Layer Urban Canopy Model

[![Fortran](https://img.shields.io/badge/Fortran-734f96?logo=fortran&logoColor=white)](https://fortran-lang.org/)
[![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-CeCILL--C-blue.svg)](https://cecill.info/licences/Licence_CeCILL-C_V1-en.html)

TEB-Ru is a single-layer urban canopy model developed at Lomonosov Moscow State University based on the popular French open-source model TEB (Town Energy Balance) [[Masson, 2000]](#references). This model provides simplified but computationally effective parameterization of turbulent and radiant energy exchange within the urban canopy described as an idealized street canyon, considering building energy use, including heating and air conditioning, simulated by building energy model (BEM) [[Bueno et al., 2012]](#references). It also allows representing urban vegetation inside the street canyon [[Lemonsu et al., 2012]](#references) and on buildings' roofs [[De Munck et al., 2013]](#references), as well as solar panels on the roofs.

## Key Features

- **Single-layer urban canopy scheme** with idealized street canyon geometry
- **Building Energy Model (BEM)** for simulating heating and air conditioning energy use
- **Urban vegetation** inside street canyons and on green roofs
- **Solar panels** on building roofs
- **Advanced wind profile** parameterization following [[Wang, 2012]](#references) verified with microscale modelling [[Tarasova et al., 2024]](#references)
- **Anthropogenic heat flux** from traffic with diurnal cycle parameterization
- **Flexible coupling interface** for standalone mode with given atmospheric forcing or two-way coupling with atmospheric models (e.g., COSMO) [[Tarasova et al., 2025]](#references)

## Distinctive Features of TEB-Ru

Compared to the original TEB model, TEB-Ru includes:

- **Improvements to physical parameterizations** and their adaptation to Russian cities
- **Elaborate program interfaces** for easier coupling and configuration
- **Multiple modifications to BEM** for better representation of urban energy consumption
- **New wind speed profile parameterization** following the Wang (2012) approach
- **New parameterization of diurnal cycle** of anthropogenic heat flux from traffic
- **New interface for coupling with land surface models** for describing soil and vegetation in street canyons
- **Flexible mode switching** between standalone and coupled operation
- **Python library suite** for preparing atmospheric forcing data, including utilities for processing meteorological observations, reanalysis data, and generating input files for offline simulations

### Quick Start

#### Option 1: Google Colab (Recommended)

Open and run the [`run_in_collab.ipynb`](https://github.com/mkolennikova/TEB-Ru/blob/main/run_in_collab.ipynb) notebook in Google Colab. It will automatically:

1. Clone the repository
2. Set up the environment
3. Compile the model
4. Download meteorological forcing 
5. Run a test simulation
6. Visualize results

#### Option 2: Local Build

To build and run TEB-Ru locally:

# Clone the repository
git clone https://github.com/mkolennikova/TEB-Ru.git
cd TEB-Ru

# Check compiler flags in gfortran_args
# The model automatically detects ifort or gfortran

# Build the model
make clean
make

# Run the model
./TEB_offline.exe

## Configuration

Model configuration is controlled through Fortran namelist files in the [`namelist/`](https://github.com/mkolennikova/TEB-Ru/tree/main/namelist) directory:

- **[namelist_forcing.nml](https://github.com/mkolennikova/TEB-Ru/blob/main/namelist/namelist_forcing.nml)** – Atmospheric forcing parameters (temperature, humidity, wind, radiation, precipitation, etc.)
- **[namelist.nml](https://github.com/mkolennikova/TEB-Ru/blob/main/namelist/namelist.nml)** – Urban geometry, material properties, BEM parameters, vegetation settings, and other model options

### Compiler Flags

Compiler settings are defined in [`gfortran_args`](https://github.com/mkolennikova/TEB-Ru/blob/main/gfortran_args). The model automatically detects the available compiler:

- `ifort` – Intel Fortran Compiler (if available)
- `gfortran` – GNU Fortran Compiler (fallback)

Key compilation flags:
- `-ffree-line-length-0` – Allow unlimited line length (avoids line truncation errors)
- `-fdefault-real-8` – Use double precision real numbers
- `-J$(OBJDIR)` – Place module files in the `obj/` directory

## References

1. [Bueno, B., Pigeon, G., Norford, L.K., Zibouche, K., Marchadier, C., 2012. Development and evaluation of a building energy model integrated in the TEB scheme. Geoscientific Model Development 5, 433–448.](https://doi.org/10.5194/gmd-5-433-2012)

2. [De Munck, C.S., Lemonsu, A., Bouzouidja, R., Masson, V., Claverie, R., 2013. The GREENROOF module (v7.3) for modelling green roof hydrological and energetic performances within TEB. Geoscientific Model Development 6, 1941–1960.](https://doi.org/10.5194/gmd-6-1941-2013)

3. [Lemonsu, A., Masson, V., Shashua-Bar, L., Erell, E., Pearlmutter, D., 2012. Inclusion of vegetation in the Town Energy Balance model for modelling urban green areas. Geoscientific Model Development 5, 1377–1393.](https://doi.org/10.5194/gmd-5-1377-2012)

4. [Masson, V., 2000. A Physically-Based Scheme For The Urban Energy Budget In Atmospheric Models. Boundary-Layer Meteorology 94, 357–397.](https://doi.org/10.1023/A:1002463829265)

5. [Meyer, D., Schoetter, R., Masson, V., Grimmond, S., 2020. Enhanced software and platform for the Town Energy Balance (TEB) model. Journal of Open Source Software 5, 2008.](https://doi.org/10.21105/joss.02008)

6. [Tarasova, M.A., Debolskiy, A.V., Mortikov, E.V., Varentsov, M.I., Glazunov, A.V., Stepanenko, V.M., 2024. On the Parameterization of the Mean Wind Profile for Urban Canopy Models. Lobachevskii Journal of Mathematics 45, 3198–3210.](https://doi.org/10.1134/S1995080224603801)

7. [Tarasova, M.A., Varentsov, M.I., Debolskiy, A.V., Stepanenko, V.M., 2025. Coupling the Town Energy Balance (TEB) Scheme with the COSMO Atmospheric Model: Evaluation Against a Bulk Parameterization (TERRA_URB) for the Moscow Megacity. GES 18, 118–134.](https://doi.org/10.24057/2071-9388-2025-3975)

8. [Wang, W., 2012. An Analytical Model for Mean Wind Profiles in Sparse Canopies. Boundary-Layer Meteorology 142, 383–399.](https://doi.org/10.1007/s10546-011-9687-0)

## Citation

If you use TEB-Ru in your research, please cite:

> [Tarasova, M.A., Varentsov, M.I., Debolskiy, A.V., Stepanenko, V.M., 2025. Coupling the Town Energy Balance (TEB) Scheme with the COSMO Atmospheric Model: Evaluation Against a Bulk Parameterization (TERRA_URB) for the Moscow Megacity. GES 18, 118–134.](https://doi.org/10.24057/2071-9388-2025-3975)

Also, please cite the original TEB model and the relevant references listed above.

## License

TEB-Ru is distributed under the [CeCILL-C](https://cecill.info/licences/Licence_CeCILL-C_V1-en.html) license, following the original TEB model.

## Acknowledgments

TEB-Ru development is supported by Lomonosov Moscow State University and acknowledges the original TEB model development team at CNRM (Météo-France/CNRS).
