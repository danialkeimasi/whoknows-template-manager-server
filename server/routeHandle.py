from server.route import index, get_question, test_template, find_template, new_template

def addRoutes():
    index.add()
    get_question.add()
    test_template.add()
    find_template.add()
    new_template.add()