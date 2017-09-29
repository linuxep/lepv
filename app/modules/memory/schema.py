from model.db import DBclient
import graphene
import json


class Memory(graphene.ObjectType):
    """docstring for Memory"""
    host = graphene.String()
    total = graphene.Float()
    free = graphene.Float()
    buffers = graphene.Float()
    cached = graphene.Float()


class Query(graphene.ObjectType):
    # memory = graphene.String(description='Memory Info',
    #                          name=graphene.String(default_value="stranger"))
    memory = graphene.List(Memory)

    def resolve_memory(self, args, context, info):
        result = DBclient.query('select * from memory;')
        # for item in result.items():
        #     print(list(item[1]))
        items = list(result.items()[0][1])
        json = []
        for item in items:
            mem = Memory()
            mem.host = format(item["host"])
            mem.free = item["free"]
            mem.buffers = item["buffers"]
            mem.cached = item["caches"]
            mem.total = item["total"]
            json.append(mem)
        return json


MemorySchema = graphene.Schema(query=Query)
