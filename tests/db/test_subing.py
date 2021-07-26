# -*- encoding: utf-8 -*-
"""
tests.app.apping module

"""
import os

import pytest

import pysodium

from keri.core import coring, eventing
from keri.db import dbing, subing
from keri.app import keeping
from keri.help import helping


def test_suber():
    """
    Test Suber LMDBer sub database class
    """

    with dbing.openLMDB() as db:
        assert isinstance(db, dbing.LMDBer)
        assert db.name == "test"
        assert db.opened

        sdb = subing.Suber(db=db, subkey='bags.')
        assert isinstance(sdb, subing.Suber)

        sue = "Hello sailer!"

        keys = ("test_key", "0001")
        sdb.put(keys=keys, val=sue)
        actual = sdb.get(keys=keys)
        assert actual == sue

        sdb.rem(keys)
        actual = sdb.get(keys=keys)
        assert actual is None

        sdb.put(keys=keys, val=sue)
        actual = sdb.get(keys=keys)
        assert actual == sue

        kip = "Hey gorgeous!"
        result = sdb.put(keys=keys, val=kip)
        assert not result
        actual = sdb.get(keys=keys)
        assert actual == sue

        result = sdb.pin(keys=keys, val=kip)
        assert result
        actual = sdb.get(keys=keys)
        assert actual == kip

        # test with keys as string not tuple
        keys = "keystr"

        bob = "Shove off!"

        sdb.put(keys=keys, val=bob)
        actual = sdb.get(keys=keys)
        assert actual == bob

        sdb.rem(keys)

        actual = sdb.get(keys=keys)
        assert actual is None


        liz =  "May live is insane."
        keys = ("test_key", "0002")

        sdb.put(keys=keys, val=liz)
        actual = sdb.get(("not_found", "0002"))
        assert actual is None

        w = "Blue dog"
        x = "Green tree"
        y = "Red apple"
        z = "White snow"

        sdb = subing.Suber(db=db, subkey='pugs.')
        assert isinstance(sdb, subing.Suber)

        sdb.put(keys=("a","1"), val=w)
        sdb.put(keys=("a","2"), val=x)
        sdb.put(keys=("a","3"), val=y)
        sdb.put(keys=("a","4"), val=z)

        items = [(keys, data) for keys, data in sdb.getItemIter()]
        assert items == [(('a', '1'), w),
                        (('a', '2'), x),
                        (('a', '3'), y),
                        (('a', '4'), z)]

    assert not os.path.exists(db.path)
    assert not db.opened


def test_serder_suber():
    """
    Test SerderSuber LMDBer sub database class
    """

    with dbing.openLMDB() as db:
        assert isinstance(db, dbing.LMDBer)
        assert db.name == "test"
        assert db.opened

        sdb = subing.SerderSuber(db=db, subkey='bags.')
        assert isinstance(sdb, subing.SerderSuber)

        pre = "BWzwEHHzq7K0gzQPYGGwTmuupUhPx5_yZ-Wk1x4ejhcc"
        srdr0 = eventing.incept(keys=[pre])

        keys = (pre, srdr0.dig)
        sdb.put(keys=keys, val=srdr0)
        actual = sdb.get(keys=keys)
        assert isinstance(actual, coring.Serder)
        assert actual.dig == srdr0.dig

        sdb.rem(keys)
        actual = sdb.get(keys=keys)
        assert actual is None

        sdb.put(keys=keys, val=srdr0)
        actual = sdb.get(keys=keys)
        assert isinstance(actual, coring.Serder)
        assert actual.dig == srdr0.dig

        srdr1 = eventing.rotate(pre=pre, keys=[pre], dig=srdr0.dig)
        result = sdb.put(keys=keys, val=srdr1)
        assert not result
        assert isinstance(actual, coring.Serder)
        assert actual.dig == srdr0.dig

        result = sdb.pin(keys=keys, val=srdr1)
        assert result
        actual = sdb.get(keys=keys)
        assert isinstance(actual, coring.Serder)
        assert actual.dig == srdr1.dig

        # test with keys as string not tuple
        keys = "{}.{}".format(pre, srdr1.dig)

        sdb.put(keys=keys, val=srdr1)
        actual = sdb.get(keys=keys)
        assert isinstance(actual, coring.Serder)
        assert actual.dig == srdr1.dig

        sdb.rem(keys)
        actual = sdb.get(keys=keys)
        assert actual is None

        # test missing entry at keys
        badkey = "badkey"
        actual = sdb.get(badkey)
        assert actual is None

        # test iteritems
        sdb = subing.SerderSuber(db=db, subkey='pugs.')
        assert isinstance(sdb, subing.SerderSuber)
        sdb.put(keys=("a","1"), val=srdr0)
        sdb.put(keys=("a","2"), val=srdr1)

        items = [(keys, srdr.dig) for keys, srdr in sdb.getItemIter()]
        assert items == [(('a', '1'), srdr0.dig),
                         (('a', '2'), srdr1.dig)]

    assert not os.path.exists(db.path)
    assert not db.opened



