import numpy as np
from Crypto.Cipher import ChaCha20_Poly1305
from argon2.low_level import hash_secret_raw, Type


def derive_key(password: bytes, salt: bytes) -> bytes:
    # Derive a 32-byte key using Argon2
    return hash_secret_raw(
        secret=password,
        salt=salt,
        time_cost=4,
        memory_cost=102400,
        parallelism=2,
        hash_len=32,
        type=Type.ID,
    )


class StegoDecoder:
    def __init__(self):
        pass

    def decode(self, img: np.ndarray, password: str) -> str:
        flat_img = img.reshape(-1)

        # Extract header (first 32 bits)
        header_bits = "".join(str(px & 1) for px in flat_img[:32])
        header_int = int(header_bits, 2)
        header_bytes = header_int.to_bytes(4, byteorder="big")
        payload_len = int.from_bytes(header_bytes, byteorder="big")

        total_bytes = payload_len + 4  # header + payload
        total_bits_needed = total_bytes * 8

        if flat_img.size < total_bits_needed:
            raise ValueError("Image does not contain the full payload data.")

        bitstream = "".join(str(px & 1) for px in flat_img[:total_bits_needed])
        # Convert bitstream back to bytes
        final_payload = bytes(
            int(bitstream[i : i + 8], 2) for i in range(0, len(bitstream), 8)
        )

        # Remove header
        payload = final_payload[4:]
        if len(payload) < (16 + 12 + 16):
            raise ValueError("Payload is corrupted or incomplete.")

        salt = payload[:16]
        nonce = payload[16:28]  # 12 bytes nonce
        tag = payload[28:44]  # 16 bytes authentication tag
        ciphertext = payload[44:]

        key = derive_key(password.encode("utf-8"), salt)
        cipher = ChaCha20_Poly1305.new(key=key, nonce=nonce)
        try:
            plaintext = cipher.decrypt_and_verify(ciphertext, tag)
        except ValueError:
            # Catch the MAC check error and re-raise with a more user-friendly message
            raise ValueError("Incorrect password or the payload has been corrupted.")

        return plaintext.decode("utf-8")
