import enum


class SmartRateAccuracy(enum.Enum):
    Percentile50 = ("percentile_50",)
    Percentile75 = ("percentile_75",)
    Percentile85 = ("percentile_85",)
    Percentile90 = ("percentile_90",)
    Percentile95 = ("percentile_95",)
    Percentile97 = ("percentile_97",)
    Percentile99 = "percentile_99"