def test_matter_suber():
    """
    Test MatterSuber LMDBer sub database class
    """

    with dbing.openLMDB() as db:
        assert isinstance(db, dbing.LMDBer)
        assert db.name == "test"
        assert db.opened

        sdb = subing.MatterSuber(db=db, subkey='bags.')  # default klas is Matter
        assert isinstance(sdb, subing.MatterSuber)
        assert issubclass(sdb.klas, coring.Matter)

        pre0 = "BWzwEHHzq7K0gzQPYGGwTmuupUhPx5_yZ-Wk1x4ejhcc"
        val0 = coring.Matter(qb64=pre0)

        keys = ("alpha", "dog")
        sdb.put(keys=keys, val=val0)
        actual = sdb.get(keys=keys)
        assert isinstance(actual, coring.Matter)
        assert actual.qb64 == val0.qb64

        sdb.rem(keys)
        actual = sdb.get(keys=keys)
        assert actual is None

        sdb.put(keys=keys, val=val0)
        actual = sdb.get(keys=keys)
        assert isinstance(actual, coring.Matter)
        assert actual.qb64 == val0.qb64

        pre1 = "BHHzqZWzwE-Wk7K0gzQPYGGwTmuupUhPx5_y1x4ejhcc"
        val1 = coring.Matter(qb64=pre1)
        result = sdb.put(keys=keys, val=val1)
        assert not result
        assert isinstance(actual, coring.Matter)
        assert actual.qb64 == val0.qb64

        result = sdb.pin(keys=keys, val=val1)
        assert result
        actual = sdb.get(keys=keys)
        assert isinstance(actual, coring.Matter)
        assert actual.qb64 == val1.qb64

        # test with keys as string not tuple
        keys = "{}.{}".format("beta", "fish")

        sdb.put(keys=keys, val=val1)
        actual = sdb.get(keys=keys)
        assert isinstance(actual, coring.Matter)
        assert actual.qb64 == val1.qb64

        sdb.rem(keys)
        actual = sdb.get(keys=keys)
        assert actual is None

        # test missing entry at keys
        badkey = "badkey"
        actual = sdb.get(badkey)
        assert actual is None

        # test iteritems
        sdb = subing.MatterSuber(db=db, subkey='pugs.')
        assert isinstance(sdb, subing.MatterSuber)
        sdb.put(keys=("a","1"), val=val0)
        sdb.put(keys=("a","2"), val=val1)

        items = [(keys, srdr.qb64) for keys, srdr in sdb.getItemIter()]
        assert items == [(('a', '1'), val0.qb64),
                         (('a', '2'), val1.qb64)]

        #  Try other classs
        sdb = subing.MatterSuber(db=db, subkey='pigs.', klas=coring.Diger)
        assert isinstance(sdb, subing.MatterSuber)
        assert issubclass(sdb.klas, coring.Diger)

        dig0 = "EQPYGGwTmuupWzwEHHzq7K0gzUhPx5_yZ-Wk1x4ejhcc"
        val0 = coring.Diger(qb64=dig0)

        keys = ("alpha", "dog")
        sdb.put(keys=keys, val=val0)
        actual = sdb.get(keys=keys)
        assert isinstance(actual, coring.Diger)
        assert actual.qb64 == val0.qb64

        sdb.rem(keys)
        actual = sdb.get(keys=keys)
        assert actual is None

        sdb.put(keys=keys, val=val0)
        actual = sdb.get(keys=keys)
        assert isinstance(actual, coring.Diger)
        assert actual.qb64 == val0.qb64

        pre1 = "EHHzqZWzwE-Wk7K0gzQPYGGwTmuupUhPx5_y1x4ejhcc"
        val1 = coring.Matter(qb64=pre1)
        result = sdb.put(keys=keys, val=val1)
        assert not result
        assert isinstance(actual, coring.Diger)
        assert actual.qb64 == val0.qb64

        result = sdb.pin(keys=keys, val=val1)
        assert result
        actual = sdb.get(keys=keys)
        assert isinstance(actual, coring.Diger)
        assert actual.qb64 == val1.qb64

        # test iteritems
        sdb = subing.MatterSuber(db=db, subkey='figs.')
        assert isinstance(sdb, subing.MatterSuber)
        sdb.put(keys=("a","1"), val=val0)
        sdb.put(keys=("a","2"), val=val1)

        items = [(keys, srdr.qb64) for keys, srdr in sdb.getItemIter()]
        assert items == [(('a', '1'), val0.qb64),
                         (('a', '2'), val1.qb64)]



    assert not os.path.exists(db.path)
    assert not db.opened


