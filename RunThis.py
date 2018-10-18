from flask import Flask, request, render_template, url_for, redirect
app = Flask(__name__)
from sklearn.neural_network import MLPClassifier
import csv
import random
import math
import numpy as np
import time
from datetime import datetime
from flask_moment import Moment
import importlib

moment = Moment(app)

def import_data():
    data = np.loadtxt('hpdata.csv', dtype=np.float)
    y = data[:,-1]
    x = data[:,:-1]
    return x,y

def ensemble(reg,mlp,nb,dt):
    countW = 0
    countR = 0
    countB = 0
    lst = [reg,mlp,nb,dt]

    for i in range (len(lst)):
        if lst[i] == "White":
            countW = countW + 1
        if lst[i] == "Red":
            countR = countR + 1
        if lst[i] == "Black":
            countB = countB + 1

    if (countR > 1 and countW < 2 and countB < 2):
        print( "\nOverall prediction is Red since",countR, "models predict so")
    elif (countB > 1 and countR < 2 and countW < 2):
        print( "\nOverall prediction is Black since",countB, "models predict so")
    elif (countW > 1 and countR < 2 and countB < 2):
        print( "\nOverall prediction is White since",countW, "models predict so")
    else:
        print( "\nSince there's equity among the models, MLP prevails due to higher weightage")
        print( "Overall prediction is thus", mlp)

    print( "----------------------------------------------------------")
    return mlp

def decision(Gender, Age, Education):
    if(Age>29):
        if (Education=="Tertiary"):
            if(Gender=="M"):
                return("Black")
            else:
                if(Age>40):
                    return("White")
                else:
                    return("Black")
        else:
            return("White")
    elif(Age<=29):
        if(Gender=="F" and (Education=="Tertiary" or Education=="Primary" or Education=="Secondary")):
            return("Red")
        else:
            if(Education=="Tertiary"):
                return("Black")
            else:
                return("White")

def mlp(X,y,Gender,Age,Edu):
    clf = MLPClassifier(solver='lbfgs', alpha=1e-1, hidden_layer_sizes=(5,2), random_state=1)
    clf.fit(X,y)
    result = clf.predict([[Gender,Age,Edu]])
    if result==1:
        return "Black"
    elif result ==2:
        return "Red"
    else:
        return "White"

def reg(int_Gender, Age, Edu):

    A_gender  = -0.562186054990492
    B_Age  = 0.0183349975122713
    C_Education = 0.310168168067336
    D_Intercept = 1.60494509174322
    Eqn = [A_gender, B_Age, C_Education, D_Intercept]

    RWB = [1,2,3]
    Color = ["Red", "White", "Black"]

    Inputs = [int_Gender, Age, Edu, 1]
    Label = np.multiply(Eqn,Inputs)
    Score = sum(Label)
    Min = 5
    for i in range(len(RWB)):
        if abs(Score - RWB[i])<Min:
            Min = abs(Score - RWB[i])
            Colorindex = i

    return Color[Colorindex]

def nb(Gender, Age, Education):
    Female  = [1,0.584745763,0.272727273]
    Male  = [0,0.415254237,0.727272727]
    Age1 = [0.263157895,0.059322034,0.022727273]
    Age2 = [0.736842105,0.050847458,0.159090909]
    Age3 = [0,0.262711864,0.363636364]
    Age4 = [0,0.296610169,0.227272727]
    Age5 = [0,0.330508475,0.227272727]
    Primary = [0.342105263,0.457627119,0.022727273]
    Secondary = [0.394736842,0.415254237,0]
    Tertiary = [0.263157895,0.127118644,0.977272727]
    RWB = [0.19 ,0.59,0.22]
    Color = ["Red", "White", "Black"]

    if Gender.upper() =="F":
        PGender = Female
    if Gender.upper() =="M":
        PGender = Male

    AgeRange = Age/10

    if AgeRange <= 1 :
        PAge = Age1
    elif AgeRange <=2:
        PAge = Age2
    elif AgeRange <=3:
        PAge = Age3
    elif AgeRange <=4:
        PAge = Age4
    elif AgeRange >=5:
        PAge = Age5

    if Education == 1 or Education == 2:
        PEdu = Primary
    elif Education == 3:
        PEdu = Secondary
    elif Education == 4:
        PEdu = Tertiary


    Prob1 = np.multiply(PGender,PAge)
    Prob2 = np.multiply(Prob1,PEdu)
    Prob = np.multiply(Prob2,RWB)

    Max = 0
    for i in range(len(Prob)):
        if Prob[i]>Max:
            Max = Prob[i]
            Colorindex = i

    Score = Prob[Colorindex]/sum(Prob)

    return Color[Colorindex]


