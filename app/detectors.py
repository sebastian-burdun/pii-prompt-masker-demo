"""
This module contains just a few examples of detectors that need to be created
to fix cases where third-party ones fail.
"""

import re


import scrubadub


class ProbableEntityDetector(scrubadub.detectors.Detector):
    """
    Class adding basic support for finding entities using regex.
    """
    def iter_filth(self, text: str, **kwargs):
        for match in self.regex.finditer(text):
            yield self.filth_cls(
                match=match,
                detector_name=self.name,
                locale=self.locale,
            )


class ProbableAddressFilth(scrubadub.filth.Filth):
    name = "probable_address"


class ProbableAddressDetector(ProbableEntityDetector):
    """
    Assumes that if there appears a phrase 'lives at ' then it is followed
    by an address up to a comma or a dot. Detector might be too greedy,
    but it is assumed that it is better to mask something that is not an address,
    than to pass the address to the model.
    """

    name = "probable_address_detector"
    regex = re.compile(r"(?<=lives at )[^.,]+", re.IGNORECASE)
    filth_cls = ProbableAddressFilth


class ProbablePhoneNumberFilth(scrubadub.filth.Filth):
    name = "probable_phone_number"


class ProbablePhoneNumberDetector(ProbableEntityDetector):
    """
    Assumes that if there appears a phrase 'phone number is ' then it is followed
    some digits separated by hyphens and that digit-hyphen's string should be treated
    as a phone nuber.
    """

    name = "probable_phone_number_detector"
    regex = re.compile(r"(?<=phone number is )[\d-]+", re.IGNORECASE)
    filth_cls = ProbablePhoneNumberFilth
