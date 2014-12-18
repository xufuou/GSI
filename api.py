from rdflib import Graph, RDF, URIRef,  RDFS #, Literal, BNode
from SPARQLWrapper import SPARQLWrapper, JSON
import sys, getopt
import textwrap 

class ServiceSystem:
    'A API to a Service Systems'
    filename = ''
    g = Graph()
    print g

    commands = { 
    'q': ['quit',(lambda: ss.quit())],
    '1': ['Get Interactions',(lambda: ss.print_interations())],
    '2': ['Get Locations',(lambda: ss.print_locations())],
    '3': ['Get Goals',(lambda: ss.print_goals())],
    '4': ['Get Roles',(lambda: ss.print_roles())],
    '5': ['Get Times',(lambda: ss.print_times())],
    '6': ['Get Processes',(lambda: ss.print_processes())],
    '7': ['Get Resources',(lambda: ss.print_resources())],
    '8': ['Get Comments',(lambda: ss.print_comments())], 
    '9': ['Get External Knowledge',(lambda: ss.print_externalk())],
    '10': ['Get ITIL Knowledge',(lambda: ss.print_itilk())]

    } 

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
    # def getRoles(self):
    #     qres = ServiceSystem.g.query(
    #         """PREFIX  lss-usdl:  <http://w3id.org/lss-usdl/v2#>
    #             SELECT DISTINCT ?int ?role
    #             WHERE {
    #               ?s ?prop ?o .
    #               ?lss lss-usdl:hasInteraction ?int .
    #               ?int lss-usdl:performedBy ?role .
    #             }""")

    #     results = []
    #     for row in qres:
            
    #         r=getattr(row, "role")
    #         i=getattr(row, "int")
    #         interaction=i.rsplit("#", 2)[1]
    #         role = r.rsplit("#", 2)[1]
    #         results.append([interaction,role])

    #     return results


        
    #------------------------------------------------------------------
    #-------------- Get Service Goals ---------------------------------
    #------------------------------------------------------------------
    def getGoals(self):
        qres = ServiceSystem.g.query(
            """PREFIX  lss-usdl:  <http://w3id.org/lss-usdl/v2#>
                SELECT DISTINCT ?int ?goal
                WHERE {
                  ?s ?prop ?o .
                  ?lss lss-usdl:hasInteraction ?int .
                  ?int lss-usdl:hasGoal ?goal .
                }""")

        results = []
        for row in qres:
            r=getattr(row, "goal")
            i=getattr(row, "int")
            interaction=i.rsplit("#", 2)[1]
            goal = r.rsplit("#", 2)[1]
            results.append([interaction,goal])

        return results

    #------------------------------------------------------------------
    #-------------- Get Service Locations -----------------------------
    #------------------------------------------------------------------
    def getLocations(self):
        qres = ServiceSystem.g.query(
            """PREFIX  lss-usdl:  <http://w3id.org/lss-usdl/v2#>
                SELECT DISTINCT ?int ?location
                WHERE {
                  ?s ?prop ?o .
                  ?lss lss-usdl:hasInteraction ?int .
                  ?int lss-usdl:hasLocation ?location .
                }""")

        results = []
        for row in qres:
            
            i=getattr(row,"int")
            r=getattr(row, "location")
            interaction=i.rsplit("#", 2)[1]
            location = r.rsplit("#", 2)[1]
            results.append([interaction,location])

        return results

    #------------------------------------------------------------------
    #-------------- Get Service Resources -----------------------------
    #------------------------------------------------------------------
    # def getResources(self):
    #     qres = ServiceSystem.g.query(
    #         """PREFIX  lss-usdl:  <http://w3id.org/lss-usdl/v2#>
    #             SELECT DISTINCT ?resources
    #             WHERE {
    #               ?s ?prop ?o .
    #               ?lss lss-usdl:hasInteraction ?int .
    #               ?int lss-usdl:hasResource ?resources .
    #             }""")

    #     results = []
    #     for row in qres:
    #         r=getattr(row, "resource")
    #         resource = r.rsplit("#", 2)[1]
    #         results.append(resource)

    #     return results

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
            i=getattr(row, "int")
            interaction=i.split("#")[1]
            time = r.rsplit("#")[1]
            results.append([interaction,time])

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
            }""")

        qres1 = ServiceSystem.g.query(
        """PREFIX  lss-usdl:  <http://w3id.org/lss-usdl/v2#>
            SELECT DISTINCT ?lss ?int ?resource
            WHERE {
              ?lss lss-usdl:hasInteraction ?int .
              ?int lss-usdl:createsResource ?resource .
            }""")
      
        results = []
        for row in qres:
            s, i, r = row
            service = s.rsplit("#", 2)[1]
            interaction = i.rsplit("#", 2)[1]
            resource = r.rsplit("#", 2)[1]
            results.append([interaction, resource])

        for row in qres1:
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
            #service = s.rsplit("#", 2)[1]
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


    def getCommentsByRole(self):
        qres = ServiceSystem.g.query(
            """PREFIX  lss-usdl:  <http://w3id.org/lss-usdl/v2#>
                SELECT DISTINCT ?role ?c
                WHERE {
                  ?role a lss-usdl:Role ;
                  rdfs:comment ?c .
                }""")

        results = []
        for row in qres:
            r,c = row;
            role = r.rsplit("#", 2)[1]
            comment =  c
            results.append([role,comment.toPython()])

        return results

    def getCommentsByLocation(self):
        qres = ServiceSystem.g.query(
            """PREFIX  lss-usdl:  <http://w3id.org/lss-usdl/v2#>
                SELECT DISTINCT ?location ?c
                WHERE {
                  ?location a lss-usdl:Location ;
                  rdfs:comment ?c .
                }""")

        results = []
        for row in qres:
            l,c = row;
            location = l.rsplit("#", 2)[1]
            comment =  c
            results.append([location,comment.toPython()])
        return results

    def getCommentsByGoal(self):
        qres = ServiceSystem.g.query(
            """PREFIX  lss-usdl:  <http://w3id.org/lss-usdl/v2#>
                SELECT DISTINCT ?goal ?c
                WHERE {
                  ?goal a lss-usdl:Goal ;
                  rdfs:comment ?c .
                }""")

        results = []
        for row in qres:
            g,c = row;
            goal = g.rsplit("#", 2)[1]
            comment =  c
            results.append([goal,comment.toPython()])

        return results

    def getCommentsByResource(self):
        qres = ServiceSystem.g.query(
            """PREFIX  lss-usdl:  <http://w3id.org/lss-usdl/v2#>
                SELECT DISTINCT ?resource ?c
                WHERE {
                  ?resource a lss-usdl:Resource ;
                  rdfs:comment ?c .
                }""")

        results = []
        for row in qres:
            r,c = row;
            resource = r.rsplit("#", 2)[1]
            comment =  c
            results.append([resource,comment.toPython()])

        return results

    def getCommentsByTime(self):
        qres = ServiceSystem.g.query(
            """PREFIX  lss-usdl:  <http://w3id.org/lss-usdl/v2#>
                SELECT DISTINCT ?time ?c
                WHERE {
                  ?time a lss-usdl:Time ;
                  rdfs:comment ?c .
                }""")

        results = []
        for row in qres:
            t,c = row;
            time = t.rsplit("#", 2)[1]
            comment =  c
            results.append([time,comment.toPython()])

        return results

    def getCommentsByStep(self):
        qres = ServiceSystem.g.query(
            """PREFIX  lss-usdl:  <http://w3id.org/lss-usdl/v2#>
                SELECT DISTINCT ?step ?c
                WHERE {
                  ?step a lss-usdl:Step ;
                  rdfs:comment ?c .
                }""")

        results = []
        for row in qres:
            s,c = row;
            step = s.rsplit("#", 2)[1]
            comment =  c
            results.append([step,comment.toPython()])

        return results



    def quit(self): 
        raise SystemExit()

    def print_serviceInformation(self):
        results = ss.getServiceInformation()
        print "Service System name: " + results[0].rsplit("#", 2)[1]
        print "Service System description:\n" + results[1]
        print("")

    def print_getXOR(self):
        results = ss.getGatewaysAndTypes("XOR")
        for gateway,tipo in results:
            print "Gateway: " + gateway + " -> " + tipo 
        print("")

    def print_getAND(self):
        results = ss.getGatewaysAndTypes("AND")
        for gateway,tipo in results:
            print "Gateway: " + gateway + " -> " + tipo 
        print("")  

    def print_getOR(self):
        results = ss.getGatewaysAndTypes("OR")
        for gateway,tipo in results:
            print "Gateway: " + gateway + " -> " + tipo 
        print("")



    def print_commands(self):
        for key,values in ServiceSystem.commands.items():
            print('{} - {}'.format(key, values[0]))

    
    def print_interations(self):
        results = ss.getInteractions()
        for interation in results:
            print "Interaction: " + interation
        print("")

    def print_locations(self):
        results = ss.getLocations()
        for result in results:
            print "Location: "  + result[0] + ' with location ' + result[1]
        print("")

    def print_goals(self):
        results = ss.getGoals()
        for result in results:
            print "Goal: " + result[0] + ' with goal ' + result[1]
        print("")

    def print_roles(self):
        results = ss.getInterationsByRole()
        for result in results:
            print "Role: " + result[0] + ' with role ' + result[1]
        print("")

    def print_times(self):
        results = ss.getTimes()
        for result in results:
            print 'Time: ' + result[0] + ' with time ' + result[1]
        print("")

    def print_resources(self):
        results = ss.getInteractionResources()
        for result in results:
            print 'Resource: ' + result[0] + ' with resource ' + result[1]
        print("")

    def print_processes(self):
        results = ss.getStepsByInteraction()
        for service in results:
            print "Get Steps from: " + service[0]
            for step in service[1]:
                print "Step: " + step
            print("")

    def print_comments(self):
        results = []
        role_comments = ss.getCommentsByRole();

        print " "
        print "- Who"
        for role,comment in ss.getCommentsByRole():
            print('{} - {}'.format(role, comment))
        
        print " "
        print "- Where"
        for location,comment in ss.getCommentsByLocation():
            print('{} - {}'.format(location, comment))

        print " "
        print "- Why"
        for goal,comment in ss.getCommentsByGoal():
            print('{} - {}'.format(goal, comment))

        print " "
        print "- How"
        for step,comment in ss.getCommentsByStep():
            print('{} - {}'.format(step, comment))

        print " "
        print "- When"
        for time,comment in ss.getCommentsByTime():
            print('{} - {}'.format(time, comment))

        print " "
        print "- What"
        for resource,comment in ss.getCommentsByResource():
            print('{} - {}'.format(resource, comment))



    def print_itilk(shelf):
        results = ss.getDBPediaResourcesC()
        for result in results:
            print 'getDBPediaResources: ' + result[0] + ' with resource ' + result[1] + ' -> ' + result[2]

        print("")
    
        results = ss.getDBPediaResourcesR()
        for result in results:
            print 'getDBPediaResources: ' + result[0] + ' with resource ' + result[1] + ' -> ' + result[2]

        print("")


    #def print_externalk(self):



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

    choice = None
    ss.print_commands()
    while choice is None: 
        choice = raw_input("Command: ") 
        if choice in ServiceSystem.commands: 
            ServiceSystem.commands[choice][1]()
            choice = None  
        else: 
            choice = None 
            ss.print_commands() 



    # results = ss.getConnectors()
    # for result in results:
    #     str = 'getConnectors: (' + result[0] + ' -> ' + result[1] + ') with condition "' + result[2] + '"'''
    #     print str
    # print("")



    # results = ss.getInterationsByRole()
    # for result in results:
    #     str = 'getInterationsByRole: ' + result[0] + ' with role ' + result[1]
    #     print str
    # print("")

    # results = ss.getInteractionResources()
    # for result in results:
    #     str = 'getInteractionResources: ' + result[0] + ' with resource ' + result[1]
    #     print str
    # print("")

    # results = ss.getInteractionResourcesReceived()
    # for result in results:
    #     str = 'getInteractionResourcesReceived: ' + result[0] + ' receives resource ' + result[1]
    #     print str
    # print("")

    # results = ss.getInteractionResourcesCreated()
    # for result in results:
    #     str = 'getInteractionResourcesCreated: ' + result[0] + ' creates resource ' + result[1]
    #     print str
    # print("")

    # results = ss.getFirstInteraction()
    # if results:
    #     str = 'getFirstInteraction: ' + results
    #     print str
    #     print("")

    # results = ss.getLastInteraction()
    # if results:
    #     str = 'getLastInteraction: ' + results
    #     print str
    #     print("")

    # results = ss.getDBPediaResourcesC()
    # for result in results:
    #     str = 'getDBPediaResources: ' + result[0] + ' with resource ' + result[1] + ' -> ' + result[2]
    #     print str
    # print("")
    
    # results = ss.getDBPediaResourcesR()
    # for result in results:
    #     str = 'getDBPediaResources: ' + result[0] + ' with resource ' + result[1] + ' -> ' + result[2]
    #     print str
    # print("")
    
    # results = ss.getDBPediaResourcesC()
    # for result in results:
    #     dbpediaAbstracts = ss.getDBPediaAbstract(result[2])
    #     for dbpediaAbstract in dbpediaAbstracts:
    #         str = 'getDBPediaAbstract: ' + result[2] + ': ' +  dbpediaAbstract
    #         print str
    #         print("")
    # print("")

    # results = ss.getDBPediaResourcesR()
    # for result in results:
    #     dbpediaAbstracts = ss.getDBPediaAbstract(result[2])
    #     for dbpediaAbstract in dbpediaAbstracts:
    #         str = 'getDBPediaAbstract: ' + result[2] + ': ' +  dbpediaAbstract
    #         print str
    #         print("")
    # print("")
