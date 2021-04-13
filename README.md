# Installation

1. Install the required python modules using 

``` pip  install jupyterlab Flask==1.1.2 lightgbm==3.0.0 nexmo==2.5.2 matplotlib==3.3.2 plotly==4.12.0 plotly-express==0.4.1 python-dotenv==0.15.0 nltk==3.5 numpy==1.19.2 pandas==1.1.3 regex==2020.10.23 scikit-learn==0.23.2 wordcloud==1.8.0 ```


2. To compile the AppHttpPostJson.java                [optional] 

   Go to the `spam-detection\web_app\JavaFiles\HttpPostJsonReq\src` folder and type 
    ```javac -cp ..\lib\json-20201115.jar AppHttpPostJson.java```


# How to Run

1. Go to spam-detection\web_app and run 

``` python app.py ```

2. Go to the `spam-detection\web_app\JavaFiles\HttpPostJsonReq\src` folder and type  

``` java -cp .;..\lib\json-20201115.jar AppHttpPostJson ```
