from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib as mpl
import seaborn as sns
mpl.use("agg")
import matplotlib.pyplot as plt  # noqa: E402
mpl.rcParams['font.size'] = 8
mpl.rcParams['axes.titlesize'] = 8
mpl.rcParams['axes.labelsize'] = 9
mpl.rcParams['xtick.labelsize'] = 8
mpl.rcParams['ytick.labelsize'] = 8
mpl.rcParams['legend.fontsize'] = 8
mpl.rcParams['legend.title_fontsize'] = 9
sns.set_style("ticks")
sns.plotting_context("paper", font_scale=1, rc={'font.size': 8.0,
                                                'axes.labelsize': 8.0,
                                                'axes.titlesize': 9.0,
                                                'xtick.labelsize': 8.0,
                                                'ytick.labelsize': 8.0,
                                                'legend.fontsize': 8.0,
                                                'legend.title_fontsize': 9.0})

base_path = Path(__file__).parent

# abbreviations of selected scientific journals
journals = ['JH', 'HP', 'WRR', 'HESS', 'HS', 'JHM', 'ESM', 'GRL', 'AWR', 'ERL', 'GMD']
journal_labels = {'JH': 'Journal of Hydrology', 
                  'HP': 'Hydrological Processes',  
                  'WRR': 'Water Resources Research',  
                  'HESS': 'Hydrol. Earth Syst. Sci.',  
                  'HS': 'Hydrological Sciences Journal',  
                  'JHM': 'Journal of Hydrometeorology',  
                  'ESM': 'Environmental Software & Modelling',  
                  'GRL': 'Geophysical Research Letters',  
                  'AWR': 'Advances in Water Resources',  
                  'ERL': 'Environmental Research Letters',  
                  'GMD': 'Geosci. Model Dev.'}

# abbreviations of soil hydrological models
models = ['HYDRUS', 'Hydrogeosphere', 'ParFlow', 'mHM']

# investigated period. First data and code sharing platforms were introduced in year 2010
idx = pd.date_range(start='2010-01-01', end='2022-01-01', freq='Y')
# data for journals
df_journals = pd.DataFrame(index=idx)
# open-access
df_journals_oa = pd.DataFrame(index=idx)
# open-access + code/data availability
df_journals_oaa = pd.DataFrame(index=idx)
# data for models
df_models = pd.DataFrame(index=idx)
# open-access
df_models_oa = pd.DataFrame(index=idx)
# open-access + code/data availability
df_models_oaa = pd.DataFrame(index=idx)

# join data for journals into a single dataframes
for journal in journals:
    file = base_path / 'data' / 'by_journals' / f'{journal}.txt'
    data = pd.read_csv(file, sep='\t', index_col=0)
    data = data.sort_index()
    data1 = pd.DataFrame(index=range(2011, 2023))
    data1 = data1.join(data)
    data1.index = idx
    df_journals.loc[:, journal] = data1.iloc[:, 0].values

    file = base_path / 'data' / 'by_journals' / f'{journal}_open-access.txt'
    data = pd.read_csv(file, sep='\t', index_col=0)
    data = data.sort_index()
    data1 = pd.DataFrame(index=range(2011, 2023))
    data1 = data1.join(data)
    data1.index = idx
    df_journals_oa.loc[:, journal] = data1.iloc[:, 0].values

    file = base_path / 'data' / 'by_journals' / f'{journal}_open-access_availability.txt'
    data = pd.read_csv(file, sep='\t', index_col=0)
    data = data.sort_index()
    data1 = pd.DataFrame(index=range(2011, 2023))
    data1 = data1.join(data)
    data1.index = idx
    df_journals_oaa.loc[:, journal] = data1.iloc[:, 0].values

