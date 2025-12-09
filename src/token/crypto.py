#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
cryptography库实战代码脚本
包含：Fernet对称加密、RSA非对称加密、AES-CBC加密、自签名证书生成
运行环境：Python 3.7+，cryptography 40.0.0+
"""

import os
import datetime
from cryptography import x509
from cryptography.fernet import Fernet, InvalidToken
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.padding import PKCS7  # 规范的PKCS7填充


def fernet_encryption_demo():
    """Fernet高级对称加密示例（开箱即用，自动处理IV和签名）"""
    print("=== Fernet对称加密示例 ===")
    # 生成并保存密钥
    key = Fernet.generate_key()
    with open("cryptions/fernet_key.key", "wb") as f:
        f.write(key)
    print(f"生成的密钥：{key.decode()}")

    # 加载密钥并初始化加密器
    with open("cryptions/fernet_key.key", "rb") as f:
        loaded_key = f.read()
    fernet = Fernet(loaded_key)

    # 加密数据
    plaintext = b"Hello, cryptography! - Fernet Demo"
    ciphertext = fernet.encrypt(plaintext)
    print(f"加密后数据：{ciphertext}")

    # 解密数据
    decrypted_text = fernet.decrypt(ciphertext)
    print(f"解密后数据：{decrypted_text.decode('utf-8')}")

    # 过期时间验证示例
    print("\n=== Fernet数据过期验证 ===")
    ciphertext_exp = fernet.encrypt_at_time(plaintext, current_time=100)
    try:
        # 尝试解密10秒前加密的数据（ttl=10表示有效期10秒）
        fernet.decrypt(ciphertext_exp, ttl=10)
        print("数据未过期，解密成功")
    except InvalidToken:
        print("数据已过期，解密失败")
    print("-" * 50)


def rsa_asymmetric_encryption_demo():
    """RSA非对称加密与解密示例"""
    print("=== RSA非对称加密示例 ===")
    # 生成RSA密钥对（2048位，推荐生产环境用4096位）
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    public_key = private_key.public_key()

    # 保存密钥对到文件
    # 保存私钥（PEM格式，加密保护）
    with open("cryptions/rsa_private_key.pem", "wb") as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.BestAvailableEncryption(
                b"password123")
        ))
    # 保存公钥
    with open("cryptions/rsa_public_key.pem", "wb") as f:
        f.write(public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))

    # 公钥加密
    plaintext = b"Hello, cryptography! - RSA Demo"
    ciphertext = public_key.encrypt(
        plaintext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    print(f"加密后数据：{ciphertext.hex()}")

    # 私钥解密
    decrypted_text = private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    print(f"解密后数据：{decrypted_text.decode('utf-8')}")
    print("-" * 50)


def aes_cbc_encryption_demo():
    """AES-CBC模式对称加密示例（使用PKCS7规范填充）"""
    print("=== AES-CBC对称加密示例 ===")
    # 生成AES-256密钥（32字节）和CBC初始化向量（16字节，必须随机）
    key = os.urandom(32)
    iv = os.urandom(16)
    print(f"生成的AES密钥（16进制）：{key.hex()}")
    print(f"生成的IV（16进制）：{iv.hex()}")

    # 初始化加密器
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    padder = PKCS7(128).padder()  # AES块大小为128位（16字节）

    # 加密数据（先填充再加密）
    plaintext = b"Hello, cryptography! - AES-CBC Demo"
    padded_data = padder.update(plaintext) + padder.finalize()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    print(f"加密后数据（16进制）：{ciphertext.hex()}")

    # 初始化解密器
    decryptor = cipher.decryptor()
    unpadder = PKCS7(128).unpadder()

    # 解密数据（先解密再去填充）
    decrypted_padded = decryptor.update(ciphertext) + decryptor.finalize()
    decrypted_text = unpadder.update(decrypted_padded) + unpadder.finalize()
    print(f"解密后数据：{decrypted_text.decode('utf-8')}")
    print("-" * 50)


def generate_self_signed_cert():
    """生成自签名X.509证书（用于测试/内部系统SSL/TLS）"""
    print("=== 生成自签名X.509证书 ===")
    # 生成RSA私钥
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )

    # 证书主体与颁发者信息（自签名证书两者相同）
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, u"CN"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"Beijing"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, u"Beijing"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"Test Org"),
        x509.NameAttribute(NameOID.COMMON_NAME, u"test.example.com"),
    ])

    # 构建证书
    cert_builder = x509.CertificateBuilder()
    cert = cert_builder.subject_name(subject)\
        .issuer_name(issuer)\
        .public_key(private_key.public_key())\
        .serial_number(x509.random_serial_number())\
        .not_valid_before(datetime.datetime.now())\
        .not_valid_after(datetime.datetime.now() + datetime.timedelta(days=365))\
        .add_extension(
            x509.SubjectAlternativeName([x509.DNSName(u"test.example.com")]),
            critical=False
    )\
        .sign(private_key, hashes.SHA256())

    # 保存证书和私钥
    with open("cryptions/self_signed_cert.pem", "wb") as f:
        f.write(cert.public_bytes(serialization.Encoding.PEM))
    with open("cryptions/cert_private_key.pem", "wb") as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ))
    print("自签名证书已保存为：self_signed_cert.pem")
    print("证书私钥已保存为：cert_private_key.pem")
    print("-" * 50)


if __name__ == "__main__":
    # 依次运行所有示例
    try:
        fernet_encryption_demo()
        rsa_asymmetric_encryption_demo()
        aes_cbc_encryption_demo()
        generate_self_signed_cert()
        print("所有示例运行完成！生成的文件：fernet_key.key、rsa_*.pem、self_signed_cert.pem等")
    except Exception as e:
        print(f"运行出错：{e}")
        print("请确保已安装cryptography库：pip install cryptography")
