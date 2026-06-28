import pandas as pd
import os
import f90nml
import glob

def read_output (output_dir, namelist_path):
  file_paths = glob.glob(f'{output_dir}/*.txt')

  output_df = pd.DataFrame()
  for out_file in file_paths:
    var_name = os.path.basename(out_file).split('.')[0]
    var_data = pd.read_csv(out_file, header=None)
    output_df[var_name] = var_data

  namelist = f90nml.read(namelist_path)

  t1 = pd.Timestamp (namelist['tebforcing']['iyear'], namelist['tebforcing']['imonth'],  namelist['tebforcing']['iday'])
  t2 = t1 + pd.Timedelta (seconds=namelist['tebforcing']['timestep']) * (namelist['tebforcing']['num_timesteps']-2)

  output_df.index = pd.date_range(t1, t2, freq=pd.Timedelta (seconds=namelist['tebforcing']['timestep']))
  return output_df

