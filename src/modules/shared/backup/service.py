import json
import os
import tarfile
import tempfile

from fastapi import HTTPException, Response
from fastapi.responses import JSONResponse
from src.core.database.backup import BackupEncoder, dump_to_json, populate_from_json
from src.core.deps import DataBaseDep
from src.core.utils.security import decrypt_data, derive_key, encrypt_data, generate_salt


async def generate_backup_service(db: DataBaseDep, password: str):
    data = await dump_to_json(db)

    print("Data dumped")

    with tempfile.TemporaryDirectory() as tmp_dir:
        json_file_path = os.path.join(tmp_dir, "backup.json")
        with open(json_file_path, "w") as json_file:
            json.dump(data, json_file, indent=4, cls=BackupEncoder)

        print("Data dumped to JSON file")

        compressed_file_path = os.path.join(tmp_dir, "backup.tar.gz")
        with tarfile.open(compressed_file_path, "w:gz") as tar:
            tar.add(json_file_path, arcname="backup.json")

        print("Data compressed")

        with open(compressed_file_path, "rb") as compressed_file:
            compressed_data = compressed_file.read()

        salt = generate_salt()
        key = derive_key(password, salt)

        print("Key derived")

        iv, encrypted_data = encrypt_data(compressed_data, key)

        print("Data encrypted")

        combined_data = salt + iv + encrypted_data

    return Response(
        content=combined_data,
        media_type="application/octet-stream",
        headers={"Content-Disposition": "attachment; filename=backup.enc"}
    )


async def restore_backup_service(db: DataBaseDep, password: str, file):
    with tempfile.TemporaryDirectory() as tmp_dir:
        file_path = os.path.join(tmp_dir, file.filename)
        with open(file_path, "wb") as tmp_file:
            tmp_file.write(await file.read())

        with open(file_path, "rb") as encrypted_file:
            combined_data = encrypted_file.read()

        salt = combined_data[:16]
        combined_data = combined_data[16:]

        iv = combined_data[:16]
        encrypted_data = combined_data[16:]

        key = derive_key(password, salt)

        decrypted_data = decrypt_data(encrypted_data, key, iv)

        decrypted_file_path = os.path.join(
            tmp_dir, "decrypted_data.tar.gz")
        with open(decrypted_file_path, "wb") as decrypted_file:
            decrypted_file.write(decrypted_data)

        with tarfile.open(decrypted_file_path, mode="r:gz") as tar:
            tar.extractall(tmp_dir)

        with open(os.path.join(tmp_dir, "backup.json"), "r") as json_file:
            restored_data = json.load(json_file)

        await populate_from_json(db, restored_data)

    return {"message": "Data restored successfully"}
