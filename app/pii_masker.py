import nltk
import scrubadub, scrubadub_address, scrubadub_stanford

nltk.download("punkt_tab")


class PIIMaskMapBuilder(scrubadub.post_processors.PostProcessor):
    name = "pii_mask_map_builder"
    mapping = {}

    def process_filth(self, item_list):
        for item in item_list:
            self.mapping[item.replacement_string] = item.text
        return item_list


pii_masker = scrubadub.Scrubber(
    post_processor_list=[
        scrubadub.post_processors.FilthReplacer(
            include_hash=True, hash_salt="example", hash_length=5
        ),
        PIIMaskMapBuilder(),
    ]
)
pii_masker.add_detector(scrubadub_stanford.detectors.StanfordEntityDetector)
pii_masker.add_detector(scrubadub_address.detectors.AddressDetector)
