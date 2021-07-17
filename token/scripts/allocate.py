from brownie import (
    VegaToken,
    VestingMath,
    VegaMaster,
    VestingConstants,
    VestingBucket,
    accounts,
    chain,
)


def allocate(master, token, vconstants, mainAccount):
    print("allocate to buckets")

    # print(vconstants)

    amounts = [
        vconstants.seedAmount(),
        vconstants.privateAmount(),
        vconstants.publicAmount(),
        vconstants.liqAmount(),
        vconstants.lprewardsAmount(),
        vconstants.lpgrantsAmount(),
        vconstants.ecoAmount(),
        vconstants.trademiningAmount(),
        vconstants.teamAmount(),
        vconstants.advisoryAmount(),
    ]
    print(amounts)
    print(sum(amounts))
    rest = token.totalSupply() / 10 ** 18 - sum(amounts)
    print("rest ", rest)

    # now = getCurrentTime
    now = chain.time()

    DECIMALS = token.decimals()
    master.addVestingBucket(
        now + vconstants.seedCliff(),
        "SeedFunding",
        vconstants.seedPeriods(),
        vconstants.seedAmount() * (10 ** DECIMALS),
        {"from": mainAccount},
    )

    master.addVestingBucket(
        now + vconstants.privateCliff(),
        "PrivateFunding",
        vconstants.privatePeriods(),
        vconstants.privateAmount() * (10 ** DECIMALS),
        {"from": mainAccount},
    )

    master.addVestingBucket(
        now + vconstants.publicCliff(),
        "PublicFunding",
        vconstants.publicPeriods(),
        vconstants.publicAmount() * (10 ** DECIMALS),
        {"from": mainAccount},
    )

    master.addVestingBucket(
        now + vconstants.liqCliff(),
        "Liquidity",
        vconstants.liqPeriods(),
        vconstants.liqAmount() * (10 ** DECIMALS),
        {"from": mainAccount},
    )

    master.addVestingBucket(
        now + vconstants.lpwRewardsCliff(),
        "LPrewards",
        vconstants.lprewardsPeriods(),
        vconstants.lprewardsAmount() * (10 ** DECIMALS),
        {"from": mainAccount},
    )

    master.addVestingBucket(
        now + vconstants.lpgrantsCliff(),
        "LPgrants",
        vconstants.lpgrantsPeriods(),
        vconstants.lpgrantsAmount() * (10 ** DECIMALS),
        {"from": mainAccount},
    )

    master.addVestingBucket(
        now + vconstants.ecoCliff(),
        "Ecosystem",
        vconstants.ecoPeriods(),
        vconstants.ecoAmount() * (10 ** DECIMALS),
        {"from": mainAccount},
    )

    master.addVestingBucket(
        now + vconstants.trademiningCliff(),
        "TradeMining",
        vconstants.trademiningPeriods(),
        vconstants.trademiningAmount() * (10 ** DECIMALS),
        {"from": mainAccount},
    )

    master.addVestingBucket(
        now + vconstants.teamCliff(),
        "Team",
        vconstants.teamPeriods(),
        vconstants.teamAmount() * (10 ** DECIMALS),
        {"from": mainAccount},
    )

    master.addVestingBucket(
        now + vconstants.advisoryCliff(),
        "Advisory",
        vconstants.advisorsPeriods(),
        vconstants.advisoryAmount() * (10 ** DECIMALS),
        {"from": mainAccount},
    )

    master.addVestingBucket(
        now + vconstants.treasuryCliff(),
        "Treasury",
        vconstants.treasuryPeriods(),
        vconstants.treasuryAmount() * (10 ** DECIMALS),
        {"from": mainAccount},
    )
