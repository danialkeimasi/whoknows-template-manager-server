from server.route import index, get_question, check_answer, test_template, template_manager, find_template

def addRoutes():
    index.add()
    get_question.add()
    check_answer.add()
    test_template.add()
    template_manager.add()
    find_template.add()
