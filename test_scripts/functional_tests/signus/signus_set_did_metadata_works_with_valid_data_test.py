"""
Created on Dec 21, 2017

@author: nhan.nguyen

Verify that user can set metadata for a did.
"""

import pytest
from indy import signus
from utilities import common, utils
from test_scripts.functional_tests.signus.signus_test_base \
    import SignusTestBase


class TestSetMetadataForDidInWallet(SignusTestBase):
    @pytest.mark.asyncio
    async def test(self):
        # 1. Create wallet.
        # 2. Open wallet.
        self.wallet_handle = await \
            common.create_and_open_wallet_for_steps(self.steps,
                                                    self.wallet_name,
                                                    self.pool_name)

        # 3. Create did and verkey with empty json.
        self.steps.add_step("Create did and verkey with empty json")
        (my_did, _) = await \
            utils.perform(self.steps, signus.create_and_store_my_did,
                          self.wallet_handle, "{}")

        # 4. Set metadata for 'my_did' and verify that
        # there is no exception raised
        self.steps.add_step("Set metadata for 'my_did' and verify that "
                            "there is no exception raised")
        metadata = "Test signus"
        await utils.perform(self.steps, signus.set_did_metadata,
                            self.wallet_handle, my_did, metadata,
                            ignore_exception=False)

        # 5. Get metadata of 'my_did'.
        self.steps.add_step("Get metadata of 'my_did'")
        returned_metadata = await utils.perform(self.steps,
                                                signus.get_did_metadata,
                                                self.wallet_handle, my_did)

        # 6. Check returned metadata.
        self.steps.add_step("Check returned metadata")
        error_msg = "Returned metadata mismatches with original metadata"
        utils.check(self.steps, error_message=error_msg,
                    condition=lambda: returned_metadata == metadata)
