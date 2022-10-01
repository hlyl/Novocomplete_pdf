import PyPDF2
import qrcode
import fitz
import io


def makepdf(master, trial, site):
    pdf_writer = PyPDF2.PdfFileWriter()
    pdf_reader = PyPDF2.PdfFileReader(master)
    site_url = (
        f"https://novocomplete.tst.cdr.pub.aws.novonordisk.com/prod/{trial}/site/{site}"
    )
    for i in range(pdf_reader.getNumPages()):
        page = pdf_reader.getPage(i)
        img = qrcode.make(site_url)
        buf = io.BytesIO()
        img.save(buf)
        buf.seek(0)
        if "/Annots" not in page:
            continue
        for annot in page["/Annots"]:
            annot_obj = annot.getObject()
            if "/A" not in annot_obj:
                continue  # not a link
            # you have to wrap the key and value with a TextStringObject:
            key = PyPDF2.generic.TextStringObject("/URI")
            theurl = annot_obj["/A"]["/URI"]
            if theurl[0:20] == "https://novocomplete":
                value = PyPDF2.generic.TextStringObject(site_url)
                annot_obj["/A"][key] = value
                print(theurl[0:20])
        pdf_writer.addPage(page)
    with open(f"{trial}_{site}.pdf", "wb") as f:
        pdf_writer.write(f)

    doc = fitz.open(f"{trial}_{site}.pdf")
    rect = fitz.Rect(70, 220, 195, 345)  # put thumbnail in upper left corner
    img_xref = 0  # first execution embeds the image
    for page in doc:
        img_xref = page.insert_image(
            rect,
            stream=buf,
            xref=img_xref,
        )
    doc_path = f"{trial}_{site}_ok.pdf"
    print(doc_path)
    doc.save(doc_path)
    doc.close()


if __name__ == "__main__":
    makepdf("Master.pdf", "4388", "MjAwMA==")
