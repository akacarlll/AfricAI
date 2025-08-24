import plotly.express as px
import pandas as pd


def plot_country_docs(
    countries_description_dict: dict, title: str = "Documents by Country"
):
    """
    Plot a world map where countries are colored in purple
    based on the total number of legal documents across categories.

    Parameters
    ----------
    countries_description_dict : dict
        Dictionary mapping ISO3 country codes to category counts.
        Example: {"CMR": {"civil": 120, "criminal": 45}, "BEN": {"civil": 12}}
    title : str
        Title of the map
    """
    print(countries_description_dict)
    # Compute totals per country
    data = {
        country: sum(categories.values())
        for country, categories in countries_description_dict.items()
    }
    print(data)

    # Convert dict to dataframe
    df = pd.DataFrame(list(data.items()), columns=["iso_alpha", "docs"])

    fig = px.choropleth(
        df,
        locations="iso_alpha",
        color="docs",
        hover_name="iso_alpha",
        color_continuous_scale="Purples",
        projection="natural earth",
        title=title,
    )

    # Style tweaks
    fig.update_traces(marker_line_width=0.5, marker_line_color="white")
    fig.update_geos(
        showcountries=True, showcoastlines=True, showland=True, fitbounds="locations"
    )

    return fig
