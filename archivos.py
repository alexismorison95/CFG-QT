import json
import uuid


def guardar(cfg, descripcion):

    try:
        with open('data.txt') as json_file:
            content = json_file.read()

        values = json.loads(content)

        values['gramaticas'].append({
            'id': str(uuid.uuid4()),
            'descripcion': descripcion,
            'cfg': cfg
        })

        with open('data.txt', 'w') as json_file:
            json.dump(values, json_file)

    except Exception as ex:

        print(ex)

        data = {}

        data['gramaticas'] = []

        data['gramaticas'].append({
            'id': str(uuid.uuid4()),
            'descripcion': descripcion,
            'cfg': cfg
        })

        with open('data.txt', 'w') as json_file:
            json.dump(data, json_file)


def leer():

    try:

        with open('data.txt') as json_file:

            lista = []

            data = json.load(json_file)

            for cfg in data['gramaticas']:

                lista.append(cfg)

            return lista

    except Exception as ex:

        print(ex)

        return []


def buscar(lista, id):

    for i, cfg in enumerate(lista):

        if cfg['id'] == id:

            return i


def editar(lista, cfg, index):

    try:
        lista[index] = {
            'id': cfg['id'],
            'descripcion': cfg['descripcion'],
            'cfg': cfg['cfg']
        }

        data = {}

        data['gramaticas'] = lista

        with open('data.txt', 'w') as json_file:
            json.dump(data, json_file)

    except Exception as ex:

        print(ex)


def eliminar(lista, index):

    try:
        lista.pop(index)

        data = {}

        data['gramaticas'] = lista

        with open('data.txt', 'w') as json_file:
            json.dump(data, json_file)

    except Exception as ex:

        print(ex)
