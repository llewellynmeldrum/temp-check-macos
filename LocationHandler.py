from time import time as s_since_epoch
import objc
from Foundation import NSObject, NSLog, NSRunLoop, NSDate
from CoreLocation import CLLocationManager, kCLLocationAccuracyBest

import platform
if platform.system() != "Darwin":


class LocationDelegate(NSObject):
    def init(self):
        self = objc.super(LocationDelegate, self).init()
        self.location = None
        self.error = None
        return self

    def locationManager_didUpdateLocations_(self, manager, locations):
        self.location = locations[-1]

    def locationManager_didFailWithError_(self, manager, error):
        self.error = error


def macOS_queryLocation(timeout_s: float = 10.0) -> tuple[float, float, float]:
    mgr = CLLocationManager.alloc().init()
    delegate = LocationDelegate.alloc().init()
    mgr.setDelegate_(delegate)

    try:
        mgr.requestWhenInUseAuthorization()
    except Exception:
        pass

    mgr.setDesiredAccuracy_(kCLLocationAccuracyBest)
    mgr.startUpdatingLocation()

    deadline = s_since_epoch() + timeout_s
    while s_since_epoch() < deadline        \
            and delegate.location is None   \
            and delegate.error is None:
        NSRunLoop.currentRunLoop().runUntilDate_(
            NSDate.dateWithTimeIntervalSinceNow_(0.1))

    mgr.stopUpdatingLocation()

    if delegate.error is not None:
        raise RuntimeError(f"Location error: {delegate.error}")

    if delegate.location is None:
        raise TimeoutError(
            "Timed out waiting for location (permission denied? no fix?)")

    co = delegate.location.coordinate()
    return (co.latitude, co.longitude, float(delegate.location.horizontalAccuracy()))
