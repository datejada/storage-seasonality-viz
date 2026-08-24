# %% load packages
from pathlib import Path

import matplotlib.pyplot as plt
import dayplot as dp
import pandas as pd

# %% load dataset

input_file_name = "energy-storage-level_MWh"
cmap = "Blues"
data_path = Path(__file__).with_name(f"{input_file_name}.csv")
hourly_storage_levels = pd.read_csv(data_path)

# %% transform hourly time series to daily end-of-day values

start_date = pd.Timestamp("2030-01-01")
daily_storage_levels = hourly_storage_levels.loc[
    hourly_storage_levels["hour"] % 24 == 0
].copy()
daily_storage_levels["date"] = start_date + pd.to_timedelta(
    daily_storage_levels["hour"] // 24 - 1,
    unit="D",
)
value_columns = hourly_storage_levels.columns.drop("hour")
daily_storage_levels[value_columns] = daily_storage_levels[value_columns].div(
    daily_storage_levels[value_columns].max()
)

# %% calendar plots

fig, axes = plt.subplots(
    nrows=len(value_columns),
    figsize=(16, 4 * len(value_columns)),
    squeeze=False,
)

for ax, column in zip(axes[:, 0], value_columns):
    dp.calendar(
        dates=daily_storage_levels["date"],
        values=daily_storage_levels[column],
        start_date=daily_storage_levels["date"].min(),
        end_date=daily_storage_levels["date"].max(),
        month_grid=True,
        mutation_scale=1.22,
        legend=True,
        cmap=cmap,
        ax=ax,
    )
    ax.set_title(column, loc="left")

plt.tight_layout()
plt.show()
# %% Export calendar plots to PNG files

fig.savefig(Path(__file__).with_name(f"{input_file_name}.png"), dpi=300)

# %%
