from typing import Dict, List, Optional, Union

from fastapi import Body, FastAPI, Path, Query
from pydantic import BaseModel, Field, StrictStr

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}


from pyiceberg.catalog.sql import SqlCatalog

warehouse_path = "/tmp/warehouse"
catalog = SqlCatalog(
    "default",
    **{
        "uri": f"sqlite:///{warehouse_path}/pyiceberg_catalog.db",
        "warehouse": f"file://{warehouse_path}",
    },
)
# recreate the db
catalog.destroy_tables()
catalog.create_tables()

# from pyiceberg.catalog.sql import SqlCatalog

# warehouse_path = "/tmp/warehouse"
# catalog = SqlCatalog(
#     "default",
#     **{
#         "uri": "sqlite:///:memory:",
#         # "warehouse": f"file://{warehouse_path}",
#         "echo": True,
#     },
# )
# catalog.create_tables()

# from pyiceberg.catalog.rest import RestCatalog
# catalog = RestCatalog(
#     "default",
#     **{
#         "uri": "http://localhost:8181/"
#     },
# )

# /v1/config
class CatalogConfig(BaseModel):
    """
    Server-provided configuration for the catalog.
    """ # noqa: E501
    overrides: Dict[str, StrictStr] = Field(description="Properties that should be used to override client configuration; applied after defaults and client configuration.")
    defaults: Dict[str, StrictStr] = Field(description="Properties that should be used as default configuration; applied before client configuration.")

@app.get(
    "/v1/config",
    # responses={
    #     200: {"model": CatalogConfig, "description": "Server specified configuration values."},
    #     400: {"model": IcebergErrorResponse, "description": "Indicates a bad request error. It could be caused by an unexpected request body format or other forms of request validation failure, such as invalid json. Usually serves application/json content, although in some cases simple text/plain content might be returned by the server&#39;s middleware."},
    #     401: {"model": IcebergErrorResponse, "description": "Unauthorized. Authentication is required and has failed or has not yet been provided."},
    #     403: {"model": IcebergErrorResponse, "description": "Forbidden. Authenticated user does not have the necessary permissions."},
    #     419: {"model": IcebergErrorResponse, "description": "Credentials have timed out. If possible, the client should refresh credentials and retry."},
    #     503: {"model": IcebergErrorResponse, "description": "The service is not ready to handle the request. The client should wait and retry.  The service may additionally send a Retry-After header to indicate when to retry."},
    #     500: {"model": IcebergErrorResponse, "description": "A server-side problem that might not be addressable from the client side. Used for server 500 errors without more specific documentation in individual routes."},
    # },
    tags=["Configuration API"],
    summary="List all catalog configuration settings",
    response_model_by_alias=True,
)
def get_config(
    warehouse: str = Query(None, description="Warehouse location or identifier to request from the service", alias="warehouse"),
    # token_OAuth2: TokenModel = Security(
    #     get_token_OAuth2, scopes=["catalog"]
    # ),
    # token_BearerAuth: TokenModel = Security(
    #     get_token_BearerAuth
    # ),
) -> CatalogConfig:
    """ All REST clients should first call this route to get catalog configuration properties from the server to configure the catalog and its HTTP client. Configuration from the server consists of two sets of key/value pairs. - defaults -  properties that should be used as default configuration; applied before client configuration - overrides - properties that should be used to override client configuration; applied after defaults and client configuration  Catalog configuration is constructed by setting the defaults, then client- provided configuration, and finally overrides. The final property set is then used to configure the catalog.  For example, a default configuration property might set the size of the client pool, which can be replaced with a client-specific setting. An override might be used to set the warehouse location, which is stored on the server rather than in client configuration.  Common catalog configuration settings are documented at https://iceberg.apache.org/docs/latest/configuration/#catalog-properties """
    return CatalogConfig(overrides={}, defaults={})


# /v1/{prefix}/namespaces (GET/POST)
class CreateNamespaceRequest(BaseModel):
    """
    CreateNamespaceRequest
    """ # noqa: E501
    namespace: List[StrictStr] = Field(description="Reference to one or more levels of a namespace")
    properties: Optional[Dict[str, StrictStr]] = Field(default=None, description="Configured string to string map of properties for the namespace")

class CreateNamespaceResponse(BaseModel):
    """
    CreateNamespaceResponse
    """ # noqa: E501
    namespace: List[StrictStr] = Field(description="Reference to one or more levels of a namespace")
    properties: Optional[Dict[str, StrictStr]] = Field(default=None, description="Properties stored on the namespace, if supported by the server.")


