from src.forms.form import Form


class TenNinetyNineNec(Form):
    def identifier(self) -> str:
        return "1099-NEC"

    def form_matches(self) -> str:
        return "1099-NEC"

    def queries(self) -> list[str]:
        return [
            "For calendar year",
            "PAYER'S name, street address, city or town, state or province, country, ZIP or foreign postal code, and "
            "telephone no.",
            "PAYER'S TIN",
            "RECIPIENT'S TIN",
            "RECIPIENT'S name",
            "RECIPIENT'S street address",
            "RECIPIENT's city or town, state or province, country, and ZIP or foreign postal code",
            "Account number",
            "1 Nonemployee compensation",
            "2 Payer made direct sales totalling $5,000 or more of consumer products to recipient for resale",
            "3",
            "4 Federal income tax withheld",
            "4 State tax withheld",
            "6 State/Payer's state no.",
            "7 State income",
        ]
