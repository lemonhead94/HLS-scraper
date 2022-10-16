class PersonPageLocator:
    GIVEN_NAME = {"itemprop": "givenName"}
    FAMILY_NAME = {"itemprop": "familyName"}
    DATE_OF_BIRTH = ("span", {"class": "hls-dnais"})
    DATE_OF_DEATH = ("span", {"class": "hls-ddec"})
