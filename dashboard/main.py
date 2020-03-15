import gspread
import pandas as mypd
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)
#Users/shashi/Digital Gemba/snehaseva/dashboard_env
sheet = client.open("com_meeting").sheet1
sheet = client.open("teacher_qualification").sheet1
data = sheet.get_all_records()
com_meetings_data = mypd.DataFrame(data)

from bokeh.models import LabelSet , ColumnDataSource , CustomJS ,VBar , Legend
from bokeh.io import output_notebook ,curdoc
from bokeh.plotting import figure, output_file, show
from bokeh.embed import components , autoload_static
from bokeh.resources import  CDN
from bokeh.models.annotations import LegendItem
from math import pi
from bokeh.palettes import Category20c
from bokeh.transform import cumsum

output_file("hbar_stack.html")

####  Committe Meetings ####

sheet = client.open("com_meeting").sheet1
data = sheet.get_all_records()
com_meetings_data = mypd.DataFrame(data)

cmdata = ColumnDataSource(data = dict(
    mc = com_meetings_data['Meetings_Conducted'],
    fp = com_meetings_data['Further_Plan'],
    nd = com_meetings_data['Not_Done'],
    yr  = com_meetings_data['Year']))


cmplot  = figure(plot_width = 500 , plot_height = 400 ,
    y_range = (0,13) , name = "cmplot")
cmplot.vbar_stack(stackers= ['mc','fp','nd'] , x = 'yr', source = cmdata
    , color=("green","yellow","red"), width = 0.5, line_color = "black")

cmplot.toolbar_location = None
cmplot.xaxis.axis_label = "Year"
cmplot.yaxis.axis_label = "Number of Meetings"

li1 = LegendItem(label=' Done', renderers=[cmplot.renderers[0]])
li2 = LegendItem(label=' Planed', renderers=[cmplot.renderers[1]])
li3 = LegendItem(label='Not Done', renderers=[cmplot.renderers[2]])
legend1 = Legend(items=[li1, li2, li3], location='bottom_center')
cmplot.add_layout(legend1)

new_legend = cmplot.legend[0]
cmplot.add_layout(new_legend,'below')
cmplot.legend.orientation = "horizontal"

#show(cmplot)
#curdoc().add_root(cmplot)

####  teacher qualification  ####

sheet_teach = client.open("teacher_qualification").sheet1
sheet_teach = sheet_teach.get_all_records()
teachdata = mypd.DataFrame(sheet_teach)
teachdata['angle'] = teachdata['Numbers']/teachdata['Numbers'].sum() * 2*pi
teachdata['color'] = Category20c[len(teachdata['angle'])]
#print(teachdata)

teachplot = figure(plot_height=500,plot_width = 500, name="teachplot", toolbar_location=None,
           tools="hover", tooltips="@Teacher: @Numbers", x_range=(-0.5, .5))


teachplot.wedge(x=0, y=1, radius=0.4,
        start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
        line_color="white", fill_color='color', source=teachdata)

teachplot.axis.visible = None

#new_legend = teachplot.l
#teachplot.add_layout(new_legend,'below')
#teachplot.legend.orientation = "horizontal"


curdoc().add_root(teachplot, cmplot)