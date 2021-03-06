# Canvas Auto Rubric

Please find the detailed documentation [here](https://tc-imba.github.io/canvas-auto-rubric).

* [`canvasautorubric`](https://tc-imba.github.io/canvas-auto-rubric/canvasautorubric) - Sync the rubric on canvas.

![Terminal](docs/record/record.gif)

* [`canvasautoplot`](https://tc-imba.github.io/canvas-auto-rubric/canvasautoplot) - Plot the grade distribution.

![Sample Output](docs/images/sample.png)

## Installation

(choose one of these methods)

### Install as a Python Library

```bash
pip3 install git+https://github.com/tc-imba/canvas-auto-rubric.git@master
```

### Local Install or Debug

```bash
git clone git@github.com:tc-imba/canvas-auto-rubric.git
cd canvas-auto-rubric
# you can setup a virtual python env before install here
pip3 install -e .
```

## Licence        
                  
Apache 2.0        
                  
## Dependencies   
                  
* canvasapi==1.0.0
* click           
* pbr             
* logzero         
* scipy           
* pandas          
* openpyxla       
* matplotlib      
* enlighten       