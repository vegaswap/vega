# @version ^0.2.15

# Vega token has max supply
# cross chain mint and burn

from vyper.interfaces import ERC20

implements: ERC20


event Transfer:
    sender: indexed(address)
    receiver: indexed(address)
    value: uint256


event Approval:
    owner: indexed(address)
    spender: indexed(address)
    value: uint256


name: public(String[64])
symbol: public(String[32])
decimals: public(uint256)

# vyper automatically generates getters
balanceOf: public(HashMap[address, uint256])
allowances: public(HashMap[address, HashMap[address, uint256]])
totalSupply: public(uint256)
circulatingSupply: public(uint256)
deployer: public(address)


@external
def __init__():
    # _name: String[64], _symbol: String[32], _decimals: uint256, _max_supply: uint256
    self.name = "VegaToken"
    self.symbol = "VGA"
    self.decimals = 18

    # assign max supply, no more minting after that
    init_supply: uint256 = 10 ** 9 * 10 ** self.decimals
    self.balanceOf[msg.sender] = init_supply
    self.totalSupply = init_supply
    # calcuating circulation needs to be done externally
    self.circulatingSupply = 0
    self.deployer = msg.sender
    log Transfer(ZERO_ADDRESS, msg.sender, init_supply)


@internal
def swap(_from: address, _to: address, _value: uint256):
    # vyper does not allow underflows
    # so the following subtraction would revert on insufficient balance
    assert _to != ZERO_ADDRESS  # dev: transfers to 0x0 are not allowed
    self.balanceOf[_from] -= _value
    self.balanceOf[_to] += _value
    log Transfer(_from, _to, _value)


@external
def transfer(_to: address, _value: uint256) -> bool:
    """
    @notice Transfer `_value` tokens from `msg.sender` to `_to`
    @dev Vyper does not allow underflows, so the subtraction in
         this function will revert on an insufficient balance
    @param _to The address to transfer to
    @param _value The amount to be transferred
    @return bool success
    """
    self.swap(msg.sender, _to, _value)
    return True


@external
def transferFrom(_from: address, _to: address, _value: uint256) -> bool:
    """
    @notice Transfer `_value` tokens from `_from` to `_to`
    @param _from address The address which you want to send tokens from
    @param _to address The address which you want to transfer to
    @param _value uint256 the amount of tokens to be transferred
    @return bool success
    """
    self.swap(_from, _to, _value)
    self.allowances[_from][msg.sender] -= _value
    return True


@external
def approve(_spender: address, _value: uint256) -> bool:
    """
    @notice Approve `_spender` to transfer `_value` tokens on behalf of `msg.sender`
    @dev Approval may only be from zero -> nonzero or from nonzero -> zero in order
        to mitigate the potential race condition described here:
        https://github.com/ethereum/EIPs/issues/20#issuecomment-263524729
    @param _spender The address which will spend the funds
    @param _value The amount of tokens to be spent
    @return bool success
    """
    # assert _value == 0 or self.allowances[msg.sender][_spender] == 0
    self.allowances[msg.sender][_spender] = _value
    log Approval(msg.sender, _spender, _value)
    return True


@external
@view
def allowance(_owner: address, _spender: address) -> uint256:
    """
    @notice Check the amount of tokens that an owner allowed to a spender
    @param _owner The address which owns the funds
    @param _spender The address which will spend the funds
    @return uint256 specifying the amount of tokens still available for the spender
    """
    return self.allowances[_owner][_spender]


@external
def setCirculatingSupply(_circulatingSupply: uint256):
    assert msg.sender == self.deployer, "only deployer"
    self.circulatingSupply = _circulatingSupply
