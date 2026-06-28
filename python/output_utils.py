import pandas as pd
import os
import f90nml
import glob

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def read_output (output_dir, namelist_path):
  file_paths = glob.glob(f'{output_dir}/*.txt')

  output_df = pd.DataFrame()
  for out_file in file_paths:
    var_name = os.path.basename(out_file).split('.')[0]
    try:
      var_data = pd.read_csv(out_file, header=None)
    except pd.errors.EmptyDataError:
      print (f'{out_file} is empty, skipping') 

    output_df[var_name] = var_data

  namelist = f90nml.read(namelist_path)
  t1 = pd.Timestamp (namelist['tebforcing']['teb_year'], namelist['tebforcing']['teb_month'],  namelist['tebforcing']['teb_day'])
  t2 = t1 + pd.Timedelta (seconds=namelist['tebforcing']['forc_step']) * (namelist['tebforcing']['nsteps']-2)
  output_df.index = pd.date_range(t1, t2, freq=pd.Timedelta (seconds=namelist['tebforcing']['forc_step']))
  return output_df



# ============================================================================
# Default configuration for subplots (used by both backends)
# ============================================================================
DEFAULT_SUBPLOTS_CONFIG = [
    {
        'variables': ['TI_BLD', 'T_CANYON', 'T_ROOF1', 'T_WALLA1', 'T_WALLB1'],
        'title': 'Temperatures',
        'ylabel': 'Temperature (K)',
        'labels': ['Indoor', 'Canyon', 'Roof', 'Wall A', 'Wall B']
    },
    {
        'variables': ['U_CANYON'],
        'title': 'Canyon Wind Speed',
        'ylabel': 'Wind speed (m/s)'
    },
    {
        'variables': ['H_TOWN', 'LE_TOWN'],
        'title': 'Turbulent Heat Fluxes',
        'ylabel': 'Heat flux (W/m²)',
        'labels': ['Sensible (H)', 'Latent (LE)'],
        'colors': ['#e41a1c', '#4daf4a']
    },
    {
        'variables': ['RN_TOWN'],
        'title': 'Net Radiation',
        'ylabel': 'Net radiation (W/m²)'
    },
    {
        'variables': ['HVAC_HEAT', 'HVAC_COOL'],
        'title': 'HVAC Energy Consumption',
        'ylabel': 'Energy (W/m²)',
        'labels': ['Heating', 'Cooling'],
        'colors': ['#d95f02', '#1f78b4']
    }
]


def preview_output_mpl(df, subplots_config=None, figsize=(10, 18), save_path=None, dpi=300):
    """
    Preview TEB-Ru outputs using Matplotlib.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame with model outputs.
    subplots_config : list of dict, optional
        Configuration for subplots. If None, uses DEFAULT_SUBPLOTS_CONFIG.
    figsize : tuple, optional
        Figure size (width, height) in inches.
    save_path : str, optional
        Path to save figure (.png, .pdf, etc.). If None, figure is displayed.
    dpi : int, optional
        Resolution for saved figure.
    
    Returns:
    --------
    fig : matplotlib.figure.Figure
    axes : numpy.ndarray
    """
    
    if subplots_config is None:
        subplots_config = DEFAULT_SUBPLOTS_CONFIG
    
    n_rows = len(subplots_config)
    fig, axes = plt.subplots(n_rows, 1, figsize=figsize, sharex=True)
    
    if n_rows == 1:
        axes = [axes]
    
    x = df.index
    
    for idx, config in enumerate(subplots_config):
        ax = axes[idx]
        
        variables = config.get('variables', [])
        title = config.get('title', '')
        ylabel = config.get('ylabel', '')
        labels = config.get('labels', None)
        colors = config.get('colors', None)
        linestyles = config.get('linestyles', None)
        linewidths = config.get('linewidths', None)
        
        # Filter valid variables
        valid_vars = [v for v in variables if v in df.columns and not df[v].isna().all()]
        
        if not valid_vars:
            ax.text(0.5, 0.5, 'No data available', ha='center', va='center', transform=ax.transAxes,
                   fontsize=12, color='gray')
            ax.set_title(title)
            ax.grid(True, alpha=0.3)
            continue
        
        # Prepare legend labels
        if labels is None:
            leg_labels = valid_vars
        else:
            leg_labels = [labels[i] for i, v in enumerate(variables) if v in df.columns and not df[v].isna().all()]
            if len(leg_labels) != len(valid_vars):
                leg_labels = valid_vars
        
        # Colors
        if colors is None:
            color_cycle = plt.rcParams['axes.prop_cycle'].by_key()['color']
            colors = [color_cycle[i % len(color_cycle)] for i in range(len(valid_vars))]
        else:
            colors = [colors[i] for i, v in enumerate(variables) if v in df.columns and not df[v].isna().all()]
            if len(colors) != len(valid_vars):
                color_cycle = plt.rcParams['axes.prop_cycle'].by_key()['color']
                colors = [color_cycle[i % len(color_cycle)] for i in range(len(valid_vars))]
        
        # Linestyles
        if linestyles is None:
            linestyles = ['-'] * len(valid_vars)
        else:
            linestyles = [linestyles[i] for i, v in enumerate(variables) if v in df.columns and not df[v].isna().all()]
            if len(linestyles) != len(valid_vars):
                linestyles = ['-'] * len(valid_vars)
        
        # Linewidths
        if linewidths is None:
            linewidths = [2] * len(valid_vars)
        else:
            linewidths = [linewidths[i] for i, v in enumerate(variables) if v in df.columns and not df[v].isna().all()]
            if len(linewidths) != len(valid_vars):
                linewidths = [2] * len(valid_vars)
        
        # Plot
        for var, label, color, ls, lw in zip(valid_vars, leg_labels, colors, linestyles, linewidths):
            ax.plot(x, df[var], label=label, color=color, linestyle=ls, linewidth=lw)
        
        if ylabel:
            ax.set_ylabel(ylabel)
        if title:
            ax.set_title(title)
        
        if len(valid_vars) > 1:
            ax.legend(loc='upper right', fontsize=8)
        
        ax.grid(True, alpha=0.3)
    
    axes[-1].set_xlabel('Time')
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=dpi, bbox_inches='tight')
        print(f"Figure saved to: {save_path}")
    
    return fig, axes


