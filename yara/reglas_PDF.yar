rule Se_Detecto_PDF_Malicioso_En {
    meta:
        author = "Ing. Dipl. Franck Tscherig"
        description = "Regla para detectar contenido malicioso en archivos PDF 1v2"
        date = "2023-03-21"
    strings:
        $pdf_header = { 25 50 44 46 }
        $javascript = " /JavaScript"
        $embedded_file = "/EmbeddedFile"
        $obj_keyword = /\/Obj\s+\d+/
        $stream_keyword = /\/Length\s+\d+\s*\/Filter\s*\/FlateDecode/
        $suspicious_keywords = /exploit|malware|vulnerability/i

    condition:
        $pdf_header at 0 and
        ($javascript or $embedded_file or $obj_keyword or $stream_keyword or $suspicious_keywords)
}
