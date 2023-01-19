# Biorobotics_NaturalLanguage
Using the Spacy Parser to build the conceptual dependencies

## Setup
**Clone this repository into the src folder:**

```ruby
git clone https://github.com/StephanyChanelo/Biorobotics_NaturalLanguage
```
**You need a structure like this: catkin_ws/src/biorobotics_nlu**
```
├── ...
| catkin_ws                   
│   └── src         
│        └── biorobotics_nlu         
|              └── ...
└──
```
**You may need to install the spacy library: https://spacy.io/usage**

```ruby
pip install -U pip setuptools wheel
pip install -U spacy
python -m spacy download en_core_web_sm
```

**Build the project**
```ruby
cd catkin_ws
source devel/setup.bash
catkin_make
```

## Initialization
**Start ROS in one terminal**

```ruby
roscore
```

**Start the nlu_server on a different terminal**

```ruby
rosrun biorobotics_nlu nlu_server.py
```



