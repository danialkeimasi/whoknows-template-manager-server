from server.route import index, get_question, check_answer

def addRoutes():
    index.add()
    get_question.add()
    check_answer.add()
