from rdflib import Graph, RDF, URIRef,  RDFS #, Literal, BNode
from SPARQLWrapper import SPARQLWrapper, JSON
import sys, getopt

class ServiceSystem:
    'A API to a Service Systems'
    filename = ''
    g = Graph()
    print g

    def __init__(self, filename):
        ServiceSystem.filename = filename
        ServiceSystem.g.parse(filename, format='n3')

    #------------------------------------------------------------------
    #---------- Show information about the Service System -------------
    #------------------------------------------------------------------
    def getServiceInformation(self):
        URIServiceSystem = URIRef("http://w3id.org/lss-usdl/v2#ServiceSystem")
        if ( None, RDF.type, URIServiceSystem ) in ServiceSystem.g:
            lss = ServiceSystem.g.value(predicate = RDF.type, object = URIServiceSystem, any = False)
            #print "Service System found! " + lss
        else:
            raise Exception("Cannot find Service System!!")

        if ( None, RDF.type, URIServiceSystem ) in ServiceSystem.g:
            lss_description = ServiceSystem.g.value(predicate = RDFS.comment, subject = lss, any = False)
            #print "Service System description found! " + lss_description
        else:
            raise Exception("Cannot find Service System description!!")

# Can also be done this way
#       for lss in ServiceSystem.g.subjects(RDF.type, URIRef("http://w3id.org/lss-usdl/v2#ServiceSystem")):
#           print "Service System Name: ", lss.rsplit("#", 2)[1]
#       for lss_description in ServiceSystem.g.objects(lss, RDFS.comment):
#           print "Description:", lss_description

        information=[]
        information.append(lss)
        information.append(lss_description)

        return information


    #------------------------------------------------------------------
    #-------------- Get Interactions   --------------------------------
    #------------------------------------------------------------------
    def getInteractions(self):
        qres = ServiceSystem.g.query(
            """PREFIX  lss-usdl:  <http://w3id.org/lss-usdl/v2#>
                SELECT DISTINCT ?a ?b
                WHERE {
                  ?a lss-usdl:hasInteraction ?b .
                }""")

        results = []
        for row in qres:
            s, r = row
            sl = s.rsplit("#", 2)[1]
            rl = r.rsplit("#", 2)[1]
            results.append(rl)

        return results

