import nltk
from nltk.tree import Tree
from nltk.draw import TreeView, TreeWidget
from nltk.draw.util import CanvasFrame
from PIL import Image
import uuid


def split_cadena(word):

    return [char for char in word]


def split_cadena2(word):

    return word.split()


def gramatica_to_arbol(gramatica, cadena):

    a = []

    parser = nltk.ChartParser(gramatica)

    for tree in parser.parse(cadena):
        a.append(tree)

    if len(a) > 0:
        return a
    else:
        return False


def generar_png(file_name):

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