@app.post(
    "/v1/namespaces",
    # responses={
    #     200: {"model": CreateNamespaceResponse, "description": "Represents a successful call to create a namespace. Returns the namespace created, as well as any properties that were stored for the namespace, including those the server might have added. Implementations are not required to support namespace properties."},
    #     # 400: {"model": IcebergErrorResponse, "description": "Indicates a bad request error. It could be caused by an unexpected request body format or other forms of request validation failure, such as invalid json. Usually serves application/json content, although in some cases simple text/plain content might be returned by the server&#39;s middleware."},
    #     # 401: {"model": IcebergErrorResponse, "description": "Unauthorized. Authentication is required and has failed or has not yet been provided."},
    #     # 403: {"model": IcebergErrorResponse, "description": "Forbidden. Authenticated user does not have the necessary permissions."},
    #     # 406: {"model": ErrorModel, "description": "Not Acceptable / Unsupported Operation. The server does not support this operation."},
    #     # 409: {"model": IcebergErrorResponse, "description": "Conflict - The namespace already exists"},
    #     # 419: {"model": IcebergErrorResponse, "description": "Credentials have timed out. If possible, the client should refresh credentials and retry."},
    #     # 503: {"model": IcebergErrorResponse, "description": "The service is not ready to handle the request. The client should wait and retry.  The service may additionally send a Retry-After header to indicate when to retry."},
    #     # 500: {"model": IcebergErrorResponse, "description": "A server-side problem that might not be addressable from the client side. Used for server 500 errors without more specific documentation in individual routes."},
    # },
    tags=["Catalog API"],
    summary="Create a namespace",
    response_model_by_alias=True,
)
def create_namespace(
    # prefix: str = Path(..., description="An optional prefix in the path"),
    create_namespace_request: CreateNamespaceRequest = Body(None, description=""),
    # token_OAuth2: TokenModel = Security(
    #     get_token_OAuth2, scopes=["catalog"]
    # ),
    # token_BearerAuth: TokenModel = Security(
    #     get_token_BearerAuth
    # ),
) -> CreateNamespaceResponse:
    """Create a namespace, with an optional set of properties. The server might also add properties, such as &#x60;last_modified_time&#x60; etc."""
    namespace = "".join(create_namespace_request.namespace)
    properties = create_namespace_request.properties
    catalog.create_namespace(namespace, properties)
    return CreateNamespaceResponse(namespace=create_namespace_request.namespace, properties=create_namespace_request.properties)

class ListNamespacesResponse(BaseModel):
    """
    ListNamespacesResponse
    """ # noqa: E501
    # next_page_token: Optional[StrictStr] = Field(default=None, description="An opaque token which allows clients to make use of pagination for a list API (e.g. ListTables). Clients will initiate the first paginated request by sending an empty `pageToken` e.g. `GET /tables?pageToken` or `GET /tables?pageToken=` signaling to the service that the response should be paginated. Servers that support pagination will recognize `pageToken` and return a `next-page-token` in response if there are more results available. After the initial request, it is expected that the value of `next-page-token` from the last response is used in the subsequent request. Servers that do not support pagination will ignore `next-page-token` and return all results.", alias="next-page-token")
    namespaces: Optional[List[List[StrictStr]]] = None


