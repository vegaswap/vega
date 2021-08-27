# @version ^0.2.14

# def depositOwner(uint256 amount) public onlyOwner :
def addClaim(address _claimAddress, uint256 _claimTotalAmount)
def getVestedAmount(Claim memory claim) public view returns (uint256) :
def getVestableAmount(address _claimAddress)
def vestClaimMax(address _claimAddress) public :
def allClaim() public onlyRefOwner :
def withdrawOwner(uint256 amount) public onlyRefOwner :
# def revokeClaim(address _claimAddress) public onlyRefOwner :

# struct Claim
# mapping(address => Claim) public claims;
# address[] public claimAddresses;
# uint256 public totalClaimAmount;
# uint256 public totalWithdrawnAmount;
