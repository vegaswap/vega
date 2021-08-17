// SPDX-License-Identifier: MIT
pragma solidity ^0.8.5;

import "./VegaToken.sol";
import "./Ownable.sol";
import "./VestingBucket.sol";
import "./VestingConstants.sol";

// VegaMaster is the main token handler
// master distributes tokens to buckets
// bucket allocation is defined in VestingConstants
contract VegaMaster is Ownable {
    VegaToken public vega_token;
    address public vega_token_address;

    address[] public buckets;
    uint256 public bucket_num;
    uint256 private constant maxbuckets = 30;

    constructor(address _vega_token_address) {

        vega_token_address = _vega_token_address;
        vega_token = VegaToken(vega_token_address);

        bucket_num = 0;

        buckets = new address[](maxbuckets);
    }

    // add a vesting bucket from master and tranfer the entire amount to it
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
        vbucket.setRefOwner(owner());

        vbucket.setName(name);
        require(bucket_num < maxbuckets, "VegaMaster: bucket number too large");
        buckets[bucket_num] = address(vbucket);
        bucket_num += 1;
        transferToVested(address(vbucket), amount);
    }

    // transfer amount to vesting bucket from master
    function transferToVested(address recipient, uint256 amount) private {
        bool success = vega_token.transfer(address(recipient), amount);
        require(success, "VegaMaster: transfer failed");
    }

    function maxSupply() public view returns (uint256) {
        return vega_token.MAX_SUPPLY();
    }
}