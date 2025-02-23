# import cv2
import os
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


class StegoEncoder:
    def __init__(self):
        pass

    def encode(self, img: np.ndarray, message: str, password: str) -> np.ndarray:
        # Convert message to bytes
        message_bytes = message.encode("utf-8")
        # Generate 16-byte salt and 12-byte nonce
        salt = os.urandom(16)
        nonce = os.urandom(12)
        key = derive_key(password.encode("utf-8"), salt)

        # Encrypt message with ChaCha20_Poly1305
        cipher = ChaCha20_Poly1305.new(key=key, nonce=nonce)
        ciphertext, tag = cipher.encrypt_and_digest(message_bytes)

        # Build the payload
        payload = salt + nonce + tag + ciphertext
        payload_len = len(payload)
        header = payload_len.to_bytes(4, byteorder="big")
        final_payload = header + payload  # Total bytes = 4 + payload_len

        # Convert payload to bitstream
        bitstream = "".join(format(b, "08b") for b in final_payload)

        flat_img = img.reshape(-1)
        if len(bitstream) > flat_img.size:
            raise ValueError(
                f"Image too small to hold secret message. Required bits: {len(bitstream)}; Available: {flat_img.size}."
            )

        # Embed each bit into the LSB of image pixels
        for i, bit in enumerate(bitstream):
            flat_img[i] = (flat_img[i] & 0xFE) | int(bit)

        encoded_img = flat_img.reshape(img.shape)
        return encoded_img
