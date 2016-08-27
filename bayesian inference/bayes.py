import sys
import re
import copy
from decimal import Decimal
import string

def topological_sort(bayes_net):
    nodes = bayes_net.keys()
    sorted_nodes = []

    while len(sorted_nodes) < len(nodes):
        for node in nodes:
            if node not in sorted_nodes:
                if all(parent in sorted_nodes for parent in bayes_net[node]['parents']):
                    sorted_nodes.append(node)

    return sorted_nodes

def split_literal(literal):
    literal = literal.strip()
    temp_para = literal.split(' = ')
    variable = temp_para[0].strip()
    value = temp_para[1].strip()
    value = True if value == '+' else False
    return variable,value

def get_sorted_nodes(evidence,bayes_net,sorted_nodes):
    curr_nodes_set = set(evidence.keys())
    check_for_node = [True if x in curr_nodes_set else False for x in sorted_nodes]

    while len(curr_nodes_set) != 0:
        popNode = curr_nodes_set.pop()
        for parent in bayes_net[popNode]['parents']:
            curr_nodes_set.add(parent)
            parentIndex = sorted_nodes.index(parent)
            check_for_node[parentIndex] = True

    all_sorted_nodes = []
    for node in sorted_nodes:
        if check_for_node[sorted_nodes.index(node)] == True:
            all_sorted_nodes.append(node)

    return all_sorted_nodes


def enumeration_all(vars,ev,bayes_net):
    if len(vars) == 0:
        return 1.0

    curr_var = vars[0]

    if curr_var in ev:
        result = find_probability(curr_var,ev,bayes_net)*enumeration_all(vars[1:],ev,bayes_net)
    else:
        sumfind_probability = []
        ev2 = copy.deepcopy(ev)
        for bool in [True,False]:
            ev2[curr_var] = bool
            sumfind_probability.append(find_probability(curr_var,ev2,bayes_net)*enumeration_all(vars[1:],ev2,bayes_net))
        result =sum(sumfind_probability)

    return result


def find_probability(curr_var,ev,bayes_net):

    if len(bayes_net[curr_var]['parents']) == 0:
        if ev[curr_var] == True:
            return float(bayes_net[curr_var]['prob'])
        else:
            return 1.0-float(bayes_net[curr_var]['prob'])
    else:
        parentTuple = tuple(ev[parent] for parent in bayes_net[curr_var]['parents'])

        if ev[curr_var] == True:
            return float(bayes_net[curr_var]['cond_prob'][parentTuple])
        else:
            return 1-float(bayes_net[curr_var]['cond_prob'][parentTuple])

def main():
    filename = sys.argv[1]
    f1 = open(filename, "r")
    if f1.mode == 'r':
        data = f1.read().splitlines()
    query_count = int(data[0])
    query_list = []
    for query in range(1,query_count+1):
        query_list.append(data[query].strip())
    curr_line = query_count + 1
    bayes_network = {}
    while(curr_line < len(data)):
        parent_nodes = []

        line = data[curr_line].strip()
        node_parent_list = line.split(' | ')
        node = node_parent_list[0].strip()
        if len(node_parent_list) != 1:
            parent_nodes = node_parent_list[1].strip().split(' ')
            
        bayes_network[node] = {}
        bayes_network[node]['parents'] = parent_nodes
        bayes_network[node]['children'] = []

        for parent in parent_nodes:
            bayes_network[parent]['children'].append(node)

        curr_line += 1

        if curr_line < len(data):
            if len(parent_nodes) == 0:
                prob = data[curr_line].strip()
                bayes_network[node]['prob'] = prob
            else:
                conditional_prob = {}
                no_of_probvalues= len(parent_nodes)
                for i in range(0, pow(2, no_of_probvalues)):
                    line = data[curr_line].strip()
                    lines = line.split(' ')
                    prob = lines[0]
                    lines = lines[1:]
                    truth = tuple(True if x == '+' else False for x in lines)
                    conditional_prob[truth] = prob
                    curr_line += 1

                bayes_network[node]['cond_prob'] = conditional_prob
        curr_line+=1
        if curr_line<len(data):
            line = data[curr_line].strip()
        if line == '***':
            curr_line+=1

    sort_nodes = topological_sort(bayes_network)



    outputFile = open('output.txt', 'w')

    count = 0

    for query in query_list:
        full_evidence = {}
        after_bar_evidence = {}
        result = 1.0
        is_conditional = False
        parameters = query[query.index('(') + 1:query.index(')')]
        bar_index = parameters.index('|') if '|' in parameters else -1

        if bar_index != -1:
            is_conditional = True
            temp_para = parameters[:parameters.index(' | ')]
            xparameters = temp_para.strip()
            xparameters = xparameters.split(',')
            for xLiteral in xparameters:
                xLiteral = xLiteral.strip()
                xVar, xVal = split_literal(xLiteral)
                full_evidence[xVar] = xVal
            temp_para = parameters[parameters.index(' | ') + 3:]
        else:
            temp_para = parameters

        parameters = temp_para.strip()
        parameters = parameters.split(',')
        for literal in parameters:
            literal = literal.strip()
            var, val = split_literal(literal)
            full_evidence[var] = val
            after_bar_evidence[var] = val

        if is_conditional == True:
            
            sorted_nodesForNumerator = get_sorted_nodes(full_evidence, bayes_network, sort_nodes)
            numerator = enumeration_all(sorted_nodesForNumerator, full_evidence, bayes_network)

            sorted_nodesForDenominator = get_sorted_nodes(after_bar_evidence, bayes_network, sort_nodes)
            denominator = enumeration_all(sorted_nodesForDenominator, after_bar_evidence, bayes_network)

            result = numerator / denominator

        else:
            selected_query_nodes = get_sorted_nodes(after_bar_evidence, bayes_network, sort_nodes)
            result = enumeration_all(selected_query_nodes, after_bar_evidence, bayes_network)

        result = Decimal(str(result + 1e-8)).quantize(Decimal('.01'))

        outputFile.write(str(result))
        count += 1
        if count<query_count:
            outputFile.write('\n')


if __name__ == '__main__':
    main()