def test_signer_suber():
    """
    Test SignerSuber LMDBer sub database class
    """

    with dbing.openLMDB() as db:
        assert isinstance(db, dbing.LMDBer)
        assert db.name == "test"
        assert db.opened

        sdb = subing.SignerSuber(db=db, subkey='bags.')  # default klas is Signer
        assert isinstance(sdb, subing.SignerSuber)
        assert issubclass(sdb.klas, coring.Signer)

        # preseed = pysodium.randombytes(pysodium.crypto_sign_SEEDBYTES)
        seed0 = (b'\x18;0\xc4\x0f*vF\xfa\xe3\xa2Eee\x1f\x96o\xce)G\x85\xe3X\x86\xda\x04\xf0\xdc'
                           b'\xde\x06\xc0+')
        signer0 = coring.Signer(raw=seed0, code=coring.MtrDex.Ed25519_Seed)
        assert signer0.verfer.code == coring.MtrDex.Ed25519
        assert signer0.verfer.transferable  # default
        assert signer0.qb64b == b'AGDswxA8qdkb646JFZWUflm_OKUeF41iG2gTw3N4GwCs'
        assert signer0.verfer.qb64b == b'DhixhZjC1Wj2bLR1QdADT79kS2zwHld29ekca0elxHiE'

        # preseed = pysodium.randombytes(pysodium.crypto_sign_SEEDBYTES)
        seed1 = (b'`\x05\x93\xb9\x9b6\x1e\xe0\xd7\x98^\x94\xc8Et\xf2\xc4\xcd\x94\x18'
                 b'\xc6\xae\xb9\xb6m\x12\xc4\x80\x03\x07\xfc\xf7')

        signer1 = coring.Signer(raw=seed1, code=coring.MtrDex.Ed25519_Seed)
        assert signer1.verfer.code == coring.MtrDex.Ed25519
        assert signer1.verfer.transferable  # default
        assert signer1.qb64b == b'AYAWTuZs2HuDXmF6UyEV08sTNlBjGrrm2bRLEgAMH_Pc'
        assert signer1.verfer.qb64b == b'Dgekf6SB_agwx96mVSZI6PTC09j4Sp8qUbgKglN8uLjY'

        keys = (signer0.verfer.qb64, )  # must be verfer as key to get transferable
        sdb.put(keys=keys, val=signer0)
        actual = sdb.get(keys=keys)
        assert isinstance(actual, coring.Signer)
        assert actual.qb64 == signer0.qb64
        assert actual.verfer.qb64 == signer0.verfer.qb64

        sdb.rem(keys)
        actual = sdb.get(keys=keys)
        assert actual is None

        sdb.put(keys=keys, val=signer0)
        actual = sdb.get(keys=keys)
        assert isinstance(actual, coring.Signer)
        assert actual.qb64 == signer0.qb64
        assert actual.verfer.qb64 == signer0.verfer.qb64

        #  try put different val when already put
        result = sdb.put(keys=keys, val=signer1)
        assert not result
        assert isinstance(actual, coring.Signer)
        assert actual.qb64 == signer0.qb64
        assert actual.verfer.qb64 == signer0.verfer.qb64

        #  now overwrite with pin. Key is wrong but transferable property is
        #  the same so that is all that matters to get back signer
        result = sdb.pin(keys=keys, val=signer1)
        assert result
        actual = sdb.get(keys=keys)
        assert isinstance(actual, coring.Signer)
        assert actual.qb64 == signer1.qb64
        assert actual.verfer.qb64 == signer1.verfer.qb64

        # test with keys as string not tuple
        keys = signer0.verfer.qb64

        sdb.pin(keys=keys, val=signer0)
        actual = sdb.get(keys=keys)
        assert isinstance(actual, coring.Signer)
        assert actual.qb64 == signer0.qb64
        assert actual.verfer.qb64 == signer0.verfer.qb64

        sdb.rem(keys)
        assert not  sdb.get(keys=keys)

        # test missing entry at keys
        badkey = b'D1QdADT79kS2zwHld29hixhZjC1Wj2bLRekca0elxHiE'
        assert not  sdb.get(badkey)

        # test iteritems
        sdb = subing.SignerSuber(db=db, subkey='pugs.')
        assert isinstance(sdb, subing.SignerSuber)
        assert sdb.put(keys=signer0.verfer.qb64b, val=signer0)
        assert sdb.put(keys=signer1.verfer.qb64b, val=signer1)

        items = [(keys, srdr.qb64) for keys, srdr in sdb.getItemIter()]
        assert items == [((signer1.verfer.qb64, ), signer1.qb64),
                         ((signer0.verfer.qb64, ), signer0.qb64)]


    assert not os.path.exists(db.path)
    assert not db.opened



