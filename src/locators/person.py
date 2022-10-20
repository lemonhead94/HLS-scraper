class PersonPageLocator:
    GIVEN_NAME = {"itemprop": "givenName"}
    FAMILY_NAME = {"itemprop": "familyName"}
    DATE_OF_BIRTH = ("span", {"class": "hls-dnais"})
    DATE_OF_BIRTH_2 = ("span", {"class": "hls-bapt"})
    FIRST_MENTION_BIRTH = ("span", {"class": "hls-cit"})
    DATE_OF_DEATH = ("span", {"class": "hls-ddec"})
    LAST_MENTION_DEATH = ("span", {"class": "hls-cit2"})
    NO_DATES_SPECIFIED = ("td", {"class": "hls-service-box-table-text"})
