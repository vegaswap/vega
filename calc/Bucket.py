# @version ^0.2.15

# a vesting bucket
# a bucket is a wrapper over an account with access control
# vesting occurs linearly over time
# the owner deposits funds upfront and adds claims

# from vyper.interfaces import ERC20


# interface ClaimList:
#     def addresses(i: int -> address:
#         nonpayable

#     def amounts(i: int -> int:
#         nonpayable

#     def count() -> int:
#         nonpayable


# original deployer
# owner: address
# # name of the bucket
# name: String[15]
# vegaToken: address
# registerTime: int
days = 86400
default_period: int = 30 * days
# period: int
# cliffTime: int
# duration: int
# endTime: int
# totalAmount: int
# numPeriods: int
# initialized: bool
# openClaimAmount: int
# totalWithdrawnAmount: int
# totalClaimAmount: int
# claim_addresses: address[1000])
# claimCount: int


class Claim:
    def __init__(self, _claimAddress, _claimTotalAmount, _amountPeriod, _withdrawnAmount) -> None:
        self.laimAddress = _claimAddress
        self.claimTotalAmount = _claimTotalAmount
        self.amountPeriod = _amountPeriod
        self.withdrawnAmount = _withdrawnAmount
        self.isAdded = True


# claims: HashMap[address, Claim])


# event DepositOwner:
#     owner: address
#     amount: int


# event WithdrawOwner:
#     owner: address
#     amount: int


# event ClaimAdded:
#     claimAddress: address
#     claimTotalAmount: int


# event WithdrawClaim:
#     claimAddress: address
#     amount: int

# event Slog:
#     foo: String[20]
#     amount: int


# div if even otherwise ceil

def ceildiv(a: int, m: int) -> int:
    t: int = a % m
    if t == 0:
        return a / m
    else:
        return (a + (m - t)) / m

