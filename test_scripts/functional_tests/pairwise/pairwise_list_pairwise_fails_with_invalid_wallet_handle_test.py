"""
Created on Dec 26, 2017

@author: nhan.nguyen

Verify that user cannot list pairwises with invalid wallet handle.
"""

import json
import pytest
from indy import signus, pairwise
from indy.error import ErrorCode
from utilities import utils, common
from test_scripts.functional_tests.pairwise.pairwise_test_base \
    import PairwiseTestBase


class TestListPairwiseWithInvalidWallet(PairwiseTestBase):
    @pytest.mark.asyncio
    async def test(self):
        # 1. Create wallet.
        # 2. Open wallet.
        self.wallet_handle = await common.create_and_open_wallet_for_steps(
            self.steps, self.wallet_name, self.pool_name)

        # 3. Create and store 'my_did' by random seed.
        self.steps.add_step("Create and store 'my_did' by random seed")
        (my_did, _) = await utils.perform(self.steps,
                                          signus.create_and_store_my_did,
                                          self.wallet_handle, "{}")

        # 4. Create and "their_did".
        self.steps.add_step("Create 'their_did'")
        (their_did, _) = await utils.perform(self.steps,
                                             signus.create_and_store_my_did,
                                             self.wallet_handle, "{}")

        # 5. Store 'their_did'.
        self.steps.add_step("Store 'their_did")
        await utils.perform(self.steps, signus.store_their_did,
                            self.wallet_handle,
                            json.dumps({"did": their_did}))

        # 6. Create pairwise.
        self.steps.add_step("Create pairwise")
        await utils.perform(self.steps, pairwise.create_pairwise,
                            self.wallet_handle, their_did, my_did, None)

        # 7. Get list of pairwise with invalid wallet handle and
        # verify that list pairwise cannot be gotten.
        self.steps.add_step("Get list of pairwise with invalid wallet handle"
                            " and verify that list pairwise cannot be gotten")
        error_code = ErrorCode.WalletInvalidHandle
        await utils.perform_with_expected_code(self.steps,
                                               pairwise.list_pairwise,
                                               self.wallet_handle + 1,
                                               expected_code=error_code)
