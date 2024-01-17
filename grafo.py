# JJS
# SSR
# Import libraries
import os
import shutil
import matplotlib
import pygad
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import warnings
warnings.filterwarnings("ignore")
#          Down,   DownL     Left     UpLeft
vecinos = [(1, 0), (1, -1), (0, -1), (-1, -1),
           (-1, 0), (-1, 1), (0, 1), (1, 1)]  # Up, UpRight, Right, DownRight (i, j)
#                   Down   Left     Up       Right
vecinos_lejanos = [(2, 0), (0, -2), (-2, 0), (0, 2)]


def recorrer(dictionary, lista, oracion, idx, pos, matriz, recorrido={}):
    continua = False
    if oracion[idx] == "#":
        lista.append([recorrido, idx])
        return

    for vecino in vecinos:
        vecino_i = pos[0] + vecino[0]
        vecino_j = pos[1] + vecino[1]

        if 0 <= vecino_i <= 4 and 0 <= vecino_j <= 6:
            if matriz[vecino_i][vecino_j] == oracion[idx]:
                rn = recorrido.copy()
                if not vecino_i*7 + vecino_j + 1 in rn:
                    rn[vecino_i*7 + vecino_j + 1] = set()

                if not pos[0]*7 + pos[1] + 1 in rn:
                    rn[pos[0]*7 + pos[1] + 1] = set()
                # Review diagonal intersections
                numeroVecino = vecino_i*7 + vecino_j + 1
                numeroPosicion = pos[0]*7 + pos[1] + 1
                # Which has smaller coordinates
                if numeroVecino < numeroPosicion:
                    numeroMenor = numeroVecino
                else:
                    numeroMenor = numeroPosicion
                # Left to Right (UpLeft -> DownRight)
                if vecino == (1, 1) or vecino == (-1, -1):
                    if numeroMenor+1 in recorrido and numeroMenor+7 in recorrido:
                        if numeroMenor+1 in recorrido[numeroMenor+7]:
                            continue
                # Right to Left (UpRight -> DownLeft)
                if vecino == (1, -1) or vecino == (-1, 1):
                    if numeroMenor-1 in recorrido and numeroMenor+7 in recorrido:
                        if numeroMenor-1 in recorrido[numeroMenor+7]:
                            continue
                rn[vecino_i*7 + vecino_j + 1].add(pos[0]*7 + pos[1] + 1)
                rn[pos[0]*7 + pos[1] + 1].add(vecino_i*7 + vecino_j + 1)
                continua = True

                dictionary[oracion[idx]].add((vecino_i, vecino_j))
                recorrer(dictionary, lista, oracion, idx +
                         1, (vecino_i, vecino_j), matriz, rn)

    for vecino_l in vecinos_lejanos:
        vecino_i = pos[0] + vecino_l[0]
        vecino_j = pos[1] + vecino_l[1]

        if 0 <= vecino_i <= 4 and 0 <= vecino_j <= 6:
            if matriz[vecino_i][vecino_j] == oracion[idx] and matriz[pos[0] + vecino_l[0]//2][pos[1] + vecino_l[1]//2] == ' ':
                rn = recorrido.copy()
                if not vecino_i*7 + vecino_j + 1 in rn:
                    rn[vecino_i*7 + vecino_j + 1] = set()

                if not pos[0]*7 + pos[1] + 1 in rn:
                    rn[pos[0]*7 + pos[1] + 1] = set()
                # Check large horizontal relations
                numeroVecino = vecino_i*7 + vecino_j + 1
                numeroPosicion = pos[0]*7 + pos[1] + 1
                if numeroVecino < numeroPosicion:
                    numeroMenor = numeroVecino
                else:
                    numeroMenor = numeroPosicion
                # Check if there is a vertical relation between our horizontal relationship
                if vecino_l[0] == 0:
                    if numeroMenor-7+1 in recorrido and numeroMenor+7+1 in recorrido:
                        if numeroMenor-7+1 in recorrido[numeroMenor+7+1]:
                            continue  # Intersection, dont allow this relation

                else:
                    # Check if there is an horizontal relation between our vertical relationship.
                    if numeroMenor+7-1 in recorrido and numeroMenor+7+1 in recorrido:
                        if numeroMenor+7-1 in recorrido[numeroMenor+7+1]:
                            continue
                rn[vecino_i*7 + vecino_j + 1].add(pos[0]*7 + pos[1] + 1)
                rn[pos[0]*7 + pos[1] + 1].add(vecino_i*7 + vecino_j + 1)
                continua = True

                dictionary[oracion[idx]].add((vecino_i, vecino_j))
                recorrer(dictionary, lista, oracion, idx +
                         1, (vecino_i, vecino_j), matriz, rn)
    if continua == False:
        lista.append([recorrido, idx])


def graphCreation(sentence):
    # Sentence modification
    sentence = ''.join(filter(str.isalnum, sentence)).upper()
    # Get the letters of the sentence
    letters = list(set(x for x in sentence)) + [' ']
    # End of sentence
    sentence = sentence + "#"
    '''
    Rules:
    1. There are blank spaces. (" ").
    2. The maximum repetition for each letter is 2, only 2 letters can have a maximum repetition of 3 (how many times the letter apears in the matrix)
    3. 3 types of relations: Vertical, horizontal and diagonal.
    4. Vertical and horizontal relations can jump 1 blank space.
    4. Relations can´t intersect.
    5. Matrix 7*5.
    '''
    # Our fitness function

    def fitness_function(ga_instance, solution, solution_idx):
        score = 0
        # Convert solution to a 5*7 Matrix
        matrix = np.reshape([letters[i] for i in solution], (5, 7))
        # Time to check if the sentence is in the matrix
        lista = []
        repeticiones = {letter: set() for letter in letters[:-1]}
        # For in the rows of the matrix
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                if matrix[i][j] == sentence[0]:
                    # Count the repetitions of the letters inside our matrix
                    repeticiones[sentence[0]].add((i, j))
                    recorrer(repeticiones, lista, sentence,
                             1, (i, j), matrix, recorrido={})
        # Sum the best route (Amount of letters)
        lista.sort(key=lambda x: x[1], reverse=True)
        if len(lista) >= 1:
            score += lista[0][1]
        # Score can be affected by:
        # Letter has more than 3 repetitions.
        # Letter has 3 repetitions and there is already 2 letters with a repetition of 3.
        tresRepeticiones = 0
        for value in repeticiones.values():
            if len(value) <= 2:
                continue

            if len(value) > 3:
                score -= 120
                continue

            if len(value) == 3 and tresRepeticiones >= 2:
                score -= 60
            else:
                tresRepeticiones += 1

        return score

    # Creation of our genetic algorithm
    num_generations = 2000
    population_size = 25
    mutation_probability = 0.1
    ga_instance = pygad.GA(num_generations=num_generations,
                           num_parents_mating=population_size*3//8,
                           fitness_func=fitness_function,
                           sol_per_pop=population_size,
                           num_genes=35,
                           gene_space=list(range(len(letters))),
                           mutation_percent_genes=mutation_probability,
                           crossover_type="single_point",
                           mutation_type="random",
                           gene_type=int,
                           init_range_low=0,
                           init_range_high=len(letters)-1,
                           stop_criteria="reach_"+str(len(sentence)-1))

    ctr = 0
    while ctr < 1E2:
        ga_instance = pygad.GA(num_generations=num_generations,
                               num_parents_mating=population_size*3//8,
                               fitness_func=fitness_function,
                               sol_per_pop=population_size,
                               num_genes=35,
                               gene_space=list(range(len(letters))),
                               mutation_percent_genes=mutation_probability,
                               crossover_type="single_point",
                               mutation_type="random",
                               gene_type=int,
                               init_range_low=0,
                               init_range_high=len(letters)-1,
                               stop_criteria="reach_"+str(len(sentence)-1))
        ga_instance.run()
        best_sol = ga_instance.best_solution()
        if best_sol[1] == len(sentence) - 1:
            break
        ctr += 1

    solution = best_sol
    matrix = np.reshape([letters[i] for i in solution[0]], (5, 7))
    if solution[1] == len(sentence) - 1:
        # To do:
        # 1. Check the route.
        # 2. Change the letters of non-route
        # 3. Draw graph

        # 1. Check the route
        lista = []
        repeticiones = {letter: set() for letter in letters[:-1]}
        # For in the rows of the matrix
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                if matrix[i][j] == sentence[0]:
                    # Time to check if the sentence is in the matrix
                    repeticiones[sentence[0]].add((i, j))
                    recorrer(repeticiones, lista, sentence,
                             1, (i, j), matrix, recorrido={})
        lista.sort(key=lambda x: x[1], reverse=True)
        lista = lista[0][0]
        # Count letters used in the graph
        letters = set(letters[:-1])
        letters2 = list(set("ABCDEFGHIJKLMNOPQRSTUVWXYZ") - letters)
        for letter in letters:
            letters2.append(letter)
        repeticiones = {letter: set() for letter in letters2}
        coordinates = set()
        for values in lista.values():
            for coordinate in values:
                if coordinate not in coordinates:
                    repeticiones[matrix[(coordinate-1)//7]
                                 [(coordinate-1) % 7]].add(coordinate)
                    coordinates.add(coordinate)
        # Change the letters for the letters not used
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                if matrix[i][j] != " " and ((7*i)+j+1) not in lista:
                    for letra in repeticiones:
                        if len(repeticiones[letra]) < 2:
                            matrix[i][j] = letra
                            repeticiones[letra].add((7*i)+j+1)
                            break
        # Draw graph
        # Creation of the graph
        G = nx.Graph()
        # Add all the letters of the matrix to the graph
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                G.add_node((7*i)+j+1, pos=(j, i), letter=matrix[i][j])
        for key in lista:
            for value in lista[key]:
                if matrix[(key-1)//7][(key-1) % 7] in letters and matrix[(value-1)//7][(value-1) % 7] in letters:
                    G.add_edge(key, value)
        # Colors for the nodes
        colors = {
            'A': '#f75e5e',
            'B': '#85e085',
            'C': '#aee5f7',
            'D': '#f7b54a',
            'E': '#d895f7',
            'F': '#f5f5dc',
            'G': '#d3d3d3',
            'H': '#ffb6c1',
            'I': '#50c878',
            'J': '#a2c585',
            'K': '#a0c5f5',
            'L': '#ffa07a',
            'M': '#ffd700',
            'N': '#aeea00',
            'O': '#f5b7f5',
            'P': '#f5deb3',
            'Q': '#87ceeb',
            'R': '#f59595',
            'S': '#98fb98',
            'T': '#a0522d',
            'U': '#add8e6',
            'V': '#e8eaf6',
            'W': '#f5f5f5',  
            'X': '#f5cdcd',
            'Y': '#f0e68c',
            'Z': '#6495ed',
            ' ': 'white'  
        }
        node_colors = [colors[letter]
                       for letter in nx.get_node_attributes(G, 'letter').values()]
        fig = plt.figure()
        nx.draw_networkx(G, pos=nx.get_node_attributes(
            G, 'pos'), labels=nx.get_node_attributes(G, 'letter'),node_size=500,node_color=node_colors)
        plt.gca().invert_yaxis()
        plt.box(False)
        matplotlib.use("Agg")
        fig.savefig("static/images/graphs/graph.png")
    else:
        # Copy error png to graph png
        source = os.path.join('static', 'images', 'error.png')
        destination = os.path.join(
            'static', 'images', 'graphs', 'graph.png')
        shutil.copy(source, destination)


def checkSentence(sentence, matrix):
    # Change the format of the matrix
    matrix = np.reshape(matrix, (5, 7))
    # Change the format of the sentence
    sentence = ''.join(filter(str.isalnum, sentence)).lower()
    # The easiest one: Check the repetitions of the letters
    letters = list(set(x for x in sentence)) + [' ']
    letters2 = 'abcdefghijklmnopqrstuvwxyz'
    repetition = {letter: 0 for letter in letters2}
    threeRepetition = 0
    for row in matrix:
        for letter in row:
            if letter != " ":
                repetition[letter] += 1
                if repetition[letter] == 3 and threeRepetition < 2:
                    threeRepetition += 1
                elif repetition == 3 and threeRepetition >= 2:
                    return False
                if repetition[letter] > 3:
                    return False
    # End of sentence
    repetition = {letter: set() for letter in letters[:-1]}
    sentence = sentence + "#"
    # Check route
    lista = []
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == sentence[0]:
                # Count the repetitions of the letters inside our matrix
                repetition[sentence[0]].add((i, j))
                recorrer(repetition, lista, sentence,
                         1, (i, j), matrix, recorrido={})
    lista.sort(key=lambda x: x[1], reverse=True)
    if len(lista) >= 1:
        if lista[0][1] == len(sentence)-1:
            return True
        else:
            return False
    else:
        return False
