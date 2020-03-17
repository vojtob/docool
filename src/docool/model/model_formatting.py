import docool.model.model_processing as mp

LINE_FORMAT = '| {0} | {1} |'

def realizationdesc(realization):
    """extract realization description. Try to use description from realization,
        if it is not available, use realizing element description
        if it is not available, warning"""

    if realization[1] != '--':
        return realization[1]           
    if realization[0].desc != '--':
        return realization[0].desc
    return '<font color="orange">XXXXXX TODO: ' + realization[0].name + ' BEZ POPISU</font>'

def requirement_as_table(req):
    """ format single requirement as a list of lines in the table
        every line is one realization
        the first column is requirement name
        the second column is a description how the requirement is realized based on related architecture elements
    """
    if len(req.realizations) == 0:
        return [LINE_FORMAT.format(req.name, '<font color="red">XXXXXX TODO: Ziadna realizacia poziadavky</font>')]

    docs = []
    for realization in req.realizations:
        docs.append(LINE_FORMAT.format(req.name, realizationdesc(realization)))
    return docs

def requirement_as_text(req):
    """ format single requirement as a list of lines in the table
        every line is one realization
        the first column is requirement name
        the second column is a description how the requirement is realized based on related architecture elements
    """
    if len(req.realizations) == 0:
        return ['<font color="red">XXXXXX TODO: Ziadna realizacia poziadavky</font>\n\n']

    docs = []
    for realization in req.realizations:
        docs.append(realizationdesc(realization))
        docs.append('\n\n')
    return docs

def requirements_as_table(reqs):
    """ format list of requirements into one table, join lines for every requirement """
    docs = [LINE_FORMAT.format('Požiadavka', 'Realizácia požiadavky'), LINE_FORMAT.format(' --- ', ' --- ')]
    for r in reqs:
        docs.extend(requirement_as_table(r))        
    return docs
