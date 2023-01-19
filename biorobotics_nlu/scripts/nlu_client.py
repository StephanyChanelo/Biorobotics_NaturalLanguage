
#!/usr/bin/env python
#import sys
import rospy
from biorobotics_nlu.srv import SParser

def nlu_client(text):
    rospy.init_node('service_client')
    rospy.wait_for_service('spacy_parser_service')
    sparser_function = rospy.ServiceProxy('spacy_parser_service', SParser)
    response = sparser_function(text)
    print(response.cds)

if __name__ == "__main__":
    frase = input("Enter a command: ")
    nlu_client(frase)