# join data for models into a single dataframes
for model in models:
    file = base_path / 'data' / 'by_models' / f'{model}.txt'
    data = pd.read_csv(file, sep='\t', index_col=0)
    data = data.sort_index()
    data1 = pd.DataFrame(index=range(2011, 2023))
    data1 = data1.join(data)
    data1.index = idx
    df_models.loc[:, model] = data1.iloc[:, 0].values

    file = base_path / 'data' / 'by_models' / f'{model}_open-access.txt'
    data = pd.read_csv(file, sep='\t', index_col=0)
    data = data.sort_index()
    data1 = pd.DataFrame(index=range(2011, 2023))
    data1 = data1.join(data)
    data1.index = idx
    df_models_oa.loc[:, model] = data1.iloc[:, 0].values

    file = base_path / 'data' / 'by_models' / f'{model}_open-access_availability.txt'
    data = pd.read_csv(file, sep='\t', index_col=0)
    data = data.sort_index()
    data1 = pd.DataFrame(index=range(2011, 2023))
    data1 = data1.join(data)
    data1.index = idx
    df_models_oaa.loc[:, model] = data1.iloc[:, 0].values

# fill NaN
df_journals = df_journals.fillna(0)
df_journals_oa = df_journals_oa.fillna(0)
df_journals_oaa = df_journals_oaa.fillna(0)
df_models = df_models.fillna(0)
df_models_oa = df_models_oa.fillna(0)
df_models_oaa = df_models_oaa.fillna(0)

# cumulate number of publications
df_journals1 = df_journals.copy()
df_journals1.loc[:, :] = 0
df_journals1.iloc[:, 1:] = df_journals.iloc[:, :-1]
for i, journal in enumerate(journals):
    df_journals1.iloc[:, i] = np.cumsum(df_journals1.iloc[:, i].values)
df_journals1.iloc[:, :] = np.cumsum(df_journals1.values, axis=1)


df_models1 = df_models.copy()
df_models1.loc[:, :] = 0
df_models1.iloc[:, 1:] = df_models.iloc[:, :-1]
for i, journal in enumerate(models):
    df_models1.iloc[:, i] = np.cumsum(df_models1.iloc[:, i].values)
df_models1.iloc[:, :] = np.cumsum(df_models1.values, axis=1)

# plot publications for journals
labels = [journal_labels[journal] for journal in journals]
colors = sns.color_palette("husl", 12)[1:]
fig, ax = plt.subplots(3, 1, figsize=(5, 6), sharex=True)
ax[0].stackplot(df_journals.index, df_journals.cumsum(axis=0).T,
             labels=labels, alpha=0.8, colors=colors, edgecolors=None, linewidth=0)
ax[0].set_xlim(df_journals.index[0], df_journals.index[-1])
ax[0].set_ylabel('# Publications')
ax[1].stackplot(df_journals.index, df_journals_oa.cumsum(axis=0).T,
             labels=labels, alpha=0.8, colors=colors, edgecolors=None, linewidth=0)
ax[1].set_xlim(df_journals.index[0], df_journals.index[-1])
ax[1].set_ylabel('# Open-access Publications')
ax[2].stackplot(df_journals.index, df_journals_oaa.cumsum(axis=0).T,
             labels=labels, alpha=0.8, colors=colors, edgecolors=None, linewidth=0)
ax[2].set_xlim(df_journals.index[0], df_journals.index[-1])
ax[2].set_xlabel('Year of publication')
ax[2].set_ylabel('# Open-access Publications\n with code/data availability')
handles, labels = ax[2].get_legend_handles_labels()
ax[2].legend(handles[::-1], labels[::-1], loc='upper left', fontsize=7, frameon=False)
fig.tight_layout()
file = base_path / 'figures' / 'journals_.png'
fig.savefig(file, dpi=250)
plt.close(fig=fig)


# plot publications for models
colors = ['#b2df8a', '#fdbf6f', '#cab2d6', '#a6cee3']
fig, ax = plt.subplots(3, 1, figsize=(5, 6), sharex=True)
ax[0].stackplot(df_models.index, df_models.cumsum(axis=0).T,
             labels=models, alpha=0.8, colors=colors, edgecolors=None, linewidth=0)
