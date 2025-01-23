from fpdf import FPDF

pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=12)
pdf.cell(200, 10, txt="Test d'ajout de logo", ln=True, align="C")

try:
    pdf.image("story_maker_logo.png", x=10, y=8, w=30)
except RuntimeError as e:
    print(f"Erreur lors de l'insertion du logo : {e}")

pdf.output("test_logo.pdf")