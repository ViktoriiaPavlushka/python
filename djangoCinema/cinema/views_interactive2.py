from datetime import datetime
from django.shortcuts import render
from .models import Film
from .repositories import FilmRepository, TicketRepository, UserRepository
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import ColumnDataSource
from bokeh.palettes import Category20
from bokeh.transform import cumsum
import math
import pandas as pd


def graphic1(request):
    # Get all films for the dropdown
    films = FilmRepository.getAll()

    selected_films = []
    if request.method == "POST":
        selected_film_ids = request.POST.getlist('films')  # Get selected films
        selected_film_ids = [int(film_id) for film_id in selected_film_ids if film_id.isdigit()]  # Ensure valid IDs

        if selected_film_ids:
            selected_films = Film.objects.filter(filmID__in=selected_film_ids)

        # Generate age statistics
        age_groups = {}  # Dictionary to store age ranges and counts
        for film in selected_films:
            tickets = [ticket for ticket in TicketRepository.getAll() if ticket.sessionID.filmID == film]
            for ticket in tickets:
                user = UserRepository.getByID(ticket.userID.userID)
                if user:
                    age = (datetime.now().date() - user.yearOfBirth).days // 365  # Calculate age
                    age_range = f"{(age // 5) * 5}-{((age // 5) * 5) + 4}"  # Define age range (e.g., 20-24, 25-29)
                    if age_range in age_groups:
                        age_groups[age_range] += 1
                    else:
                        age_groups[age_range] = 1

        # Prepare data for Bokeh
        data = pd.DataFrame({
            'age_group': list(age_groups.keys()),
            'count': list(age_groups.values())
        })

        # Calculate angles for the pie chart
        data['angle'] = data['count'] / data['count'].sum() * 2 * math.pi
        data['color'] = Category20[len(data)] if len(data) <= 20 else Category20[20]

        # Create Bokeh figure
        p = figure(
            title="Age Distribution of Buyers",
            toolbar_location=None,
            tools="hover",
            tooltips="@age_group: @count",
            x_range=(-0.5, 1.0),
        )

        # Add pie chart to the figure
        p.wedge(
            x=0, y=1, radius=0.4,
            start_angle=cumsum('angle', include_zero=True),
            end_angle=cumsum('angle'),
            line_color="white",
            fill_color='color',
            legend_field='age_group',
            source=ColumnDataSource(data)
        )

        p.axis.axis_label = None
        p.axis.visible = False
        p.grid.grid_line_color = None

        # Get Bokeh components
        script, div = components(p)

        return render(request, 'interactive_dashboard.html', {
            'films': films,
            'bokeh_script': script,
            'bokeh_div': div
        })

    return render(request, 'interactive_dashboard.html', {'films': films})
