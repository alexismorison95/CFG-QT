import json
import uuid


def guardar_cfg(cfg, descripcion):

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


def leer_cfg():

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


def buscar_cfg(lista, id):

    for i, cfg in enumerate(lista):

        if cfg.id == id:

            return i


def editar_cfg(lista, id, descripcion, cfg):

    i = buscar_cfg(lista, id)

    lista['gramaticas'][i] = {
        'id': id,
        'descripcion': descripcion,
        'cfg': cfg
    }

    data = {}

    data['gramaticas'] = lista

    with open('data.txt', 'w') as json_file:
        json.dump(data, json_file)


def eliminar_cfg(lista, id):

    i = buscar_cfg(lista, id)

    lista.pop(i)

    data = {}

    data['gramaticas'] = lista

    with open('data.txt', 'w') as json_file:
        json.dump(data, json_file)
