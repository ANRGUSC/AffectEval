from feature_extractor.feature_extractor import FeatureExtractor
from signal_acquisition.signal_acquisition import SignalAcquisition
from signal_preprocessor.signal_preprocessor import SignalPreprocessor
from pipeline.pipeline import Pipeline


if __name__ == "__main__":
    signal_acq = SignalAcquisition()
    signal_preprocessor = SignalPreprocessor()
    feature_extractor = FeatureExtractor()

    pipeline = Pipeline()
