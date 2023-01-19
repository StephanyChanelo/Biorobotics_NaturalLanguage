
#!/usr/bin/env python

import rospy
import sys
import spacy
import numpy as np
from biorobotics_nlu.srv import SParser, SParserResponse

CD_structures = { "go" : "PTRANS",
"navigate" : "PTRANS",
"walk" : "PTRANS",
"lead" : "PTRANS",
"guide" : "PTRANS",
"meet" : "PTRANS",
"follow" : "PTRANS",
"bring" : "ATRANS",
"give" : "ATRANS",
"deliver" : "ATRANS",
"take" : "GRASP",
"find" : "ATTEND",
"look" : "ATTEND",
"open" : "PROPEL",
"close" : "PROPEL",
"push" : "PROPEL",
"pull" : "PROPEL"
    }

def sparser_callback(request):

  print("=====================================================================")
  print("                          SPACY PARSER                               ")
  print("=====================================================================")

  verb_list = []
  prim_list = []
  pron_list = []
  pos_list = []
  obj = []
  loc = []

#Remove the word "Robot" in order to obtain a clean separation of the types of "obj"
  frase = str(request.text)
  frase = frase.replace('Robot,', '')
  print(frase)

  #Extracting tokens from the sentence
  nlp = spacy.load("en_core_web_sm")
  doc = nlp(frase)

  #Creating the list of nouns and positions
  for token in doc:
      text_list = [token.text for token in doc]
      pos_list1 = [token.pos_ for token in doc]
  print("INITIAL LIST: ")
  print(text_list)
  print(pos_list1)

  print("=====================================================================")

  pron_list = [chunk.text for chunk in doc.noun_chunks]
  pos_list = [[t.pos_ for t in chunk]for chunk in doc.noun_chunks]
  print("PRONOUN LIST: ")
  print(pron_list)
  print("POSITION LIST: ")
  print(pos_list)

  verb_list = [token.lemma_ for token in doc if token.pos_ == "VERB"]
  print("VERB LIST: ")
  print(verb_list)

#=======================================================================
#If doesn't exist verb or nouns then send a request for a new sentece
  if len(verb_list) == 0 or len(pron_list) == 0:
      print("I can't understand you.")
  else:

  #Sentences with structures like: [NOUN]+[ADP]+[NOUN], ex: ... a glass of water
  #Sentences with structures like: [NOUM]+[CCONJ]+[NOUN], ex: ... coffee and donuts
  #These sentences need to check for two consecutive nouns in the noun_list and analize
  #the type of word between them.
      for pos in range(len(pos_list)):
          if pos_list[pos] == ["NOUN"] and pos_list[pos-1][-1] == "NOUN":
              #print("<--------------------------")
              inter = text_list[text_list.index(pron_list[pos])-1]
              #int = pos_list1[text_list.index(pron_list[pos])+1]

              if inter == "of":
                  new_noun = pron_list[pos-1] + " "+ inter + " " +pron_list[pos]
                  pron_list[pos-1] = new_noun
                  pron_list = np.delete(pron_list, [pos])
                  #print(pron_list)


  #Sentences where "me" the recipient of the action, ex: give me ....
  #Check for the word me, which change the order of noun_list, so the word "me" is added
  #to the end of the list instead of the beggining
      s = len(pron_list)-1
      for m in range(len(pron_list)):
          if pos_list[m] == ['PRON'] and m != s:
              pron_b =  pron_list[m]
              pron_list[m] = pron_list[m+1]
              pron_list[m+1] = pron_b


  #Sentences like: give Mary an apple ---> [PROPN] [DET] [NOUN]
      """for per in range(len(pos_list1)):
          if pos_list1[per] == 'PROPN' and pos_list1[per+1] == 'DET' and pos_list1[per+2] == 'NOUN':
              find_propn = pron_list.index(text_list[per])
              propn = pron_list[find_propn]
              #print(propn)
              pron_list[find_propn] = pron_list[find_propn+1]
              pron_list[find_propn+1] = propn"""


  #Sentences where her o him are included, ex: ... and give an apple to her
  #Check for the words "her" or "him" and replace them with the last PROPN
      for pron in range(len(pron_list)):
          if pron_list[pron] == 'her' or pron_list[pron] == "him":
              for i in range(len(pos_list)):
                  for p in pos_list[i]:
                      if p == "PROPN":
                          pron_list[pron] = pron_list[i]
                          break


      for k in verb_list:
          prim_list = np.append(prim_list, CD_structures[k])
          #print(prim_list)

      print("=====================================================================")
      print("                     CONCEPTUAL DEPENDENCIES                         ")
      print("=====================================================================")

  #Building the DC structure
      cds = str()
      for k in range(len(prim_list)):
          if prim_list[k] == 'PTRANS':
              #cd = prim_list[k]+'((ACTOR Robot)(OBJECT Robot)(FROM Robot place)(TO '+pron_list[0]+'))'
              cd = prim_list[k]+'((ACTOR Robot)(OBJECT Robot)(TO '+pron_list[0]+'))'
              cd = cd.lower()
              print(cd)
              cds = cds + " " + cd
              pron_list = np.delete(pron_list, 0)
          elif prim_list[k] == 'ATRANS':
              #cd = prim_list[k]+'((ACTOR Robot)(OBJECT '+pron_list[0]+')(FROM '+pron_list[0]+ ' place)(TO '+pron_list[1]+'))'
              cd = prim_list[k]+'((ACTOR Robot)(OBJECT '+pron_list[0]+')(TO '+pron_list[1]+'))'
              cd = cd.lower()
              print(cd)
              cds = cds + " " + cd
              pron_list = np.delete(pron_list, 0)
              pron_list = np.delete(pron_list, 0)
          elif prim_list[k] == 'ATTEND':
              cd = prim_list[k]+'((ACTOR Robot)(TO '+pron_list[0]+'))'
              cd = cd.lower()
              cds = cds + " " + cd
              print(cd)
              pron_list = np.delete(pron_list, 0)
          elif prim_list[k] == 'GRASP':
              cd = prim_list[k]+'((ACTOR Robot)(OBJ '+pron_list[0]+'))'
              cd = cd.lower()
              cds = cds + " " + cd
              print(cd)
              pron_list = np.delete(pron_list, 0)
          elif prim_list[k] == 'PROPEL':
              cd = prim_list[k]+'((ACTOR Robot)(OBJ '+pron_list[0]+'))'
              cd = cd.lower()
              cds = cds + " " + cd
              print(cd)
              pron_list = np.delete(pron_list, 0)

  cds = str(cds)
  print("=====================================================================")
  print("=====================================================================")
  print("=====================================================================")
  print("Conceptual Dependencies: " +  cds)
  cds = cds.replace('\\', '')
  return cds

def nlu_server():
  rospy.init_node('spacy_parser')
  service = rospy.Service('spacy_parser_service', SParser, sparser_callback)
  print("Ready to parser...")
  rospy.spin()

if __name__ == "__main__":
    nlu_server()
