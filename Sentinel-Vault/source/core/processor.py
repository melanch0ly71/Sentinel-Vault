import zipfile
import io
import os
import shutil
from core.crypto import SentinelEngine

class VaultProcessor:
    @staticmethod
    def pack_and_encrypt_folder(folder_path, output_path, password):
        """Compresses, encrypts, and deletes the original folder."""
        abs_folder = os.path.abspath(folder_path)
        abs_output = os.path.abspath(output_path)
        
        # 1. Zip folder contents into memory
        byte_stream = io.BytesIO()
        with zipfile.ZipFile(byte_stream, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for root, _, files in os.walk(abs_folder):
                for file in files:
                    full_p = os.path.join(root, file)
                    # relpath ensures we don't store the full C:\ drive path
                    arcname = os.path.relpath(full_p, abs_folder)
                    zip_file.write(full_p, arcname)
        
        raw_data = byte_stream.getvalue()
        
        # 2. Encrypt
        engine = SentinelEngine(password)
        encrypted_blob = engine.encrypt_data(raw_data)
        
        # 3. Save .sentinel file
        with open(abs_output, "wb") as f:
            f.write(encrypted_blob)
            f.flush()
            os.fsync(f.fileno()) 
            
        # 4. Cleanup original
        if os.path.exists(abs_output) and os.path.getsize(abs_output) > 0:
            shutil.rmtree(abs_folder)
        else:
            raise Exception("Failed to verify encrypted file. Original preserved.")

    @staticmethod
    def decrypt_and_unpack_payload(file_path, extract_to_root, password):
        """Decrypts and restores the original folder structure."""
        abs_file = os.path.abspath(file_path)
        
        with open(abs_file, "rb") as f:
            encrypted_blob = f.read()
            
        # Decrypt (Raises error if password/data is tampered)
        decrypted_data = SentinelEngine.decrypt_data(password, encrypted_blob)
        
        # Load ZIP from memory
        zip_stream = io.BytesIO(decrypted_data)
        with zipfile.ZipFile(zip_stream, 'r') as zip_ref:
            # We determine the original folder name from the .sentinel filename
            folder_name = os.path.basename(abs_file).replace(".sentinel", "")
            final_dest = os.path.join(extract_to_root, folder_name)
            
            # Ensure we don't overwrite an existing folder
            if not os.path.exists(final_dest):
                os.makedirs(final_dest)
            
            zip_ref.extractall(final_dest)
            
        # Optional: os.remove(abs_file) # Uncomment if you want the vault deleted after use