# Can also be done this way
#       print("")
#       print "--- Interaction Points: ---"
#       for sub, obj in ServiceSystem.g.subject_objects(URIRef("http://w3id.org/lss-usdl/v2#hasInteraction")):
#          interaction = obj.rsplit("#", 2)[1]
#          print interaction


    #------------------------------------------------------------------
    #-------------- Connectors ----------------------------------------
    #------------------------------------------------------------------
    def getConnectors(self):
        qres = ServiceSystem.g.query(
            """PREFIX  lss-usdl:  <http://w3id.org/lss-usdl/v2#>
                SELECT DISTINCT ?src ?tgt ?cond
                WHERE {
                  ?ss lss-usdl:hasControlFlow ?cf.
                  ?cf lss-usdl:hasSource ?src  .
                  ?cf lss-usdl:hasTarget ?tgt .
                  ?cf lss-usdl:hasCondition ?cond .
                }""")

        results = []
        for row in qres:
            src, tgt, cond = row
            source = src.rsplit("#", 2)[1]
            target = tgt.rsplit("#", 2)[1]
            condition = cond
            results.append([source, target, condition])
            #str = 'ControlFlow (' + source + ' -> ' + target + ') with condition "' + condition + '"'''
            #print str

        return results


    #------------------------------------------------------------------
    #-------------- Get Service Roles ---------------------------------
    #------------------------------------------------------------------
    def getRoles(self):
        qres = ServiceSystem.g.query(
            """PREFIX  lss-usdl:  <http://w3id.org/lss-usdl/v2#>
                SELECT DISTINCT ?role
                WHERE {
                  ?s ?prop ?o .
                  ?lss lss-usdl:hasInteraction ?int .
                  ?int lss-usdl:performedBy ?role .
                }""")

        results = []
        for row in qres:
            r=getattr(row, "role")
            role = r.rsplit("#", 2)[1]
            results.append(role)

        return results


        
    #------------------------------------------------------------------
    #-------------- Get Service Goals ---------------------------------
    #------------------------------------------------------------------
    def getGoals(self):
        qres = ServiceSystem.g.query(
            """PREFIX  lss-usdl:  <http://w3id.org/lss-usdl/v2#>
                SELECT DISTINCT ?goal
                WHERE {
                  ?s ?prop ?o .
                  ?lss lss-usdl:hasInteraction ?int .
                  ?int lss-usdl:hasGoal ?goal .
                }""")

        results = []
        for row in qres:
            r=getattr(row, "goal")
            goal = r.rsplit("#", 2)[1]
            results.append(goal)

        return results

    #------------------------------------------------------------------
    #-------------- Get Service Locations -----------------------------
    #------------------------------------------------------------------
    def getLocations(self):
        qres = ServiceSystem.g.query(
            """PREFIX  lss-usdl:  <http://w3id.org/lss-usdl/v2#>
                SELECT DISTINCT ?location
                WHERE {
                  ?s ?prop ?o .
                  ?lss lss-usdl:hasInteraction ?int .
                  ?int lss-usdl:hasLocation ?location .
                }""")

        results = []
        for row in qres:
            r=getattr(row, "location")
            location = r.rsplit("#", 2)[1]
            results.append(location)

        return results

    #------------------------------------------------------------------
    #-------------- Get Service Resources -----------------------------
    #------------------------------------------------------------------
    def getResources(self):
        qres = ServiceSystem.g.query(
            """PREFIX  lss-usdl:  <http://w3id.org/lss-usdl/v2#>
                SELECT DISTINCT ?resources
                WHERE {
                  ?s ?prop ?o .
                  ?lss lss-usdl:hasInteraction ?int .
                  ?int lss-usdl:hasResource ?resources .
                }""")

        results = []
        for row in qres:
            r=getattr(row, "resource")
            resource = r.rsplit("#", 2)[1]
            results.append(resource)

        return results



    #------------------------------------------------------------------
    #-------------- Get Service Times ---------------------------------
    #------------------------------------------------------------------
    def getTimes(self):
        qres = ServiceSystem.g.query(
            """PREFIX  lss-usdl:  <http://w3id.org/lss-usdl/v2#>
                SELECT DISTINCT ?lss ?int ?time ?tempEntity 
                WHERE {
                  ?s ?prop ?o .
                  ?lss lss-usdl:hasInteraction ?int .
                  ?int lss-usdl:hasTime ?time .
                  ?time lss-usdl:hasTemporalEntity ?tempEntity .
                }""")

        results = []
        for row in qres:
            r=getattr(row, "tempEntity")
            time = r.rsplit("#")[1]
            results.append(time)

        return results



#------------------------------------------------------------------
#-------------- Interactions done by Role -------------------------
#------------------------------------------------------------------
    def getInterationsByRole(self):
        qres = ServiceSystem.g.query(
            """PREFIX  lss-usdl:  <http://w3id.org/lss-usdl/v2#>
                SELECT DISTINCT ?lss ?int ?role
                WHERE {
                  ?lss lss-usdl:hasInteraction ?int .
                  ?int lss-usdl:performedBy ?role .
                }""")

        results = []
        for row in qres:
            s, i, r = row
            service = s.rsplit("#", 2)[1]
            interaction = i.rsplit("#", 2)[1]
            role = r.rsplit("#", 2)[1]
            results.append([interaction, role])

        return results


#------------------------------------------------------------------
#-------------- Resources received ---
#------------------------------------------------------------------
    def getInteractionResources(self):
        qres = ServiceSystem.g.query(
        """PREFIX  lss-usdl:  <http://w3id.org/lss-usdl/v2#>
            SELECT DISTINCT ?lss ?int ?resource
            WHERE {
              ?lss lss-usdl:hasInteraction ?int .
              ?int lss-usdl:receivesResource ?resource .
              ?int lss-usdl:returnsResource ?resource .
            }""")

        results = []
        for row in qres:
            s, i, r = row
            service = s.rsplit("#", 2)[1]
            interaction = i.rsplit("#", 2)[1]
            resource = r.rsplit("#", 2)[1]
            results.append([interaction, resource])

        return results

