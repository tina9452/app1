from get_data import extract_data
from get_visualization import show_area_chart, show_radar_chart, show_line_chart


# 1.extract data
dataframes = extract_data()

# 2.draw graph
file_name = 'private_bystate_bymonth'
file_name2 = 'public_bystate_bymonth'
file_name3 = 'sole_bystate_bymonth'
states = ['ACT', 'NSW', 'NT', 'QLD', 'SA', 'TAS', 'VIC', 'WA']
months = 24


if __name__ == "__main__":
    # area chart
    show_area_chart(file_name, states, months)

    # radar chart
    months = ["January", "February", "March", "April", "May", "June"]
    show_radar_chart(file_name, states)

    # line chart
    state = "ACT"
    months = 24
    show_line_chart(state, months, file_name, file_name3)
