from server.route import index, get_question, check_answer, test_template

def addRoutes():
    index.add()
    get_question.add()
    check_answer.add()
    test_template.add()
    