ax[0].set_xlim(df_models.index[0], df_models.index[-1])
ax[0].set_ylabel('# Publications')
ax[1].stackplot(df_models.index, df_models_oa.cumsum(axis=0).T,
             labels=models, alpha=0.8, colors=colors, edgecolors=None, linewidth=0)
ax[1].set_xlim(df_models.index[0], df_models.index[-1])
ax[1].set_ylabel('# Open-access Publications')
ax[2].stackplot(df_models.index, df_models_oaa.cumsum(axis=0).T,
             labels=models, alpha=0.8, colors=colors, edgecolors=None, linewidth=0)
ax[2].set_xlim(df_models.index[0], df_models.index[-1])
ax[2].set_xlabel('Year of publication')
ax[2].set_ylabel('# Open-access Publications\n with code/data availability')
handles, labels = ax[2].get_legend_handles_labels()
ax[2].legend(handles[::-1], labels[::-1], loc='upper left', fontsize=7, frameon=False)
fig.tight_layout()
file = base_path / 'figures' / 'models_.png'
fig.savefig(file, dpi=250)
plt.close(fig=fig)

# plot publications for journals and models
labels = [journal_labels[journal] for journal in journals]
colors = sns.color_palette("husl", 12)[1:]
fig, ax = plt.subplots(3, 2, figsize=(6, 6))
ax[0, 0].stackplot(df_journals.index, df_journals.cumsum(axis=0).T,
             labels=labels, alpha=0.8, colors=colors, edgecolors=None, linewidth=0)
ax[0, 0].set_xlim(df_journals.index[0], df_journals.index[-1])
ax[0, 0].set_ylabel('# Publications')
ax[1, 0].stackplot(df_journals.index, df_journals_oa.cumsum(axis=0).T,
             labels=labels, alpha=0.8, colors=colors, edgecolors=None, linewidth=0)
ax[1, 0].set_xlim(df_journals.index[0], df_journals.index[-1])
ax[1, 0].set_ylabel('# Open-access Publications')
# ax[1, 0].set_xticks([2012, 2014, 2016, 2018, 2020])
ax[1, 0].set_xlabel('Year of publication')
handles, labels = ax[1, 0].get_legend_handles_labels()
ax[2, 0].legend(handles[::-1], labels[::-1], loc='upper left', fontsize=8, frameon=False, bbox_to_anchor=(-0.15, 1.0))
ax[2, 0].set_axis_off()

colors = ['#b2df8a', '#fdbf6f', '#cab2d6', '#a6cee3']
ax[0, 1].stackplot(df_models.index, df_models.cumsum(axis=0).T,
             labels=models, alpha=0.9, colors=colors, edgecolors=None, linewidth=0)
ax[0, 1].set_xlim(df_models.index[0], df_models.index[-1])
ax[1, 1].stackplot(df_models.index, df_models_oa.cumsum(axis=0).T,
             labels=models, alpha=0.9, colors=colors, edgecolors=None, linewidth=0)
ax[1, 1].set_xlim(df_models.index[0], df_models.index[-1])
ax[2, 1].stackplot(df_models.index, df_models_oaa.cumsum(axis=0).T,
             labels=models, alpha=0.9, colors=colors, edgecolors=None, linewidth=0)
ax[2, 1].set_xlim(df_models.index[0], df_models.index[-1])
ax[2, 1].set_ylabel('# Open-access Publications\n with code/data availability')
ax[2, 1].set_xlabel('Year of publication')
handles, labels = ax[2, 1].get_legend_handles_labels()
ax[2, 1].legend(handles[::-1], labels[::-1], loc='upper left', fontsize=8, frameon=False)
fig.tight_layout()
file = base_path / 'figures' / 'journals_models.png'
fig.savefig(file, dpi=250)
plt.close(fig=fig)
file = base_path / 'figures' / 'journals_models.pdf'
fig.savefig(file, dpi=250)
plt.close(fig=fig)

# display percentage of open-acces publications
print('Journals: ', (np.sum(df_journals_oa.values) / np.sum(df_journals.values)) * 100, '%')
print('Models: ', (np.sum(df_models_oa.values) / np.sum(df_models.values)) * 100, '%')