def preview_output_plotly(df, subplots_config=None, save_path=None, height=None):
    """
    Preview TEB-Ru outputs using Plotly (interactive).
    
    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame with model outputs.
    subplots_config : list of dict, optional
        Configuration for subplots. If None, uses DEFAULT_SUBPLOTS_CONFIG.
    save_path : str, optional
        Path to save figure (.html recommended). If None, figure is displayed.
    height : int, optional
        Height of the figure in pixels. If None, automatically calculated based on number of subplots.
    
    Returns:
    --------
    fig : plotly.graph_objects.Figure
    """
    
    try:
        import plotly.graph_objects as go
        from plotly.subplots import make_subplots
    except ImportError:
        raise ImportError("Plotly is required for preview_output_plotly. Install with: pip install plotly")
    
    if subplots_config is None:
        subplots_config = DEFAULT_SUBPLOTS_CONFIG
    
    n_rows = len(subplots_config)
    
    # Calculate appropriate height if not provided
    if height is None:
        height = max(800, n_rows * 250)
    
    # Create subplot grid with shared x-axis
    fig = make_subplots(rows=n_rows, cols=1, shared_xaxes=True,
                        vertical_spacing=0.08,
                        subplot_titles=[cfg.get('title', '') for cfg in subplots_config])
    
    x = df.index
    
    for row_idx, config in enumerate(subplots_config, start=1):
        variables = config.get('variables', [])
        ylabel = config.get('ylabel', '')
        labels = config.get('labels', None)
        colors = config.get('colors', None)
        linestyles = config.get('linestyles', None)
        linewidths = config.get('linewidths', None)
        
        # Filter valid variables
        valid_vars = [v for v in variables if v in df.columns and not df[v].isna().all()]
        
        if not valid_vars:
            # Add empty trace with annotation if no data
            fig.add_trace(go.Scatter(x=[], y=[], name='No data', showlegend=False), row=row_idx, col=1)
            continue
        
        # Prepare legend labels
        if labels is None:
            leg_labels = valid_vars
        else:
            leg_labels = [labels[i] for i, v in enumerate(variables) if v in df.columns and not df[v].isna().all()]
            if len(leg_labels) != len(valid_vars):
                leg_labels = valid_vars
        
        # Colors (default Plotly colors)
        if colors is None:
            colors = [None] * len(valid_vars)  # will use default plotly colors
        else:
            colors = [colors[i] for i, v in enumerate(variables) if v in df.columns and not df[v].isna().all()]
            if len(colors) != len(valid_vars):
                colors = [None] * len(valid_vars)
        
        # Linestyles
        if linestyles is None:
            linestyles = ['solid'] * len(valid_vars)
        else:
            linestyles = [linestyles[i] for i, v in enumerate(variables) if v in df.columns and not df[v].isna().all()]
            if len(linestyles) != len(valid_vars):
                linestyles = ['solid'] * len(valid_vars)
        
        # Linewidths
        if linewidths is None:
            linewidths = [2] * len(valid_vars)
        else:
            linewidths = [linewidths[i] for i, v in enumerate(variables) if v in df.columns and not df[v].isna().all()]
            if len(linewidths) != len(valid_vars):
                linewidths = [2] * len(valid_vars)
        
        # Add traces
        for var, label, color, ls, lw in zip(valid_vars, leg_labels, colors, linestyles, linewidths):
            fig.add_trace(
                go.Scatter(
                    x=x,
                    y=df[var],
                    mode='lines',
                    name=label,
                    line=dict(color=color, dash=ls, width=lw)
                ),
                row=row_idx, col=1
            )
        
        # Update y-axis label
        if ylabel:
            fig.update_yaxes(title_text=ylabel, row=row_idx, col=1)
    
    # Update x-axis label on the last subplot
    fig.update_xaxes(title_text='Time', row=n_rows, col=1)
    
    # Update layout
    fig.update_layout(
        height=height,
        showlegend=True,
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
        hovermode='x unified'
    )
    
    # Save or show
    if save_path:
        if save_path.endswith('.html'):
            fig.write_html(save_path)
        else:
            # Try to save as static image (requires kaleido)
            try:
                fig.write_image(save_path)
            except Exception as e:
                print(f"Could not save as image. Saving as HTML instead: {save_path}.html")
                fig.write_html(save_path + '.html')
        print(f"Figure saved to: {save_path}")
    
    return fig