@app.route('/newcampaigninputs', methods=['GET', 'POST'])
def newcampinputs():
    if request.method == 'POST':
        hpcolor = request.form.get('hpcolor')
        print('hpcolor')
        Gender = request.form.get('Gender')
        campaign_name = request.form.get('CampaignName')
        Education = int(request.form.get('Education'))
        no_of_images = int(request.form.get('numofimages'))
        if hpcolor == 'Handphone Colour':
            print("hpcolor is: " + str(hpcolor))
            print(Gender)
            if Gender.upper() == "F":
                int_Gender = 2
            elif Gender.upper() == "M":
                int_Gender = 1
            print(campaign_name)    

            print(type(request.form.get('Age')))
            Age = int(request.form.get('Age'))
            print(Age)
            print(Education)
            if Education == 1 or Education == 2:
                Edu = 1
                strEdu = "Primary"
            elif Education == 3:
                Edu = 2
                strEdu = "Secondary"
            elif Education == 4:
                Edu = 3
                strEdu = "Tertiary"

            X, y = import_data()

            reg_result = reg(int_Gender, Age, Edu)
            mlp_result = mlp(X, y, int_Gender, Age, Edu)
            nb_result = nb(Gender, Age, Edu)
            dt_result = decision(Gender.upper(), Age, strEdu)

            print("Training Phase.....\n")
            time.sleep(1.5)
            print("Linear Regression predicts : ", reg_result)
            time.sleep(0.1)
            print("              MLP predicts : ", mlp_result)
            time.sleep(0.1)
            print("      Naive Bayes predicts : ", nb_result)
            time.sleep(0.1)
            print("    Decision Tree predicts : ", dt_result)
            time.sleep(0.2)

            color = ensemble(reg_result, mlp_result, nb_result, dt_result)
            if Gender == 'M':
            	gend = 'Male'
            elif Gender == 'F':
            	gend = 'Female'
            return render_template('Insight Report.html', current_time = datetime.utcnow(), campaign_name = campaign_name, age = Age, gender = gend, education = strEdu, hphone = hpcolor, color = color)
        elif hpcolor == 'Premier Face Tissue':
        	return redirect(url_for('premier_tissue', current_time=datetime.utcnow(), no_of_images = no_of_images))
        elif hpcolor == 'Cutie Tissue Campaign':
            moduleName = "CutieLogo"
            logo_maker = importlib.import_module(moduleName)
            logo_maker.cutie_logo_maker(no_of_images)
            return redirect(url_for('cutie_tissue', current_time = datetime.utcnow(), no_of_images = no_of_images))
    else:
        return render_template('New Campaign inputs.html', current_time=datetime.utcnow())

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] !=  'ntpm' or request.form['password'] != 'Campaign1':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('dashboard', username="ntpm"))
    return render_template('login.html', error=error)

@app.route('/dashboard/<username>', methods =['GET', 'POST'])
def dashboard(username):
    if request.method == 'POST':
        if request.form['submit'] == 'ACCESS FULL REPORT':
            return redirect(url_for('dashboard', username="ntpm"))
        elif request.form['submit'] == '+ NEW PROJECT':
            return redirect(url_for('newcampinputs'))
        else:
            return redirect(url_for('dashboard'))
    elif request.method == 'GET':
    	return render_template('Main Dashboard.html', username = username, current_time=datetime.utcnow())


@app.route('/premier_tissue/<no_of_images>')
def premier_tissue(no_of_images):
    return render_template('Premier Tissue.html', current_time=datetime.utcnow(), num_of_imgs = no_of_images)

@app.route('/cutie_tissue/<no_of_images>', methods = ['GET', 'POST'])
def cutie_tissue(no_of_images):
    return render_template('Cutie Tissue.html', current_time = datetime.utcnow(), num_of_imgs = no_of_images)

if __name__== "__main__":
 app.run(debug=True)
