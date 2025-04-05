import dash
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import pandas as pd
import json

def create_dash_app(system_state):
    """
    Create a Dash app for the Starbucks Procurement Multi-Agent System dashboard.
    
    Args:
        system_state: The system state dictionary
        
    Returns:
        Dash app instance
    """
    # Initialize the Dash app
    app = dash.Dash(
        __name__,
        external_stylesheets=[dbc.themes.BOOTSTRAP],
        routes_pathname_prefix='/',
        suppress_callback_exceptions=True
    )
    
    # Define the app layout
    app.layout = html.Div([
        dcc.Store(id='system-state', data=system_state),
        dcc.Interval(
            id='interval-component',
            interval=5 * 1000,  # in milliseconds (5 seconds)
            n_intervals=0
        ),
        
        # Header
        dbc.Navbar(
            dbc.Container([
                html.A(
                    dbc.Row([
                        dbc.Col(html.Img(src="/static/starbucks_logo.png", height="40px")),
                        dbc.Col(dbc.NavbarBrand("Starbucks Procurement Multi-Agent System", className="ms-2")),
                    ], align="center", className="g-0"),
                    href="/",
                    style={"textDecoration": "none"},
                ),
                dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
                dbc.Collapse(
                    dbc.Nav([
                        dbc.NavItem(dbc.NavLink("Dashboard", href="/")),
                        dbc.NavItem(dbc.NavLink("Suppliers", href="/suppliers")),
                        dbc.NavItem(dbc.NavLink("Contracts", href="/contracts")),
                        dbc.NavItem(dbc.NavLink("Orders", href="/orders")),
                    ], className="ms-auto", navbar=True),
                    id="navbar-collapse",
                    navbar=True,
                ),
            ]),
            color="dark",
            dark=True,
            className="mb-4",
        ),
        
        # Main content
        dbc.Container([
            # Agent Status Row
            dbc.Row([
                dbc.Col([
                    html.H4("Agent Status", className="text-center"),
                    html.Div(id="agent-status-cards", className="d-flex justify-content-between")
                ], width=12)
            ], className="mb-4"),
            
            # Market Conditions and Supplier Map Row
            dbc.Row([
                # Market Conditions
                dbc.Col([
                    html.H4("Coffee Market Conditions", className="text-center"),
                    dbc.Card([
                        dbc.CardBody([
                            html.Div(id="market-price-indicator"),
                            dcc.Graph(id="price-history-chart")
                        ])
                    ])
                ], md=6),
                
                # Supplier Map
                dbc.Col([
                    html.H4("Global Sourcing Map", className="text-center"),
                    dbc.Card([
                        dbc.CardBody([
                            dcc.Graph(id="supplier-map")
                        ])
                    ])
                ], md=6)
            ], className="mb-4"),
            
            # Contracts and Orders Row
            dbc.Row([
                # Contracts
                dbc.Col([
                    html.H4("Active Contracts", className="text-center"),
                    html.Div(id="contracts-table")
                ], md=6),
                
                # Orders
                dbc.Col([
                    html.H4("Recent Orders", className="text-center"),
                    html.Div(id="orders-table")
                ], md=6)
            ], className="mb-4"),
            
            # Agent Communication Log
            dbc.Row([
                dbc.Col([
                    html.H4("Agent Communication Log", className="text-center"),
                    dbc.Card([
                        dbc.CardBody([
                            html.Div(id="agent-log", style={"maxHeight": "300px", "overflow": "auto"})
                        ])
                    ])
                ], width=12)
            ])
        ], fluid=True)
    ])
    
    # Define callbacks
    @app.callback(
        Output('system-state', 'data'),
        Input('interval-component', 'n_intervals')
    )
    def update_system_state(n):
        """
        Update the system state from the server.
        
        Args:
            n: Interval counter
            
        Returns:
            Updated system state
        """
        try:
            # In a real implementation, this would fetch the latest state from the server
            # For now, we'll just return the current state
            return system_state
        except Exception as e:
            print(f"Error updating system state: {str(e)}")
            # Return the original state if there's an error
            return system_state
    
    @app.callback(
        Output('agent-status-cards', 'children'),
        Input('system-state', 'data')
    )
    def update_agent_status(data):
        """
        Update the agent status cards.
        
        Args:
            data: System state data
            
        Returns:
            List of agent status cards
        """
        # Create a status card for each agent
        cards = []
        
        # Sourcing Agent
        cards.append(
            dbc.Card([
                dbc.CardHeader("Coffee Bean Sourcing Agent", className="text-center"),
                dbc.CardBody([
                    html.H5("Status: Active", className="card-title text-center"),
                    html.P(f"Evaluating {len(data['suppliers'])} suppliers", className="card-text text-center"),
                    html.P(f"Last activity: {datetime.now().strftime('%H:%M:%S')}", className="card-text text-center text-muted")
                ])
            ], className="m-2", style={"width": "30%"})
        )
        
        # Negotiation Agent
        cards.append(
            dbc.Card([
                dbc.CardHeader("Contract Negotiation Agent", className="text-center"),
                dbc.CardBody([
                    html.H5("Status: Active", className="card-title text-center"),
                    html.P(f"Managing {len(data['contracts'])} contracts", className="card-text text-center"),
                    html.P(f"Last activity: {datetime.now().strftime('%H:%M:%S')}", className="card-text text-center text-muted")
                ])
            ], className="m-2", style={"width": "30%"})
        )
        
        # Order Management Agent
        cards.append(
            dbc.Card([
                dbc.CardHeader("Order Management Agent", className="text-center"),
                dbc.CardBody([
                    html.H5("Status: Active", className="card-title text-center"),
                    html.P(f"Tracking {len(data['orders'])} orders", className="card-text text-center"),
                    html.P(f"Last activity: {datetime.now().strftime('%H:%M:%S')}", className="card-text text-center text-muted")
                ])
            ], className="m-2", style={"width": "30%"})
        )
        
        return cards
    
    @app.callback(
        [Output('market-price-indicator', 'children'),
         Output('price-history-chart', 'figure')],
        Input('system-state', 'data')
    )
    def update_market_conditions(data):
        """
        Update the market conditions display.
        
        Args:
            data: System state data
            
        Returns:
            Market price indicator and price history chart
        """
        market_conditions = data['market_conditions']
        
        # Create price indicator
        current_price = market_conditions['average_price']
        price_trend = market_conditions['price_trend']
        
        if price_trend == "Rising":
            trend_color = "success"
            trend_icon = "↑"
        elif price_trend == "Falling":
            trend_color = "danger"
            trend_icon = "↓"
        else:
            trend_color = "warning"
            trend_icon = "→"
        
        price_indicator = html.Div([
            html.H3([
                f"${current_price}/kg ",
                html.Span(trend_icon, className=f"text-{trend_color}")
            ], className="text-center mb-3"),
            html.P(f"Trend: {price_trend}", className=f"text-center text-{trend_color}")
        ])
        
        # Create price history chart
        history_data = market_conditions['price_history']
        df = pd.DataFrame(history_data)
        df['date'] = pd.to_datetime(df['date'])
        
        fig = px.line(
            df, 
            x='date', 
            y='price',
            title='Coffee Price History (30 Days)',
            labels={'date': 'Date', 'price': 'Price ($/kg)'}
        )
        
        fig.update_layout(
            margin=dict(l=20, r=20, t=40, b=20),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='#333'
        )
        
        return price_indicator, fig
    
    @app.callback(
        Output('supplier-map', 'figure'),
        Input('system-state', 'data')
    )
    def update_supplier_map(data):
        """
        Update the supplier map.
        
        Args:
            data: System state data
            
        Returns:
            Supplier map figure
        """
        suppliers = data['suppliers']
        
        # Map region names to approximate coordinates
        region_coords = {
            "Ethiopia": (9.1450, 40.4897),
            "Colombia": (4.5709, -74.2973),
            "Brazil": (-14.2350, -51.9253),
            "Vietnam": (14.0583, 108.2772),
            "Guatemala": (15.7835, -90.2308),
            "Costa Rica": (9.7489, -83.7534),
            "Kenya": (0.0236, 37.9062),
            "Indonesia": (-0.7893, 113.9213)
        }
        
        # Create dataframe for map
        supplier_data = []
        for supplier in suppliers:
            if supplier['region'] in region_coords:
                lat, lon = region_coords[supplier['region']]
                
                # Determine if we have a contract with this supplier
                has_contract = any(c['supplier_id'] == supplier['id'] for c in data['contracts'])
                
                supplier_data.append({
                    'name': supplier['name'],
                    'region': supplier['region'],
                    'lat': lat,
                    'lon': lon,
                    'quality_score': supplier['quality_score'],
                    'bean_types': ', '.join(supplier['bean_types']),
                    'has_contract': 'Yes' if has_contract else 'No',
                    'marker_size': 15 if has_contract else 10,
                    'marker_color': 'green' if has_contract else 'blue'
                })
        
        df = pd.DataFrame(supplier_data)
        
        # Create map
        fig = px.scatter_geo(
            df,
            lat='lat',
            lon='lon',
            hover_name='name',
            hover_data={
                'region': True,
                'bean_types': True,
                'quality_score': True,
                'has_contract': True,
                'lat': False,
                'lon': False,
                'marker_size': False,
                'marker_color': False
            },
            size_max=15,
            color='marker_color',
            size='marker_size',
            projection='natural earth'
        )
        
        fig.update_layout(
            margin=dict(l=0, r=0, t=0, b=0),
            paper_bgcolor='rgba(0,0,0,0)',
            geo=dict(
                showland=True,
                landcolor='rgb(243, 243, 243)',
                countrycolor='rgb(204, 204, 204)',
                showocean=True,
                oceancolor='rgb(230, 230, 250)',
                showlakes=True,
                lakecolor='rgb(230, 230, 250)',
                showrivers=True,
                rivercolor='rgb(230, 230, 250)'
            ),
            showlegend=False
        )
        
        return fig
    
    @app.callback(
        Output('contracts-table', 'children'),
        Input('system-state', 'data')
    )
    def update_contracts_table(data):
        """
        Update the contracts table.
        
        Args:
            data: System state data
            
        Returns:
            Contracts table
        """
        contracts = data['contracts']
        suppliers = data['suppliers']
        
        if not contracts:
            return html.P("No active contracts", className="text-center text-muted")
        
        # Create table rows
        rows = []
        for contract in contracts:
            # Find supplier name
            supplier_name = "Unknown"
            for supplier in suppliers:
                if supplier['id'] == contract['supplier_id']:
                    supplier_name = supplier['name']
                    break
            
            # Format dates
            start_date = datetime.fromisoformat(contract['start_date'].replace('Z', ''))
            end_date = datetime.fromisoformat(contract['end_date'].replace('Z', ''))
            
            # Create row
            rows.append(
                html.Tr([
                    html.Td(contract['id']),
                    html.Td(supplier_name),
                    html.Td(f"${contract['price_per_kg']}/kg"),
                    html.Td(f"{contract['volume_commitment']:,} kg"),
                    html.Td(f"{start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}"),
                    html.Td(contract['status'].capitalize())
                ])
            )
        
        # Create table
        table = dbc.Table([
            html.Thead(
                html.Tr([
                    html.Th("ID"),
                    html.Th("Supplier"),
                    html.Th("Price"),
                    html.Th("Volume"),
                    html.Th("Duration"),
                    html.Th("Status")
                ])
            ),
            html.Tbody(rows)
        ], bordered=True, hover=True, responsive=True, size="sm")
        
        return table
    
    @app.callback(
        Output('orders-table', 'children'),
        Input('system-state', 'data')
    )
    def update_orders_table(data):
        """
        Update the orders table.
        
        Args:
            data: System state data
            
        Returns:
            Orders table
        """
        orders = data['orders']
        suppliers = data['suppliers']
        
        if not orders:
            return html.P("No orders", className="text-center text-muted")
        
        # Create table rows
        rows = []
        for order in orders:
            # Find supplier name
            supplier_name = "Unknown"
            for supplier in suppliers:
                if supplier['id'] == order['supplier_id']:
                    supplier_name = supplier['name']
                    break
            
            # Format dates
            order_date = datetime.fromisoformat(order['order_date'].replace('Z', ''))
            expected_delivery = datetime.fromisoformat(order['expected_delivery'].replace('Z', ''))
            
            # Determine status color
            status_color = {
                'pending': 'warning',
                'in_transit': 'info',
                'delayed': 'danger',
                'delivered': 'success',
                'cancelled': 'secondary'
            }.get(order['status'], 'primary')
            
            # Create row
            rows.append(
                html.Tr([
                    html.Td(order['id']),
                    html.Td(supplier_name),
                    html.Td(f"{order['quantity']:,} kg"),
                    html.Td(f"${order['total_cost']:,.2f}"),
                    html.Td(order_date.strftime('%Y-%m-%d')),
                    html.Td(expected_delivery.strftime('%Y-%m-%d')),
                    html.Td(dbc.Badge(order['status'].capitalize(), color=status_color))
                ])
            )
        
        # Create table
        table = dbc.Table([
            html.Thead(
                html.Tr([
                    html.Th("ID"),
                    html.Th("Supplier"),
                    html.Th("Quantity"),
                    html.Th("Cost"),
                    html.Th("Order Date"),
                    html.Th("Expected Delivery"),
                    html.Th("Status")
                ])
            ),
            html.Tbody(rows)
        ], bordered=True, hover=True, responsive=True, size="sm")
        
        return table
    
    @app.callback(
        Output('agent-log', 'children'),
        Input('system-state', 'data')
    )
    def update_agent_log(data):
        """
        Update the agent communication log.
        
        Args:
            data: System state data
            
        Returns:
            Agent log content
        """
        messages = data.get('agent_messages', [])
        
        if not messages:
            return html.P("No agent activity", className="text-center text-muted")
        
        # Create log entries
        log_entries = []
        for message in reversed(messages):  # Show newest first
            # Handle different timestamp formats
            if isinstance(message['timestamp'], str):
                try:
                    timestamp = datetime.fromisoformat(message['timestamp'].replace('Z', ''))
                except:
                    timestamp = datetime.now()
            else:
                timestamp = datetime.now()
            
            # Determine agent type and badge color
            agent_type = message.get('agent', 'Unknown')
            badge_color = "primary"
            
            if "Sourcing Agent" in agent_type:
                badge_color = "primary"
                agent_type = "Sourcing"
            elif "Negotiation Agent" in agent_type:
                badge_color = "success"
                agent_type = "Negotiation"
            elif "Order Agent" in agent_type or "Order Management" in agent_type:
                badge_color = "warning"
                agent_type = "Order"
            elif "System" in agent_type:
                badge_color = "info"
                agent_type = "System"
            
            # Clean up the content
            content = message.get('content', '')
            # Truncate very long messages
            if len(content) > 300:
                content = content[:297] + "..."
            
            # Create log entry
            log_entries.append(
                dbc.ListGroupItem([
                    dbc.Row([
                        dbc.Col(dbc.Badge(agent_type, color=badge_color), width=2),
                        dbc.Col(html.P(content), width=8),
                        dbc.Col(html.Small(timestamp.strftime('%H:%M:%S')), width=2, className="text-muted text-end")
                    ])
                ])
            )
        
        # Create log
        log = dbc.ListGroup(log_entries)
        
        return log
    
    return app
