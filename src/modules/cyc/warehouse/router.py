from pydantic import UUID4

from fastapi import APIRouter, status, UploadFile

from src.core.deps import DataBaseDep
from src.server import dependencies
from src.modules.cyc.warehouse import controller
from src.modules.cyc.warehouse import model

router = APIRouter(tags=['Warehouse'], dependencies=dependencies)


@router.get(
    '',
    status_code=status.HTTP_200_OK,
    response_model=list[model.Warehouse],
    responses={
        200: {"description": "Successful Response"},
        500: {"description": "Internal Server Error"}
    }
)
async def get_warehouses(db: DataBaseDep):
    """
    **Retrieve a list of all warehouses.**

    Queries the database and returns a list of all warehouses, each including
    its name, location, and the products it stores.
    """
    return await controller.get_warehouses_controller(db)


@router.get(
    '/product',
    status_code=status.HTTP_200_OK,
    response_model=model.GetProducts,
    responses={
        200: {"description": "Successful Response"},
        500: {"description": "Internal Server Error"}
    }
)
async def get_products(db: DataBaseDep, limit: int = 100, offset: int = 0):
    """
    **Retrieve a list of all products in all warehouses.**

    Queries the database to return a list of all products across all warehouses,
    including each product's name, quantity, expiration date, and the ID of the warehouse
    it's stored in.
    """
    return await controller.get_products_controller(db, limit, offset)


@router.get(
    '/product/{product_id}',
    status_code=status.HTTP_200_OK,
    response_model=model.ProductOut,
    responses={
        200: {"description": "Successful Response"},
        404: {"description": "Product not found"},
    }
)
async def get_product(db: DataBaseDep, product_id: UUID4):
    return await controller.get_product_controller(db, product_id)


@router.get(
    '/{warehouse_id}',
    status_code=status.HTTP_200_OK,
    response_model=model.Warehouse,
    responses={
        200: {"description": "Successful Response"},
        500: {"description": "Internal Server Error"}
    }
)
async def get_warehouse(db: DataBaseDep, warehouse_id: UUID4):
    """
    **Retrieve a warehouses by its ID.**

    Queries the database and returns a warehouses, which include
    its name, location, and the products it stores.
    """
    return await controller.get_warehouse_controller(db, warehouse_id)


@router.post(
    '',
    status_code=status.HTTP_201_CREATED,
    response_model=model.Warehouse,
    responses={
        201: {"description": "Warehouse created successfully"},
        400: {"description": "Bad Request - Warehouse already exists"},
        500: {"description": "Internal Server Error"}
    }
)
async def create_warehouse(db: DataBaseDep, warehouse: model.WarehouseCreate):
    """
    **Create a new warehouse.**

    Accepts warehouse information and creates a new warehouse record in the database.
    The warehouse information includes its name, location, and initial products if any.
    """
    return await controller.create_warehouse_controller(db, warehouse)


@router.post(
    '/product',
    status_code=status.HTTP_201_CREATED,
    response_model=list[model.ProductOut],
    responses={
        201: {"description": "Products created successfully"},
        400: {"description": "Bad Request - Product already exists"},
        404: {"description": "Warehouse not found"},
        500: {"description": "Internal Server Error"}
    }
)
async def create_product(db: DataBaseDep, product: model.ProductCreate):
    """
    **Create new products within a warehouse.**

    Accepts product information to create new products within the specified warehouse.
    Each product must include its name, quantity, expiration date, and the ID of the warehouse.
    """
    return await controller.create_product_controller(db, product)


@router.post(
    '/product/excel',
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None,
    responses={
        200: {"description": "Products in excel created successfully"},
        404: {"description": "Warehouse not found"},
        400: {"description": "The data was incorrect"},
    }
)
async def upload_excel_products(db: DataBaseDep, products: UploadFile):
    return await controller.upload_excel_products_controller(db, products)


@router.delete(
    '/product/{product_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        204: {"description": "Product successfully deleted"},
        404: {"description": "Product not found"},
    }
)
async def delete_product(db: DataBaseDep, product_id: UUID4):
    """
    **Delete a product by its ID.**

    Deletes the product identified by the given UUID from the database.
    """
    await controller.delete_product_controller(db, product_id)
    return None


@router.delete(
    '/{warehouse_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        204: {"description": "Warehouse successfully deleted"},
        404: {"description": "Warehouse not found"},
        500: {"description": "Internal Server Error"}
    }
)
async def delete_warehouse(db: DataBaseDep, warehouse_id: UUID4):
    """
    **Delete a warehouse by its ID.**

    Deletes the warehouse identified by the given UUID from the database.
    """
    await controller.delete_warehouse_controller(db, warehouse_id)
    return None


@router.patch(
    '/product',
    status_code=status.HTTP_200_OK,
    response_model=list[model.ProductOut],
    responses={
        200: {"description": "Products updated successfully"},
        404: {"description": "Warehouse or product not found"},
        500: {"description": "Internal Server Error"}
    }
)
async def update_product(db: DataBaseDep, product_update: model.ProductUpdate):
    """
    **Update existing products within a warehouse.**

    Accepts product information to update existing products. Each product update must specify
    the product ID,
    and can update the product's name, quantity, and expiration date.
    """
    return await controller.update_product_controller(db, product_update)


@router.patch(
    '/{warehouse_id}',
    status_code=status.HTTP_200_OK,
    response_model=model.Warehouse,
    responses={
        200: {"description": "Warehouse successfully updated"},
        404: {"description": "Warehouse not found"}
    }
)
async def update_warehouse(
    db: DataBaseDep,
    warehouse_id: UUID4,
    update_warehouse: model.WarehouseUpdate
):
    return await controller.update_warehouse_controller(
        db,
        warehouse_id,
        update_warehouse
    )