@app.get(
    "/v1/namespaces",
    # responses={
    #     200: {"model": ListNamespacesResponse, "description": "A list of namespaces"},
    #     # 400: {"model": IcebergErrorResponse, "description": "Indicates a bad request error. It could be caused by an unexpected request body format or other forms of request validation failure, such as invalid json. Usually serves application/json content, although in some cases simple text/plain content might be returned by the server&#39;s middleware."},
    #     # 401: {"model": IcebergErrorResponse, "description": "Unauthorized. Authentication is required and has failed or has not yet been provided."},
    #     # 403: {"model": IcebergErrorResponse, "description": "Forbidden. Authenticated user does not have the necessary permissions."},
    #     # 404: {"model": IcebergErrorResponse, "description": "Not Found - Namespace provided in the &#x60;parent&#x60; query parameter is not found."},
    #     # 419: {"model": IcebergErrorResponse, "description": "Credentials have timed out. If possible, the client should refresh credentials and retry."},
    #     # 503: {"model": IcebergErrorResponse, "description": "The service is not ready to handle the request. The client should wait and retry.  The service may additionally send a Retry-After header to indicate when to retry."},
    #     # 500: {"model": IcebergErrorResponse, "description": "A server-side problem that might not be addressable from the client side. Used for server 500 errors without more specific documentation in individual routes."},
    # },
    tags=["Catalog API"],
    summary="List namespaces, optionally providing a parent namespace to list underneath",
    response_model_by_alias=True,
)
def list_namespaces(
    # prefix: str = Path(..., description="An optional prefix in the path"),
    # page_token: str = Query(None, description="", alias="pageToken"),
    # page_size: int = Query(None, description="For servers that support pagination, this signals an upper bound of the number of results that a client will receive. For servers that do not support pagination, clients may receive results larger than the indicated &#x60;pageSize&#x60;.", alias="pageSize", ge=1),
    # parent: str = Query(None, description="An optional namespace, underneath which to list namespaces. If not provided or empty, all top-level namespaces should be listed. If parent is a multipart namespace, the parts must be separated by the unit separator (&#x60;0x1F&#x60;) byte.", alias="parent"),
    # token_OAuth2: TokenModel = Security(
    #     get_token_OAuth2, scopes=["catalog"]
    # ),
    # token_BearerAuth: TokenModel = Security(
    #     get_token_BearerAuth
    # ),
) -> ListNamespacesResponse:
    """List all namespaces at a certain level, optionally starting from a given parent namespace. If table accounting.tax.paid.info exists, using &#39;SELECT NAMESPACE IN accounting&#39; would translate into &#x60;GET /namespaces?parent&#x3D;accounting&#x60; and must return a namespace, [\&quot;accounting\&quot;, \&quot;tax\&quot;] only. Using &#39;SELECT NAMESPACE IN accounting.tax&#39; would translate into &#x60;GET /namespaces?parent&#x3D;accounting%1Ftax&#x60; and must return a namespace, [\&quot;accounting\&quot;, \&quot;tax\&quot;, \&quot;paid\&quot;]. If &#x60;parent&#x60; is not provided, all top-level namespaces should be listed."""
    return ListNamespacesResponse(namespaces=catalog.list_namespaces())

# /v1/{prefix}/namespaces/{namespace} (GET/DELETE/HEAD)
class GetNamespaceResponse(BaseModel):
    """
    GetNamespaceResponse
    """ # noqa: E501
    namespace: List[StrictStr] = Field(description="Reference to one or more levels of a namespace")
    properties: Optional[Dict[str, StrictStr]] = Field(default=None, description="Properties stored on the namespace, if supported by the server. If the server does not support namespace properties, it should return null for this field. If namespace properties are supported, but none are set, it should return an empty object.")

@app.get(
    "/v1/namespaces/{namespace}",
    # responses={
    #     200: {"model": GetNamespaceResponse, "description": "Returns a namespace, as well as any properties stored on the namespace if namespace properties are supported by the server."},
    #     400: {"model": IcebergErrorResponse, "description": "Indicates a bad request error. It could be caused by an unexpected request body format or other forms of request validation failure, such as invalid json. Usually serves application/json content, although in some cases simple text/plain content might be returned by the server&#39;s middleware."},
    #     401: {"model": IcebergErrorResponse, "description": "Unauthorized. Authentication is required and has failed or has not yet been provided."},
    #     403: {"model": IcebergErrorResponse, "description": "Forbidden. Authenticated user does not have the necessary permissions."},
    #     404: {"model": IcebergErrorResponse, "description": "Not Found - Namespace not found"},
    #     419: {"model": IcebergErrorResponse, "description": "Credentials have timed out. If possible, the client should refresh credentials and retry."},
    #     503: {"model": IcebergErrorResponse, "description": "The service is not ready to handle the request. The client should wait and retry.  The service may additionally send a Retry-After header to indicate when to retry."},
    #     500: {"model": IcebergErrorResponse, "description": "A server-side problem that might not be addressable from the client side. Used for server 500 errors without more specific documentation in individual routes."},
    # },
    tags=["Catalog API"],
    summary="Load the metadata properties for a namespace",
    response_model_by_alias=True,
)
def load_namespace_metadata(
    # prefix: str = Path(..., description="An optional prefix in the path"),
    namespace: str = Path(..., description="A namespace identifier as a single string. Multipart namespace parts should be separated by the unit separator (&#x60;0x1F&#x60;) byte."),
    # token_OAuth2: TokenModel = Security(
    #     get_token_OAuth2, scopes=["catalog"]
    # ),
    # token_BearerAuth: TokenModel = Security(
    #     get_token_BearerAuth
    # ),
) -> GetNamespaceResponse:
    """Return all stored metadata properties for a given namespace"""
    properties = catalog.load_namespace_properties(namespace=namespace)
    return GetNamespaceResponse(namespace=[namespace], properties=properties)

