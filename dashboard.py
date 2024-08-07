from etl import get_data, get_data_query
import pandas as pd
import plotly.express as px
import dashboard
from dashboard import dcc, html
from dashboard.dependencies import Output, Input
import plotly.graph_objects as go
import base64

sales = get_data('sales_by_category_location_v')
supplier = get_data('supplier_product_count_v')
order_v = get_data('orders_v')
returns_order = get_data('returns_order_v')
orders_date = get_data_query('request')

orders_date['order_date'] = pd.to_datetime(orders_date.order_date)
min_date = orders_date['order_date'].min()
max_date = orders_date['order_date'].max()

######################################
sales['created_at'] = pd.to_datetime(sales.created_at)
min_date_register = sales['created_at'].min()
max_date_register = sales['created_at'].max()

block_1 = html.Div(
    children=[
        html.H1(
            f'E-commerce Analytics',
            style={'font-size': 60, 'background-color': 'lightyellow', 'text-align': 'center'}
        )
    ]
)

block_6 = html.Div(
    children=[
        dcc.DatePickerRange(
            id='date_prange_register',
            min_date_allowed=min_date_register,
            max_date_allowed=max_date_register,
        )
    ]
)
# map
block_7 = html.Div(
    children=[
        dcc.Graph(id='map_fig')
    ]
)
#pie
block_5 = html.Div(
    children=[
        dcc.Graph(id='pie_chart',
                  figure=go.Figure(
                      data=[
                          {
                              'labels': returns_order['return_status'],
                              'values': returns_order['order_id'],
                              'type': 'pie'
                          }
                      ],
                      layout=go.Layout(
                          title='Percentage of orders by product return status',
                          titlefont={
                              'size': 18,
                              'color': 'grey'
                          },
                          plot_bgcolor='rgba(0,0,0,0)',
                          paper_bgcolor='rgba(0,0,0,0)',
                          font={
                              'color': 'black',
                              'size': 14
                          },
                          margin={
                              't': 30,  # Top margin
                              'b': 30,  # Bottom margin
                              'l': 30,  # Left margin
                              'r': 30  # Right margin
                          },
                          height=600,
                          width=600
                      )
                  )
                  )
    ],
    style={'width': '50%', 'display': 'inline-block'}
)


# контейнер
block_container = html.Div(
    children=[
        html.Div(
            children=[
                block_7  # Map
            ],
            style={
                'width': '50%',
                'display': 'inline-block',
                'vertical-align': 'top'
            }
        ),
        html.Div(
            children=[
                block_5  # Pie chart
            ],
            style={
                'width': '50%',
                'display': 'inline-block',
                'vertical-align': 'top',
                'margin-left': '200px'  # Добавляем отступ слева
            }
        )
    ],
    style={
        'display': 'flex',
        'flex-direction': 'row',
        'justify-content': 'space-between',
        'align-items': 'center',
        'margin': '80px 0'
    }
)

block_4 = html.Div(
    children=[
        dcc.DatePickerRange(
            id='date_prange_orders',
            min_date_allowed=min_date,
            max_date_allowed=max_date,
        ),
        dcc.Dropdown(
            id='category',
            options=[
                {'label': c, 'value': c} for c in returns_order['category'].unique().tolist()
            ]
        )
    ]
)

top_95_suppliers = supplier.sort_values(by='product_count', ascending=False).head(95)

block_2 = html.Div(
    children=[
        dcc.Graph(id='line_fig',
                  figure=go.Figure(
                      data=[
                          go.Scatter(
                              x=top_95_suppliers['country'],
                              y=top_95_suppliers['product_count'],
                              mode='lines+markers',
                              name='Top 95 Suppliers'
                          )
                      ],
                      layout=go.Layout(
                          title='Top 95 Suppliers by Product Count',
                          xaxis_title='Country',
                          yaxis_title='Product Count'
                      )
                  )
                  )
    ],
    style={
        'width': '100%',
        'height': '500px',
        'display': 'inline-block',
        'border-right': '1px solid black',
        'padding': '15px auto',
        'margin': '10px'
    }
)

