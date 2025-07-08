import os
import xml.etree.ElementTree as ET

folder = "xml_kvitancii"
log_file = "errors.log"

with open(log_file, "w", encoding="utf-8") as log:
    for filename in os.listdir(folder):
        if filename.endswith(".xml") or filename.endswith(".ack"):
            path = os.path.join(folder, filename)
            tree = ET.parse(path)
            root = tree.getroot()

            entry = None
            for elem in root.iter():
                if elem.tag.endswith("entry"):
                    entry = elem
                    break

            if entry is not None:
                entry_err = entry.get("errCode")
                if entry_err == "0":
                    log.write(f"{filename} — Обработан успешно\n")
                else:
                    log.write(f"{filename} — Ошибки:\n")
                    for fault in entry:
                        if fault.tag.endswith("fault"):
                            line = fault.get("line")
                            code = fault.get("errCode")
                            description = fault.get("description")
                            log.write(f"  ➤ Строка {line}: Ошибка {code} — {description}\n")
