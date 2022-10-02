import qrcode
import fitz
import io


def makepdf(master, trial, site):
    site_url = (
        f"https://novocomplete.tst.cdr.pub.aws.novonordisk.com/prod/{trial}/site/{site}"
    )
    img = qrcode.make(site_url)
    buf = io.BytesIO()
    img.save(buf)
    buf.seek(0)
    doc = fitz.open(master)
    Page = doc[0]
    lnks = Page.get_links()
    for l in lnks:
        theurl = l["uri"]
        print(theurl)
        if theurl[0:20] == "https://novocomplete":
            l["uri"] = site_url
            Page.update_link(l)
    rect = fitz.Rect(70, 220, 195, 345)  # put thumbnail in upper left corner
    Page.insert_image(
        rect,
        stream=buf,
    )
    p1 = (20, 40)
    Page.insert_text(p1, f"This is for {trial}, V1")
    doc_path = f"{trial}_{site}_ok.pdf"
    print(doc_path)
    doc.save(doc_path)
    doc.close()


if __name__ == "__main__":
    makepdf("Master.pdf", "4389", "MjAwMA==")