@app.delete(
    "/v1/namespaces/{namespace}",
    # responses={
    #     204: {"description": "Success, no content"},
    #     400: {"model": IcebergErrorResponse, "description": "Indicates a bad request error. It could be caused by an unexpected request body format or other forms of request validation failure, such as invalid json. Usually serves application/json content, although in some cases simple text/plain content might be returned by the server&#39;s middleware."},
    #     401: {"model": IcebergErrorResponse, "description": "Unauthorized. Authentication is required and has failed or has not yet been provided."},
    #     403: {"model": IcebergErrorResponse, "description": "Forbidden. Authenticated user does not have the necessary permissions."},
    #     404: {"model": IcebergErrorResponse, "description": "Not Found - Namespace to delete does not exist."},
    #     419: {"model": IcebergErrorResponse, "description": "Credentials have timed out. If possible, the client should refresh credentials and retry."},
    #     503: {"model": IcebergErrorResponse, "description": "The service is not ready to handle the request. The client should wait and retry.  The service may additionally send a Retry-After header to indicate when to retry."},
    #     500: {"model": IcebergErrorResponse, "description": "A server-side problem that might not be addressable from the client side. Used for server 500 errors without more specific documentation in individual routes."},
    # },
    tags=["Catalog API"],
    summary="Drop a namespace from the catalog. Namespace must be empty.",
    response_model_by_alias=True,
)
def drop_namespace(
    # prefix: str = Path(..., description="An optional prefix in the path"),
    namespace: str = Path(..., description="A namespace identifier as a single string. Multipart namespace parts should be separated by the unit separator (&#x60;0x1F&#x60;) byte."),
    # token_OAuth2: TokenModel = Security(
    #     get_token_OAuth2, scopes=["catalog"]
    # ),
    # token_BearerAuth: TokenModel = Security(
    #     get_token_BearerAuth
    # ),
) -> None:
    catalog.drop_namespace(namespace)


# @app.head(
#     "/v1/namespaces/{namespace}",
#     # responses={
#     #     204: {"description": "Success, no content"},
#     #     400: {"model": IcebergErrorResponse, "description": "Indicates a bad request error. It could be caused by an unexpected request body format or other forms of request validation failure, such as invalid json. Usually serves application/json content, although in some cases simple text/plain content might be returned by the server&#39;s middleware."},
#     #     401: {"model": IcebergErrorResponse, "description": "Unauthorized. Authentication is required and has failed or has not yet been provided."},
#     #     403: {"model": IcebergErrorResponse, "description": "Forbidden. Authenticated user does not have the necessary permissions."},
#     #     404: {"model": IcebergErrorResponse, "description": "Not Found - Namespace not found"},
#     #     419: {"model": IcebergErrorResponse, "description": "Credentials have timed out. If possible, the client should refresh credentials and retry."},
#     #     503: {"model": IcebergErrorResponse, "description": "The service is not ready to handle the request. The client should wait and retry.  The service may additionally send a Retry-After header to indicate when to retry."},
#     #     500: {"model": IcebergErrorResponse, "description": "A server-side problem that might not be addressable from the client side. Used for server 500 errors without more specific documentation in individual routes."},
#     # },
#     tags=["Catalog API"],
#     summary="Check if a namespace exists",
#     response_model_by_alias=True,
# )
# def namespace_exists(
#     # prefix: str = Path(..., description="An optional prefix in the path"),
#     namespace: str = Path(..., description="A namespace identifier as a single string. Multipart namespace parts should be separated by the unit separator (&#x60;0x1F&#x60;) byte."),
#     # token_OAuth2: TokenModel = Security(
#     #     get_token_OAuth2, scopes=["catalog"]
#     # ),
#     # token_BearerAuth: TokenModel = Security(
#     #     get_token_BearerAuth
#     # ),
# ) -> None:
#     """Check if a namespace exists. The response does not contain a body."""
#     return BaseCatalogAPIApi.subclasses[0]().namespace_exists(prefix, namespace)

