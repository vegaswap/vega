// SPDX-License-Identifier: MIT
pragma solidity ^0.8.5;

import "./IERC20.sol";
import "./Ownable.sol";

// Initial Dex Offering (IDO) contract for launching ventures
// TODO only allow full USDT amounts
contract VegaIDO is Ownable {
    address public vegaTokenAddress;
    address public investTokenAddress;

    IERC20 public investToken;
    IERC20 public vegaToken;

    // single round
    // price tokens are sold at
    uint256 public askPriceMultiple;
    // total maximum amount invested
    uint256 public cap;
    // total amount invested
    uint256 invested;
    address[] whitelistAddresses;
    mapping(address => uint256) whitelistAmounts;

    uint256 private investTokenDecimals;
    // investors and how much they invest
    mapping(address => uint256) investors;

    //event Invested(address, uint) invest;

    constructor(
        address _launchTokenAddress,
        address _investTokenAddress,
        uint256 _investTokenDecimals,
        uint256 _askPriceMultiple,
        uint256 _cap
    ) {
        vegaTokenAddress = _launchTokenAddress;
        investTokenAddress = _investTokenAddress;
        investTokenDecimals = _investTokenDecimals;

        investToken = IERC20(investTokenAddress);
        vegaToken = IERC20(vegaTokenAddress);
        askPriceMultiple = _askPriceMultiple;
        cap = _cap;
    }

    //TODO review
    function addWhiteList(
        address[] memory addresses,
        uint256[] memory maxInvestAmounts
    ) external onlyOwner {
        require(
            addresses.length == maxInvestAmounts.length,
            "Addresses and amounts array lengths must match"
        );

        for (uint256 i = 0; i < addresses.length; i++) {
            whitelistAmounts[addresses[i]] = maxInvestAmounts[i];
        }
    }

    // participate in the funding event
    function invest(uint256 investAmount) external {
        require(
            invested + investAmount <= cap,
            "VegaIDO: Cap for current round reached"
        );
        //TODO
        require(
            investAmount != whitelistAmounts[msg.sender],
            "VegaIDO: Invest amount is not equal to the whitelist amount"
        );
        require(
            investToken.allowance(msg.sender, address(this)) >= investAmount,
            "VegaIDO: Please approve amount to invest"
        );
        require(
            investToken.balanceOf(msg.sender) >= investAmount,
            "VegaIDO: Insufficient balance to invest"
        );
        require(investors[msg.sender] == 0, "VegaIDO: Already invested");

        //price takes into account decimals
        uint256 buyTokenAmount = investAmount * askPriceMultiple;
        require(
            vegaToken.balanceOf(address(this)) >= buyTokenAmount,
            "VegaIDO: out of stock"
        );

        //safetransfer?
        // Transfer tokens from sender to this contract
        bool ts = investToken.transferFrom(
            msg.sender,
            address(this),
            investAmount
        );
        require(ts, "VegaIDO: transfer invest tokens failed");

        bool vts = vegaToken.transfer(msg.sender, buyTokenAmount);
        require(vts, "VegaIDO: transfer vega tokens failed");

        investors[msg.sender] += investAmount;
        invested += investAmount;

        //emit Invested(msg.sender, investAmount);
    }

    function withDrawTokens(uint256 amount) public onlyOwner {
        vegaToken.transfer(owner(), amount);
    }
}
