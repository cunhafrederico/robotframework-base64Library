import base64
import os
from robot.api import logger
from typing import Optional

class base64Library:
    """Robot Framework library for Base64 file operations with large file support.
    
    Features:
    - Optional chunk_size parameter for all operations
    - Memory-efficient streaming for large files
    - Automatic handling of file paths
    
    = Example =
    | *** Settings ***   |
    | Library           | Base64Library |
    | 
    | *** Test Cases *** |
    | Encode Small File |
    |   ${base64}=      | File To Base64 | small.txt |
    | 
    | Encode Large File |
    |   ${base64}=      | File To Base64 | large.bin | chunk_size=10485760 |
    | 
    | Stream Huge File  |
    |   File To Base64 File | huge.iso | encoded.txt | chunk_size=5242880 |
    """

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    DEFAULT_CHUNK_SIZE = 3 * 1024 * 1024  # 3MB (optimal for Base64)

    def file_to_base64(self, file_path: str, chunk_size: Optional[int] = None) -> str:
        """Converts file to Base64 string with optional chunking.
        
        Args:
            file_path: Input file path
            chunk_size: Optional processing chunk size (bytes)
            
        Returns:
            Base64 encoded string
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
            
        chunk_size = self._validate_chunk_size(chunk_size)
        chunks = []
        
        with open(file_path, 'rb') as f:
            while chunk := f.read(chunk_size):
                encoded_chunk = base64.b64encode(chunk)
                chunks.append(encoded_chunk)
                
        base64_str = b''.join(chunks).decode('utf-8')
        logger.info(f"Encoded {file_path} to Base64 ({len(base64_str)} chars)")
        return base64_str

    def file_to_base64_file(self, input_path: str, output_path: str, 
                           chunk_size: Optional[int] = None) -> None:
        """Streams file to Base64 file with optional chunk size.
        
        Args:
            input_path: Source file path
            output_path: Target Base64 file path
            chunk_size: Optional processing chunk size (bytes)
        """
        self._validate_path(input_path)
        chunk_size = self._validate_chunk_size(chunk_size)
        output_dir = os.path.dirname(output_path)
        
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        with open(input_path, 'rb') as in_file, \
             open(output_path, 'w', encoding='utf-8') as out_file:
            
            while chunk := in_file.read(chunk_size):
                encoded = base64.b64encode(chunk).decode('utf-8')
                out_file.write(encoded)
                
        logger.info(f"Stream-encoded {input_path} to {output_path} using {chunk_size} byte chunks")

    def base64_file_to_file(self, input_path: str, output_path: str,
                           chunk_size: Optional[int] = None) -> None:
        """Converts Base64 file to binary file with optional chunk size.
        
        Args:
            input_path: Base64 file path
            output_path: Target binary file path
            chunk_size: Optional processing chunk size (bytes)
        """
        self._validate_path(input_path)
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        # Use 4:3 ratio for Base64 decoding chunks
        decode_chunk_size = self._calculate_decode_chunk_size(chunk_size)
        
        with open(input_path, 'r', encoding='utf-8') as in_file, \
             open(output_path, 'wb') as out_file:
            
            while base64_chunk := in_file.read(decode_chunk_size):
                # Handle incomplete chunks at end of file
                if len(base64_chunk) % 4 != 0:
                    base64_chunk += '=' * (4 - len(base64_chunk) % 4)
                    
                binary_data = base64.b64decode(base64_chunk)
                out_file.write(binary_data)
                
        logger.info(f"Stream-decoded {input_path} to {output_path}")

    # Existing base64_to_file remains unchanged
    def base64_to_file(self, base64_str: str, output_path: str) -> None:
        """Saves Base64 string to a file (for smaller content)."""
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        binary_data = base64.b64decode(base64_str)
        with open(output_path, 'wb') as f:
            f.write(binary_data)
            
        logger.info(f"Created {output_path} from Base64 string ({len(binary_data)} bytes)")

    # Helper methods
    def _validate_path(self, path: str) -> None:
        if not os.path.exists(path):
            raise FileNotFoundError(f"Path not found: {path}")
            
    def _validate_chunk_size(self, chunk_size: Optional[int]) -> int:
        """Ensure chunk size is valid and optimized for Base64."""
        if chunk_size is None:
            return self.DEFAULT_CHUNK_SIZE
            
        # Ensure minimum size and multiple of 3 for encoding efficiency
        chunk_size = max(chunk_size, 1024)  # At least 1KB
        return (chunk_size // 3) * 3  # Round down to nearest multiple of 3
        
    def _calculate_decode_chunk_size(self, chunk_size: Optional[int]) -> int:
        """Calculate optimal read size for Base64 decoding."""
        if chunk_size is None:
            return 4 * 1024 * 1024  # 4MB default for decoding
            
        # Base64 uses 4 characters for every 3 bytes
        return max((chunk_size * 4) // 3, 4096)  # At least 4KB