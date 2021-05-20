import numpy as np
import pandas as pd
import sklearn
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier,RandomForestClassifier
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input,Output,State
from dash.exceptions import PreventUpdate

#import os


app=dash.Dash(__name__)                            ## initialize dash app

data=pd.read_csv("D:\\Users\\MASTER\\Desktop\\perkinson data\\parkinson_data.csv")   ## get the data


target=data.iloc[:,17]                                            ## get target variable
features=data.drop(['name','status'],axis=1)                      ## get features and drop unnecessary columns
imp_columns=["MDVP:Fo(Hz)","MDVP:Fhi(Hz)","MDVP:Flo(Hz)","MDVP:APQ","NHR","spread1","spread2","PPE"]
features_imp=features[imp_columns]


xtrain,xtest,ytrain,ytest=train_test_split(features_imp,target,train_size=0.7,random_state=0)  ## split data into training and testing parts

rf=RandomForestClassifier(random_state=0,n_jobs=-1)
rf.fit(xtrain,ytrain)



## layout of app: 
app.layout=html.Div(children=[                                   ## main div of app
dcc.Tabs(id='tabs',value='tbs',children=[                        ## declaring tabs 
    dcc.Tab(label='INFO',value="tab1",className="tb"),
    dcc.Tab(label="MODEL",value="tab2",className="tb")
],className="tbs"),
    
html.Div(id="tab-content")

])



@app.callback(
    Output('err','displayed'),
    Output('my-output','children'),
    [Input('button','n_clicks')],
    [State('fho','value'),
    State('fhi','value'),
    State('flo','value'),
    State('apq','value'),
    State('nhr','value'),
    State('spd1','value'),
    State('spd2','value'),
    State('ppe','value')]
    
)



def gt(n_clk,in1,in2,in3,in4,in5,in6,in7,in8):
    
    if n_clk is None:
        raise PreventUpdate
    else:
        xx=[in1,in2,in3,in4,in5,in6,in7,in8]
        c=0
        for i in xx:
            if i is None:
                c=1
        if c==1:
            return True,["enter all inputs properly"]

        else:    

            temp=np.array([in1,in2,in3,in4,in5,in6,in7,in8])
            temp_df=pd.DataFrame(temp[np.newaxis,:])
            out=rf.predict(temp_df)
            if out==1:
                out1=["YOU HAVE PARKINSON'S DISEASE."]
            
            else:
                out1=["YOU DON'T HAVE PARKINSON'S DISEASE."]
            
            return  False, out1



@app.callback(
    Output("tab-content","children"),
    Input("tabs","value")
)