#------------------------------------------------------------------
#-------------- Interactions that only receive Resources: ---------
#------------------------------------------------------------------
    def getInteractionResourcesReceived(self):
        qres = ServiceSystem.g.query(
            """PREFIX  lss-usdl:  <http://w3id.org/lss-usdl/v2#>
                SELECT DISTINCT ?lss ?int ?role
                WHERE {
                  ?lss lss-usdl:hasInteraction ?int .
                  ?int lss-usdl:receivesResource ?role .
                }""")

        results = []
        for row in qres:
            s, i, r = row
            service = s.rsplit("#", 2)[1]
            interaction = i.rsplit("#", 2)[1]
            resource = r.rsplit("#", 2)[1]
            results.append([interaction, resource])

        return results

#------------------------------------------------------------------
#-------------- Interactions that only create Resources: ---------
#------------------------------------------------------------------
    def getInteractionResourcesCreated(self):
        qres = ServiceSystem.g.query(
            """PREFIX  lss-usdl:  <http://w3id.org/lss-usdl/v2#>
                SELECT DISTINCT ?lss ?int ?role
                WHERE {
                  ?lss lss-usdl:hasInteraction ?int .
                  ?int lss-usdl:createsResource ?role .
                }""")

        results = []
        for row in qres:
            s, i, r = row
            service = s.rsplit("#", 2)[1]
            interaction = i.rsplit("#", 2)[1]
            resource = r.rsplit("#", 2)[1]
            results.append([interaction, resource])

        return results


#------------------------------------------------------------------
#-------------- Print first interaction: --------------------------
#------------------------------------------------------------------
# Look for an interaction which is a source but not the target of any connector
#
    def getFirstInteraction(self):
        qres = ServiceSystem.g.query(
            """PREFIX  lss-usdl: <http://w3id.org/lss-usdl/v2#>
               PREFIX time: <http://www.w3.org/2006/time/>
                SELECT DISTINCT ?lss ?tgt
                WHERE {
                  ?lss lss-usdl:hasControlFlow ?cf.
                  ?cf lss-usdl:hasSource ?src  .
                  ?cf lss-usdl:hasTarget ?tgt .
                  MINUS {?temp lss-usdl:hasTarget ?src .}
                }""")

        interaction = ''
        for row in qres:
            s, i= row
            service = s.rsplit("#", 2)[1]
            interaction = i.rsplit("#", 2)[1]

        return interaction



#------------------------------------------------------------------
#-------------- get last interaction(s) -------------------------
#------------------------------------------------------------------
# Look for an interaction which is a target but not the source of any connector
#
    def getLastInteraction(self):
        qres = ServiceSystem.g.query(
            """PREFIX  lss-usdl: <http://w3id.org/lss-usdl/v2#>
               PREFIX time: <http://www.w3.org/2006/time/>
                SELECT DISTINCT ?lss ?tgt
                WHERE {
                  ?lss lss-usdl:hasControlFlow ?cf.
                  ?cf lss-usdl:hasSource ?src  .
                  ?cf lss-usdl:hasTarget ?tgt .
                  MINUS {?temp lss-usdl:hasSource ?tgt .}
                }""")

        interaction = ''
        for row in qres:
            s, i= row
            service = s.rsplit("#", 2)[1]
            interaction = i.rsplit("#", 2)[1]

        return interaction



#------------------------------------------------------------------
#-------------- get DBpedia Resources(created) -----------------------------
#------------------------------------------------------------------
    def getDBPediaResourcesC(self):
        qres = ServiceSystem.g.query(
            """PREFIX  lss-usdl: <http://w3id.org/lss-usdl/v2#>
               PREFIX dbpedia: <http://dbpedia.org/>
                SELECT DISTINCT ?int ?res ?dbres
                WHERE {
                  ?lss lss-usdl:hasInteraction ?int .
                  ?int lss-usdl:createsResource ?res .
                  ?res a ?dbres .
                }""")

        results = []
        for row in qres:
            i, r, dbr = row
            interaction = i.rsplit("#", 2)[1]
            resource = r.rsplit("#", 2)[1]
            results.append([interaction, resource, dbr])

        return results

