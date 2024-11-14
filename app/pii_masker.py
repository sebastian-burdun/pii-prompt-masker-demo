from typing import List, NoReturn

import nltk
import scrubadub, scrubadub_address, scrubadub_stanford

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


class PIIMasker(scrubadub.Scrubber):

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
        unmasked_text = masked_text
        for masked_item, unmasked_item in self.pii_mask_map.items():
            unmasked_text = unmasked_text.replace(masked_item, unmasked_item)

        return unmasked_text

    def unmask_token(self, masked_token: str) -> str:
        return (
            self._update_pii_mask_map(masked_token)
            if masked_token in self._update_pii_mask_map
            else masked_token
        )


pii_masker = PIIMasker(
    post_processor_list=[
        scrubadub.post_processors.FilthReplacer(
            include_hash=True, hash_salt="example", hash_length=5
        ),
        PIIMaskMapBuilder(),
    ]
)
pii_masker.add_detector(scrubadub_stanford.detectors.StanfordEntityDetector)
pii_masker.add_detector(scrubadub_address.detectors.AddressDetector)
