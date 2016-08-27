from collections import defaultdict

import re, sys, copy, ast

standardize_count = 0
rules_dict = {}
facts = []
explored = {}


def isVariable(expr):
    check = False
    if expr == 'x':
        return not check
    else:
        return check


def unify_var(x, y, theta):
    if x in theta:
        return unify(theta[x], y, theta)
    elif y in theta:
        return unify(x, theta[y], theta)
    else:
        theta[x] = y
        return theta


def isCompound(expr):
    check = False
    if '(' and ')' not in expr:
        return check
    else:
        return not check


def get_args_list(expr):
    index = expr.index("(")
    arg_list = []
    arg = ''
    for char in range(index + 1, len(expr)):
        if expr[char] == ')':
            arg_list.append(arg)
            break
        if expr[char] == ',':
            arg_list.append(arg)
            arg = ''
        else:
            arg += expr[char]
    return arg_list


def unify(x, y, theta={}):
    if theta is None:
        return None
    elif x == y:
        return theta
    elif isVariable(x):
        return unify_var(x, y, theta)
    elif isVariable(y):
        return unify_var(y, x, theta)
    elif isCompound(x) and isCompound(y):
        return unify(get_args_list(x), get_args_list(y), unify(get_pred(x), get_pred(y), theta))
    elif isinstance(x, list) and isinstance(y, list) and len(x) == len(y):
        if len(x) and len(y) > 1:
            return unify(x[1:], y[1:], unify(x[0], y[0], theta))
        else:
            return unify(x[0], y[0], theta)
    else:
        return None


def get_pred(expr):
    index = expr.index("(")
    return expr[:index]


# def get_args(expr):





def main():
    global rules_dict

    global facts
    kb_lines = []
    query_results = []

    file = open(sys.argv[1], "r")
    # file = open("sample01.txt","r")
    file_out = open("output.txt", "w+")

    queries = file.readline().strip()
    queries_list = queries.split('&')

    kb_len = int(file.next().strip())

    for i in range(kb_len):
        line = file.next().strip()
        kb_lines.append(line)
        kb_len -= 1
    rules = []
    facts = []
    for line in kb_lines:
        if '=>' in line:
            rules.append(line)
        else:
            facts.append(line)
    rules_dict = get_rules_dict(rules)
    # lhs=get_lhs(rules)


    sys.stdout = file_out

    query_count = 0
    if '&' in queries:
        print "Query: " + queries
    result_ask = []
    while query_count in range(len(queries_list)):
        curr_query = queries_list[query_count]
        if 'x' in get_args_list(curr_query):
            result_ask_divide = fol_bc_ask(rules_dict, curr_query)
            if query_count == 0:
                result_ask = result_ask_divide
            else:
                result_ask = intersect(result_ask, result_ask_divide)

        else:
            print "Query: " + curr_query
            result_fact_unify=facts_unify(curr_query)
            if curr_query in facts:
                print curr_query+":True"
                if query_count == 0:
                    result_ask = result_fact_unify
                else:
                    result_ask = intersect(result_ask, result_fact_unify)
            else:
                result_ask_divide = fol_bc_ask_constant(rules_dict, curr_query)
                if query_count == 0:
                    result_ask = result_ask_divide
                else:
                    result_ask = intersect(result_ask, result_ask_divide)
                if len(result_ask)>0:
                    print curr_query+": True"
                else:
                    print curr_query+": False"
        query_count += 1
        # result= fol_bc_ask(rules_dict, curr_query)
        var_there=False
        for query in queries_list:
            if 'x' in get_args_list(query):
                var_there=True
    if len(queries_list)>1:
        if var_there:
            if len(result_ask) > 0:
                print queries + ": True: " + str(result_ask)
            else:
                print queries + ": False"
        else:
            if len(result_ask) > 0:
                print queries + ": True: "
            else:
                print queries + ": False"
    file_out.close()
    file.close()


def get_rules_dict(lines):
    rhs = ''
    lhs = ''
    rldict = defaultdict(list)
    for line in lines:
        imp_index = line.index("=>")
        lhs = (line[:imp_index])
        rhs = (line[imp_index + 2:])
        rldict[rhs].append(lhs)
        lhs = []
    return rldict


def fol_bc_ask_constant(kb, query):
    result = False
    result_unify_facts = facts_unify(query)
    if len(result_unify_facts) > 0:
        result = True
        return result
    else:
        for rule in kb:
            result_unify = unify(rule, query, {})
            if result_unify is not None:
                const_rule = substitute(result_unify, rule)
                r = fol_bc_or_const(kb, const_rule, result_unify, rule)
                i=0
                if (i==0):
                    result=r
                    i=1
                else:
                    result=result and r
                return result
    if result:
        return result_unify['x']
    else:
        return []


def fol_bc_ask(kb, query):
    result = []
    result = union(result, fol_bc_or(kb, query, {}))
    results_fact_unify = facts_unify(query)
    result = union(result, results_fact_unify)
    print query + ": True: " + str(sorted(result))
    return result


"""def get_lhs(rule):
    if ('=>') in rule:
        return rule[:rule.index('=>')]
    else:
        return []"""


def get_rhs(rule):
    rhs = ''
    for key in rules_dict:
        for i in range(len(rules_dict[key])):
            if rules_dict[key][i] == rule:
                rhs = key
    return rhs


def unique(a):
    return list(set(a))


def union(theta, theta_tmp):
    return list(set(theta) | set(theta_tmp))


def intersect(theta, theta_tmp):
    return list(set(theta) & set(theta_tmp))


def isexplored(goal, fetched_rule):
    try:
        return explored[goal] == fetched_rule
    except KeyError:
        return False


