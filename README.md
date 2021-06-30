# Star Wars DaaS API

A Python GraphQL Flask microservice for querying Star Wars data in AWS DocumentDB.



## Usage

After cloning this repo, ensure all dependencies are installed by running:
```bash
$ pip install -r requirements.txt
```
Once created, run the flask application with a development configuration:
```bash
$ flask run --host=127.0.0.1
```

The application supports two `routes` for requests:

```bash
# GraphiQL route for testing and development
http://127.0.0.1:5000/api/starwars/graphiql

# Main route 
http://127.0.0.1:5000/api/starwars
```


## API Reference

* [GraphQL](https://graphql.org/)
* [Graphene](https://graphene-python.org/)
* [Schema](https://docs.graphene-python.org/en/latest/types/schema/)
* [Scalars](https://docs.graphene-python.org/en/latest/types/scalars/)
* [ObjectType](https://docs.graphene-python.org/en/latest/types/objecttypes/)
* [Executing a query](https://docs.graphene-python.org/en/latest/execution/execute/)
* [Dataloader](https://docs.graphene-python.org/en/latest/execution/dataloader/)