class Bucket:

    def __init__(
        self,
        _name,
        _vegaToken,
        _cliffTime: int,
        _numPeriods: int,
        _totalAmount: int,
        _period: int,
    ):
        # assert _vegaToken != ZERO_ADDRESS, "BUCKET: Vegatoken is zero address"
        # assert _cliffTime >= block.timestamp, "BUCKET: cliff must be in the future"
        # assert _numPeriods > 0, "BUCKET: numPeriods must be larger than 0"
        # assert _numPeriods < 25, "BUCKET: numPeriods must be smaller than 25"
        self.vegaToken = _vegaToken
        self.name = _name
        # self.registerTime = block.timestamp
        self.cliffTime = _cliffTime
        self.numPeriods = _numPeriods
        self.totalAmount = _totalAmount
        self.totalWithdrawnAmount = 0
        self.totalClaimAmount = 0
        self.initialized = False
        # self.owner = msg.sender
        self.period = _period
        self.claimCount = 0

    def initialize(self):
        # assert msg.sender == self.owner, "BUCKET: not the owner"
        # assert not self.initialized
        amountPerPeriod: int = self.totalAmount / self.numPeriods
        #actual periods
        self.duration = self.period * ceildiv(self.totalAmount, amountPerPeriod)
        # assert self.duration < 731 * days, "BUCKET: don't vest more than 2 years"
        self.endTime = self.cliffTime + self.duration
        self.initialized = True

    def currentPeriod(self) -> int:
        blocktimestamp = 100
        timeSinceCliff: int = blocktimestamp - self.cliffTime
        # at cliff, one amount is withdrawable
        validPeriodCount: int = 1 + timeSinceCliff / default_period
        return validPeriodCount


    def depositOwner(amount: int):
        pass
        # assert msg.sender == self.owner, "BUCKET: not the owner"
        # assert (
        #     ERC20(self.vegaToken).allowance(msg.sender, self) >= amount
        # ), "BUCKET: not enough allowance"

        # assert (
        #     ERC20(self.vegaToken).balanceOf(msg.sender) >= amount
        # ), "BUCKET: not enough balance"
        # transferSuccess: bool = ERC20(self.vegaToken).transferFrom(msg.sender, self, amount)
        # assert transferSuccess, "BUCKET: deposit failed"
        # log DepositOwner(msg.sender, amount)


    def withdrawOwner(self, amount: int):
        # assert msg.sender == self.owner, "BUCKET: not the owner"
        # bucketbalance: int = ERC20(self.vegaToken).balanceOf(self)
        # unclaimedbalance: int = bucketbalance - self.openClaimAmount
        # assert amount <= unclaimedbalance, "BUCKET: can't withdraw claimed amounts"
        # transferSuccess: bool = ERC20(self.vegaToken).transfer(msg.sender, amount)
        # assert transferSuccess, "BUCKET: withdraw failed"
        # log WithdrawOwner(msg.sender, amount)
        pass

    def _getVestableAmount(self, _claimAddress) -> int:
        # claim: Claim = self.claims[_claimAddress]
        blocktimestamp = 100
        if blocktimestamp < self.cliffTime:
            return 0

        if blocktimestamp >= self.endTime:
            return 200 #claim.claimTotalAmount

        # return self.currentPeriod() * claim.amountPeriod
        return 0

    def getVestableAmount(self, _claimAddress) -> int:
        return self._getVestableAmount(_claimAddress)

    def capat(self, amount: int, cap: int) -> int:
        if amount > cap:
            return cap
        else:
            return amount

    def _vestClaimMax(self, _claimAddress):
        pass
        # assert self.claims[_claimAddress].isAdded, "BUCKET: claim does not exist"

        # claim: Claim = self.claims[_claimAddress]

        # vestableAmount: int = self._getVestableAmount(_claimAddress)
        # log Slog("vestableAmount", vestableAmount)
        # vestableAmount = self.capat(vestableAmount, claim.claimTotalAmount)
        # log Slog("cap", vestableAmount)

        # assert vestableAmount >= claim.withdrawnAmount, "BUCKET: no vestable amount"
        # withdrawAmount: int = vestableAmount - claim.withdrawnAmount
        # log Slog("withdrawmount", withdrawAmount)
        # totalAfterwithdraw: int = claim.withdrawnAmount + withdrawAmount
        # log Slog("totalAfterwithdraw", totalAfterwithdraw)

        # assert (
        #     totalAfterwithdraw <= claim.claimTotalAmount
        # ), "BUCKET: can not withdraw more than total"

        # assert withdrawAmount > 0, "BUCKET: no amount claimed"
        

        # assert ERC20(self.vegaToken).transfer(
        #     _claimAddress, withdrawAmount
        # ), "BUCKET: transfer failed"

        # log WithdrawClaim(claim.claimAddress, withdrawAmount)

        # # assert self.openClaimAmount >= withdrawAmount, concat("no amount left to claim", withdrawAmount)
        # log Slog("openClaimAmount", self.openClaimAmount)
        # assert self.openClaimAmount >= withdrawAmount, "no amount left to claim"

        # claim.withdrawnAmount += withdrawAmount
        # self.totalWithdrawnAmount += withdrawAmount
        # self.openClaimAmount -= withdrawAmount

    def vestClaimMax(self, _claimAddress):
        pass
        # isclaimer: bool = msg.sender == _claimAddress
        # assert msg.sender == self.owner or isclaimer, "BUCKET: not the owner or claimer"

        # self._vestClaimMax(_claimAddress)

    def _addClaim(_claimAddress, _claimTotalAmount: int):
        pass
        # assert not self.claims[_claimAddress].isAdded, "BUCKET: added already"

        # assert _claimTotalAmount > 0, "BUCKET: claim can not be zero"

        # assert (
        #     self.totalClaimAmount + _claimTotalAmount <= self.totalAmount
        # ), "BUCKET: can not claim more than total"

        # bal: int = ERC20(self.vegaToken).balanceOf(self)
        # unclaimed: int = bal - self.totalClaimAmount
        # assert (
        #     _claimTotalAmount <= unclaimed
        # ), "BUCKET: can not claim tokens that are not deposited"

        # _amountPeriod: int = _claimTotalAmount / self.numPeriods
        # existclaim: Claim = self.claims[_claimAddress]
        # assert existclaim == empty(Claim), "BUCKET: claim at this address already exists"
        # self.claims[_claimAddress] = Claim(
        #     {
        #         claimAddress: _claimAddress,
        #         amountPeriod: _amountPeriod,
        #         claimTotalAmount: _claimTotalAmount,
        #         withdrawnAmount: 0,
        #         isAdded: True,
        #     }
        # )

        # self.claim_addresses[self.claimCount] = _claimAddress
        # self.claimCount += 1

        # self.totalClaimAmount += _claimTotalAmount
        # self.openClaimAmount += _claimTotalAmount

        # log ClaimAdded(_claimAddress, _claimTotalAmount)



    def addClaim(_claimAddress, _claimTotalAmount):
        pass
        # assert msg.sender == self.owner, "BUCKET: not owner"
        # self._addClaim(_claimAddress, _claimTotalAmount)


    def vestAll():
        pass
        # assert msg.sender == self.owner, "BUCKET: not owner"
        # for i in range(0, 1000):
        #     addr: address = self.claim_addresses[i]
        #     if self.claims[addr].isAdded:
        #         self._vestClaimMax(addr)
        #     else:
        #         return

    def addClaimsBatch(list_addr):
        pass
        # for i in range(0, 1000):
        #     amount: int = ClaimList(list_addr).amounts(i)
        #     if amount > 0:
        #         self._addClaim(ClaimList(list_addr).addresses(i), amount)
        #     else:
        #         return

b = Bucket("Basic", "", 0, 1, 100, 1)
b.initialize()
print(b.totalAmount)
print(b.duration)
print(b.endTime)