def update_tab(tab):
    if tab=="tab1":
        return html.Div([html.P("Parkinson's disease :",className="p1"),
        html.P("Parkinson's disease is a progressive nervous system disorder that affects movement. Symptoms start gradually, sometimes starting with a barely noticeable tremor in just one hand. Tremors are common, but the disorder also commonly causes stiffness or slowing of movement.In the early stages of Parkinson's disease, your face may show little or no expression. Your arms may not swing when you walk. Your speech may become soft or slurred. Parkinson's disease symptoms worsen as your condition progresses over time.Although Parkinson's disease can't be cured, medications might significantly improve your symptoms. Occasionally, your doctor may suggest surgery to regulate certain regions of your brain and improve your symptoms."),
        
        html.P("Symptoms:",className="p1"),
        
        html.Ul(children=[
            html.Li(html.P("Tremor. A tremor, or shaking, usually begins in a limb, often your hand or fingers. You may rub your thumb and forefinger back and forth, known as a pill-rolling tremor. Your hand may tremble when it's at rest.")),
            html.Li(html.P("Slowed movement (bradykinesia). Over time, Parkinson's disease may slow your movement, making simple tasks difficult and time-consuming. Your steps may become shorter when you walk. It may be difficult to get out of a chair. You may drag your feet as you try to walk.")),
            html.Li(html.P("Rigid muscles. Muscle stiffness may occur in any part of your body. The stiff muscles can be painful and limit your range of motion")),
            html.Li(html.P("Impaired posture and balance. Your posture may become stooped, or you may have balance problems as a result of Parkinson's disease.")),
            html.Li(html.P("Loss of automatic movements. You may have a decreased ability to perform unconscious movements, including blinking, smiling or swinging your arms when you walk.")),
            html.Li(html.P("Speech changes. You may speak softly, quickly, slur or hesitate before talking. Your speech may be more of a monotone rather than have the usual inflections.")),
            html.Li(html.P("Writing changes. It may become hard to write, and your writing may appear small."))
         ],className="ulp"),

        html.P("Complications:",className="p1"),

        html.Ul(children=[
            html.Li(html.P("Thinking difficulties. You may experience cognitive problems (dementia) and thinking difficulties. These usually occur in the later stages of Parkinson's disease. Such cognitive problems aren't very responsive to medications")),
            html.Li(html.P("Swallowing problems. You may develop difficulties with swallowing as your condition progresses. Saliva may accumulate in your mouth due to slowed swallowing, leading to drooling.")),
            html.Li(html.P("Chewing and eating problems. Late-stage Parkinson's disease affects the muscles in your mouth, making chewing difficult. This can lead to choking and poor nutrition.")),
            html.Li(html.P("Sleep problems and sleep disorders. People with Parkinson's disease often have sleep problems, including waking up frequently throughout the night, waking up early or falling asleep during the day.")),
            html.Li(html.P("Blood pressure changes. You may feel dizzy or lightheaded when you stand due to a sudden drop in blood pressure (orthostatic hypotension).")),
            html.Li(html.P("Bladder problems. Parkinson's disease may cause bladder problems, including being unable to control urine or having difficulty urinating"))
        ],className="ulp")

        
        
        ])

    if tab=='tab2':
        return html.Div([
        html.P("features info:",className="p1"),
        html.P("MDVP:Fo(Hz) - Average vocal fundamental frequency"),
        html.P("MDVP:Fhi(Hz) - Maximum vocal fundamental frequency"),  
        html.P("MDVP:Flo(Hz) - Minimum vocal fundamental frequency"),
        html.P("MDVP:APQ - Several measures of variation in amplitude"),
        html.P("NHR - Two measures of ratio of noise to tonal components in the voice"),
        html.P("spread1,spread2,PPE - Three nonlinear measures of fundamental frequency variation"),
        html.Br(),
        html.H3("Enter Average Vocal Fundamental Frequency:",className="ips"),
        dcc.Input(id='fho',placeholder="enter value", type="number",className="dccin"),

        html.H3("Enter Maximum Vocal Fundamental Frequency:",className="ips"),
        dcc.Input(id='fhi',placeholder='enter value',type='number',className="dccin"),

        html.H3("Enter Minimum Vocal Fundamental Frequency:",className="ips"),
        dcc.Input(id='flo',placeholder='enter value',type='number',className="dccin"),

        html.H3("Enter MDVP-APQ:",className="ips"),
        dcc.Input(id="apq",placeholder="enter value",type='number',className="dccin"),

        html.H3("Enter NHR:",className="ips"),
        dcc.Input(id='nhr',placeholder='enter value',type='number',className="dccin"),

        html.H3("Enter spread1:",className="ips"),
        dcc.Input(id='spd1',placeholder='enter value',type='number',className="dccin"),

        html.H3("Enter spread2:",className="ips"),
        dcc.Input(id='spd2',placeholder='enter value',type='number',className="dccin"),

        html.H3("Enter PPE:",className="ips"),
        dcc.Input(id='ppe',placeholder='enter value',type='number',className="dccin"),

        html.Br(),
    
        html.Button('click me',id='button',n_clicks=None,type='submit',className="btn"),
        html.Br(),
        html.Br(),
        
        html.H3("Your output is:",className="out"),
        dcc.ConfirmDialog(id='err',message="Please fill all the inputs."),
        html.Div(id="my-output",className="output")
    ])






if __name__=="__main__":
    app.run_server(debug=True)