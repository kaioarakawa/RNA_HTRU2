# -*- coding: utf-8 -*-
"""RNA.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1XCL_OArTFhRV9sk3CC4EssxQEgjmM1bW
"""

# Commented out IPython magic to ensure Python compatibility.
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
import itertools
warnings.filterwarnings("ignore")
# %matplotlib inline
from PIL import Image

img = np.array(Image.open("/content/data/__results___2_0.png"))
plt.figure(figsize=(15,12))
plt.imshow(img)
plt.axis("off")
plt.show()

data = pd.read_csv(r"/content/data/pulsar_stars.csv")
data.head()

print ("Number of rows    :",data.shape[0])
print ("Number of columns :",data.shape[1])

print ("data info  :",data.info())

print (data.isnull().sum())
data = data.rename(columns={' Mean of the integrated profile':"mean_profile",
       ' Standard deviation of the integrated profile':"std_profile",
       ' Excess kurtosis of the integrated profile':"kurtosis_profile",
       ' Skewness of the integrated profile':"skewness_profile", 
        ' Mean of the DM-SNR curve':"mean_dmsnr_curve",
       ' Standard deviation of the DM-SNR curve':"std_dmsnr_curve",
       ' Excess kurtosis of the DM-SNR curve':"kurtosis_dmsnr_curve",
       ' Skewness of the DM-SNR curve':"skewness_dmsnr_curve",
       })

plt.figure(figsize=(12,8))
sns.heatmap(data.describe()[1:].transpose(),
            annot=True,linecolor="w",
            linewidth=2,cmap=sns.color_palette("Set2"))
plt.title("Data summary")
plt.show()

correlation = data.corr()
plt.figure(figsize=(10,8))
sns.heatmap(correlation,annot=True,
            cmap=sns.color_palette("magma"),
            linewidth=2,edgecolor="k")
plt.title("CORRELATION BETWEEN VARIABLES")
plt.show()

st = data[data["target_class"] == 1].reset_index()
nst= data[data["target_class"] == 0].reset_index()
new = pd.concat([nst,st]).reset_index()

plt.figure(figsize=(13,10))
plt.stackplot(new.index,new["mean_profile"],
              alpha =.5,color="b",labels=["mean_profile"])
plt.stackplot(new.index,new["std_profile"],
              alpha=.5,color="r",labels=["std_profile"])
plt.stackplot(new.index,new["skewness_profile"],
              alpha=.5,color ="g",labels=["skewness_profile"])
plt.stackplot(new.index,new["kurtosis_profile"],
              alpha=.5,color = "m",labels=["kurtosis_profile"])
plt.axvline(x=16259,color = "black",linestyle="dashed",
            label = "separating pulsars vs non pulsars")
plt.axhline(new["mean_profile"].mean(),color = "b",
            linestyle="dashed",label = "average mean profile")
plt.axhline(new["std_profile"].mean(),color = "r",
            linestyle="dashed",label = "average std profile")
plt.axhline(new["skewness_profile"].mean(),color = "g",
            linestyle="dashed",label = "average skewness profile")
plt.axhline(new["kurtosis_profile"].mean(),color = "m",
            linestyle="dashed",label = "average kurtosis profile")
plt.legend(loc="best")
plt.title("Area plot for attributes for pulsar stars vs non pulsar stars")
plt.show()

from mpl_toolkits.mplot3d import Axes3D
fig = plt.figure(figsize=(13,13))
ax  = fig.add_subplot(111,projection = "3d")

ax.scatter(data[data["target_class"] == 1][["mean_profile"]],data[data["target_class"] == 1][["std_profile"]],data[data["target_class"] == 1][["skewness_dmsnr_curve"]],
           alpha=.5,s=80,linewidth=2,edgecolor="k",color="lime",label="Pulsar star")
ax.scatter(data[data["target_class"] == 0][["mean_profile"]],data[data["target_class"] == 0][["std_profile"]],data[data["target_class"] == 0][["skewness_dmsnr_curve"]],
           alpha=.5,s=80,linewidth=2,edgecolor="k",color="r",label=" NotPulsar star")

