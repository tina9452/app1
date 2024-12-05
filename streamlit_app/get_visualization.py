import streamlit as st
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from get_data import adjust_data_area, adjust_data_radar, adjust_data_line
import math


# 显示折线图
def show_line_chart(state, months, file_path_private_comp, file_path_sole_comp):
    filtered_data_private = adjust_data_line(
        file_path_private_comp, state, months)
    filtered_data_sole = adjust_data_line(file_path_sole_comp, state, months)

    # 定义图表配置和数据
    fig = go.Figure(
        data=[
            go.Scatter(
                x=filtered_data_private['month'],
                y=filtered_data_private['percentage_increase'],
                text=filtered_data_private['total'],
                textposition='top center',
                mode='lines+markers',
                line=dict(
                    color='rgba(79, 152, 123, 0.3)',
                    width=2
                ),
                marker=dict(
                    size=8,
                    color='rgba(79, 152, 123, 1)',
                    line=dict(width=1, color='rgba(79, 152, 123, 0.9)')
                ),
                name="Private Companies",
                hoverinfo='x+y+text'
            ),
            go.Scatter(
                x=filtered_data_sole['month'],
                y=filtered_data_sole['percentage_increase'],
                text=filtered_data_sole['total'],
                textposition='top center',
                mode='lines+markers',
                line=dict(
                    color='rgba(255, 9, 71, 0.3)',
                    width=2
                ),
                marker=dict(
                    size=8,
                    color='rgba(255, 9, 71, 1)',
                    line=dict(width=1, color='rgba(255, 99, 71, 0.9)')
                ),
                name="Sole Traders",
                hoverinfo='x+y+text'
            )
        ]
    )

    fig.update_xaxes(
        tickangle=-45,
        nticks=10,  # 调整为所需的显示标签数量
    )

    # 添加0%水平线
    fig.add_shape(
        type="line",
        x0=0, x1=1,
        y0=0, y1=0,
        xref='paper',
        yref='y',
        line=dict(color="rgba(0,0,0,0.5)", width=2, dash="dash")
    )

    # 更新布局
    fig.update_layout(
        title="ACT - Percentage Increase (Private vs Sole Traders)",
        xaxis_title="Month",
        yaxis_title="Percentage Increase (%)",
        xaxis=dict(tickangle=0, tickfont=dict(size=12)),
        yaxis=dict(tickfont=dict(size=12)),
        margin=dict(t=50, b=50, l=50, r=50),
        plot_bgcolor='rgba(0, 0, 0, 0)',
        showlegend=True
    )

    # 使用 Streamlit 显示图表
    st.title("Line Chart - Percentage Increase (Private vs Sole Traders)")
    st.plotly_chart(fig)

# 显示雷达图
def show_radar_chart(file_path, states):
    st.title("Radar Charts for Different States")
    for state in states:
        filtered_data = adjust_data_radar(
            file_path, state, '2024-01-01', '2024-06-01')
        if not filtered_data.empty:
            radar_chart = create_radar_chart(filtered_data, state)
            st.plotly_chart(radar_chart)
        else:
            st.write(f"No data available for {state}")


def create_radar_chart(filtered_data, title_text):
    months_order = ['January', 'February', 'March', 'April', 'May', 'June']
    filtered_data = filtered_data.set_index(
        'month').reindex(months_order).reset_index()
    categories = filtered_data['month'].tolist()
    values = filtered_data['total'].tolist()

    categories.append(categories[0])
    values.append(values[0])

    radar_chart = go.Figure()
    radar_chart.add_trace(
        go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            mode='lines+markers',
            line=dict(color='rgba(79, 152, 123, 1)'),
            marker=dict(size=8, color='rgba(79, 152, 123, 1)'),
            hoverinfo='r+theta+text',
            hovertemplate='<b>Total:</b> %{r}<extra></extra>',
            name=title_text
        )
    )

    radar_chart.update_layout(
        polar=dict(
            bgcolor='rgba(0,0,0,0)',
            gridshape='linear',
            radialaxis=dict(
                visible=True,
                showline=False,
                showgrid=True,
                gridcolor='rgba(0,0,0,0.3)',
                linecolor='rgba(0,0,0,0.5)',
                range=[0, math.ceil(max(values) * 1.2)],
                dtick=math.ceil(max(values) * 1.2) / 5,
                showticklabels=False
            ),
            angularaxis=dict(
                showline=True,
                showgrid=True,
                gridcolor='rgba(0,0,0,0.3)',
                linecolor='rgba(0,0,0,0.5)',
                direction="clockwise",
                rotation=90
            ),
        ),
        title=title_text,
        annotations=[
            dict(
                x=0.5,
                y=-0.2,
                xref='paper',
                yref='paper',
                text="January-June 2024",
                showarrow=False,
                font=dict(size=14)
            )
        ]
    )

    return radar_chart


# area chart
def show_area_chart(file_name, states, months):
    # 创建子图布局，4 行 2 列
    fig = make_subplots(
        rows=4, cols=2,
        subplot_titles=states,
        shared_xaxes=False,
        vertical_spacing=0.1,
    )

    # 遍历每个州并添加图表
    for idx, state in enumerate(states):
        filtered_data = adjust_data_area(file_name, state, months)
        row = (idx // 2) + 1
        col = (idx % 2) + 1
        add_area_chart_to_subplot(fig, filtered_data, state, row, col)

    fig.update_layout(
        title_text="Private Companies by State",
        height=1200,
        width=1500,
        showlegend=False,
        plot_bgcolor='rgba(0, 0, 0, 0)',
        hovermode="x unified"
    )

    # 在 Streamlit 中显示图表
    st.title("Area Charts for Different States")
    st.plotly_chart(fig)


def add_area_chart_to_subplot(fig, filtered_data, title_text, row, col):
    fig.add_trace(
        go.Scatter(
            x=filtered_data['month'],
            y=filtered_data['total'],
            fill='tozeroy',
            mode='lines+markers',
            line=dict(
                color='rgba(79, 152, 123, 1)',
                shape='spline'
            ),
            marker=dict(
                size=8,
                color='rgba(79, 152, 123, 1)',
                opacity=0
            ),
            hoverinfo='x+y',
            hoveron='points+fills',
            hovertemplate='<b>Number:</b> %{y}<extra></extra>',
            name=title_text
        ),
        row=row, col=col
    )

    fig.update_xaxes(
        tickangle=-45,
        nticks=10,  # 调整为所需的显示标签数量
        row=row, col=col
    )
