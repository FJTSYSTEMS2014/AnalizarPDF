import os
import subprocess
import datetime

def install_tool(tool_name):
    subprocess.run(["sudo", "apt", "install", "-y", tool_name])

def check_and_install_tools():
    required_tools = ["pdfid", "pdf-parser", "pdfextract", "strings", "yara", "pdftotext", "pdftoppm", "img2pdf"]
    for tool in required_tools:
        try:
            subprocess.run([tool, "--help"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print(f"{tool} ya está instalado.")
        except FileNotFoundError:
            print(f"{tool} no está instalado. Instalando...")
            install_tool(tool)

def run_pdf_analysis(pdf_path):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_folder = "analysis_results"
    pdftotext_output_folder = f"{output_folder}/pdftotext"
    os.makedirs(output_folder, exist_ok=True)
    pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]  # Obtener el nombre del archivo sin extensión
    tools_to_run = [
        (f"pdfid -e {pdf_path}", f"pdfid_log_{pdf_path}_{timestamp}.txt"),
        (f"pdf-parser {pdf_path}", f"pdf-parser_log_{pdf_path}_{timestamp}.txt"),
        (f"sudo pdfextract {pdf_path}",None ),
        (f"strings {pdf_path}", f"strings_log_{pdf_path}_{timestamp}.txt"),
        (f"yara yara/reglas_PDF.yar {pdf_path}", f"yara_log_{pdf_path}_{timestamp}.txt"),
        (f"pdftotext {pdf_path}", None),
        (f"pdftoppm -png {pdf_path} {output_folder}/{pdf_name}-pagina", None),
        (f"img2pdf {output_folder}/{pdf_name}-pagina-*.png -o PDF-{pdf_name}-Seguro.pdf", None)
    ]

    for tool, log_file in tools_to_run:
        if log_file:
            command = f"{tool} > {output_folder}/{log_file}"
        else:
            command = tool
        subprocess.run(command, shell=True, executable="/bin/bash", text=True, check=True)

if __name__ == "__main__":
    check_and_install_tools()
    print("")
    print("#################  V1.2 ###################")
    print("####  Analisis de PDFs Sospechosos  #######")
    print("   Autor: Ing. Dipl. Franck Tscherig       ")
    print("###########################################")
    print("")
    pdf_path = input("Ingrese el nombre del archivo PDF (ej: archivo.pdf): ")
    print("")
    if pdf_path:
        confirm = input(f"¿Desea analizar el archivo '{pdf_path}'? (Sí/No): ").lower()
        if confirm == "sí" or confirm == "si":
            run_pdf_analysis(pdf_path)
        else:
            print("Análisis cancelado.")
    else:
        print("Debe ingresar un nombre de archivo.")

