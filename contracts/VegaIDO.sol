// SPDX-License-Identifier: MIT
pragma solidity ^0.8.5;

import "./IERC20.sol";
import "./Ownable.sol";
// import "./Util.sol";
import "./NRT.sol";

// Initial Dex Offering (IDO) contract for launching ventures
// assumes that decimals are 18 for vega and investToken
// only tracks invest amount
// state 1: 50$ x 1000 tickets
// state 2: 800 are filled (200 left, 200x 50$)
// state 3: set cap to 200$ (5x guys invest more)
// state 4: FCFS

//TODO: NRT
contract VegaIDO is Ownable {
    
    address public investTokenAddress;
    IERC20 public investToken;
    NRT public nrt;

    // single round
    // total maximum amount invested
    uint256 public totalcap;
    uint256 public askpriceMultiple;
    // total amount invested
    uint256 public totalInvested;
    address[] public whitelistAddresses;
    uint256 public capPerAccount;
    uint256 startTime;
    uint256 endTime;


    //mapping(address => uint256) whitelistAmounts;

    // investors and how much they invest
    mapping(address => uint256) investedAmounts;

    event InvestEvent(address, uint256);

    constructor(address _investTokenAddress, uint256 _askpriceMultiple, uint256 _totalcap, uint256 _capPerAccount, uint256 _startTime, uint256 _endTime) {
        require(_investTokenAddress != address(0), "_investTokenAddress: zero address");
        investTokenAddress = _investTokenAddress;

        investToken = IERC20(investTokenAddress);
        totalcap = _totalcap;
        capPerAccount = _capPerAccount;
        askpriceMultiple = _askpriceMultiple;
        startTime = _startTime;
        endTime = _endTime;
        // nrt = new NRT("VegaNRT");
    }

    // function string memory reason)
    //     private
    //     pure
    //     returns (string memory)
    // {
    //     return Util."VegaIDO", reason);
    // }

    // function string memory reason, string memory data)
    //     private
    //     pure
    //     returns (string memory)
    // {
    //     return Util."VegaIDO", reason, data);
    // }

    //in case not enough filled
    function setCapPerAccount (uint256 _capPerAccount) public onlyOwner {
        require(_capPerAccount > capPerAccount,"should be bigger than before");
        capPerAccount = _capPerAccount;
    }

    // collected from external
    function addWhiteList(
        address[] memory addresses
    ) external onlyOwner {
        for (uint256 i = 0; i < addresses.length; i++) {
            address w = addresses[i];
            whitelistAddresses.push(w);
        }
    }

    function inWhitelist(address f) public view returns (bool) {
        for (uint256 i = 0; i < whitelistAddresses.length; i++) {
            address w = whitelistAddresses[i];
            if (w == f) {
                return true;
            }
        }
        return false;
    }

    // participate in the funding event
    function invest(uint256 investAmount) external {
        require(block.timestamp > startTime, "IDO not started");
        require(block.timestamp < endTime, "IDO has ended");
        require(inWhitelist(msg.sender), "not whitelisted");
        require(
            totalInvested + investAmount <= totalcap,
                "totalcap for current round reached"
                // Util.uintToString(totalInvested + investAmount
        );

        //will be zero if first time investor
        uint256 investedAmount = investedAmounts[msg.sender];
        
        require(investedAmount + investAmount <= capPerAccount, "more than cap invested");
        
        require(
            investToken.allowance(msg.sender, address(this)) >= investAmount,
            "Please approve amount to invest"
        );
        require(
            investToken.balanceOf(msg.sender) >= investAmount,
            "Insufficient balance to invest"
        );
        
        // Transfer tokens from sender to this contract
        bool ts = investToken.transferFrom(
            msg.sender,
            address(this),
            investAmount
        );
        require(ts, "transfer invest tokens failed");

        investedAmounts[msg.sender] += investAmount;
        totalInvested += investAmount;

        uint256 nrtReceived = investAmount * askpriceMultiple;
        //TODO check decimals
        nrt.issue(msg.sender, nrtReceived);

        emit InvestEvent(msg.sender, investAmount);
    }

    // withdraw the funding amount
    function withDrawFunding() public onlyOwner {
        uint256 balance = investToken.balanceOf(address(this));
        investToken.transfer(owner(), balance);
    }
}