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
## Usage
**Run the nlu_client on a different terminal**

**- python client**

```
NOTE 1: The client will ask you for a command.
NOTE 2: The personal pronouns have to start with capital letters: Robot, Mary, John
For example: 
* go to the bedroom
* give the book to the mother
* go to the kitchen, find Mary and deliver an apple to her
* Robot, give me an apple
```
```ruby
rosrun biorobotics_nlu nlu_client.py
```

**- c++ client**
```
NOTE 1: You need to give a command just after the name of the script.
NOTE 2: The personal pronouns have to start with capital letters: Robot, Mary, John

```

```ruby
rosrun biorobotics_nlu nlu_server_client_c go to the kitchen
```