def standardize(lhs, rhs):
    global standardize_count
    standardize_count += 1
    temp = []
    if len(lhs) > 0:
        if bool(re.search(r'\(x\d', lhs)) or bool(re.search(r'x\d\)', lhs)):
            temp.append(lhs)
        else:
            if '(x' in lhs:
                lhs = lhs.replace('(x', '(x' + str(standardize_count))
                temp.append(lhs)
            elif 'x)' in lhs:
                lhs = lhs.replace('x)', 'x' + str(standardize_count) + ')')
                temp.append(lhs)
            else:
                if len(lhs) == 0:
                    lhs = ''
                temp.append(lhs)
    else:
        lhs = ''
        temp.append(lhs)
    if len(rhs) > 0:
        if bool(re.search(r'\(x\d', rhs)) or bool(re.search(r'x\d\)', rhs)):
            temp.append(lhs)
        else:
            if '(x' in rhs:
                rhs = rhs.replace('(x', '(x' + str(standardize_count))
                temp.append(rhs)
            elif 'x)' in rhs:
                rhs = rhs.replace('x)', 'x' + str(standardize_count) + ')')
                temp.append(rhs)
            else:
                temp.append(rhs)
    else:
        rhs = ''
        temp.append(rhs)
    return temp


def fol_bc_or(kb, goal, theta):
    global explored
    global standardize_count
    print "Query: " + goal
    fetched_rules_for_goal = fetch_rules_for_goal(kb, goal)
    if len(fetched_rules_for_goal) == 0:
        result_fact_unify = facts_unify(goal)
        if len(result_fact_unify) == 0:
            print goal + ": False"
        else:
            result_fact_unify = unique(result_fact_unify)

        return result_fact_unify
    else:
        result_multi_run=[]
        j=0
        for fetched_rule in fetched_rules_for_goal:
            print "Query: " + str(fetched_rule) + str('=>') + str(get_rhs(fetched_rule))
            lhs = fetched_rule
            rhs = goal
            lhs_list = lhs.split('&')
            result_list = []
            i = 0
            for item in lhs_list:

                result_divided = fol_bc_or(kb, item, {})

                if i == 0:
                    result_list = result_divided
                    if len(result_divided) != 0:
                        print item + ": True: " + str(sorted(result_divided))
                    else:
                        result_list = union(result_list, facts_unify(goal))
                    i = 1
                else:
                    result_list = intersect(result_list, result_divided)
                    if len(result_divided) != 0:
                        print item + ": True: " + str(sorted(result_divided))
                    result_list = union(result_list, facts_unify(goal))
                    result_list = unique(result_list)
            if j==0:
                result_multi_run=result_list
                j=1
            else:
                result_multi_run=union(result_multi_run,result_list)
        return result_multi_run


def fol_bc_or_const(kb, goal, theta, key):
    global explored
    global standardize_count
    result=False
    fetched_rules_for_goal = fetch_rules_for_goal(kb, key)
    if len(fetched_rules_for_goal) == 0:
        result_fact_unify = facts_unify(goal)
        if result_fact_unify is None:
            print key + ": False"
            return result
        else:
            return not result
    else:
        result_multi_run = []
        j = 0
        for fetched_rule in fetched_rules_for_goal:
            print "Query: " + str(fetched_rule) + str('=>') + str(get_rhs(fetched_rule))
            lhs = fetched_rule
            rhs = goal
            lhs_list = lhs.split('&')
            result = False
            i = 0
            for item in lhs_list:
                print "Query: "+item
                const_item=substitute(theta,item)
                result_divided = fol_bc_ask_constant(kb,const_item)
                if i == 0:
                    result = result_divided
                    if result_divided == True:
                        print item + ": True"
                        result = True
                    else:
                        print item  + ": False"
                    i = 1
                else:
                    result = result and result_divided
                    if result == True:
                        print item + ": True"
                        result = True
                    else:
                        print item + ": False"
            if j == 0:
                result_multi_run = result
                j = 1
            else:
                result_multi_run = result_multi_run or result
        return result_multi_run




def substitute(theta, expr):
    global standardize_count
    if len(theta.keys()) == 0:
        return expr
    args_list = get_args_list(expr)
    if 'x' in args_list and 'x' in theta:
        value = theta['x']
        if '(x' in expr:
            expr = expr.replace('(x', '(' + value)
        else:
            expr = expr.replace('x)', value + ')')
    return expr


"""def fol_bc_and(kb, goals, theta):
    if theta is None:
        yield theta
    elif len(goals) == 0:
        yield theta
    else:
        print "Query: " + str(goals) + str('=>') + str(get_rhs(goals))
        goals_list = str(goals).split('&')
        first = goals_list[:2][0]
        rest = goals_list[1:]
        if len(rest) == 0:
            rest = ''
        for theta_dash in fol_bc_or(kb, substitute(theta, first), theta):
            for theta_tmp_and in fol_bc_and(kb, rest, theta):
                yield theta_tmp_and"""


def fetch_rules_for_goal(kb, goal):
    clauses = []
    for key in kb:
        result_find_match = unify(key, goal, {})
        if result_find_match is not None:
            list_len = len(kb[key])
            for i in range(0, list_len):
                clauses.append(kb[key][i])
    """for fact in facts:
        if get_pred(fact) == get_pred(goal):
            clauses.append(fact)"""
    return clauses


def facts_unify(goal):
    result_list = []
    for fact in facts:
        theta = {}
        result_unify = unify(fact, goal, {})
        # print "after" + str(result_unify)
        if result_unify is not None:
            if len(result_unify) == 0:
                result_list.append(get_args_list(goal)[0])
            else:
                match = result_unify['x']
                result_list.append(match)
    return result_list


if __name__ == '__main__':
    main()