#------------------------------------------------------------------
#-------------- get DBpedia Resources(received) -----------------------------
#------------------------------------------------------------------
    def getDBPediaResourcesR(self):
        qres = ServiceSystem.g.query(
            """PREFIX  lss-usdl: <http://w3id.org/lss-usdl/v2#>
               PREFIX dbpedia: <http://dbpedia.org/>
                SELECT DISTINCT ?int ?res ?dbres
                WHERE {
                  ?lss lss-usdl:hasInteraction ?int .
                  ?int lss-usdl:receivesResource ?res .
                  ?res a ?dbres .
                }""")

        results = []
        for row in qres:
            i, r, dbr = row
            interaction = i.rsplit("#", 2)[1]
            resource = r.rsplit("#", 2)[1]
            results.append([interaction, resource, dbr])

        return results
#------------------------------------------------------------------
#-------------- get Abstract for DBpedia Resource -----------------
#------------------------------------------------------------------
    def getDBPediaAbstract(self, resource):

    #              ?dbres <http://dbpedia.org/ontology/abstract> ?abs .
        sparql=SPARQLWrapper("http://dbpedia.org/sparql")
        qs="""SELECT DISTINCT ?abs
             WHERE {
             <"""
        qe="""> dbpedia-owl:abstract ?abs .
              FILTER(langMatches(lang(?abs), "EN"))
             }"""

        q=qs+resource+qe
        sparql.setQuery(q)
        sparql.setReturnFormat(JSON)
        sparqlresults=sparql.query().convert()

        results = []
        for sparqlresult in sparqlresults["results"]["bindings"]:
            str = sparqlresult["abs"]["value"] + ''
            results.append(str)

        return results
#------------------------------------------------------------------
#-------------------- Get Interaction Steps -----------------------
#------------------------------------------------------------------
   
    def getStepsByInteraction(self):
        qres = ServiceSystem.g.query(
        """PREFIX  lss-usdl:  <http://w3id.org/lss-usdl/v2#>
            SELECT ?lss ?int (group_concat(?step) as ?steps)
            WHERE {
              ?lss lss-usdl:hasInteraction ?int .
              ?int lss-usdl:hasStep ?step .
            }
            GROUP BY ?int
            """)

        interaction = ''
        results = []
        for row in qres:
            interaction_steps = []
            l,i,s = row

            service = i.rsplit("#", 2)[1]
            steps_array = s.rsplit(" ")

            for step in steps_array:
                step = step.rsplit("#", 2)[1]
                interaction_steps.append(step)

            results.append([service,interaction_steps])
            
        return results

#------------------------------------------------------------------
#------------------- Get Gateways and Types -----------------------
#------------------------------------------------------------------

    def getGatewaysAndTypes(self,tipo):

        qres1 = """PREFIX  lss-usdl:  <http://w3id.org/lss-usdl/v2#>
            SELECT ?lss ?int ?type
            WHERE {
                ?int a ?type .
                FILTER regex(str(?type),'"""


        qres2 = """') 
            }
            """

        qfinal = qres1 + "#"+tipo + qres2

        qres = ServiceSystem.g.query(qfinal)

        results = []
        print tipo

        for row in qres:
            l,i,t = row
            if len(str(t)) > 0:
                results.append([i.rsplit("#", 2)[1],t.rsplit("#", 2)[1]])

        return results

    def getComments(self):
        qres = ServiceSystem.g.query(
        """PREFIX  lss-usdl:  <http://w3id.org/lss-usdl/v2#>
            SELECT ?c WHERE{?int rdfs:comment ?c }
            """)

        return qres




#------------------------------------------------------------------
#-------------- parse command line  -------------------------------
#------------------------------------------------------------------

