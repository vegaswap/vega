// contract allocate {
//     function allocatcalc() public onlyOwner {
//         //function allocate() private {
//         uint8 DECIMALS = vega_token.decimals();

//         addVestingBucket(
//             VestingConstants.seedCliff,
//             "SeedFunding",
//             VestingConstants.seedPeriods,
//             VestingConstants.seedAmount * (10**DECIMALS)
//         );

//         addVestingBucket(
//             VestingConstants.privateCliff,
//             "PrivateFunding",
//             VestingConstants.privatePeriods,
//             VestingConstants.privateAmount * (10**DECIMALS)
//         );

//         addVestingBucket(
//             VestingConstants.publicCliff,
//             "PublicFunding",
//             VestingConstants.publicPeriods,
//             VestingConstants.publicAmount * (10**DECIMALS)
//         );

//         addVestingBucket(
//             VestingConstants.liqCliff,
//             "Vega_Liquidity",
//             VestingConstants.liqPeriods,
//             VestingConstants.liqAmount * (10**DECIMALS)
//         );

//         addVestingBucket(
//             VestingConstants.lpwRewardsCliff,
//             "LP_rewards",
//             VestingConstants.lprewardsPeriods,
//             VestingConstants.lprewardsAmount * (10**DECIMALS)
//         );

//         // addVestingBucket(
//         //     VestingConstants.lpgrantsCliff,
//         //     "LP_grants",
//         //     VestingConstants.lpgrantsPeriods,
//         //     VestingConstants.lpgrantsAmount * (10**DECIMALS)
//         // );

//         addVestingBucket(
//             VestingConstants.ecoCliff,
//             "Ecosystem",
//             VestingConstants.ecoPeriods,
//             VestingConstants.ecoAmount * (10**DECIMALS)
//         );

//         //VestingConstants.trademiningAmount * (10**DECIMALS)
//         addVestingBucket(
//             VestingConstants.trademiningCliff,
//             "Trade_Mining",
//             VestingConstants.trademiningPeriods,
//             100
//         );

//         // addVestingBucket(
//         //     VestingConstants.teamCliff,
//         //     "Team",
//         //     VestingConstants.teamPeriods,
//         //     VestingConstants.teamAmount * (10**DECIMALS)
//         // );

//         // addVestingBucket(
//         //     VestingConstants.advisoryCliff,
//         //     "Advisors",
//         //     VestingConstants.advisorsPeriods,
//         //     VestingConstants.advisoryAmount * (10**DECIMALS)
//         // );

//         // addVestingBucket(
//         //     VestingConstants.treasuryCliff,
//         //     "Advisors",
//         //     VestingConstants.treasuryPeriods,
//         //     VestingConstants.treasuryAmount * (10**DECIMALS)
//         // );
//     }
// }
