def check_global_constants(question, problems):
    """
    Checks conditional values of a question to be right
    TODO: Logger must be added
    """

    if not 2 <= question['NOC'] <= 6:
        problems += ['NOC is wrong!... NOC range is between 2 to 6']

    if not 2 <= question['NOS'] <= 6:
        problems += ['NOS is wrong!... NOS range is between 2 to 6']


def check_template(template, question, problems):
    """
    Checks if a template has all of necessary parts and returns every problem in template if there is any

    Parameters
    ----------
    template : dict
        wanted template to be checked
    """

    if question['QT'] == 'true_false':
        if not 'title_true_false' in template:
            problems += ['titles (t-f) is empty!']

        if not 'answer_true_false' in template:
            problems += ['answer (t-f) is empty!']

    elif question['QT'] == 'multichoices':
        if not 'title_multichoices' in template:
            problems += ['titles (mu) is empty!']

        if not 'answer_multichoices' in template:
            problems += ['answer (mu) is empty!']

        if not 'choices_multichoices' in template:
            problems += ['choices(mu) is empty!']


    elif question['QT'] == 'writing':
        if not 'title_writing' in template:
            problems += ['titles (wr) is empty!']

        if not 'answer_writing' in template:
            problems += ['answer (wr) is empty!']


    elif question['QT'] == 'selective':
        if not 'title_selective' in template:
            problems += ['titles (sel) is empty!']

        if not 'answer_selective' in template:
            problems += ['answer (sel) is empty!']

        if not 'choices_selective' in template:
            problems += ['choices(sel) is empty!']

    print(f'check_template()\t-----> problems is {problems}')
    return problems


def check_question(question, QT):
    """
    Checks if a question has all of necessary parts and returns every problem in template if there is any

    Parameters
    ----------
    template : dict
        wanted template to be checked
    """

    problems = []

    if 'choices' in question:
        # check if choices are different from another

        choices = question['choices']
        if len(choices) != len(set(choices)):
            problems += ['there are repetitive choices']

        for choice in choices:
            choice = str(choice)
            if any([choice.find(item) != -1 for item in ['None', 'NaN', 'null']]) or all(
                    choice.find(item) != -1 for item in question['answer']):
                print(f"*****{choice.find(question['answer'])}")
                problems += ['section "choices" has wrong values']
        if (QT != "writing" or QT != "true_false") and choices == []:
            problems += ['section "choices" has shit']

    for section in question:
        for item in section if isinstance(section, list) else [section]:
            if any([item.find(x) != -1 for x in ['None', 'NaN', 'null']]):
                problems += [f'section "{section}" has wrong values']

    for section in ['title', 'answer']:
        if section not in question:
            problems += [f'section "{section}" is missing']

    for key in question:
        if question[key] in [float('nan')]:
            problems += [f'{key} in values section is empty']

    print(f'check_question()\t-----> problems is {problems}')
    return problems