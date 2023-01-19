#include "ros/ros.h"
#include "biorobotics_nlu/SParser.h"
#include <cstdlib>

int main(int argc, char **argv)
{
  ros::init(argc, argv, "spacy_parser_client");
  ros::NodeHandle n;
  ros::ServiceClient client = n.serviceClient<biorobotics_nlu::SParser>("spacy_parser_service");
  biorobotics_nlu::SParser srv;
  std::string aux ="";
  std::string cds ="";

  //std::cout<<"argc "<< argc<<std::endl;
  srv.request.text = "";
  for( int i=1; i<argc; i++){
    aux= argv[i];
    srv.request.text.append(aux).append(" ");
    //std::cout<<"argv "<< argv[i]<<std::endl;
  }
  std::cout<<"request "<< srv.request.text<<std::endl;

  if (client.call(srv))
  {
      cds = srv.response.cds;
      std::cout<<"cds: "<< cds <<std::endl;
  }
  else
  {
    ROS_ERROR("Failed to call service Service X______________X");
    return 1;
  }
  return 0;
}
