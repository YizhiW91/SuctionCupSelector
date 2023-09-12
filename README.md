# SuctionCupSelector
The project is for recommending suction cups in piece picking automation process with robotic arms


## Table of Contents
- [Summary](#summary)
- [Run the app](#run the app)
- [Features](#features)
- [License](#license)


## Summary

The project contains data analysis and the webpage for user to access the tools. Here is the list of key files and purpose of each file:

* Suction Cup Configuration Automation
    * SuctionCupRules.py - This is the implementation of the suction cup selection rules.
    * notebook.ipynb - This is the Jupyter notebook for demonstrating the process of batch suction cup selection.
* AB Test
    * ABTestToolKit.py - This is the file that contiains the utility functions for AB test analysis.
    * AB_test.ipynb - This is the prerequsite guide for beginner to start AB test
    * PickingDataProcess.ipynb - This is the Jupyter notebook for demonstrating the process of batch AB test analysis.
* Webpage
    * Suction_Cup_Configuration.py - This is the home page of the streamlit webpage.
    * pages/2_AB_Test_Sample_Size_Calculator.py - This is page for sample size calculation.
    * pages/3_AB_Test_Analyzer.py - This is page for AB test.
    * Checkout the webpage at [SuctionCupAnalysisTool](https://suctioncupselector.streamlit.app)

<p align="center">
  <img src="suctionCupInitializerDemo.gif" width="400px">
</p>


## Run the app

### Install the Python Dependency

The project uses Python 3.9. You can create a virtual environment and run the following command to install the required packages.

```cli
pip install -r requirements.txt
```

To run the webpage locally, please run:

```cli
streamlit run Suction_Cup_Configuration.py
```

### Docker

Alternatively, with Docker, use the following command and then navigate to localhost.

```
docker run -dp 80:8080 ryanfox212/samplesize
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.