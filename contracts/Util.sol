// SPDX-License-Identifier: MIT
pragma solidity ^0.8.5;

library Util {
    function errorMessage(string memory contractString, string memory reason)
        public
        pure
        returns (string memory)
    {
        return strConcat(contractString, ": ", reason);
    }

    function errorMessage(
        string memory contractString,
        string memory reason,
        string memory data
    ) public pure returns (string memory) {
        return strConcat(contractString, ": ", reason, ": ", data);
    }

    function uintToString(uint256 v) public pure returns (string memory) {
        if (v == 0) return "0";
        // max uint 115792089237316195423570985008687907853269984665640564039457584007913129639935 has 78 digits
        uint256 maxlength = 78;
        bytes memory reversed = new bytes(maxlength);
        uint256 i = 0;
        while (v != 0) {
            uint256 remainder = v % 10;
            v = v / 10;
            reversed[i++] = bytes1(uint8(48 + remainder));
        }
        bytes memory s = new bytes(i);
        for (uint256 j = 0; j < i; j++) {
            s[j] = reversed[i - j - 1];
        }
        string memory str = string(s);
        return str;
    }

    function strConcat(
        string memory _a,
        string memory _b,
        string memory _c,
        string memory _d,
        string memory _e
    ) public pure returns (string memory) {
        bytes memory _ba = bytes(_a);
        bytes memory _bb = bytes(_b);
        bytes memory _bc = bytes(_c);
        bytes memory _bd = bytes(_d);
        bytes memory _be = bytes(_e);
        string memory abcde = new string(
            _ba.length + _bb.length + _bc.length + _bd.length + _be.length
        );
        bytes memory babcde = bytes(abcde);
        uint256 k = 0;
        uint256 i = 0;
        for (i = 0; i < _ba.length; i++) babcde[k++] = _ba[i];
        for (i = 0; i < _bb.length; i++) babcde[k++] = _bb[i];
        for (i = 0; i < _bc.length; i++) babcde[k++] = _bc[i];
        for (i = 0; i < _bd.length; i++) babcde[k++] = _bd[i];
        for (i = 0; i < _be.length; i++) babcde[k++] = _be[i];
        return string(babcde);
    }

    function strConcat(
        string memory _a,
        string memory _b,
        string memory _c,
        string memory _d
    ) public pure returns (string memory) {
        return strConcat(_a, _b, _c, _d, "");
    }

    function strConcat(
        string memory _a,
        string memory _b,
        string memory _c
    ) public pure returns (string memory) {
        return strConcat(_a, _b, _c, "", "");
    }

    function strConcat(string memory _a, string memory _b)
        public
        pure
        returns (string memory)
    {
        return strConcat(_a, _b, "", "", "");
    }
}