if __name__ == "__main__":

    inputfile = ''
    try:
        opts, args = getopt.getopt(sys.argv[1:],"hf:",["file="])
    except getopt.GetoptError:
        print 'LSS-USDL_API.py -f <service_system_file>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'LSS-USDL_API.py -f <service_system_file>'
            sys.exit()
        elif opt in ("-f", "--file"):
            inputfile = arg

    print 'Input file is: ', inputfile
    print("")

    ss = ServiceSystem("file:" + inputfile)
    results = ss.getServiceInformation()
    print "Service System name: " + results[0].rsplit("#", 2)[1]
    print "Service System description:\n" + results[1]
    print("")


    results = ss.getGatewaysAndTypes("XOR")
    for gateway,tipo in results:
        print "Gateway: " + gateway + " -> " + tipo 
    print("")

    results = ss.getGatewaysAndTypes("AND")
    for gateway,tipo in results:
        print "Gateway: " + gateway + " -> " + tipo 
    print("")

    results = ss.getGatewaysAndTypes("OR")
    for gateway,tipo in results:
        print "Gateway: " + gateway + " -> " + tipo 
    print("")



    results = ss.getInteractions()
    for interation in results:
        print "Interaction: " + interation
    print("")

    results = ss.getConnectors()
    for result in results:
        str = 'getConnectors: (' + result[0] + ' -> ' + result[1] + ') with condition "' + result[2] + '"'''
        print str
    print("")

    results = ss.getRoles()
    for role in results:
        print "getRoles: " + role
    print("")

    results = ss.getGoals()
    for goal in results:
        print "getGoals: " + goal
    print("")

    results = ss.getLocations()
    for location in results:
        print "getLocations: " + location
    print("")

    results = ss.getResources()
    for resource in results:
        print "getResources: " + resource
    print("")

    results = ss.getTimes()
    for time in results:
        print "getTimes: " + time
    print("")


    results = ss.getStepsByInteraction()
    for service in results:
        print "Get Steps from: " + service[0]
        for step in service[1]:
            print "Step: " + step
        print("")


    results = ss.getInterationsByRole()
    for result in results:
        str = 'getInterationsByRole: ' + result[0] + ' with role ' + result[1]
        print str
    print("")

    results = ss.getInteractionResources()
    for result in results:
        str = 'getInteractionResources: ' + result[0] + ' with resource ' + result[1]
        print str
    print("")

    results = ss.getInteractionResourcesReceived()
    for result in results:
        str = 'getInteractionResourcesReceived: ' + result[0] + ' receives resource ' + result[1]
        print str
    print("")

    results = ss.getInteractionResourcesCreated()
    for result in results:
        str = 'getInteractionResourcesCreated: ' + result[0] + ' creates resource ' + result[1]
        print str
    print("")

    results = ss.getFirstInteraction()
    if results:
        str = 'getFirstInteraction: ' + results
        print str
        print("")

    results = ss.getLastInteraction()
    if results:
        str = 'getLastInteraction: ' + results
        print str
        print("")

    results = ss.getDBPediaResourcesC()
    for result in results:
        str = 'getDBPediaResources: ' + result[0] + ' with resource ' + result[1] + ' -> ' + result[2]
        print str
    print("")
    
    results = ss.getDBPediaResourcesR()
    for result in results:
        str = 'getDBPediaResources: ' + result[0] + ' with resource ' + result[1] + ' -> ' + result[2]
        print str
    print("")
    
    results = ss.getDBPediaResourcesC()
    for result in results:
        dbpediaAbstracts = ss.getDBPediaAbstract(result[2])
        for dbpediaAbstract in dbpediaAbstracts:
            str = 'getDBPediaAbstract: ' + result[2] + ': ' +  dbpediaAbstract
            print str
            print("")
    print("")

    results = ss.getDBPediaResourcesR()
    for result in results:
        dbpediaAbstracts = ss.getDBPediaAbstract(result[2])
        for dbpediaAbstract in dbpediaAbstracts:
            str = 'getDBPediaAbstract: ' + result[2] + ': ' +  dbpediaAbstract
            print str
            print("")
    print("")
