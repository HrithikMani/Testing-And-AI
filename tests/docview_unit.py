"""
    Unit test to track rendering of documents
    SELECT MAX(d.doc_id),d.storage_type,st.description,lr.interface
	FROM documents d
	LEFT JOIN lab_requests lr ON lr.doc_id=d.doc_id
	LEFT JOIN storage_types st USING (storage_type)
	GROUP BY d.storage_type,lr.interface;
    @owners: dcornewell
    @filedep: src/storage.c, src/detailview.c, system/layouts/Storage Type*, system/layouts/Document/*
"""
def main(d, WCURL):
    """
    Verifies how one of each document type in snapshot looks in detailview
    """
    d.miedb.dbExec("UPDATE system_settings SET value='' WHERE module='E-Chart' AND section='Conversion Server' AND item='Address'")

    d.navigate("?f=chart&s=doc&doc_id=408")
    d.wcutils.waitForAJAX(45);
    d.screenshot("Plain Text Document 408")

#  Libre Office cannot convert this document
#    d.navigate("?f=chart&s=doc&doc_id=164")
#    d.wcutils.waitForAJAX(45);
#    d.screenshot("RTF Document 164")

    d.navigate("?f=chart&s=doc&doc_id=608")
    d.wcutils.waitForAJAX(45);
    d.screenshot("PNG Document 608")

    d.navigate("?f=chart&s=doc&doc_id=632")
    d.wcutils.waitForAJAX(45);
    d.screenshot("HTML Document 632")

    d.navigate("?f=chart&s=doc&doc_id=489")
    d.wcutils.waitForAJAX(45);
    d.screenshot("WORD Document 489")

    d.navigate("?f=chart&s=doc&doc_id=606")
    d.wcutils.waitForAJAX(45);
    d.screenshot("TIFF Document 606")

    d.navigate("?f=chart&s=doc&doc_id=538")
    d.wcutils.waitForAJAX(45);
    d.screenshot("JPEG Document 538")

    d.navigate("?f=chart&s=doc&doc_id=451")
    d.wcutils.waitForAJAX(45);
    d.screenshot("DICOM Document 451")

    d.navigate("?f=chart&s=doc&doc_id=583")
    d.wcutils.waitForAJAX(45);
    d.screenshot("TASK Document 583")

    d.navigate("?f=chart&s=doc&doc_id=655")
    d.wcutils.waitForAJAX(45);
    d.screenshot("Injection Document 655")

    d.navigate("?f=chart&s=doc&doc_id=510")
    d.wcutils.waitForAJAX(45);
    d.screenshot("Lab Request Document 510")

    d.navigate("?f=chart&s=doc&doc_id=630")
    d.wcutils.waitForAJAX(45);
    d.screenshot("Questionnaire Document ")

    d.navigate("?f=chart&s=doc&doc_id=109")
    d.wcutils.waitForAJAX(45);
    d.screenshot("Pre-Formated Text Document 109")

    d.navigate("?f=chart&s=doc&doc_id=596")
    d.wcutils.waitForAJAX(45);
    d.screenshot("Orders Document 596")

    d.navigate("?f=chart&s=doc&doc_id=298")
    d.wcutils.waitForAJAX(45);
    d.screenshot("PDF Document 298")

    d.navigate("?f=chart&s=doc&doc_id=595")
    d.wcutils.waitForAJAX(45);
    d.screenshot("CDA Document 595")

    d.navigate("?f=chart&s=doc&doc_id=614")
    d.wcutils.waitForAJAX(45);
    d.screenshot("CCR Document 614")

    d.navigate("?f=chart&s=doc&doc_id=540")
    d.wcutils.waitForAJAX(45);
    d.screenshot("Email Document 540")

    d.navigate("?f=chart&s=doc&doc_id=542")
    d.wcutils.waitForAJAX(45);
    d.screenshot("OCP Audio Document 542")

    d.navigate("?f=chart&s=doc&doc_id=527")
    d.wcutils.waitForAJAX(45);
    d.screenshot("Pulmonary Function Test Document 527")
