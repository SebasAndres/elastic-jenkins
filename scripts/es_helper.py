from elasticsearch import Elasticsearch

def search_content(host:str, query:dict) -> list:
    ## Set up ES connections
    es = Elasticsearch(hosts=host)
    response = es.search(query)
    if isinstance(response, None):
        print("* No results.")
        return
            
    out = set()
    ## Here you filter the response according to what you need.  
    for r in response.items():
        if filter_response(r) == "APPROVED":
            out.add(r)
    ##
    return out
    

def filter_response(r):
    return "APPROVED"