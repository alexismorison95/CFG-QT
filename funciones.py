import nltk
from nltk.tree import Tree
from nltk.draw import TreeView, TreeWidget
from nltk.draw.util import CanvasFrame
from PIL import Image
import uuid
import json


def split_cadena(word):
    """
    Funcion split simple para cuando la gramatica posee variables y terminales formados por un solo simbolo.\n
    Ej:\n
    S -> '(' L ')' | 'a' \n
    L -> L ',' S | S
    """

    return [char for char in word]


def split_cadena2(word):
    """
    Funcion split para cuando la gramatica posee variables y terminales formados por varios simbolos. \n
    Es necesario escribir la cadena a validar separando por espacios los simbolos y los terminales.\n
    Ej:\n
    S -> F S | F \n
    F -> 'FUNCTION' 'id' '(' P ')' C 'END' \n
    etc.
    """

    return word.split()


def gramatica_to_arbol(gramatica, cadena):
    """
        Funcion que dada una gramática y una cadena genera los arboles de derivación.
    """

    a = []

    parser = nltk.ChartParser(gramatica)

    for tree in parser.parse(cadena):
        a.append(tree)

    if len(a) > 0:
        return a
    else:
        return False


def generar_png(file_name):
    """
        Funcion para generar una imagen .png a partir de un archivo .ps, solo funciona en Linux.
    """

    pic = Image.open('./res/{}.ps'.format(file_name))
    pic.load(scale=10)

    if pic.mode in ('P', '1'):
        pic = pic.convert("RGB")

    # Save to PNG
    pic.save("./res/{}.png".format(file_name))


def generar_arbol(gramatica, cadena_input, funcion_split, graficar=False):

    cadena = funcion_split(cadena_input)

    arboles = gramatica_to_arbol(gramatica, cadena)

    if graficar:

        cf = CanvasFrame()

        for arbol in arboles:

            file_name = str(uuid.uuid4())

            tc = TreeWidget(cf.canvas(), arbol)

            tc['node_font'] = 'arial 10 bold'
            tc['leaf_font'] = 'arial 10'
            tc['node_color'] = '#005990'
            tc['leaf_color'] = '#3F8F57'
            tc['line_color'] = '#175252'

            cf.add_widget(tc)

            cf.canvas().update()

            # Bug si hay parentesis en los terminales de la gramatica
            t = Tree.fromstring(str(arbol))

            TreeView(t)._cframe.print_to_file('./res/{}.ps'.format(file_name))

            # No funciona en windows
            try:
                generar_png(file_name)
            except Exception as ex:
                print(ex)

        cf.mainloop()

    if arboles:
        return True
    else:
        return False


def string_to_cfg(cfg):

    return nltk.CFG.fromstring(cfg)


def ejecutar_cfg(gramatica, cadena, graficar=False):

    try:
        return generar_arbol(gramatica, cadena, split_cadena, graficar)

    except IndexError as ie:

        print(ie)
        return False

    except:

        try:
            return generar_arbol(gramatica, cadena, split_cadena2, graficar)

        except IndexError as ie:

            print(ie)
            return False

        except Exception as ex:

            print(ex)
            return False


def guardar_json_cfg(cfg):

    try:
        with open('data.txt') as json_file:
            content = json_file.read()

        values = json.loads(content)

        values['cfgs'].append({'cfg': cfg})

        with open('data.txt', 'w') as json_file:
            json.dump(values, json_file)

    except Exception as ex:

        print(ex)

        data = {}
        data['cfgs'] = []
        data['cfgs'].append({'cfg': cfg})

        with open('data.txt', 'w') as json_file:
            json.dump(data, json_file)



def leer_json_cfg():

    with open('data.txt') as json_file:

        try:

            lista_cfgs = []

            data = json.load(json_file)

            for cfg in data['cfgs']:
                lista_cfgs.append(cfg['cfg'])

            return lista_cfgs

        except Exception as ex:
            print(ex)
