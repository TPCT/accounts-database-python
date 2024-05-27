import os

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec
import time
import based58
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


class PerfMetric:
    CURVE = ec.SECP256R1()
    ALPHABET = based58.Alphabet(
        b"MfoqFNBUnJ4l7DWedPvLs-YtVz8wK15rZc90Rm3EbiCSjhaApkxOHIy2XQ"
    )

    def __init__(self):
        self.private_key = None
        self.public_key = None
        self.shared_key: bytes
        self.session_key: bytes

    def gen_start_chat(self, prkey=None, pbkey=None, return_key=False):
        self.private_key = prkey or ec.generate_private_key(
            self.CURVE, default_backend()
        )
        self.public_key = pbkey or self.private_key.public_key()
        public_key_bytes = self.public_key.public_bytes(
            encoding=serialization.Encoding.X962,
            format=serialization.PublicFormat.UncompressedPoint,
        )

        timestamp = int(time.time()).to_bytes(8, byteorder="little", signed=True)
        public_key_bytes += timestamp
        token = based58.b58encode(public_key_bytes, self.ALPHABET)

        if return_key is False:
            return token.decode("utf8")
        else:
            return token.decode("utf8"), self.private_key, self.public_key

    def resolve_shared_key(self, other_party_public_hash):
        other_party_public_hash = bytes(other_party_public_hash, encoding="utf8")
        other_party_public_key = based58.b58decode(
            other_party_public_hash, self.ALPHABET
        )
        other_party_public_key_ec_point = ec.EllipticCurvePublicKey.from_encoded_point(
            self.CURVE, other_party_public_key
        )
        self.shared_key = self.private_key.exchange(
            ec.ECDH(), other_party_public_key_ec_point
        )

    @staticmethod
    def get_package(user_id):
        val = (
            str(user_id)
            + "."
            + str(int(time.time()))
            + "."
            + str(PackageHelper.get_data_bundle(int(time.time())))
        )
        return val

    def encrypt_message(self, message):
        message = bytes(message, encoding="utf8")
        iv = os.urandom(12)
        cipher = Cipher(
            algorithms.AES(self.shared_key), modes.GCM(iv), backend=default_backend()
        )
        encryptor = cipher.encryptor()

        ciphertext = encryptor.update(message)
        ciphertext += encryptor.finalize()
        tag = encryptor.tag
        full_data = iv + ciphertext + tag
        return (based58.b58encode(full_data, self.ALPHABET)).decode("utf8")

    def get_journey_token(self, user_id):
        package = self.get_package(user_id)
        return self.encrypt_message(package)


