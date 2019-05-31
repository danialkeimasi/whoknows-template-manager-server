from server.routes import index, get_question, test_template, find_template, new_template, edit_template


def add_routes():
    index.add()
    get_question.add()
    test_template.add()
    find_template.add()
    new_template.add()
    edit_template.add()
