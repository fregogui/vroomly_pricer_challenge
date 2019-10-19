import csv

vehicle ="77752"
intervention="front_brake_pads"

##Parse article_vehicle_relations file and store the result in a dict. It is not necessary if we need only one request but it will be helpfull to extend 

articleByVehicle={}

with open('./data/article_vehicle_relations.csv', newline='') as csvfile:
  reader = csv.reader(csvfile, delimiter=',')
  next(reader, None)  # skip the headers
  for row in reader:
    if row[0] not in articleByVehicle: #attention au titre
      articleByVehicle[row[0]]=set()
    articleByVehicle[row[0]].add(row[1])

articleByType={}
with open('./data/articles.csv', newline='') as csvfile:
  reader = csv.reader(csvfile, delimiter=',')
  next(reader, None)  # skip the headers
  for row in reader:
    if row[0] not in articleByType:
      articleByType[row[0]]=set()
    articleByType[row[0]].add(row[2])

articlesByIntervention={
  "front_brake_pads": {
    "brake_pad":4
  },
  "front_brake_rotors_and_pads":{
    "brake_pad":4,
    "brake_rotor":2
  },
  "oil_change":{},
  "injectors":{}
}




def getPrice(intervention,vehicle):
  print(articleByType["brake_pad"].intersection(articleByVehicle[vehicle]))

getPrice(intervention,vehicle)

#questions: oil filter = fuel filter ?
