import bootstrap  # noqa
import pandas as pd
import geopandas as gpd
import datetime
import os
from functools import reduce

from unicef_dssg.config import (
    SECONDARY_DATA_SOURCES,
    PROCESSED_DATA_SOURCES,
    POPULATION,
    GADM_WORLD,
    MOBILITY,
    COUNTRY,
    COVID,
    GINI,
)


class MergeCountryData:
    def __init__(
        self,
        pop_count_df: pd.DataFrame,
        pop_den_df: pd.DataFrame,
        global_mobility_df: pd.DataFrame,
        workplace_closures_covid_df: pd.DataFrame,
        internal_movement_covid_df: pd.DataFrame,
        stay_at_home_covid_df: pd.DataFrame,
        gini_df: pd.DataFrame,
    ):
        self.pop_count_df = pop_count_df
        self.pop_den_df = pop_den_df
        self.global_mobility_df = global_mobility_df
        self.workplace_closures_covid_df = workplace_closures_covid_df
        self.internal_movement_covid_df = internal_movement_covid_df
        self.stay_at_home_covid_df = stay_at_home_covid_df
        self.gini_df = gini_df

    def execute(self, country_gdf: gpd.GeoDataFrame):
        timeseries_country_gdf = self.create_timeseries_dataframe(country_gdf)
        timeseries_country_gdf_pop = self.join_pop_count_data(timeseries_country_gdf)
        timeseries_country_gdf_pop_den = self.join_pop_density_data(timeseries_country_gdf_pop)
        timeseries_country_gdf_pop_den_mob = self.join_mobility_data(timeseries_country_gdf_pop_den)
        timeseries_country_gdf_pop_den_mob_covid = self.join_COVID_data(
            timeseries_country_gdf_pop_den_mob
        )
        timeseries_country_gdf_pop_den_mob_covid_gini = self.join_gini_data(
            timeseries_country_gdf_pop_den_mob_covid
        )
        self._rename_columns(timeseries_country_gdf_pop_den_mob_covid_gini)
        print(timeseries_country_gdf_pop_den_mob_covid_gini)
        timeseries_country_gdf_pop_den_mob_covid_gini.to_file(
            os.path.dirname(os.getcwd())
            + f"/unicef-dssg/{PROCESSED_DATA_SOURCES}{COUNTRY}Country_level_data.geojson",
            driver="GeoJSON",
        )
        timeseries_country_gdf_pop_den_mob_covid_gini.to_csv(
            os.path.dirname(os.getcwd())
            + f"/unicef-dssg/{PROCESSED_DATA_SOURCES}{COUNTRY}Country_level_data.csv"
        )

    def create_timeseries_dataframe(self, country_gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
        country_gdf = country_gdf.loc[
            country_gdf.index.repeat(len(self._expand_dates()))
        ].reset_index(drop=True)
        df_list = []
        for country in country_gdf.GID_0.unique():
            mask = country_gdf["GID_0"] == country
            df1 = country_gdf[mask]
            df1["Week"] = self._expand_dates()
            df_list.append(df1)
        timeseries_country_gdf = pd.concat(df_list)

        return timeseries_country_gdf

    def _expand_dates(self):
        datelist = pd.date_range(start="31/12/2018", end="23/09/2020", freq="W")
        datelist = pd.DatetimeIndex(datelist) + pd.DateOffset(1)
        return datelist.map(lambda t: t.strftime("%Y-%m-%d")).tolist()

    def join_pop_count_data(self, country_gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
        country_gdf = country_gdf.merge(
            self.pop_count_df, left_on="GID_0", right_on="adm0_a3", how="left"
        ).drop("adm0_a3", axis=1)
        return country_gdf

    def join_pop_density_data(self, country_gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
        country_gdf = country_gdf.merge(
            self.pop_den_df[["adm0_a3", "mean"]], left_on="GID_0", right_on="adm0_a3", how="left"
        ).drop("adm0_a3", axis=1)
        return country_gdf

    def join_mobility_data(self, country_gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
        country_gdf["Week"] = pd.to_datetime(country_gdf["Week"])
        self.global_mobility_df["date"] = pd.to_datetime(self.global_mobility_df["date"])
        country_gdf = (
            country_gdf.merge(
                self.global_mobility_df,
                left_on=["NAME_0", "Week"],
                right_on=["country_region", "date"],
                how="left",
            )
            .drop(
                ["country_region", "date", "Unnamed: 0", "census_fips_code", "Unnamed: 0.1"], axis=1
            )
            .reset_index(drop=True)
        )
        return country_gdf

    def join_COVID_data(self, country_gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
        covid_data_dfs = [
            self.workplace_closures_covid_df,
            self.internal_movement_covid_df,
            self.stay_at_home_covid_df,
        ]

        covid_data_df_merge = reduce(
            lambda left, right: pd.merge(left, right, on=["Code", "Date"]), covid_data_dfs
        ).drop(["Entity", "Entity_y"], axis=1)
        covid_data_df_merge["Date"] = covid_data_df_merge["Date"].apply(
            lambda row: datetime.datetime.strptime(row, "%b %d, %Y").strftime("%Y-%m-%d")
        )
        covid_data_df_merge["Date"] = pd.to_datetime(covid_data_df_merge["Date"], errors="coerce")
        covid_data_df_merge = covid_data_df_merge.set_index(["Date"])
        covid_data_df_merge.index = pd.to_datetime(covid_data_df_merge.index)
        covid_data_df_merge_gb = covid_data_df_merge.groupby("Entity_x").resample("W").first()
        covid_data_df_merge_gb = covid_data_df_merge_gb.reset_index("Date").reset_index(drop=True)
        covid_data_df_merge_gb["Week"] = pd.DatetimeIndex(
            covid_data_df_merge_gb["Date"]
        ) + pd.DateOffset(1)
        country_gdf = (
            country_gdf.merge(
                covid_data_df_merge_gb,
                left_on=["GID_0", "Week"],
                right_on=["Code", "Week"],
                how="left",
            )
            .drop(["Entity_x", "Code", "Date"], axis=1)
            .reset_index(drop=True)
        )
        return country_gdf

    def join_gini_data(self, country_gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
        self.gini_df = self.gini_df.sort_values("TIME").groupby("LOCATION").tail(1)
        country_gdf = (
            country_gdf.merge(
                self.gini_df[["LOCATION", "Value"]],
                left_on="GID_0",
                right_on="LOCATION",
                how="left",
            )
            .drop("LOCATION", axis=1)
            .reset_index(drop=True)
        )

        return country_gdf

    def _rename_columns(self, country_gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
        return country_gdf.rename(
            columns={
                "GID_0": "country_code",
                "NAME_0": "country_name",
                "pop18": "population_count_2018",
                "mean": "average_population_density",
                "Workplace Closures (OxBSG)": "workplace_closure",
                "Restrictions on internal movement (OxBSG)": "restrictions_internal_movement",
                "Stay at home requirements (OxBSG)": "stay_at_home_requirements",
                "Value": "gini_coefficient",
            },
            inplace=True,
        )


if __name__ == "__main__":
    merge_country_data = MergeCountryData(
        pd.read_csv(
            os.path.dirname(os.getcwd())
            + f"/unicef-dssg/{SECONDARY_DATA_SOURCES}{POPULATION}pop_count_18_country.csv"
        ),
        pd.read_csv(
            os.path.dirname(os.getcwd())
            + f"/unicef-dssg/{SECONDARY_DATA_SOURCES}{POPULATION}pop_dens_country.csv"
        ),
        pd.read_csv(
            os.path.dirname(os.getcwd())
            + f"/unicef-dssg/{PROCESSED_DATA_SOURCES}{MOBILITY}Global_mobility_weekly.csv"
        ),
        pd.read_csv(
            os.path.dirname(os.getcwd())
            + f"/unicef-dssg/{SECONDARY_DATA_SOURCES}{COVID}workplace-closures-covid.csv"
        ),
        pd.read_csv(
            os.path.dirname(os.getcwd())
            + f"/unicef-dssg/{SECONDARY_DATA_SOURCES}{COVID}internal-movement-covid.csv"
        ),
        pd.read_csv(
            os.path.dirname(os.getcwd())
            + f"/unicef-dssg/{SECONDARY_DATA_SOURCES}{COVID}stay-at-home-covid.csv"
        ),
        pd.read_csv(
            os.path.dirname(os.getcwd()) + f"/unicef-dssg/{SECONDARY_DATA_SOURCES}{GINI}/gini.csv"
        ),
    )

    merge_country_data.execute(
        gpd.read_file(
            os.path.dirname(os.getcwd())
            + f"/unicef-dssg/{SECONDARY_DATA_SOURCES}{GADM_WORLD}GADM_COUNTRY.shp"
        )
    )