ax.set_xlabel("mean_profile",fontsize=15)
ax.set_ylabel("std_profile",fontsize=15)
ax.set_zlabel("skewness_dmsnr_curve",fontsize=15)
plt.legend(loc="best")
fig.set_facecolor("w")
plt.title("3D PLOT FOR MEAN_PROFILE VS STD_PROFILE VS SKEWNESS_DMSNR_CURVE",fontsize=10)
plt.show()

from sklearn.model_selection import train_test_split

train , test = train_test_split(data,test_size = .3,random_state = 123)

plt.figure(figsize=(12,6))
plt.subplot(121)
train["target_class"].value_counts().plot.pie(labels = ["not star","star"],
                                              autopct = "%1.0f%%",
                                              shadow = True,explode=[0,.1])
plt.title("proportion of target class in train data")
plt.ylabel("")
plt.subplot(122)
test["target_class"].value_counts().plot.pie(labels = ["not star","star"],
                                             autopct = "%1.0f%%",
                                             shadow = True,explode=[0,.1])
plt.title("proportion of target class in train data")
plt.ylabel("")
plt.show()

train_X = train[[x for x in train.columns if x not in ["target_class"]]]
train_Y = train[["target_class"]]
test_X  = test[[x for x in test.columns if x not in ["target_class"]]]
test_Y  = test[["target_class"]]

#MODEL FUNCTION

from sklearn.metrics import classification_report,confusion_matrix,accuracy_score,roc_curve,auc

def model(algorithm,dtrain_x,dtrain_y,dtest_x,dtest_y,of_type):
    
    print ("*****************************************************************************************")
    print ("MODEL - OUTPUT")
    print ("*****************************************************************************************")

    algorithm.fit(dtrain_x,dtrain_y)
    predictions = algorithm.predict(dtest_x)

  
    
    print (algorithm)
    print ("\naccuracy_score :",accuracy_score(dtest_y,predictions))

    print ("\nclassification report :\n",(classification_report(dtest_y,predictions)))
        
    plt.figure(figsize=(13,10))
    plt.subplot(221)
    sns.heatmap(confusion_matrix(dtest_y,predictions),annot=True,fmt = "d",linecolor="k",linewidths=3)
    plt.title("CONFUSION MATRIX",fontsize=20)
    
    predicting_probabilites = algorithm.predict_proba(dtest_x)[:,1]
    fpr,tpr,thresholds = roc_curve(dtest_y,predicting_probabilites)
    plt.subplot(222)
    plt.plot(fpr,tpr,label = ("Area_under the curve :",auc(fpr,tpr)),color = "r")
    plt.plot([1,0],[1,0],linestyle = "dashed",color ="k")
    plt.legend(loc = "best")
    plt.title("ROC - CURVE & AREA UNDER CURVE",fontsize=20)

    
    if  of_type == "feat":
        
        dataframe = pd.DataFrame(algorithm.feature_importances_,dtrain_x.columns).reset_index()
        dataframe = dataframe.rename(columns={"index":"features",0:"coefficients"})
        dataframe = dataframe.sort_values(by="coefficients",ascending = False)
        plt.subplot(223)
        ax = sns.barplot(x = "coefficients" ,y ="features",data=dataframe,palette="husl")
        plt.title("FEATURE IMPORTANCES",fontsize =20)
        for i,j in enumerate(dataframe["coefficients"]):
            ax.text(.011,i,j,weight = "bold")
    
    elif of_type == "coef" :
        
        dataframe = pd.DataFrame(algorithm.coef_.ravel(),dtrain_x.columns).reset_index()
        dataframe = dataframe.rename(columns={"index":"features",0:"coefficients"})
        dataframe = dataframe.sort_values(by="coefficients",ascending = False)
        plt.subplot(223)
        ax = sns.barplot(x = "coefficients" ,y ="features",data=dataframe,palette="husl")
        plt.title("FEATURE IMPORTANCES",fontsize =20)
        for i,j in enumerate(dataframe["coefficients"]):
            ax.text(.011,i,j,weight = "bold")
            
    elif of_type == "none" :
        return (algorithm)


    print ("\nfpr :",auc(fpr,tpr))
    print ("\ntpr :",auc(tpr,fpr))

from sklearn.ensemble import RandomForestClassifier
rf =RandomForestClassifier()
model(rf,train_X,train_Y,test_X,test_Y,"feat")