# /v1/{prefix}/namespaces/{namespace}/properties (POST)
class UpdateNamespacePropertiesRequest(BaseModel):
    """
    UpdateNamespacePropertiesRequest
    """ # noqa: E501
    removals: Optional[List[StrictStr]] = None
    updates: Optional[Dict[str, StrictStr]] = None

class UpdateNamespacePropertiesResponse(BaseModel):
    """
    UpdateNamespacePropertiesResponse
    """ # noqa: E501
    updated: List[StrictStr] = Field(description="List of property keys that were added or updated")
    removed: List[StrictStr] = Field(description="List of properties that were removed")
    missing: Optional[List[StrictStr]] = Field(default=None, description="List of properties requested for removal that were not found in the namespace's properties. Represents a partial success response. Server's do not need to implement this.")

@app.post(
    "/v1/namespaces/{namespace}/properties",
    # responses={
    #     200: {"model": UpdateNamespacePropertiesResponse, "description": "JSON data response for a synchronous update properties request."},
    #     400: {"model": IcebergErrorResponse, "description": "Indicates a bad request error. It could be caused by an unexpected request body format or other forms of request validation failure, such as invalid json. Usually serves application/json content, although in some cases simple text/plain content might be returned by the server&#39;s middleware."},
    #     401: {"model": IcebergErrorResponse, "description": "Unauthorized. Authentication is required and has failed or has not yet been provided."},
    #     403: {"model": IcebergErrorResponse, "description": "Forbidden. Authenticated user does not have the necessary permissions."},
    #     404: {"model": IcebergErrorResponse, "description": "Not Found - Namespace not found"},
    #     406: {"model": ErrorModel, "description": "Not Acceptable / Unsupported Operation. The server does not support this operation."},
    #     422: {"model": IcebergErrorResponse, "description": "Unprocessable Entity - A property key was included in both &#x60;removals&#x60; and &#x60;updates&#x60;"},
    #     419: {"model": IcebergErrorResponse, "description": "Credentials have timed out. If possible, the client should refresh credentials and retry."},
    #     503: {"model": IcebergErrorResponse, "description": "The service is not ready to handle the request. The client should wait and retry.  The service may additionally send a Retry-After header to indicate when to retry."},
    #     500: {"model": IcebergErrorResponse, "description": "A server-side problem that might not be addressable from the client side. Used for server 500 errors without more specific documentation in individual routes."},
    # },
    tags=["Catalog API"],
    summary="Set or remove properties on a namespace",
    response_model_by_alias=True,
)
def update_properties(
    # prefix: str = Path(..., description="An optional prefix in the path"),
    namespace: str = Path(..., description="A namespace identifier as a single string. Multipart namespace parts should be separated by the unit separator (&#x60;0x1F&#x60;) byte."),
    update_namespace_properties_request: UpdateNamespacePropertiesRequest = Body(None, description=""),
    # token_OAuth2: TokenModel = Security(
    #     get_token_OAuth2, scopes=["catalog"]
    # ),
    # token_BearerAuth: TokenModel = Security(
    #     get_token_BearerAuth
    # ),
) -> UpdateNamespacePropertiesResponse:
    """Set and/or remove properties on a namespace. The request body specifies a list of properties to remove and a map of key value pairs to update. Properties that are not in the request are not modified or removed by this call. Server implementations are not required to support namespace properties."""
    properties_update_summary = catalog.update_namespace_properties(namespace=namespace, removals=set(update_namespace_properties_request.removals), updates=update_namespace_properties_request.updates)
    return UpdateNamespacePropertiesResponse(updated=properties_update_summary.updated, removed=properties_update_summary.removed, missing=properties_update_summary.missing)

# /v1/{prefix}/namespaces/{namespace}/tables (GET/POST)
# /v1/{prefix}/namespaces/{namespace}/register (POST)
# /v1/{prefix}/namespaces/{namespace}/tables/{table} (GET/POST/DELETE/HEAD)
# /v1/{prefix}/transactions/commit (POST)


# /v1/oauth/tokens
# /v1/{prefix}/namespaces/{namespace}/views
# /v1/{prefix}/namespaces/{namespace}/views/{view}
# /v1/{prefix}/views/rename
# /v1/{prefix}/tables/rename (POST)
# /v1/{prefix}/namespaces/{namespace}/tables/{table}/metrics (POST)