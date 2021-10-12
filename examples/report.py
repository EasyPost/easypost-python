import easypost

easypost.api_key = "API_KEY"

report = easypost.Report.create(
    start_date="2012-12-01",
    end_date="2013-01-01",
    type="shipment",
)
print(report.id)

report1 = easypost.Report.retrieve(report.id)

print(report1.id)

report2 = easypost.Report.create(
    start_date="2013-12-02",
    end_date="2014-01-01",
    type="shipment",
)

reports3 = easypost.Report.all(type="shipment")

print(reports3)
