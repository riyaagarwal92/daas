import time
import functools
import logging
from datetime import date, datetime
from typing import List, Dict, Union
from graphql.execution.base import ResolveInfo
from graphql.language.ast import FragmentSpread, Field
from promise import Promise
from promise.dataloader import DataLoader
from common.config import DATA_LOADER, DEFAULT_LIMIT, DEFAULT_OFFSET, DEFAULT_FILTER
from graphql.utils.ast_to_dict import ast_to_dict


def format_logs(logging_dict):
    """Formats the logs to a string format."""

    logging_response = ""
    for key, value in logging_dict.items():
        logging_response = logging_response + f"{str(key).replace(' ', '')} = {str(value)};"
    return logging_response


def get_argument_map(node):
    """This method parses over the Query String AST to fetch the query arguments and variables."""
    arg_map = {}
    if node.get("selection_set"):
        for leaf in node.get("selection_set").get("selections"):
            for subleaf in leaf.get("arguments"):
                if subleaf.get("kind") == "Argument":
                    if subleaf.get("value").get("kind") == "Variable":
                        arg_map.update(
                            {
                                subleaf["name"]["value"]: subleaf.get("value")
                                .get("name")
                                .get("value")
                            }
                        )
                    else:
                        arg_map.update(
                            {
                                subleaf["name"]["value"]: subleaf.get("value").get(
                                    "value"
                                )
                            }
                        )
    return arg_map


def get_limit(info, args):
    """A convenience function to call get_argument_map with info
    Args:
        info (ResolveInfo)
    Returns:
        value: Returns the limit
    """

    if "__limit" in args.keys():
        del args["__limit"]

    limit = DEFAULT_LIMIT
    node = ast_to_dict(info.operation)
    query_args = info.variable_values
    mapping = get_argument_map(node)

    for key in mapping:
        if key == "_Limit":
            if mapping[key] in query_args.keys():
                limit = query_args[mapping[key]]
            else:
                limit = mapping[key]
    return int(limit)


def get_offset(args):
    """Extracts the offset from the args."""

    if "__offset" in args.keys():
        offset = args["__offset"]
        del args["__offset"]
        return offset
    else:
        return DEFAULT_OFFSET


def extract_requested_fields(
    info: ResolveInfo, fields: List[Union[Field, FragmentSpread]]
) -> Dict:
    """Extracts the fields requested in a GraphQL query by processing the AST
    and returns a nested dictionary representing the requested fields.
    GD
    Note:
        This function should support arbitrarily nested field structures
        including fragments.
    Example:
        Consider the following query passed to a resolver and running this
        function with the `ResolveInfo` object passed to the resolver.
        >>> query = "query getAuthor{author(authorId: 1){nameFirst, nameLast}}"
        >>> extract_requested_fields(info, info.field_asts, True)
        {'author': {'name_first': None, 'name_last': None}}
    Args:
        info (ResolveInfo): The GraphQL query info passed
            to the resolver function.
        fields (List[Union[Field, FragmentSpread]]): The list of `Field` or
            `FragmentSpread` objects parsed out of the GraphQL query and stored
            in the AST.
        do_convert_to_snake_case (bool): Whether to convert the fields as they
            appear in the GraphQL query (typically in camel-case) back to
            snake-case (which is how they typically appear in ORM classes).
    Returns:
        Dict: The nested dictionary containing all the requested fields.
    """
    result = {}
    for field in fields:
        key = field.name.value
        val = 1

        if isinstance(field, Field):
            if hasattr(field, "selection_set") and field.selection_set is not None:
                val = extract_requested_fields(
                    info=info,
                    fields=field.selection_set.selections,
                )
            result[key] = val

        elif isinstance(field, FragmentSpread):
            print("isInstance FragmentSpread")
            fragment = info.fragments[field.name.value]
            val = extract_requested_fields(
                info=info,
                fields=fragment.selection_set.selections,
            )
            result = val
    return result


def recursive_cleanup(requestedValues: dict, projection={}, key_prefix=""):
    """[summary]
    Args:
        requestedValues (dict): [description]
        projection (dict, optional): [description]. Defaults to {}.
        key_prefix (str, optional): [description]. Defaults to "".
    Returns:
        [dict]: cleaned up projection
    """
    for key, val in requestedValues.items():
        if val == 1:
            projection[key_prefix + key] = val
        else:
            for inner_key, inner_val in val.items():
                if inner_val == 1:
                    projection[key_prefix + key + "." + inner_key] = 1
                else:
                    recursive_cleanup(
                        inner_val, projection, key + "." + inner_key + "."
                    )
    return projection


def get_projection(info: ResolveInfo) -> Dict:
    """[summary]
    Args:
        info (ResolveInfo): [description]
    Returns:
        Dict: Cleaned up projection attributes, including nested projection, to query only the relevant requested fields out of DocumentDB
    """

    requested_fields = extract_requested_fields(info, info.field_asts)
    first_key = next(iter(requested_fields))
    projection = recursive_cleanup(requested_fields[first_key], {})
    return projection


def data_loader_processor(key_name: str, keys: [str], results: [list]) -> Promise[list]:
    """
    Data Loader Helper clenas up the result of a batch request to return the responses in the order of the requests, as a Promise
    Args:
        key_name (str): Key name for this execution
        keys ([str]): Array of Keys to query from DocumentDB
        results ([list]):  Results from DocumentDB Find() Query
    Returns:
        Promise[list]: Promise of result per key
    """
    nested_key_name = None
    result_organized_by_keys = {}

    if "." in key_name:
        nested_key_name = key_name.split(".")[1]
        key_name = key_name.split(".")[0]

    def create_result_organized_by_keys(key, value):
        if key in result_organized_by_keys:
            result_organized_by_keys[key].append(value)
        else:
            result_organized_by_keys[key] = [value]

    if nested_key_name:
        for result in results:
            for inner_result in result[key_name]:
                create_result_organized_by_keys(inner_result[nested_key_name], result)
    else:
        for result in results:
            create_result_organized_by_keys(result[key_name], result)
    return Promise.resolve([result_organized_by_keys.get(key, []) for key in keys])


class BatchLoad(DataLoader):
    cache = False
    """
    DataLoader will coalesce all individual requests which occur within a single frame of execution (a single tick of the event loop) and then call your batch function with all requested keys. \n
    Learn more here: https://docs.graphene-python.org/en/latest/execution/dataloader/
    Args:
        DataLoader ([type]): [description]
    """

    def batch_load_fn(self, keys):
        batch_key = DATA_LOADER[self._promise_cache["batch_key"]]
        results = self._promise_cache["fn"](
            {batch_key["key_name"]: {"$in": keys}}, batch_key["info"]
        )
        return data_loader_processor(batch_key["key_name"], keys, results)


def timer(func):
    """Times the decorated function"""
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        start_time = time.perf_counter()
        value = func(*args, **kwargs)
        end_time = time.perf_counter()
        run_time = end_time - start_time
        logging.info(f"Completed function {func.__name__!r} in {run_time:.4f} secs")
        return value
    return wrapper_timer


def format_date_args(args):
    """Performs any date conversions for the input request."""
    
    for key in list(args.keys()):
        if isinstance(args[key], date):
            dt = datetime.combine(args[key], datetime.min.time())
            args[key] = dt      
    return args 


def build_mongo_query(args: dict) -> Dict:
    """[summary]
    Args:
        args (dict): list of args received from graphQL query
    Returns:
        Dict: parameters for DocDb find query.
    """   

    # Formats date fields
    format_date_args(args)

    # Adding validity filter to fetch only valid docs
    args.update(DEFAULT_FILTER)

    return args
