import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import pandas as pd
from data_manager import DataManager

dm = DataManager('./vgsales.csv')
col = "a"

#generate_graph() generates the graph based on the dropdown input 
def generate_graph(dropdown):
	if(dropdown=='t1'):
		dm.reset_data()
		dm.group_sales_by(column_name="Year")
		x = dcc.Graph(
			id='sales_by_year',
			figure={
				'data': [
					{'x': dm.data.iloc[:,0] , 'y': dm.data.iloc[:,5], 'type': 'line', 'name': 'Global','mode':'lines+markers'},
					{'x': dm.data.iloc[:,0] , 'y': dm.data.iloc[:,1], 'type': 'line', 'name': 'North America','mode':'lines+markers'},
					{'x': dm.data.iloc[:,0] , 'y': dm.data.iloc[:,2], 'type': 'line', 'name': 'Europe','mode':'lines+markers'},
					{'x': dm.data.iloc[:,0] , 'y': dm.data.iloc[:,3], 'type': 'line', 'name': 'Japan','mode':'lines+markers'},
					{'x': dm.data.iloc[:,0] , 'y': dm.data.iloc[:,4], 'type': 'line', 'name': 'Other','mode':'lines+markers'},
					
				],
				'layout': {
					'title': 'Yearly Game Sales',
					'xaxis' : {'title':'Year'},
					'yaxis' : {'title':'Sales'},
					'plot_bgcolor': '#eeeeee',
					'paper_bgcolor': '#eeeeee',
				}
			}
		)
		
		return x
		
	elif(dropdown=='t2'):
		x = dcc.Tabs(
			id='plot1',
			tabs=[{'label':'Genre', 'value':'Genre'},{'label':'Platform', 'value':'Platform'},{'label':'Publisher', 'value':'Publisher'},{'label':'Region', 'value':'Region'}],
			value = 'Genre',
			), html.Div(style={'width':'100%'} , id='piec')
		return x

#generate_pie() generates a pie chart based on the different tabs 		
def generate_pie():
		dm.reset_data()
		data=[]
		labels=[]
		title = "Game Sales % by " + col
		other=0
		if col!="Region":
			dm.group_sales_by(column_name=col)
			sum = dm.data.iloc[:,5].sum()
			d = dm.data.iloc[:,5].values.tolist()
			l = dm.data.iloc[:,0].values.tolist()
			
			#Add the groups with less than 1% to others.
			for i in range(len(d)):
				if int(d[i])<(sum/100):
					other=other+d[i]
				else:
					data.append(d[i])
					labels.append(l[i])
			if other!=0:
				data.append(other)
				labels.append("Other")
		else:
			data.append(dm.data.iloc[:,6].sum())
			data.append(dm.data.iloc[:,7].sum())
			data.append(dm.data.iloc[:,8].sum())
			data.append(dm.data.iloc[:,9].sum())
			labels.append("North America")
			labels.append("Europe")
			labels.append("Japan")
			labels.append("Other")

		
		
		return dcc.Graph(
				id='pi',
				figure={
					'data': [
						{'values': data, 'labels':labels , 'type': 'pie'},
					],
					'layout': {
						'title': title,
						'plot_bgcolor': '#eeeeee',
						'paper_bgcolor': '#eeeeee',
					}
				}
			)
		
#initialize application
app = dash.Dash()
server = app.server
app.config['suppress_callback_exceptions']=True

#application layout
app.layout = html.Div(style={'backgroundImage':'url("http://www.designbolts.com/wp-content/uploads/2013/02/Golf-Shirt-Grey-Seamless-Pattern-For-Website-Background.jpg")','borderRadius':'10px','min-height':'95vh'},children=[
    html.H1(style={'textAlign':'center','font':'bold 30px Castellar, serif','padding':'20px 0px 0px 0px'} ,children='Analysing Game Sales Data'),

	html.Label(style={'margin': '0% 0% 0% 2.5%','font':'20px Britannic, serif'},children='Select a plot:'),
	html.Div(style={'width':'20%' , 'margin': '0% 0% 0% 2.5%' },children=dcc.Dropdown(
		id='plot',
		options=[{'label':'Yearly Global Sales', 'value':'t1',},{'label':'Pie Charts', 'value':'t2'}],
		value = 't1'
	)),
	html.Div(style={'width':'95%','margin':'1% 2.5% 1% 2.5%','borderRadius':'10px','opacity':'1'}, children=html.Div(id='output')),
	
	html.Div(style={'margin': '0% 0% 0% 2.5%','font':'20px Britannic, serif'},children='''
	1. Click on the legends to include/exclude data from the plot.    
	'''),
	html.Div(style={'margin': '0% 0% 0% 2.5%','font':'20px Britannic, serif'},children='''
	2. Hover over any point on the plot to get details.
	'''),
	
	html.Div(style={'textAlign':'center'} , children='''
	Web App developed by Harsh Darji
	''')
	

])

#callback for dropdown for different plots 
@app.callback(
    dash.dependencies.Output('output', 'children'),
    [dash.dependencies.Input('plot', 'value')])
	
def update_output(value):
	s = '{}'.format(value)
	return generate_graph(s)
	
#callback for different tabs for different pie charts
@app.callback(
    dash.dependencies.Output('piec', 'children'),
    [dash.dependencies.Input('plot1', 'value')])
	
def update_output(value):
	global col
	col = '{}'.format(value)
	return generate_pie()

if __name__ == '__main__':
    app.run_server(debug=True)