def test_crypt_signer_suber():
    """
    test Manager class with aeid
    """
    # preseed = pysodium.randombytes(pysodium.crypto_sign_SEEDBYTES)
    seed0 = (b'\x18;0\xc4\x0f*vF\xfa\xe3\xa2Eee\x1f\x96o\xce)G\x85\xe3X\x86\xda\x04\xf0\xdc'
                       b'\xde\x06\xc0+')
    signer0 = coring.Signer(raw=seed0, code=coring.MtrDex.Ed25519_Seed)
    assert signer0.verfer.code == coring.MtrDex.Ed25519
    assert signer0.verfer.transferable  # default
    assert signer0.qb64b == b'AGDswxA8qdkb646JFZWUflm_OKUeF41iG2gTw3N4GwCs'
    assert signer0.verfer.qb64b == b'DhixhZjC1Wj2bLR1QdADT79kS2zwHld29ekca0elxHiE'

    # preseed = pysodium.randombytes(pysodium.crypto_sign_SEEDBYTES)
    seed1 = (b'`\x05\x93\xb9\x9b6\x1e\xe0\xd7\x98^\x94\xc8Et\xf2\xc4\xcd\x94\x18'
             b'\xc6\xae\xb9\xb6m\x12\xc4\x80\x03\x07\xfc\xf7')

    signer1 = coring.Signer(raw=seed1, code=coring.MtrDex.Ed25519_Seed)
    assert signer1.verfer.code == coring.MtrDex.Ed25519
    assert signer1.verfer.transferable  # default
    assert signer1.qb64b == b'AYAWTuZs2HuDXmF6UyEV08sTNlBjGrrm2bRLEgAMH_Pc'
    assert signer1.verfer.qb64b == b'Dgekf6SB_agwx96mVSZI6PTC09j4Sp8qUbgKglN8uLjY'


    # rawsalt =pysodium.randombytes(pysodium.crypto_pwhash_SALTBYTES)
    rawsalt = b'0123456789abcdef'
    salter = coring.Salter(raw=rawsalt)
    salt = salter.qb64
    assert salt == '0AMDEyMzQ1Njc4OWFiY2RlZg'
    stem = "blue"

    # cryptseed0 = pysodium.randombytes(pysodium.crypto_sign_SEEDBYTES)
    cryptseed0 = b'h,#|\x8ap"\x12\xc43t2\xa6\xe1\x18\x19\xf0f2,y\xc4\xc21@\xf5@\x15.\xa2\x1a\xcf'
    cryptsigner0 = coring.Signer(raw=cryptseed0, code=coring.MtrDex.Ed25519_Seed,
                           transferable=False)
    seed0 = cryptsigner0.qb64
    aeid0 = cryptsigner0.verfer.qb64
    assert aeid0 == 'BJruYr3oXDGRTRN0XnhiqDeoENdRak6FD8y2vsTvvJkE'

    decrypter = coring.Decrypter(seed=seed0)
    encrypter = coring.Encrypter(verkey=aeid0)
    assert encrypter.verifySeed(seed=seed0)

    # cryptseed1 = pysodium.randombytes(pysodium.crypto_sign_SEEDBYTES)
    cryptseed1 = (b"\x89\xfe{\xd9'\xa7\xb3\x89#\x19\xbec\xee\xed\xc0\xf9\x97\xd0\x8f9\x1dyNI"
               b'I\x98\xbd\xa4\xf6\xfe\xbb\x03')
    cryptsigner1 = coring.Signer(raw=cryptseed1, code=coring.MtrDex.Ed25519_Seed,
                           transferable=False)


    with dbing.openLMDB() as db,  keeping.openKS() as ks:
        assert isinstance(db, dbing.LMDBer)
        assert db.name == "test"
        assert db.opened

        sdb = subing.CryptSignerSuber(db=db, subkey='bags.')  # default klas is Signer
        assert isinstance(sdb, subing.CryptSignerSuber)
        assert issubclass(sdb.klas, coring.Signer)

        # Test without encrypter or decrypter
        keys = (signer0.verfer.qb64, )  # must be verfer as key to get transferable
        sdb.put(keys=keys, val=signer0)
        actual = sdb.get(keys=keys)
        assert isinstance(actual, coring.Signer)
        assert actual.qb64 == signer0.qb64
        assert actual.verfer.qb64 == signer0.verfer.qb64

        sdb.rem(keys)
        actual = sdb.get(keys=keys)
        assert actual is None

        sdb.put(keys=keys, val=signer0)
        actual = sdb.get(keys=keys)
        assert isinstance(actual, coring.Signer)
        assert actual.qb64 == signer0.qb64
        assert actual.verfer.qb64 == signer0.verfer.qb64

        #  try put different val when already put
        result = sdb.put(keys=keys, val=signer1)
        assert not result
        assert isinstance(actual, coring.Signer)
        assert actual.qb64 == signer0.qb64
        assert actual.verfer.qb64 == signer0.verfer.qb64

        #  now overwrite with pin. Key is wrong but transferable property is
        #  the same so that is all that matters to get back signer
        result = sdb.pin(keys=keys, val=signer1)
        assert result
        actual = sdb.get(keys=keys)
        assert isinstance(actual, coring.Signer)
        assert actual.qb64 == signer1.qb64
        assert actual.verfer.qb64 == signer1.verfer.qb64

        # test with keys as string not tuple
        keys = signer0.verfer.qb64

        sdb.pin(keys=keys, val=signer0)
        actual = sdb.get(keys=keys)
        assert isinstance(actual, coring.Signer)
        assert actual.qb64 == signer0.qb64
        assert actual.verfer.qb64 == signer0.verfer.qb64

        sdb.rem(keys)
        assert not  sdb.get(keys=keys)

        # test missing entry at keys
        badkey = b'D1QdADT79kS2zwHld29hixhZjC1Wj2bLRekca0elxHiE'
        assert not  sdb.get(badkey)

        # test iteritems
        sdb = subing.CryptSignerSuber(db=db, subkey='pugs.')
        assert isinstance(sdb, subing.CryptSignerSuber)
        assert sdb.put(keys=signer0.verfer.qb64b, val=signer0)
        assert sdb.put(keys=signer1.verfer.qb64b, val=signer1)

        items = [(keys, sgnr.qb64) for keys, sgnr in sdb.getItemIter()]
        assert items == [((signer1.verfer.qb64, ), signer1.qb64),
                         ((signer0.verfer.qb64, ), signer0.qb64)]


        # now test with encrypter and decrypter
        encrypter0 = coring.Encrypter(verkey=cryptsigner0.verfer.qb64)
        decrypter0 = coring.Decrypter(seed=cryptsigner0.qb64b)

        # first pin with encrypter
        assert sdb.pin(keys=signer0.verfer.qb64b, val=signer0, encrypter=encrypter0)
        assert sdb.pin(keys=signer1.verfer.qb64b, val=signer1, encrypter=encrypter0)

        # now get
        actual0 = sdb.get(keys=signer0.verfer.qb64b, decrypter=decrypter0)
        assert isinstance(actual0, coring.Signer)
        assert actual0.qb64 == signer0.qb64
        assert actual0.verfer.qb64 == signer0.verfer.qb64

        actual1 = sdb.get(keys=signer1.verfer.qb64b, decrypter=decrypter0)
        assert isinstance(actual1, coring.Signer)
        assert actual1.qb64 == signer1.qb64
        assert actual1.verfer.qb64 == signer1.verfer.qb64

        # now get without decrypter
        with  pytest.raises(ValueError):
            actual0 = sdb.get(keys=signer0.verfer.qb64b)

        with  pytest.raises(ValueError):
            actual1 = sdb.get(keys=signer1.verfer.qb64b)

        # remove and test put
        sdb.rem(keys=signer0.verfer.qb64b)
        assert not  sdb.get(keys=signer0.verfer.qb64b)
        sdb.rem(keys=signer1.verfer.qb64b)
        assert not sdb.get(keys=signer1.verfer.qb64b)

        assert sdb.put(keys=signer0.verfer.qb64b, val=signer0, encrypter=encrypter0)
        assert sdb.put(keys=signer1.verfer.qb64b, val=signer1, encrypter=encrypter0)

        items = [(keys, sgnr.qb64) for keys, sgnr in sdb.getItemIter(decrypter=decrypter0)]
        assert items == [((signer1.verfer.qb64, ), signer1.qb64),
                             ((signer0.verfer.qb64, ), signer0.qb64)]


        # test re-encrypt
        encrypter1 = coring.Encrypter(verkey=cryptsigner1.verfer.qb64)
        decrypter1 = coring.Decrypter(seed=cryptsigner1.qb64b)
        for keys, sgnr in sdb.getItemIter(decrypter=decrypter0):
            sdb.pin(keys, sgnr, encrypter=encrypter1)

        items = [(keys, sgnr.qb64) for keys, sgnr in sdb.getItemIter(decrypter=decrypter1)]
        assert items == [((signer1.verfer.qb64, ), signer1.qb64),
                             ((signer0.verfer.qb64, ), signer0.qb64)]


        # now test with manager
        manager = keeping.Manager(ks=ks, seed=seed0, salt=salt, aeid=aeid0, )
        assert manager.ks.opened
        assert manager.inited
        assert manager._inits == {'aeid': 'BJruYr3oXDGRTRN0XnhiqDeoENdRak6FD8y2vsTvvJkE',
                                  'salt': '0AMDEyMzQ1Njc4OWFiY2RlZg'}
        assert manager.encrypter.qb64 == encrypter.qb64  #  aeid provided
        assert manager.decrypter.qb64 == decrypter.qb64  # aeid and seed provided
        assert manager.seed == seed0  # in memory only
        assert manager.aeid == aeid0  # on disk only
        assert manager.algo == keeping.Algos.salty
        assert manager.salt == salt  # encrypted on disk but property decrypts if seed
        assert manager.pidx == 0
        assert manager.tier == coring.Tiers.low
        saltCipher0 = coring.Cipher(qb64=manager.ks.gbls.get('salt'))
        assert saltCipher0.decrypt(seed=seed0).qb64 == salt


        manager.updateAeid(aeid=cryptsigner1.verfer.qb64, seed=cryptsigner1.qb64)
        assert manager.aeid == cryptsigner1.verfer.qb64 == 'BRw6sysb_uv81ZouXqHxQlqnAh9BYiSOsg9eQJmbZ8Uw'
        assert manager.salt == salt
        saltCipher1 = coring.Cipher(qb64=manager.ks.gbls.get('salt'))
        assert not saltCipher0.qb64 == saltCipher1.qb64  # old cipher different

    """End Test"""



if __name__ == "__main__":
    test_crypt_signer_suber()