class PackageHelper:
    class Lehmer:
        MULTIPLIER = 75
        MODULUS = 65537
        MASK = 0xFFFFFFFF

        @classmethod
        def seed(cls, seed):
            cls.state = seed & cls.MASK

        @classmethod
        def next(cls):
            cls.state = cls.MULTIPLIER * cls.state % cls.MODULUS
            return cls.state

    @staticmethod
    def get_data_bundle(timestamp):
        dn = timestamp // 86400
        v4 = timestamp % 86400 // 5400
        dp = v4 % 16
        PackageHelper.Lehmer.seed(dn)
        n28 = PackageHelper.Lehmer.next() % 28
        i = 28
        a = []
        for _ in range(4):
            n28 = (i + PackageHelper.Lehmer.next() + n28) % 28
            sk = LifeClient.sk(n28)
            a.append(sk)
            i -= 1
        return PackageHelper.compute_hash(dp, a, dn)

    @staticmethod
    def compute_hash(dp, a, dn):
        if dp == 0:
            v4 = PackageHelper.xor13(a[1], a[2], a[3], a[0])
        elif dp == 1:
            v4 = PackageHelper.xor13(a[0], a[1], a[2], a[3])
        elif dp == 2:
            v4 = PackageHelper.xor23(a[1], a[0], a[2], a[3])
        elif dp == 3:
            v4 = PackageHelper.xor23(a[0], a[3], a[1], a[2])
        elif dp == 4:
            v4 = PackageHelper.xor13(a[2], a[3], a[0], a[1])
        elif dp == 5:
            v4 = (a[3] * a[2]) ^ (a[1] * a[0])
        elif dp == 6:
            v4 = PackageHelper.xor23(a[2], a[1], a[3], a[0])
        elif dp == 7:
            v4 = a[2] * a[0] + a[3] * a[1]
        elif dp == 8:
            v4 = PackageHelper.xor13(a[3], a[0], a[1], a[2])
        elif dp == 9:
            v4 = PackageHelper.mask32(a[2] ^ (a[1] * a[0]) ^ a[3])
        elif dp == 10:
            v4 = PackageHelper.xor23(a[3], a[2], a[0], a[1])
        elif dp == 11:
            v4 = a[3] * a[0] + a[2] * a[1]
        elif dp == 12:
            v4 = (a[3] ^ a[2]) + (a[1] ^ a[0])
        elif dp == 13:
            v4 = PackageHelper.mask32(a[1] ^ a[0] ^ a[2] ^ a[3])
        elif dp == 14:
            v4 = a[1] + a[0] + a[2] + a[3]
        elif dp == 15:
            v4 = a[1] * a[0] + a[3] * a[2]
        else:
            raise ValueError("Invalid dp value")

        return PackageHelper.mask32((dn << dp) ^ (8 * (v4 ^ dn)))

    @staticmethod
    def mask32(x):
        return x & 0xFFFFFFFF

    @staticmethod
    def xor1(v4, v5, v6):
        return PackageHelper.mask32(v4 ^ (8 * v5) ^ (32 * v6))

    @staticmethod
    def xor2(v8, v9, vA):
        return PackageHelper.mask32((v8 >> 2) ^ (v9 >> 1) ^ (vA >> 3))

    @staticmethod
    def xor3(v4, v7):
        return PackageHelper.mask32(v4 ^ (v7 << 7))

    @staticmethod
    def xor13(v4, v5, v6, v7):
        return PackageHelper.xor3(PackageHelper.xor1(v4, v5, v6), v7)

    @staticmethod
    def xor23(v8, v9, vA, v7):
        return PackageHelper.xor3(PackageHelper.xor2(v8, v9, vA), v7)


class LifeClient:
    # Probably hashes of the game source files
    # 1.091.01
    SK = {
            0: 0x1C421F9C, # ActorController::sk
            1: 0x966DB328, # PetkinManager::sk
            2: 0xC9E6D75A, # AnimationStore::sk
            3: 0x49405835, # ActionController::sk
            4: 0x4F2C7E65, # CameraCollision::sk
            5: 0x16889BFB, # InteractionHighlightSystem::sk
            6: 0xFA75C029, # NavTarget::sk
            7: 0xBBBF5F16, # EventLog::sk
            8: 0x1E51324D, # FeatureVersions::sk
            9: 0x8363C262, # ItemInteraction::sk
           10: 0x247F99BE, # InteractionManager::sk
           11: 0x66106E0C, # Main::sk
           12: 0xFBE0A88D, # MysteryReward::sk
           13: 0x5ACABDCD, # CategoryItem::sk
           14: 0x225D0F28, # State::ShopMaster::sk
           15: 0xAE5FCF61, # ApplicationBackHandler::sk
           16: 0xEB9D4F72, # ObjectDestroy::sk
           17: 0x0C721B63, # TweenVelocity::sk
           18: 0xCA667AAB, # WrapitemScript::sk
           19: 0x7C7D07EA, # CameraSystem2::CameraAnchor::sk
           20: 0x55C416C2, # Avkn::Smartfox::Networking::NetActorSystem::sk
           21: 0x08FB7FF9, # Avkn::Graphics::ImageEffects::sk
           22: 0xD58DE336, # Lockwood::EquipmentManager::sk
           23: 0xFDD73279, # Lockwood::LoadingScreenManager::sk
           24: 0xFC578724, # Lockwood::GameObjectExt::sk
           25: 0xBBB9C757, # Lockwood::Photo::PhotoServiceManager::sk
           26: 0x37C44F17, # LKWD::Chat::LifeChatSystem::sk
           27: 0x4896B7F1, # LKWD::UI::Panels::GenericPanelSettings::sk
        }

    @staticmethod
    def sk(i):
        return LifeClient.SK[i % len(LifeClient.SK)]
    