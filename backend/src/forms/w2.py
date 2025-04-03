from src.forms.form import Form


class W2(Form):
    def identifier(self) -> str:
        return "W2"

    def form_matches(self) -> str:
        return "W-2"

    def queries(self) -> list[str]:
        return [
            "b Employer identification number (EIN)",
            "c Employer's name, address, and ZIP code",
            "e Employee's first name and initial",
            "e Last name",
            "e Suff.",
            "f Employee's address and ZIP code",
            "1 Wages, tips, and other compensation",
            "2 Federal income tax withheld",
            "3 Social security wages",
            "4 Social security tax withheld",
            "5 Medicare wages and tips",
            "6 Medicare tax withheld",
            "7 Social security tips",
            "8 Allocated tips",
            "9",
            "10 Dependent care benefits",
            "11 Nonqualified plans",
            "12a Code",
            "12a amount",
            "12b Code",
            "12b amount",
            "12c Code",
            "12c amount",
            "12d Code",
            "12d amount",
            "15 Employer's state ID number",
            "16 State wages, tips, etc.",
            "17 State income tax",
            "18 Local wages, tips, etc.",
            "19 Local income tax",
        ]
