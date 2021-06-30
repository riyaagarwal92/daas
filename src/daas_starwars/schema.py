from graphene import ObjectType, String, List, Int, Date
from common.config import DEFAULT_QUERY_ARGS
from daas_starwars.handlers import getCharacters


class Characters(ObjectType):
    class Meta:
        description = "This collection returns the Star Wars Character info"

    name = String(description = "Name of the character")
    dob = Date(description = "Character's date of birth")
    height = String(description = "Character's height")
    hair_color = String(description = "Character's hair color")
    eye_color = String(description = "Character's eye color")
    gender = String(description = "Character's gender")
    age = Int(description = "Character's age")


class StarwarsDomainQuery(ObjectType):
    class Meta:
        description = "Available queries and schemas within the Star Wars Characters collection"

    characters = List(
        Characters,
        DEFAULT_QUERY_ARGS,
        name = String(description = "Name of the Star Wars Character"),
        dob = Date(description = "Date of Birth of the Character"),
        description = "This query returns the Star Wars character info.",
    )

    def resolve_characters(self, info, **args):
        return getCharacters(args, info)
