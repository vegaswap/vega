// SPDX-License-Identifier: MIT

pragma solidity ^0.8.5;

import "./VegaToken.sol";
import "./Ownable.sol";
import "./VestingBucket.sol";
import "./VestingConstants.sol";

// master distributes tokens to buckets
// main token handler
// bucket allocation is defined in VestingConstants
contract VegaMaster is Ownable {
    //using VestingConstants for *;

    VegaToken public vega_token;
    address public vega_token_address;

    //VestingConstants public vestingConstants;

    uint256 private _circSupply;

    //locked supply of vega
    uint256 private _lockedSupply;

    //uint256 public depositAmount;
    //uint256 public vestedAmount;

    address[] public buckets;
    uint256 public bucket_num;

    event Debug(string msg);

    constructor() {
        vega_token = new VegaToken();

        _lockedSupply = 0;
        _circSupply = 0;

        vega_token_address = address(vega_token);

        bucket_num = 0;

        buckets = new address[](20);
    }

    function addVestingBucket(
        uint256 cliffOffset,
        string memory name,
        uint256 periods,
        uint256 amount
    ) public onlyOwner {
        VestingBucket vbucket = new VestingBucket(
            vega_token_address,
            block.timestamp + cliffOffset,
            periods,
            amount
        );
        //refowner of vbucket is owner of master
        vbucket.setRefowner(owner());
        vbucket.setName(name);
        //require(bucket_num < num_buckets, "bucket num too large");
        buckets[bucket_num] = address(vbucket);
        bucket_num += 1;
        transferToVested(address(vbucket), amount);
        //return true
    }

    function transferToVested(address recipient, uint256 amount) private {
        bool success = vega_token.transfer(address(recipient), amount);
        require(success, "transfer failed");
        //_lockedSupply += amount;
    }

    // function circSupply() public view returns (uint256) {
    //     return _circSupply;
    // }

    // function lockedSupply() public view returns (uint256) {
    //     return _lockedSupply;
    // }

    function maxSupply() public view returns (uint256) {
        return vega_token.MAX_SUPPLY();
    }

    // function crossChainMint() public onlyOwner {}

    // function crossChainBurn() public onlyOwner {}

    // Call at cliffTime/periodTime to release tokens to tokenholders
    // @dev: we pay for the fee
    // TODO: multi call maybe
    // function release() external payable onlyOwner {
    //     VestingSchedule storage vestingSchedule;
    //     uint256 i = 0;
    //     uint256 newTotalWithdrawn = 0;
    //     for (i = 0; i < registeredAddresses.length; i++) {
    //         vestingSchedule = vestingSchedules[registeredAddresses[i]];
    //         newTotalWithdrawn = _release(vestingSchedule);
    //         vestingSchedule.withdrawnAmount = newTotalWithdrawn;
    //     }
    // }
}
