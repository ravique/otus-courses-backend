import graphene

from courses.schema import Query as CoursesQuery, Mutation as LecturerMutation


class Query(CoursesQuery, graphene.ObjectType):
    pass


class Mutation(LecturerMutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
