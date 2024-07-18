from typing import (
    Optional,
    Union,
)

from easypost.easypost_object import EasyPostObject
from easypost.models.smart_rate_accuracy import SmartRateAccuracy
from pydantic import Field


class TimeInTransit(EasyPostObject):
    percentile_50: Optional[int] = Field(None, alias="percentile_50")
    percentile_75: Optional[int] = Field(None, alias="percentile_75")
    percentile_85: Optional[int] = Field(None, alias="percentile_85")
    percentile_90: Optional[int] = Field(None, alias="percentile_90")
    percentile_95: Optional[int] = Field(None, alias="percentile_95")
    percentile_97: Optional[int] = Field(None, alias="percentile_97")
    percentile_99: Optional[int] = Field(None, alias="percentile_99")

    def get_by_smart_rate_accuracy(self, smart_rate_accuracy: SmartRateAccuracy) -> Union[Optional[int], None]:
        if smart_rate_accuracy == SmartRateAccuracy.Percentile50:
            return self.percentile_50
        if smart_rate_accuracy == SmartRateAccuracy.Percentile75:
            return self.percentile_75
        if smart_rate_accuracy == SmartRateAccuracy.Percentile85:
            return self.percentile_85
        if smart_rate_accuracy == SmartRateAccuracy.Percentile90:
            return self.percentile_90
        if smart_rate_accuracy == SmartRateAccuracy.Percentile95:
            return self.percentile_95
        if smart_rate_accuracy == SmartRateAccuracy.Percentile97:
            return self.percentile_97
        if smart_rate_accuracy == SmartRateAccuracy.Percentile99:
            return self.percentile_99
        return None
