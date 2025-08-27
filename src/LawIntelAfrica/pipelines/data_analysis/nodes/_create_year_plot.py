import plotly.graph_objects as go


def create_year_title_bar_plot(countries_year_dict: dict) -> dict:
    """
    Create a bar chart of unique page_title counts by year for each country.

    Args:
        datasets: Dict mapping country to aggregated DataFrames.

    Returns:
        A dictionary representing the Plotly figure.
    """

    # Create bar chart
    fig = go.Figure()
    for country, year_data in countries_year_dict.items():
        years = sorted(year_data.keys())  # Sort for consistent display
        counts = [len(year_data[year]) for year in years]  # Count unique titles
        titles_text = [", ".join(year_data[year]) for year in years]  # For hover text

        fig.add_trace(
            go.Bar(
                x=years,
                y=counts,
                name=country,
                text=counts,
                textposition="auto",
                hovertext=titles_text,
                hoverinfo="text+x+y",
            )
        )

    fig.update_layout(
        title="Number of Unique Page Titles by Year and Country",
        xaxis_title="Year",
        yaxis_title="Number of Unique Page Titles",
        barmode="group",
        xaxis=dict(tickmode="linear", dtick=1), 
        showlegend=True,
    )

    fig_dict = fig.to_dict()
    print(fig_dict.keys())
    return fig_dict
