from fastapi import HTTPException, status,  UploadFile
import os
import openpyxl

from src.core.deps import DataBaseDep
from src.modules.cyc.family.model import Family, FamilyCreate
from src.modules.cyc.family import service


async def get_families_controller(db: DataBaseDep):
    return await service.get_families_service(db)


async def create_family_controller(db: DataBaseDep, family: FamilyCreate) -> Family:
    mongo_insert = await service.create_family_service(db, family)
    result = await service.get_family_service(db, query={'id': mongo_insert.inserted_id})
    return result


async def get_family_details_controller(db: DataBaseDep, family_id: int) -> Family:
    result = await service.get_family_service(db, query={'id': family_id})
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Family not found',
        )
    return result


# async def upload_excel_families_controller(db: DataBaseDep, families: UploadFile) -> None:
#     [_, extension] = os.path.splitext(families.filename)
#     if extension[1:] not in ['xlsx', 'xlsm']:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail=(
#                 'The files with extension ',
#                 f'"{extension[1:]}" are not supported.'
#             )
#         )
#     fields_excel = ['nombre', 'cantidad', 'fecha caducidad', 'almacen']
#     wb = openpyxl.load_workbook(families.file)
#     ws = wb.active
#     first_row = [
#         ws.cell(row=1, column=i).value
#         for i in range(1, len(fields_excel) + 1)
#     ]
#     if len(first_row) != len(fields_excel) and not all(field in fields_excel for field in first_row):
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail='The excel file is incorrect'
#         )
#     products_excel: dict[str, list[model.Product]] = {}
#     for row in ws.iter_rows(min_row=2, min_col=1, max_col=4, values_only=True):
#         if all(value is None for value in row):
#             continue
#         if row[0] is None or row[1] is None or row[3] is None:
#             raise HTTPException(
#                 status_code=status.HTTP_400_BAD_REQUEST,
#                 detail='The excel file is incorrect'
#             )
#         warehouse_name: str = row[3]
#         try:
#             new_product = model.Product(
#                 name=row[0],
#                 quantity=row[1],
#                 exp_date=row[2],
#             )
#         except ValidationError as e:
#             raise HTTPException(
#                 status_code=status.HTTP_400_BAD_REQUEST,
#                 detail=parse_validation_error(e.errors())
#             )
#         if not warehouse_name in products_excel:
#             products_excel[warehouse_name] = []
#         if new_product.name in [p.name for p in products_excel.get(warehouse_name)]:
#             raise HTTPException(
#                 status_code=status.HTTP_400_BAD_REQUEST,
#                 detail='There cannot be duplicated products'
#             )
#         products_excel.get(warehouse_name).append(new_product)
#     for key, value in products_excel.items():
#         warehouse = await service.get_warehouse_service(db, query={'name': key})
#         if warehouse is None:
#             raise HTTPException(
#                 status_code=status.HTTP_404_NOT_FOUND,
#                 detail=f'Warehouse {key} not found'
#             )
#         products_names = [p.name for p in value]
#         updated = []
#         for product in warehouse.products:
#             if product.name in products_names:
#                 new_p = next(
#                     (p for p in value if p.name == product.name),
#                     None
#                 )
#                 p = model.Product(
#                     id=product.id,
#                     name=new_p.name,
#                     quantity=new_p.quantity,
#                     exp_date=new_p.exp_date,
#                 )
#                 updated.append(p)
#                 value.remove(new_p)
#                 continue
#             updated.append(product)
#         new_products = updated + value
#         await service.update_warehouse_service(
#             db,
#             warehouse_id=warehouse.id,
#             warehouse_update=model.WarehouseUpdate(
#                 products=new_products
#             )
#         )
