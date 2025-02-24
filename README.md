# StegoHelix

StegoHelix is a cutting‐edge steganography application written in Python that securely hides secret messages inside cover images. It leverages authenticated encryption (ChaCha20-Poly1305) with Argon2-based key derivation and embeds encrypted data into the least significant bits (LSBs) of PNG images. The project features an intuitive Streamlit interface for both encoding and decoding messages.

> **Note:** This project uses [uv](https://github.com/astral-sh/uv) for dependency management. Follow the instructions below to set up your environment using uv.

---

## Table of Contents

- [StegoHelix](#stegohelix)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [Project Structure](#project-structure)
  - [Installation](#installation)
    - [Using uv](#using-uv)
    - [Alternative: Installing with pip](#alternative-installing-with-pip)
  - [Usage](#usage)
    - [Running the Application](#running-the-application)
    - [How It Works](#how-it-works)
      - [Encoding Process](#encoding-process)
      - [Decoding Process](#decoding-process)
  - [Dependencies](#dependencies)
  - [Contributing](#contributing)
  - [License](#license)
  - [Disclaimer](#disclaimer)
  - [Acknowledgments](#acknowledgments)

---

## Features

- **Robust Encryption:**  
  Utilizes ChaCha20-Poly1305 for authenticated encryption. If the password is incorrect or data is modified, decryption fails gracefully with a clear message.

- **Secure Key Derivation:**  
  Derives a 32-byte key using Argon2 from the user-supplied password and a random salt.

- **Lossless Steganography:**  
  Embeds the secret payload into the LSBs of cover images. The output is always saved as a PNG to preserve data integrity.

- **Structured Payload:**  
  The payload consists of:
  - A 4-byte header indicating payload length.
  - 16 bytes of salt.
  - 12 bytes of nonce.
  - 16 bytes of authentication tag.
  - The ciphertext.

- **User-Friendly Interface:**  
  A Streamlit web GUI lets you encode and decode messages interactively.

- **Clear Error Reporting:**  
  Friendly error messages (e.g., “Incorrect password or the payload has been corrupted”) guide users when decryption fails.

---

## Project Structure

```text
StegoHelix/
├── app.py                              # Main Streamlit GUI application
├── docs/                               # Documentation folder
│   ├── EDUNET_STEGANOGRAPHY.pptx       # Project presentation slides
│   ├── images/                         # Example images for demonstration
│   │   ├── image.png                   # Original cover image
│   │   └── protected.png               # Encrypted image (password: KEY)
├── pyproject.toml                      # Project configuration
└── src/
    ├── encoder.py                      # Module for encoding messages into images
    └── decoder.py                      # Module for decoding messages from images
```

---

## Installation

This project is managed with [uv](https://github.com/astral-sh/uv). Follow the instructions below to set up your environment.

### Using uv

1. **Install uv (if not already installed):**

   You can install uv globally using pip:

   ```bash
   pip install uv
   ```

   Or follow the installation instructions on the [uv GitHub page](https://github.com/astral-sh/uv).

2. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/StegoHelix.git
   cd StegoHelix
   ```

3. **Sync Dependencies:**

   The project configuration is in the `pyproject.toml` file. To install all dependencies, run:

   ```bash
   uv sync
   ```

<!-- 4. **Activate the Environment (Optional):**

   If you use uv’s built-in virtual environment support, run:

   ```bash
   uv shell
   ```
 -->
### Alternative: Installing with pip

If you prefer not to use uv, you can install dependencies manually. First, create and activate a virtual environment, then install the required packages:

```bash
python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install .
```

---

## Usage

### Running the Application

After installing dependencies with uv (or pip), start the Streamlit app:

```bash
uv run streamlit run app.py
```

Or, if you’re not using uv’s runner:

```bash
streamlit run app.py
```

This will open a web interface in your browser where you can:

- **Encode a Message:**  
  Upload a cover image (preferably PNG), enter your secret message and encryption key, then download the protected image.

- **Decode a Message:**  
  Upload the protected PNG image and enter the decryption key to reveal the hidden message.

### How It Works

#### Encoding Process

1. **Encryption:**  
   - The secret message is encoded into bytes.
   - A random 16-byte salt and 12-byte nonce are generated.
   - A secure 32-byte key is derived from the password using Argon2.
   - ChaCha20-Poly1305 encrypts the message, producing ciphertext and an authentication tag.

2. **Payload Construction:**  
   - A header (4 bytes) representing the payload length is prepended to the payload.
   - The final payload is:  
     `[4-byte header] + [salt (16) + nonce (12) + tag (16) + ciphertext]`

3. **Embedding:**  
   - The payload is converted to a binary bitstream (8 bits per byte).
   - This bitstream is embedded into the LSBs of the cover image pixels.
   - The output image is saved as a PNG to ensure lossless compression.

#### Decoding Process

1. **Extraction:**  
   - The LSBs of the image are read to reconstruct the embedded bitstream.
   - The first 32 bits (header) determine the payload length.

2. **Parsing & Decryption:**  
   - The payload is parsed into salt, nonce, tag, and ciphertext.
   - A key is derived using the provided password.
   - Decryption is attempted; if it fails (e.g., due to an incorrect password), a clear error message is returned.

---

## Dependencies

The project’s dependencies are managed in the `pyproject.toml` file by uv. Key libraries include:

- **Streamlit:** For building the interactive web UI.
- **opencv-python-headless:** For image processing.
- **NumPy:** For numerical and array operations.
- **PyCryptodome:** For encryption (ChaCha20-Poly1305).
- **argon2-cffi:** For secure password-based key derivation.

<!-- Example `[tool.uv.dependencies]` section from `pyproject.toml`:

```toml
[tool.uv.dependencies]
python = ">=3.8"
streamlit = ">=1.28"
opencv-python-headless = ">=4.7"
numpy = ">=1.24"
pycryptodome = ">=3.20"
argon2-cffi = ">=21.3"
```
-->
---

## Contributing

Contributions are highly welcome! To contribute:

1. Fork the repository.
2. Create a new branch:

   ```bash
   git checkout -b feature/your-feature
   ```

3. Commit your changes with clear messages.
4. Push to your fork and open a pull request describing your changes.

---

## License

This project is licensed under the [MIT License](LICENSE).

---

## Disclaimer

StegoHelix is provided for educational and research purposes only. Use it responsibly and ensure you have authorization for any images you modify. The authors are not responsible for any misuse of this software.

---

## Acknowledgments

- **Inspiration:**  
  Inspired by numerous open source steganography and cryptography projects.
  
- **Tools & Libraries:**  
  Thanks to the developers of Streamlit, OpenCV, NumPy, PyCryptodome, and Argon2-CFFI for their exceptional libraries.

- **uv:**  
  Special thanks to the [astral-sh/uv](https://github.com/astral-sh/uv) team for their modern dependency management tool.
