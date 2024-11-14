from typing import Any, List, NoReturn

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
    def _initialize_pii_mask_map(self) -> NoReturn:
        self.pii_mask_map = next(
            processor
            for processor in self._post_processors
            if isinstance(processor, PIIMaskMapBuilder)
        ).pii_mask_map

    def unmask(self, masked_text: str) -> str:
        self._initialize_pii_mask_map()
        unmasked_text = masked_text
        for masked_item, unmasked_item in self.pii_mask_map.items():
            unmasked_text = unmasked_text.replace(masked_item, unmasked_item)

        return unmasked_text


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
