# Welcome to AmbitiousEffect page



# Actors

The principle actor is the user that have direct contact with his virtual assistant.

# Preconditions

The application is installed on device and also a register is made in scope of a better user experience with the assistent. (?)

# Flow

1.The user is logged in (?) 

2.the user is informed with a day before on what should eat - this is more like a negociation, because the assistant show a list of menus and the user choose the menu and also the weight. In this way, the assistant pop up the reminder with a day before in scope to purchase the ingredients for the meal.

3.the user is informed about the menu from that day  with an hour before, the exception is in the morning because it is reminded in previous flow

4.The assistant wants necessary information from the user to create a concrete profile. The necessary are: alimentation preferences, day by day activities, height and weight of the user and other medical condition and problems. 

5.The user provide a feedback after each meal in wich a rating si provided and the user can specify some ingredients. Both interactions are made in natural language.

6.The application display the evolution of the user by graphics that are used for future actions.

7. Number of steps that are made by the user is an important factor for calculation of calories, in this case the application must provide this number of steps that can help in statistics and other function like meal recommendation.

# Arhitecture
## There are two broad approach to knowledge search:
### 1.Ontology based Knowledge Search (Mainly through knowledge Graph)
### 2.Knowledge Search through Open Domain Question Answering

High Level Architecture of a question answering module
https://miro.medium.com/max/875/1*sbAR0BSuof6bgKUcv6zNUA.png

## NLU Layer
The main purpose of NLU layer is to build a Graph Query From the Text. This is one of the bottle neck of Ontology Based Knowledge Search which is making a structured query (in GQL) from free flow of text (Open domain question answering try to solve this in a neural manner)
## Machine Translation Block
This is also not mandatory In case of Language agnostic Knowledge Graph. There are two ways to build Knowledge Graph which is language agnostic and Language Aware. Most of the Public knowledge Graph is Language agnostic (Beyond the scope of this article.
## Steps
### Train speech to text model for each language supported
### Store structured knowledge (subject, predicate, object) like wikidata or dbpedia (Crawled Wikipedia) into a Knowledge graph
### Enrich and store knowldge from unstructured news article and other sources into the knowledge graph.
### Text2Intent layer to understand (classification) user intent
### Build NLU (Natural Language Understanding) Layer to understand user query or command or Intent (look at rasa)
### Query Adapter layer to knowledge graph for intent to Graph Query Language (GQL)
### Integration hook with home automation or other third party apps
### NLG (Natural Language Generation) layer
### Conversational chatbot design
### Machine Translation layer to translate english to supported language (optional).
### Text2Speech model for each language supported
