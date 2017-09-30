import json
from app.model.db import DBclient
import graphene


class Memory(graphene.ObjectType):
    """docstring for Memory"""
    host = graphene.String()
    total = graphene.Float()
    free = graphene.Float()
    buffers = graphene.Float()
    cached = graphene.Float()
    time = graphene.String()


class Query(graphene.ObjectType):
    # memory = graphene.String(description='Memory Info',
    #                          name=graphene.String(default_value="stranger"))
    memory = graphene.List(Memory)

    def resolve_memory(self, args):
        result = DBclient.query('select * from memory;')
        data = []
        if not result:
            return data
        print(json.dumps(result.raw['series'][0]))
        # print(json.dumps([ value for value in result.raw['series'][0]['values'] ]))
        items = list(result.items()[0][1])
        for item in items:
            # print(item)
            mem = Memory()
            mem.host = format(item["host"])
            mem.free = item["free"]
            mem.buffers = item["buffers"]
            mem.cached = item["caches"]
            mem.total = item["total"]
            mem.time = item["time"]
            data.append(mem)
        return data


MemorySchema = graphene.Schema(query=Query)
