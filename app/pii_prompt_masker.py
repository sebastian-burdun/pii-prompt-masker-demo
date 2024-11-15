import logging
from typing import List, NoReturn

import nltk
import scrubadub, scrubadub_address, scrubadub_stanford

from detectors import ProbableAddressDetector, ProbablePhoneNumberDetector
from settings import TOKEN_MASK_SUFFIX, TOKEN_MASK_PREFIX


logger = logging.getLogger("uvicorn.error")


nltk.download("punkt_tab")


class PIIMaskMapBuilder(scrubadub.post_processors.PostProcessor):
    name = "pii_mask_map_builder"
    pii_mask_map = {}

    def process_filth(
        self, item_list: List[scrubadub.filth.name.NameFilth]
    ) -> List[scrubadub.filth.name.NameFilth]:
        for item in item_list:
            self.pii_mask_map[item.replacement_string] = item.text
        return item_list


class PIIPromptMasker(scrubadub.Scrubber):

    def clean(self, *args, **kwargs) -> str:
        result = super().clean(*args, **kwargs)
        self._update_pii_mask_map()
        return result

    def _update_pii_mask_map(self) -> NoReturn:
        self.pii_mask_map = next(
            processor
            for processor in self._post_processors
            if isinstance(processor, PIIMaskMapBuilder)
        ).pii_mask_map

    def unmask_answer(self, masked_text: str) -> str:
        """Unmasking for synchronous responses."""
        unmasked_text = masked_text
        for masked_item, unmasked_item in self.pii_mask_map.items():
            unmasked_text = unmasked_text.replace(masked_item, unmasked_item)

        return unmasked_text

    async def unmask_tokens(self, response_tokens: str):
        """Unmasking for streaming responses."""
        is_token_merging = False
        merged_token = ""
        answer = ""
        for response_token in response_tokens:
            answer += response_token.content
            if response_token.content == TOKEN_MASK_PREFIX:
                is_token_merging = True
                merged_token = ""
                continue
            elif response_token.content == TOKEN_MASK_SUFFIX:
                is_token_merging = False
                masked_token = f"{TOKEN_MASK_PREFIX}{merged_token}{TOKEN_MASK_SUFFIX}"
                yield (
                    self.pii_mask_map[masked_token]
                    if masked_token in self.pii_mask_map
                    else masked_token
                )
                continue
            if is_token_merging:
                merged_token += response_token.content
                continue
            yield response_token.content
        logger.debug(f"Answer from LLM: `{answer}`")


pii_prompt_masker = PIIPromptMasker(
    post_processor_list=[
        scrubadub.post_processors.FilthReplacer(
            include_hash=True, separator="", hash_salt="1gSwPNQeWRw", hash_length=5
        ),
        scrubadub.post_processors.PrefixSuffixReplacer(
            prefix=TOKEN_MASK_PREFIX, suffix=TOKEN_MASK_SUFFIX
        ),
        PIIMaskMapBuilder(),
    ]
)
pii_prompt_masker.add_detector(scrubadub_stanford.detectors.StanfordEntityDetector)
pii_prompt_masker.add_detector(scrubadub_address.detectors.AddressDetector)
pii_prompt_masker.add_detector(ProbableAddressDetector)

# Uncomment to use additional phone masking -
# pii_prompt_masker.add_detector(ProbablePhoneNumberDetector)
# This is a very curious case, please check Phone masking.pdf document in the docs folder.