# histogram_1
block_3 = html.Div(
    children=[
        dcc.Graph(id='histogram_fig_1')
    ],
    style={'width': '50%', 'display': 'inline-block'}
)
# histogram_2
block_8 = html.Div(
    children=[
        dcc.Graph(id='histogram_fig_2')
    ],
    style={'width': '50%', 'display': 'inline-block'}
)

# codding image
with open("source/dataset-cover.png", "rb") as image_file:
    encoded_image = base64.b64encode(image_file.read()).decode('utf-8')

block_9 = html.Div([
    html.Div(
        html.Img(
            src='data:image/jpeg;base64,{}'.format(encoded_image),
            alt='My Image',
            style={'display': 'block', 'margin-left': 'auto', 'margin-right': 'auto', 'width': '50%'}
        ),
        style={'text-align': 'center'}
    )
])

app = dash.Dash(__name__)
app.layout = html.Div(
    children=[
        block_1,
        block_9,
        block_4,
        block_3,
        block_8,
        block_2,
        block_6,
        block_container

    ]
)


@app.callback(
    Output(component_id='histogram_fig_1', component_property='figure'),
    Output(component_id='histogram_fig_2', component_property='figure'),
    Input(component_id='date_prange_orders', component_property='start_date'),
    Input(component_id='date_prange_orders', component_property='end_date'),
    Input(component_id='category', component_property='value')
)
def update_figure_part1(start_date, end_date, selected_category):
    category_filter = 'All categories'
    sales_date = orders_date.copy(deep=True)
    sales_category = orders_date.copy(deep=True)

    if selected_category:
        category_filter = selected_category
        sales_date = sales_date[sales_date['category'] == category_filter]
        sales_category = sales_category[sales_category['category'] == category_filter]

    if start_date and end_date:
        sales_date = sales_date[(sales_date['order_date'] >= start_date) & (sales_date['order_date'] <= end_date)]
        sales_category = sales_category[
            (sales_category['order_date'] >= start_date) & (sales_category['order_date'] <= end_date)]

    # Созданиём гистограммы :)
    histogram_fig_1 = px.histogram(
        data_frame=sales_category,
        x='category',
        y='total_price',
        width=1000,
        height=900,
        color_discrete_sequence=['blue'],
    )
    histogram_fig_1.update_layout({'xaxis': {'type': 'category'}})
    histogram_fig_1.update_layout(
        {'title': {'text': f'Total sales by  {category_filter}'}})

    histogram_fig_2 = px.histogram(
        data_frame=sales_category,
        x='category',
        y='quantity',
        width=1000,
        height=900,
        color_discrete_sequence=['lightgreen'],
    )

    histogram_fig_2.update_layout({'xaxis': {'type': 'category'}})
    histogram_fig_2.update_layout(
        {'title': {'text': f'Quantity distribution by  {category_filter}'}})

    return histogram_fig_1, histogram_fig_2


@app.callback(
    Output(component_id='map_fig', component_property='figure'),
    Input(component_id='date_prange_register', component_property='start_date'),
    Input(component_id='date_prange_register', component_property='end_date')
)
def update_figure_part2(start_date_register, end_date_register):
    register_date = sales.copy(deep=True)
    if start_date_register and end_date_register:
        sdate = start_date_register
        edate = end_date_register
        register_date = register_date[(register_date['created_at'] >= sdate) & (register_date['created_at'] <= edate)]

    customer_id_counts = register_date.groupby('country')['customer_id'].nunique()
    map_fig = go.Figure(
        data=go.Choropleth(
            locations=customer_id_counts.index,
            locationmode='country names',
            z=customer_id_counts.values,
            text=customer_id_counts.index,
            colorscale='Greens',
            reversescale=True,
            marker_line_width=0.2,
            colorbar_title='Number of Customers'
        )
    )

    map_fig.update_layout(
        title='Number of Customers by country',
        width=1000,
        height=900,
        geo=dict(
            showframe=True,
            showcoastlines=True,
            projection=dict(type='mercator'),
            showocean=True,
            oceancolor='lightblue'
        )
    )
    return map_fig


if __name__ == '__main__':
    app.run_server(debug=True)
