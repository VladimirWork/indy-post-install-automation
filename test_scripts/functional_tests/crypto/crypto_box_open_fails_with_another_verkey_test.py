"""
Created on Dec 28, 2017

@author: khoi.ngo

Verify that an encrypted message cannot be decrypted by other verkey in wallet.
"""

import pytest
from indy import crypto
from utilities import common, utils
from test_scripts.functional_tests.crypto.crypto_test_base \
    import CryptoTestBase


class TestOpenCryptoBoxWithAnotherVerkey(CryptoTestBase):
    @pytest.mark.asyncio
    async def test(self):
        # 1. Create wallet.
        # 2. Open wallet.
        self.wallet_handle = await common.create_and_open_wallet_for_steps(
            self.steps, self.wallet_name, self.pool_name)

        # 3. Create the first verkey with empty json.
        self.steps.add_step("Create the first key")
        first_key = await utils.perform(self.steps, crypto.create_key,
                                        self.wallet_handle, "{}")

        # 4. Create the second verkey with empty json.
        self.steps.add_step("Create the second key")
        second_key = await utils.perform(self.steps, crypto.create_key,
                                         self.wallet_handle, "{}")

        # 5. Create the another verkey with empty json.
        self.steps.add_step("Create the another key")
        another_key = await utils.perform(self.steps, crypto.create_key,
                                          self.wallet_handle, "{}")
        # 6. Create a crypto box".
        self.steps.add_step("Create a crypto box")
        msg = "Test crypto".encode("UTF-8")
        encrypted_msg, nonce = await utils.perform(
                                                self.steps, crypto.crypto_box,
                                                self.wallet_handle, first_key,
                                                second_key, msg)

        # 7. Open crypto box with another verkey. Expected error = 113
        self.steps.add_step("Open a crypto box with another verkey")
        await utils.perform_with_expected_code(
                                         self.steps, crypto.crypto_box_open,
                                         self.wallet_handle, first_key,
                                         another_key, encrypted_msg, nonce,
                                         expected_code=113)
