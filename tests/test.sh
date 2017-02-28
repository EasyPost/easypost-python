#!/bin/sh
#
# Runs all unittests.

cd `dirname "$0"` || exit 1

die() {
    echo
    echo "ABORT"
    echo "$@"
    exit 1
}
test_one() {
    env PYTHONPATH=`cd .. && pwd` python "$1" || die "$1 failure"
}
for x in address.py \
         batch.py \
         insurance.py \
         order.py \
         parcel.py \
         pickup.py \
         report.py \
         scan_form.py \
         shipment.py \
         tracker.py \
         user.py \
         webhook.py; do
    test_one "$x"
done
